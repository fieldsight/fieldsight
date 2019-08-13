from django.db import transaction
from django.db.models import Count, Q, Case, When, F, IntegerField, Sum
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.authentication import BasicAuthentication
from rest_framework.response import Response

from onadata.apps.fieldsight.models import Site, Project
from onadata.apps.fsforms.enketo_utils import CsrfExemptSessionAuthentication
from onadata.apps.fsforms.models import FieldSightXF, Schedule, Stage
from onadata.apps.fv3.permissions.manage_forms import ManageFormsPermission, \
    StagePermission
from onadata.apps.fv3.serializers.manage_forms import GeneralFormSerializer, \
    GeneralProjectFormSerializer, ScheduleSerializer, StageSerializer, \
    SubStageSerializer


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
            return queryset.annotate(
                response_count=Count(
                    'project_form_instances')).select_related('xf', 'em')
        elif site_id:
            project_id = get_object_or_404(Site, pk=site_id).project.id
            queryset = queryset.filter(Q(site__id=site_id, from_project=False)
                                       | Q(project__id=project_id))
            return queryset.annotate(
                site_response_count=Count("site_form_instances", ),
                response_count=Count(Case(
                    When(project__isnull=False,
                         project_form_instances__site__id=site_id,
                         then=F('project_form_instances')),
                    output_field=IntegerField(),
                ), distinct=True)

            ).select_related('xf', 'em')
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
            fxf = FieldSightXF.objects.create(
                default_submission_status=default_submission_status,
                xf_id=xf, project_id=project_id
            )
        elif site_id:
            fxf = FieldSightXF.objects.create(
                default_submission_status=default_submission_status,
                xf_id=xf, project_id=project_id
            )
        serializer = GeneralFormSerializer(fxf)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.default_submission_status = request.data.get(
            'default_submission_status')
        instance.save()
        serializer = GeneralFormSerializer(instance)
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
            return queryset.annotate(
                response_count=Count(
                    'project_form_instances')).select_related('xf', 'em')
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
        default_submission_status = request.data.get('default_submission_status')
        if project_id:
            fxf = FieldSightXF.objects.create(is_survey=True,
                                              default_submission_status=
                                              default_submission_status,
                                              xf_id=xf, project_id=project_id
            )
        serializer = GeneralProjectFormSerializer(fxf)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.default_submission_status = request.data.get(
            'default_submission_status')
        instance.save()
        serializer = GeneralProjectFormSerializer(instance)
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
            project_id = get_object_or_404(Site, pk=site_id).project.id
            queryset = queryset.filter(
                Q(site__id=site_id, schedule_forms__from_project=False)
                | Q(project__id=project_id))
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
            request.data['project_id'] = project_id
            with transaction.atomic():
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                schedule = serializer.save()
                fxf = FieldSightXF.objects.create(
                    default_submission_status=default_submission_status,
                    xf_id=xf, project_id=project_id, schedule_id=schedule.id,
                    is_scheduled=True
                )

        elif site_id:
            with transaction.atomic():
                request.data['site_id'] = site_id
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                schedule = serializer.save()
                fxf = FieldSightXF.objects.create(
                    default_submission_status=default_submission_status,
                    xf_id=xf, project_id=project_id, schedule=schedule,
                    is_scheduled=True
                )
        serializer = ScheduleSerializer(schedule)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)


class StageFormsVS(viewsets.ModelViewSet):
    queryset = Stage.objects.filter(stage__isnull=True)
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
            site = get_object_or_404(Site, pk=site_id)
            project_id = site.project_id
            queryset = queryset.filter(
                Q(site__id=site_id, project_stage_id=0) |
                Q(project__id=project_id))
            if site.type:
                project_id = site.project.id
                queryset = queryset.filter(Q(site__id=site_id,
                                             project_stage_id=0)
                                           | Q
                                           (Q(project__id=project_id) &
                                            Q(tags__contains=[site.type_id])) |
                                           Q(Q(project__id=project_id)
                                             & Q(tags=[]))
                                           )
            else:
                project_id = site.project.id
                queryset = queryset.filter(
                    Q(site__id=site_id, project_stage_id=0)
                    | Q(project__id=project_id))
        else:
            return []

        return queryset.annotate(sub_stage_weight=Sum(F('parent__weight'))
                                 ).order_by('order', 'date_created')

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


class SubStageFormsVS(viewsets.ModelViewSet):
    queryset = Stage.objects.filter(stage__isnull=False)
    serializer_class = SubStageSerializer
    permission_classes = [StagePermission]
    authentication_classes = [CsrfExemptSessionAuthentication,
                              BasicAuthentication]

    def filter_queryset(self, queryset):
        query_params = self.request.query_params
        stage_id = query_params.get('stage_id')
        return self.queryset.filter(stage__id=stage_id).select_related(
        'stage_forms', 'em').order_by('order', 'date_created')

    def get_serializer_context(self):
        return {'request': self.request}

    def perform_create(self, serializer):
        query_params = self.request.query_params
        xf = self.request.data.get('xf')
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
            xf = FieldSightXF.objects.create(
                default_submission_status=default_submission_status,
                xf_id=xf, project=stage.project, site=stage.site,
                is_staged=True, stage=sub_stage
            )


