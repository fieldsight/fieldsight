from django.db.models import Count, Q, Case, When, F, IntegerField, Sum
from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from onadata.apps.fieldsight.models import Site
from onadata.apps.fsforms.models import FieldSightXF, Schedule, Stage
from onadata.apps.fv3.permissions.manage_forms import ManageFormsPermission
from onadata.apps.fv3.serializers.manage_forms import GeneralFormSerializer, \
    GeneralProjectFormSerializer, ScheduleSerializer, StageSerializer


class GeneralFormsVS(viewsets.ModelViewSet):
    queryset = FieldSightXF.objects.filter(is_staged=False,
                                           is_scheduled=False,
                                           is_deleted=False,
                                           is_survey=False)
    serializer_class = GeneralFormSerializer
    permission_classes = [ManageFormsPermission]

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
            print(site_id)
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


class GeneralProjectFormsVS(viewsets.ModelViewSet):
    queryset = FieldSightXF.objects.filter(is_staged=False,
                                           is_scheduled=False,
                                           is_deleted=False,
                                           is_survey=True)
    serializer_class = GeneralProjectFormSerializer
    permission_classes = [ManageFormsPermission]

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


class ScheduleFormsVS(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing schedules.
    """
    queryset = Schedule.objects.filter(schedule_forms__isnull=False,
                                       schedule_forms__is_deleted=False)
    serializer_class = ScheduleSerializer
    permission_classes = [ManageFormsPermission]

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


class StageFormsVS(viewsets.ModelViewSet):
    queryset = Stage.objects.filter(stage__isnull=True)
    serializer_class = StageSerializer
    permission_classes = [ManageFormsPermission]

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

        return queryset.annotate(sub_stage_weight=Sum(F('parent__weight')))



    def get_serializer_context(self):
        return self.request.query_params
