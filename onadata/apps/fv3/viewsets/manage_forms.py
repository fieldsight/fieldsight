from django.db import transaction
from django.db.models import Count, Q, Case, When, F, IntegerField, Sum
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from onadata.apps.fieldsight.models import Site, Project
from onadata.apps.fsforms.enketo_utils import CsrfExemptSessionAuthentication
from onadata.apps.fsforms.models import FieldSightXF, Schedule, Stage, FInstance, FormSettings, ReportSyncSettings
from onadata.apps.fsforms.tasks import copy_schedule_to_sites, \
    copy_allstages_to_sites, copy_stage_to_sites, copy_sub_stage_to_sites
from onadata.apps.fsforms.utils import send_message_un_deploy_project, \
    send_message_un_deploy, send_bulk_message_stages_deployed_site, \
    send_bulk_message_stage_deployed_site, send_sub_stage_deployed_site
from onadata.apps.fv3.permissions.manage_forms import ManageFormsPermission, \
    StagePermission, DeployFormsPermission, FormsSettingsPermission
from onadata.apps.fv3.serializers.manage_forms import GeneralFormSerializer, \
    GeneralProjectFormSerializer, ScheduleSerializer, StageSerializer, \
    SubStageSerializer, FormSettingsSerializer, SettingsSerializerGeneralForm, SettingsSerializerProjectGeneralForm, \
    SettingsSerializerScheduleForm, SettingsSerializerSubStage


class GeneralFormsVS(viewsets.ModelViewSet):
    queryset = FieldSightXF.objects.filter(is_staged=False,
                                           is_scheduled=False,
                                           is_deleted=False,
                                           is_survey=False)
    serializer_class = GeneralFormSerializer
    permission_classes = [ManageFormsPermission]
    authentication_classes = [CsrfExemptSessionAuthentication,
                              BasicAuthentication]

    def filter_queryset(self, queryset):
        query_params = self.request.query_params
        site_id = query_params.get('site_id')
        project_id = query_params.get('project_id')

        if project_id:
            queryset = self.queryset.filter(project__id=project_id)
            return queryset.select_related('xf', 'em').prefetch_related("settings")
        elif site_id:
            site = Site.objects.get(pk=site_id)
            project = site.project
            project_id = project.id
            types_count = project.types.count()
            if project.cluster_sites and types_count:
                if not site.type:
                    site.type_id = 0
                if not site.region:
                    site.region_id = 0
                queryset = queryset.filter(Q(site__id=site_id, from_project=False)
                                           | Q(project__id=project_id, settings__isnull=True)
                                           | Q(project__id=project_id, settings__types__contains=[site.type_id],
                                           settings__regions__contains=[site.region_id]))
            elif project.cluster_sites:
                if not site.region:
                    site.region_id = 0
                queryset = queryset.filter(Q(site__id=site_id, from_project=False)
                                           | Q(project__id=project_id, settings__isnull=True)
                                           | Q(project__id=project_id, settings__regions__contains=[site.region_id]))
            elif types_count > 0:
                if not site.type:
                    site.type_id = 0
                queryset = queryset.filter(Q(site__id=site_id, from_project=False)
                                           | Q(project__id=project_id, settings__isnull=True)
                                           | Q(project__id=project_id, settings__types__contains=[site.type_id]))
            else:
                queryset = queryset.filter(Q(site__id=site_id, from_project=False) | Q(project__id=project_id))

            return queryset.select_related('xf', 'em').prefetch_related("settings")
        return []

    def get_serializer_context(self):
        return self.request.query_params

    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            query_params = request.query_params
            site_id = query_params.get('site_id')
            project_id = query_params.get('project_id')
            if not (site_id or project_id):
                return Response({"error": "Project or Site id required"},
                                status=status.HTTP_400_BAD_REQUEST)
            xf = request.data.get('xf')
            if not xf:
                return Response({"error": "Xform  id required"},
                                status=status.HTTP_400_BAD_REQUEST)
            default_submission_status = request.data.get('default_submission_status')
            if project_id:
                if FieldSightXF.objects.filter(
                        xf_id=xf,
                        project_id=project_id,
                        is_deleted=False,
                        is_survey=False,
                        is_scheduled=False,
                        is_staged=False
                ).exists():
                    return Response({"error": "Form already exists in general form"},
                                    status=status.HTTP_400_BAD_REQUEST)
                fxf = FieldSightXF.objects.create(
                    default_submission_status=default_submission_status,
                    xf_id=xf, project_id=project_id
                )
            elif site_id:
                if FieldSightXF.objects.filter(
                        xf_id=xf,
                        is_deleted=False,
                        is_survey=False,
                        is_scheduled=False,
                        is_staged=False
                ).filter(Q(site_id=site_id, from_project=False) |
                         Q(project_id=Site.objects.get(pk=site_id).project_id)).exists():
                    return Response({"error": "Form already exists in general form"},
                                    status=status.HTTP_400_BAD_REQUEST)
                fxf = FieldSightXF.objects.create(
                    default_submission_status=default_submission_status,
                    xf_id=xf, site_id=site_id, from_project=False
                )
            settings = request.data.get('setting')
            if settings:
                settings.update({"form": fxf.id})
                settings_serializer = SettingsSerializerGeneralForm(data=settings)
                if settings_serializer.is_valid():
                    settings_serializer.save(user=request.user)
                    serializer = GeneralFormSerializer(fxf)
                    headers = self.get_success_headers(serializer.data)
                    return Response(serializer.data, status=status.HTTP_201_CREATED,
                                    headers=headers)
                else:
                    fxf.delete()
                    return Response(settings_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            serializer = GeneralFormSerializer(fxf)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED,
                            headers=headers)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.default_submission_status = request.data.get(
            'default_submission_status')
        instance.save()
        settings = request.data.get('setting')
        if settings:
            settings.update({"form": instance.id})
            if not settings.get('id'):
                settings_serializer = SettingsSerializerGeneralForm(data=settings)
            else:
                settings_serializer = SettingsSerializerGeneralForm(instance.settings, data=settings, partial=True)

            if settings_serializer.is_valid():
                settings_serializer.save(user=request.user)
                serializer = GeneralFormSerializer(FieldSightXF.objects.filter(
                    pk=instance.id).prefetch_related("settings")[0])
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED,
                                headers=headers)
            else:
                return Response(settings_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer = GeneralFormSerializer(FieldSightXF.objects.filter(pk=instance.id).prefetch_related("settings")[0])
        return Response(serializer.data)


class GeneralProjectFormsVS(viewsets.ModelViewSet):
    queryset = FieldSightXF.objects.filter(is_staged=False,
                                           is_scheduled=False,
                                           is_deleted=False,
                                           is_survey=True,
                                           project__isnull=False)
    serializer_class = GeneralProjectFormSerializer
    permission_classes = [ManageFormsPermission]
    authentication_classes = [CsrfExemptSessionAuthentication,
                              BasicAuthentication]

    def filter_queryset(self, queryset):
        query_params = self.request.query_params
        project_id = query_params.get('project_id')

        if project_id:
            queryset = self.queryset.filter(project__id=project_id)
            return queryset.select_related('xf', 'em')
        return []

    def get_serializer_context(self):
        return self.request.query_params

    def create(self, request, *args, **kwargs):
        query_params = request.query_params
        project_id = query_params.get('project_id')
        if not project_id:
            return Response({"error": "Project id required"},
                            status=status.HTTP_400_BAD_REQUEST)
        xf = request.data.get('xf')
        if not xf:
            return Response({"error": "xf: Xform  id required"},
                            status=status.HTTP_400_BAD_REQUEST)
        if FieldSightXF.objects.filter(
                xf_id=xf,
                project_id=project_id,
                is_survey=True,
                is_deleted=False,
        ).exists():
            return Response({"error": "Form already exists in Project general form"}, status=status.HTTP_400_BAD_REQUEST)
        default_submission_status = request.data.get('default_submission_status')
        fxf = FieldSightXF.objects.create(
            is_survey=True,
            default_submission_status=default_submission_status,
            xf_id=xf, project_id=project_id
        )
        settings = request.data.get('setting')
        if settings:
            settings.update({"form": fxf.id})
            settings_serializer = SettingsSerializerProjectGeneralForm(data=settings)
            if settings_serializer.is_valid():
                settings_serializer.save(user=request.user)
                serializer = GeneralProjectFormSerializer(fxf)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED,
                                headers=headers)
            else:
                fxf.delete()
                return Response(settings_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer = GeneralProjectFormSerializer(fxf)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.default_submission_status = request.data.get(
            'default_submission_status')
        instance.save()
        settings = request.data.get('setting')
        if settings:
            settings.update({"form": instance.id})
            if not settings.get('id'):
                settings_serializer = SettingsSerializerProjectGeneralForm(data=settings)
            else:
                settings_serializer = SettingsSerializerProjectGeneralForm(instance.settings, data=settings, partial=True)

            if settings_serializer.is_valid():
                settings_serializer.save(user=request.user)
                serializer = GeneralProjectFormSerializer(FieldSightXF.objects.filter(
                    pk=instance.id).prefetch_related("settings")[0])
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED,
                                headers=headers)
            else:
                return Response(settings_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer = GeneralProjectFormSerializer(FieldSightXF.objects.filter(pk=instance.id).prefetch_related("settings")[0])
        return Response(serializer.data)


class ScheduleFormsVS(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing schedules.
    """
    queryset = Schedule.objects.filter(schedule_forms__isnull=False,
                                       schedule_forms__is_deleted=False)
    serializer_class = ScheduleSerializer
    permission_classes = [ManageFormsPermission]
    authentication_classes = [BasicAuthentication,
                              CsrfExemptSessionAuthentication]

    def filter_queryset(self, queryset):
        query_params = self.request.query_params
        site_id = query_params.get('site_id')
        project_id = query_params.get('project_id')
        if project_id:
            queryset = queryset.filter(project__id=project_id)
            return queryset.annotate(response_count=Count(
                "schedule_forms__project_form_instances")).select_related(
                'schedule_forms', 'schedule_forms__xf', 'schedule_forms__em')
        elif site_id:
            site = Site.objects.get(pk=site_id)
            project = site.project
            project_id = project.id
            types_count = project.types.count()
            if project.cluster_sites and types_count:
                if not site.type:
                    site.type_id = 0
                if not site.region:
                    site.region_id = 0
                queryset = queryset.filter(Q(site__id=site_id)
                                           | Q(project__id=project_id, schedule_forms__settings__isnull=True)
                                           | Q(project__id=project_id, schedule_forms__settings__types__contains=[site.type_id],
                                           schedule_forms__settings__regions__contains=[site.region_id]))
            elif types_count > 0:
                if not site.type_id:
                    site.type_id = 0
                queryset = queryset.filter(Q(site__id=site_id)
                                           | Q(project__id=project_id, schedule_forms__settings__isnull=True)
                                           | Q(project__id=project_id, schedule_forms__settings__types__contains=[site.type_id]))
            elif project.cluster_sites:
                if not site.region:
                    site.region_id = 0
                queryset = queryset.filter(Q(site__id=site_id)
                                           | Q(project__id=project_id, schedule_forms__settings__isnull=True)
                                           | Q(project__id=project_id, schedule_forms__settings__regions__contains=[site.region_id]))
            else:
                queryset = queryset.filter(Q(site__id=site_id) | Q(project__id=project_id))
            return queryset.annotate(
                site_response_count=Count(
                    "schedule_forms__site_form_instances", ),
                response_count=Count(Case(
                    When(project__isnull=False,
                         schedule_forms__project_form_instances__site__id=site_id,
                         then=F('schedule_forms__project_form_instances')),
                    output_field=IntegerField(),
                ), distinct=True)

            ).select_related('schedule_forms', 'schedule_forms__xf',
                             'schedule_forms__em')
        return []

    def get_serializer_context(self):
        return self.request.query_params

    def create(self, request, *args, **kwargs):
        query_params = request.query_params
        site_id = query_params.get('site_id')
        project_id = query_params.get('project_id')
        if not (site_id or project_id):
            return Response({"error": "Project or Site id required"},
                            status=status.HTTP_400_BAD_REQUEST)
        xf = request.data.get('xf')
        if not xf:
            return Response({"error": "Xform  id required"},
                            status=status.HTTP_400_BAD_REQUEST)

        default_submission_status = request.data.get('default_submission_status')
        if project_id:
            if FieldSightXF.objects.filter(
                    xf_id=xf,
                    project_id=project_id,
                    is_scheduled=True,
                    is_deleted=True
            ).exists():
                return Response({"error": "Form already exists in Schedule form"}, status=status.HTTP_400_BAD_REQUEST)
            with transaction.atomic():
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                schedule = serializer.save(project_id=project_id)
                fxf = FieldSightXF.objects.create(
                    default_submission_status=default_submission_status,
                    xf_id=xf, project_id=project_id, schedule_id=schedule.id,
                    is_scheduled=True
                )

        elif site_id:
            if FieldSightXF.objects.filter(
                    xf_id=xf,
                    is_deleted=False,
                    is_scheduled=True,
            ).filter(Q(site_id=site_id, from_project=False) | Q(project_id=Site.objects.get(pk=site_id).project_id)).exists():
                return Response({"error": "Form already exists in Schedule form"},
                                status=status.HTTP_400_BAD_REQUEST)
            with transaction.atomic():
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                schedule = serializer.save(site_id=site_id)
                fxf = FieldSightXF.objects.create(
                    default_submission_status=default_submission_status,
                    xf_id=xf, site_id=site_id, schedule=schedule,
                    is_scheduled=True, from_project=False
                )
        settings = request.data.get('setting')
        if settings and fxf and schedule:
            settings.update({"form": fxf.id})
            settings_serializer = SettingsSerializerScheduleForm(data=settings)
            if settings_serializer.is_valid():
                settings_serializer.save(user=request.user)
                serializer = ScheduleSerializer(schedule)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED,
                                headers=headers)
            else:
                fxf.delete()
                schedule.delete()
                return Response(settings_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer = ScheduleSerializer(schedule)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        schedule = serializer.save()
        ds_status = request.data.get('default_submission_status')
        if ds_status:
            form = schedule.schedule_forms
            form.default_submission_status = ds_status
            form.save()
        settings = request.data.get('setting')
        if settings:
            settings.update({"form": instance.schedule_forms.id})
            if not settings.get('id'):
                settings_serializer = SettingsSerializerScheduleForm(data=settings)
            else:
                settings_serializer = SettingsSerializerScheduleForm(instance.schedule_forms.settings,
                                                                     data=settings, partial=True)

            if settings_serializer.is_valid():
                settings_serializer.save(user=request.user)
                serializer = ScheduleSerializer(instance)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED,
                                headers=headers)
            else:
                return Response(settings_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer = ScheduleSerializer(instance)
        return Response(serializer.data)


class StageFormsVS(viewsets.ModelViewSet):
    queryset = Stage.objects.filter(stage__isnull=True).order_by('-project', 'order', 'date_created')
    serializer_class = StageSerializer
    permission_classes = [ManageFormsPermission]
    authentication_classes = [CsrfExemptSessionAuthentication,
                              BasicAuthentication]

    def filter_queryset(self, queryset):
        query_params = self.request.query_params
        site_id = query_params.get('site_id')
        project_id = query_params.get('project_id')
        if project_id:
            queryset = queryset.filter(project__id=project_id)
        elif site_id:
            site = Site.objects.get(pk=site_id)
            project = site.project
            project_id = project.id
            types_count = project.types.count()
            if project.cluster_sites and types_count:
                if not site.type:
                    site.type_id = 0
                if not site.region:
                    site.region_id = 0
                queryset = queryset.filter(Q(site__id=site_id, project_stage_id=0)
                                           | Q(project__id=project_id, tags__contains=[site.type_id],
                                               regions__contains=[site.region_id])
                                           )
            if types_count:
                if not site.type:
                    site.type_id = 0
                queryset = queryset.filter(Q(site__id=site_id,
                                             project_stage_id=0)
                                           | Q(project__id=project_id, tags__contains=[site.type_id])

                                           )
            if project.cluster_sites:
                if not site.region:
                    site.region_id = 0
                queryset = queryset.filter(Q(site__id=site_id,
                                             project_stage_id=0)
                                           | Q(project__id=project_id, regions__contains=[site.region_id])
                                           )
            else:
                queryset = queryset.filter(
                    Q(site__id=site_id, project_stage_id=0)
                    | Q(project__id=project_id))
        else:
            return []

        return queryset.annotate(
                undeployed=Count(Case(
                    When(parent__is_deleted=False,
                         parent__stage_forms__isnull=False,
                         parent__stage_forms__is_deployed=False,
                         parent__stage_forms__is_deleted=False,
                         then=1),
                    output_field=IntegerField()),
                )).prefetch_related('parent', 'parent__stage_forms')

    def get_serializer_context(self):
        return self.request.query_params

    def perform_create(self, serializer):
        query_params = self.request.query_params
        site_id = query_params.get('site_id')
        project_id = query_params.get('project_id')
        if project_id:
            serializer.save(project=Project.objects.get(pk=project_id))
        elif site_id:
            site = get_object_or_404(Site, pk=site_id)
            serializer.save(site=site)

    def perform_update(self, serializer):
        stage = serializer.save()
        tags = stage.tags
        regions = stage.regions
        sub_stages = stage.parent.all()
        for s in sub_stages:
            s.tags = [t for t in s.tags if t in tags]
            s.regions = [t for t in s.regions if t in regions]
            try:
                form_settings = s.stage_forms.settings
                form_settings.types = s.tags
                form_settings.regions = s.regions
                form_settings.save()
            except:
                pass
            Stage.objects.filter(id=s.id).update(tags=s.tags, regions=s.regions)


class SubStageFormsVS(viewsets.ModelViewSet):
    queryset = Stage.objects.filter(stage__isnull=False)
    serializer_class = SubStageSerializer
    permission_classes = [StagePermission]
    authentication_classes = [CsrfExemptSessionAuthentication,
                              BasicAuthentication]

    def filter_queryset(self, queryset):
        query_params = self.request.query_params
        stage_id = query_params.get('stage_id')
        queryset = self.queryset.filter(stage__id=stage_id)
        stage = Stage.objects.get(pk=stage_id)
        project = stage.project
        site_id = query_params.get('site_id')
        if project and site_id:
            site = Site.objects.get(pk=site_id)
            types_count = project.types.count()
            if project.cluster_sites and types_count:
                if not site.type:
                    site.type_id = 0
                if not site.region:
                    site.region_id = 0
                queryset = queryset.filter(tags__contains=[site.type_id], regions__contains=[site.region_id])
            elif types_count:
                if not site.type:
                    site.type_id = 0
                queryset = queryset.filter(tags__contains=[site.type_id])
            elif project.cluster_sites:
                if not site.region:
                    site.region_id = 0
                queryset = queryset.filter(regions__contains=[site.region_id])

        return queryset.select_related('stage_forms', 'em').order_by('order', 'date_created')

    def get_serializer_context(self):
        return {'params': self.request.query_params, 'request': self.request}

    def create(self, request, *args, **kwargs):
        xf = self.request.data.get('xf')
        if not xf:
            return Response({"error": "Form is required"}, status=status.HTTP_400_BAD_REQUEST)
        return super(SubStageFormsVS, self).create(request, *args, **kwargs)

    def perform_create(self, serializer):
        query_params = self.request.query_params
        xf = self.request.data.get('xf')
        setting = self.request.data.get('setting')
        if not xf:
            return Response({"error": "Xform  id required"},
                            status=status.HTTP_400_BAD_REQUEST)
        default_submission_status = self.request.data.get(
            'default_submission_status')
        stage_id = query_params.get('stage_id')
        if stage_id:
            stage = Stage.objects.get(pk=stage_id)
            sub_stage = serializer.save(stage=stage, project=stage.project,
                                        site=stage.site)
            fxf = FieldSightXF.objects.create(
                default_submission_status=default_submission_status,
                xf_id=xf, project=stage.project, site=stage.site,
                is_staged=True, stage=sub_stage
            )
            if setting:
                setting.update({"form": fxf.id})
                settings_serializer = SettingsSerializerSubStage(data=setting)
                if settings_serializer.is_valid():
                    setting_obj = settings_serializer.save(user=self.request.user)
                    sub_stage.tags = setting_obj.types
                    sub_stage.regions = setting_obj.regions
                    sub_stage.save()

    def update(self, request, *args, **kwargs):
        xf = self.request.data.get('xf')
        if not xf:
            return Response({"error": "Form is required"}, status=status.HTTP_400_BAD_REQUEST)
        return super(SubStageFormsVS, self).update(request, *args, **kwargs)


class DeployForm(APIView):
    permission_classes = [DeployFormsPermission]
    authentication_classes = [CsrfExemptSessionAuthentication,
                              BasicAuthentication]

    def post(self, request):
        query_params = request.query_params
        type = query_params.get('type')
        if not type:
            return Response({"error": "type: Deployment form Type Required"}
                            , status=status.HTTP_400_BAD_REQUEST)
        site_id = query_params.get('site_id')
        project_id = query_params.get('project_id')
        if not (site_id or project_id):
            return Response({"error": "site_id or project_id required"},
                            status=status.HTTP_400_BAD_REQUEST)
        if type == "general":
            id = query_params.get('id')
            if not id:
                return Response(
                    {"error": "id: general form Id Required"},
                    status=status.HTTP_400_BAD_REQUEST)
            is_deployed = request.data.get("is_deployed")
            with transaction.atomic():
                fxf = FieldSightXF.objects.get(pk=id)
                fxf.is_deployed = is_deployed
                fxf.save()
                if project_id:
                        send_message_un_deploy_project(fxf)
                else:
                    send_message_un_deploy(fxf)
                return Response({"message": "success"})
        elif type == "schedule":
            id = query_params.get('id')
            if not id:
                return Response(
                    {"error": "id: general form Id Required"},
                    status=status.HTTP_400_BAD_REQUEST)
            is_deployed = request.data.get("is_deployed")
            with transaction.atomic():
                fxf = FieldSightXF.objects.get(is_scheduled=True,
                                               schedule_id=id)
                fxf.is_deployed = is_deployed
                fxf.save()
                if project_id:
                    arguments = {'schedule_id': id,
                                 'fxf_status': is_deployed}
                    copy_schedule_to_sites.apply_async((), arguments,
                                                       countdown=2)
                else:
                    send_message_un_deploy(fxf)
                return Response({"message": "success"})
        elif type == "all":
            id = query_params.get('id')
            if not id:
                return Response(
                    {"error": "id: Project or site Id Required"},
                    status=status.HTTP_400_BAD_REQUEST)
            is_deployed = request.data.get("is_deployed")
            with transaction.atomic():
                if project_id:
                    copy_allstages_to_sites.apply_async((),
                                                        {'pk': id,
                                                         'is_deployed':
                                                             is_deployed},
                                                        countdown=2)
                else:
                    site = Site.objects.get(pk=id)
                    site.site_forms.filter(is_staged=True, xf__isnull=False,
                                           is_deployed=is_deployed,
                                           is_deleted=False).update(
                        is_deployed=True)
                    send_bulk_message_stages_deployed_site(site)
                return Response({"message": "success"})
        elif type == "stage":
            id = query_params.get('id')
            if not id:
                return Response(
                    {"error": "id: Stage Id Required"},
                    status=status.HTTP_400_BAD_REQUEST)
            is_deployed = request.data.get("is_deployed")
            with transaction.atomic():
                if project_id:
                    copy_stage_to_sites.apply_async((),
                                                    {'main_stage': id,
                                                     'pk': project_id,
                                                     'is_deployed':
                                                         is_deployed},
                                                    countdown=2)
                else:
                    site = Site.objects.get(pk=site_id)
                    main_stage = Stage.objects.get(pk=id)
                    FieldSightXF.objects.filter(stage__stage__id=main_stage.pk,
                                                is_deleted=False).update(
                        is_deployed=is_deployed)
                    send_bulk_message_stage_deployed_site(site, main_stage, 0)
                return Response({"message": "success"})
        elif type == "substage":
            id = query_params.get('id')
            if not id:
                return Response(
                    {"error": "id: Stage Id Required"},
                    status=status.HTTP_400_BAD_REQUEST)
            is_deployed = request.data.get("is_deployed")
            with transaction.atomic():
                if project_id:
                    copy_sub_stage_to_sites.apply_async(
                        (), {'sub_stage': id,
                             'pk': project_id, 'is_deployed': is_deployed},
                        countdown=2)
                else:
                    FieldSightXF.objects.filter(stage__id=id,
                                                is_deleted=False).update(
                        is_deployed=is_deployed)
                    send_sub_stage_deployed_site(Site.objects.get(pk=site_id),
                                                 None, 0)
                return Response({"message": "success"})
        return Response({"error": "not valid type"},
                        status=status.HTTP_400_BAD_REQUEST)


class DeleteUndeployedForm(APIView):
    permission_classes = [DeployFormsPermission]
    authentication_classes = [CsrfExemptSessionAuthentication,
                              BasicAuthentication]

    def post(self, request):
        query_params = request.query_params
        type = query_params.get('type')
        if not type:
            return Response({"error": "type: Delete form Type Required"}
                            , status=status.HTTP_400_BAD_REQUEST)
        site_id = query_params.get('site_id')
        project_id = query_params.get('project_id')
        if not (site_id or project_id):
            return Response({"error": "site_id or project_id required"},
                            status=status.HTTP_400_BAD_REQUEST)
        if type == "general":
            id = query_params.get('id')
            if not id:
                return Response(
                    {"error": "id: general form Id Required"},
                    status=status.HTTP_400_BAD_REQUEST)
            if FieldSightXF.objects.filter(pk=id).exists():
                general_form = FieldSightXF.objects.get(pk=id)
                if general_form.is_deployed:
                    return Response({"error": "You cannot delete a deployed "
                                              "form"},
                                    status=status.HTTP_400_BAD_REQUEST)
                extra_json = {}
                if project_id:
                    if general_form.project_form_instances.count():
                        return Response(
                            {"error": "This form have submissions, delete "
                                      "submissions first"},
                               status=status.HTTP_400_BAD_REQUEST)
                    else:
                        general_form.is_deleted = True
                        general_form.save()
                        extra_object = general_form.project
                        extra_message = "project"
                        site_id = None
                        project_id = extra_object.id
                        organization_id = extra_object.organization_id
                        extra_json[
                            'submission_count'] = \
                            general_form.project_form_instances.all().count()
                        general_form.logs.create(
                            source=self.request.user,
                            type=34,
                            title="deleted form  " + id,
                            organization_id=organization_id,
                            project_id=project_id,
                            site_id=site_id,
                            extra_json=extra_json,
                            extra_object=extra_object,
                            extra_message=extra_message,
                            content_object=general_form)
                        ReportSyncSettings.objects.filter(form_id=query_params.get('id')).update(is_deleted=True)

                        return Response({"message": "success"})
                else:
                    if general_form.site_form_instances.count():
                        return Response(
                            {"error": "This form have submissions, delete "
                                      "submissions first"},
                            status=status.HTTP_400_BAD_REQUEST)
                    else:
                        general_form.is_deleted = True
                        general_form.save()
                        extra_object = general_form.site
                        site_id = extra_object.id
                        project_id = extra_object.project_id
                        organization_id = extra_object.project.organization_id
                        extra_message = "site"
                        extra_json[
                                'submission_count'] = \
                                general_form.project_form_instances.all().count()
                        general_form.logs.create(source=self.request.user,
                                                 type=34,
                                                 title="deleted form" + id,
                                                 organization_id=organization_id,
                                                 project_id=project_id,
                                                 site_id=site_id,
                                                 extra_json=extra_json,
                                                 extra_object=extra_object,
                                                 extra_message=extra_message,
                                                 content_object=general_form)
                        return Response({"message": "success"})
            else:
                return Response(
                    {"error": "id: general form id Incorrect"},
                    status=status.HTTP_400_BAD_REQUEST)
        elif type == "schedule":
            id = query_params.get('id')
            if not id:
                return Response(
                    {"error": "id: schedule Id Required"},
                    status=status.HTTP_400_BAD_REQUEST)
            if FieldSightXF.objects.filter(schedule_id=id).exists():
                schedule_form = FieldSightXF.objects.get(schedule_id=id)
                if schedule_form.is_deployed:
                    return Response({"error": "You cannot delete a deployed "
                                              "form"},
                                    status=status.HTTP_400_BAD_REQUEST)
                extra_json = {}
                if project_id:
                    if schedule_form.project_form_instances.count():
                        return Response(
                            {"error": "This Schedule form have submissions, "
                                      "delete "
                                      "submissions first"},
                               status=status.HTTP_400_BAD_REQUEST)
                    else:
                        schedule_form.is_deleted = True
                        schedule_form.save()
                        extra_object = schedule_form.project
                        extra_message = "project"
                        site_id = None
                        project_id = extra_object.id
                        organization_id = extra_object.organization_id
                        extra_json[
                            'submission_count'] = \
                            schedule_form.project_form_instances.all().count()
                        schedule_form.logs.create(
                            source=self.request.user,
                            type=34,
                            title="deleted form  " + id,
                            organization_id=organization_id,
                            project_id=project_id,
                            site_id=site_id,
                            extra_json=extra_json,
                            extra_object=extra_object,
                            extra_message=extra_message,
                            content_object=schedule_form)
                        ReportSyncSettings.objects.filter(form=schedule_form).update(is_deleted=True)

                        return Response({"message": "success"})
                else:
                    if schedule_form.site_form_instances.count():
                        return Response(
                            {"error": "This form have submissions, delete "
                                      "submissions first"},
                            status=status.HTTP_400_BAD_REQUEST)
                    else:
                        schedule_form.is_deleted = True
                        schedule_form.save()
                        extra_object = schedule_form.site
                        site_id = extra_object.id
                        project_id = extra_object.project_id
                        organization_id = extra_object.project.organization_id
                        extra_message = "site"
                        extra_json[
                                'submission_count'] = \
                                schedule_form.project_form_instances.all().count()
                        schedule_form.logs.create(source=self.request.user,
                                                 type=34,
                                                 title="deleted form" + id,
                                                 organization_id=organization_id,
                                                 project_id=project_id,
                                                 site_id=site_id,
                                                 extra_json=extra_json,
                                                 extra_object=extra_object,
                                                 extra_message=extra_message,
                                                 content_object=schedule_form)
                        return Response({"message": "success"})
            else:
                return Response(
                    {"error": "id: general form id Incorrect"},
                    status=status.HTTP_400_BAD_REQUEST)
        elif type == "all":
            id = query_params.get('id')
            if not id:
                return Response(
                    {"error": "id: Project or site id required Id Required"},
                    status=status.HTTP_400_BAD_REQUEST)
            extra_json = {}
            if project_id:
                if FInstance.objects.filter(
                        project_fxf__project__id=id, project_fxf__is_staged=True).count():
                    return Response(
                        {"error": "This Project Stages form have submissions, "
                                  "delete submissions first"},
                           status=status.HTTP_400_BAD_REQUEST)
                elif FieldSightXF.objects.filter(is_staged=True,
                                                is_deployed=True,
                                                project_id=id).count():
                    return Response(
                        {"error": "This Project have deployed Stages, "
                                  "undeploy stages first"},
                           status=status.HTTP_400_BAD_REQUEST)
                else:
                    count = Stage.objects.filter(project_id=id).count()
                    Stage.objects.filter(project_id=id).update(is_deleted=True)
                    FieldSightXF.objects.filter(is_staged=True,
                                                is_deployed=False,
                                                project_id=id).update(
                        is_deleted=True)
                    extra_object = Project.objects.get(pk=id)
                    extra_message = "project"
                    site_id = None
                    organization_id = extra_object.organization_id
                    extra_json[
                        'stage_count'] = count
                    extra_object.logs.create(
                        source=self.request.user,
                        type=341,
                        title="All stages in project " + id,
                        organization_id=organization_id,
                        project=extra_object,
                        site_id=site_id,
                        extra_json=extra_json,
                        extra_object=extra_object,
                        extra_message=extra_message,
                        content_object=extra_object)
                    return Response({"message": "success"})
            else:
                if FInstance.objects.filter(
                        project_fxf__site__id=id).count():
                    return Response(
                        {"error": "This Site Stages form have submissions, "
                                  "delete submissions first"},
                        status=status.HTTP_400_BAD_REQUEST)
                elif FieldSightXF.objects.filter(is_staged=True,
                                                is_deployed=True,
                                                site_id=id).count():
                    return Response(
                        {"error": "This Site have deployed Stages, "
                                  "undeploy stages first"},
                           status=status.HTTP_400_BAD_REQUEST)
                else:
                    count = Stage.objects.filter(site_id=id).count()
                    Stage.objects.filter(project_id=id).update(is_deleted=True)
                    FieldSightXF.objects.filter(is_staged=True,
                                                is_deployed=False,
                                                site_id=id).update(
                        is_deleted=True)
                    extra_object = Site.objects.get(pk=id)
                    extra_message = "site"
                    site_id = None
                    organization_id = extra_object.project.organization_id
                    extra_json[
                        'stage_count'] = count
                    extra_object.logs.create(
                        source=self.request.user,
                        type=341,
                        title="All stages in site " + id,
                        organization_id=organization_id,
                        project_id=extra_object.project,
                        site_id=site_id,
                        extra_json=extra_json,
                        extra_object=extra_object,
                        extra_message=extra_message,
                        content_object=extra_object)
                    return Response({"message": "success"})
        elif type == "stage":
            id = query_params.get('id')
            if not id:
                return Response(
                    {"error": "id: stage Id Required"},
                    status=status.HTTP_400_BAD_REQUEST)
            extra_json = {}
            if project_id:
                ids = Stage.objects.filter(stage_id=id).values_list('pk',
                                                                    flat=True)
                if FInstance.objects.filter(
                        project_fxf__stage__id__in=ids).count():
                    return Response(
                        {"error": "This Stage form have submissions, "
                                  "delete submissions first"},
                           status=status.HTTP_400_BAD_REQUEST)
                elif FieldSightXF.objects.filter(is_staged=True,
                                                is_deployed=True,
                                                stage__id__in=ids).count():
                    return Response(
                        {"error": "This Stage have deployed sub Stages, "
                                  "undeploy stages first"},
                           status=status.HTTP_400_BAD_REQUEST)
                else:
                    count = len(ids)
                    extra_object = Stage.objects.get(pk=id).project
                    FieldSightXF.objects.filter(is_staged=True,
                                                is_deployed=False,
                                                stage_id__in=ids).update(
                        is_deleted=True)
                    Stage.objects.filter(stage_id=id).update(is_deleted=True)
                    Stage.objects.filter(pk=id).update(is_deleted=True)
                    extra_message = "project"
                    site_id = None
                    organization_id = extra_object.organization_id
                    extra_json[
                        'stage_count'] = count
                    extra_object.logs.create(
                        source=self.request.user,
                        type=342,
                        title="All substages in stage " + id,
                        organization_id=organization_id,
                        project=extra_object,
                        site_id=site_id,
                        extra_json=extra_json,
                        extra_object=extra_object,
                        extra_message=extra_message,
                        content_object=extra_object)
                    ReportSyncSettings.objects.filter(form__stage_id=id).update(is_deleted=True)

                    return Response({"message": "success"})
            else:
                ids = Stage.objects.filter(stage_id=id).values_list('pk',
                                                                    flat=True)
                if FInstance.objects.filter(
                        site_fxf__stage__id__in=ids).count():
                    return Response(
                        {"error": "This Site Stage form have submissions, "
                                  "delete submissions first"},
                        status=status.HTTP_400_BAD_REQUEST)
                elif FieldSightXF.objects.filter(is_staged=True,
                                                is_deployed=True,
                                                pk__in=ids).count():
                    return Response(
                        {"error": "This Stage deployed Stages, "
                                  "undeploy stages first"},
                           status=status.HTTP_400_BAD_REQUEST)
                else:
                    count = Stage.objects.filter(site_id=id).count()
                    FieldSightXF.objects.filter(is_staged=True,
                                                is_deployed=False,
                                                stage_id__in=ids).update(
                        is_deleted=True)
                    Stage.objects.filter(stage_id=id).update(is_deleted=True)
                    Stage.objects.filter(pk=id).update(is_deleted=True)
                    extra_object = Site.objects.get(pk=id)
                    extra_message = "site"
                    site_id = None
                    organization_id = extra_object.project.organization_id
                    extra_json[
                        'stage_count'] = count
                    extra_object.logs.create(
                        source=self.request.user,
                        type=341,
                        title="All substages in stage " + id,
                        organization_id=organization_id,
                        project_id=extra_object.project,
                        site_id=site_id,
                        extra_json=extra_json,
                        extra_object=extra_object,
                        extra_message=extra_message,
                        content_object=extra_object)
                    return Response({"message": "success"})
        elif type == "substage":
            id = query_params.get('id')
            if not id:
                return Response(
                    {"error": "id: stage Id Required"},
                    status=status.HTTP_400_BAD_REQUEST)
            extra_json = {}
            if project_id:
                if FInstance.objects.filter(
                        project_fxf__stage__id=id).count():
                    return Response(
                        {"error": "This Stage form have submissions, "
                                  "delete submissions first"},
                           status=status.HTTP_400_BAD_REQUEST)
                elif FieldSightXF.objects.filter(is_staged=True,
                                                is_deployed=True,
                                                stage__id=id).count():
                    return Response(
                        {"error": "This Stage have deployed sub Stages, "
                                  "undeploy stages first"},
                           status=status.HTTP_400_BAD_REQUEST)
                else:

                    FieldSightXF.objects.filter(is_staged=True,
                                                is_deployed=False,
                                                stage_id=id).update(
                        is_deleted=True)
                    extra_object = Stage.objects.get(pk=id).project
                    extra_message = "project"
                    site_id = None
                    organization_id = extra_object.organization_id
                    extra_json[
                        'stage_count'] = 1
                    extra_object.logs.create(
                        source=self.request.user,
                        type=343,
                        title="All stage in stage " + id,
                        organization_id=organization_id,
                        project=extra_object,
                        site_id=site_id,
                        extra_json=extra_json,
                        extra_object=extra_object,
                        extra_message=extra_message,
                        content_object=extra_object)
                    Stage.objects.filter(pk=id).update(is_deleted=True)
                    ReportSyncSettings.objects.filter(form__stage_id=id).update(is_deleted=True)

                    return Response({"message": "success"})
            else:
                if FInstance.objects.filter(
                        site_fxf__stage__id=id).count():
                    return Response(
                        {"error": "This Site Stage form have submissions, "
                                  "delete submissions first"},
                        status=status.HTTP_400_BAD_REQUEST)
                elif FieldSightXF.objects.filter(is_staged=True,
                                                is_deployed=True,
                                                pk=id).count():
                    return Response(
                        {"error": "This Stage is deployed, "
                                  "undeploy stage first"},
                           status=status.HTTP_400_BAD_REQUEST)
                else:
                    Stage.objects.filter(pk=id).update(is_deleted=True)
                    FieldSightXF.objects.filter(is_staged=True,
                                                is_deployed=False,
                                                stage_id=id).update(
                        is_deleted=True)
                    extra_object = Site.objects.get(pk=id)
                    extra_message = "site"
                    site_id = None
                    organization_id = extra_object.project.organization_id
                    extra_json[
                        'stage_count'] = 1
                    extra_object.logs.create(
                        source=self.request.user,
                        type=343,
                        title="All substages in stage " + id,
                        organization_id=organization_id,
                        project_id=extra_object.project,
                        site_id=site_id,
                        extra_json=extra_json,
                        extra_object=extra_object,
                        extra_message=extra_message,
                        content_object=extra_object)
                    return Response({"message": "success"})

        return Response({"error": "not valid type"},
                        status=status.HTTP_400_BAD_REQUEST)


class FormSettingsVS(viewsets.ModelViewSet):
    serializer_class = FormSettingsSerializer
    queryset = FormSettings.objects.all()
    authentication_classes = [BasicAuthentication, CsrfExemptSessionAuthentication]
    permission_classes = (IsAuthenticated, FormsSettingsPermission)

    def retrieve(self, request, *args, **kwargs):
        form_id = self.request.query_params.get("form_id")
        if form_id:
            if FormSettings.objects.filter(form_id=form_id).exists():
                instance = FormSettings.objects.get(form_id=form_id)
                serializer = self.get_serializer(instance)
                return Response(serializer.data)
            else:
                return Response({"error": "form have no settings"}, status=status.HTTP_404_NOT_FOUND)
        return Response(
            {
                "error": "form_id query params not provided"
            },
            status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        default_submission_status = self.request.data.get('default_submission_status', 0)
        weight = self.request.data.get('weight', 0)
        settings = serializer.save(user=self.request.user)
        form = settings.form
        form.default_submission_status = default_submission_status
        form.save()
        if form.is_staged:
            stage = form.stage
            stage.weight = weight
            stage.tags = settings.types
            stage.save()

    def perform_update(self, serializer):
        default_submission_status = self.request.data.get('default_submission_status', 0)
        weight = self.request.data.get('weight', 0)
        settings = serializer.save(user=self.request.user)
        form = settings.form
        form.default_submission_status = default_submission_status
        form.save()
        if form.is_staged:
            stage = form.stage
            stage.weight = weight
            stage.tags = settings.types
            stage.save()


class BreadCrumView(APIView):
    permission_classes = (ManageFormsPermission,)

    def get(self, request):
        site_id = self.request.query_params.get("site_id")
        project_id = self.request.query_params.get("project_id")
        if project_id:
            project = Project.objects.get(pk=project_id)
            return Response({'current_page': 'Manage Forms', 'name': project.name,
                             'name_url': project.get_absolute_url()}, status=status.HTTP_200_OK)
        elif site_id:
            site = Site.objects.filter(pk=site_id).select_related("project", "project__organization")
            site = site[0]
            organization = site.project.organization
            return Response({
                                'current_page': 'Manage Forms',  'name': site.name,
                                'name_url': site.get_absolute_url(),
                            }, status=status.HTTP_200_OK)


class StageReorder(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request, format=None):
        try:
            stages = self.request.data
            qs_list = []
            for i, stage in enumerate(stages):
                obj = Stage.objects.get(pk=stage.get("id"))
                obj.order = i+1
                obj.save()
                qs_list.append(obj.id)
            data = StageSerializer(Stage.objects.filter(pk__in=qs_list).order_by('order', 'date_created'), many=True).data
            return Response({'success': True, 'data': data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class SubStageReorder(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request, format=None):
        try:
            stages = self.request.data
            qs = []
            for i, stage in enumerate(stages):
                obj = Stage.objects.get(pk=stage.get("id"))
                obj.order = i+1
                obj.save()
                qs.append(obj.id)
            queryset = Stage.objects.filter(stage__isnull=False, pk__in=qs).select_related('stage_forms', 'em').order_by('order', 'date_created')
            data = SubStageSerializer(queryset, many=True).data
            return Response({'success': True, 'data': data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
