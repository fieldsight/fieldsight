from django.db.models import Count, Q, Case, When, F, IntegerField
from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from onadata.apps.fieldsight.models import Site
from onadata.apps.fsforms.models import FieldSightXF
from onadata.apps.fv3.permissions.manage_forms import ManageFormsPermission
from onadata.apps.fv3.serializers.manage_forms import GeneralFormSerializer


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
        else:
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

    def get_serializer_context(self):
        return self.request.query_params
