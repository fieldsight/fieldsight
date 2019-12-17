from django.shortcuts import get_object_or_404
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import viewsets

from onadata.apps.fieldsight.models import Project
from onadata.apps.fsforms.models import FieldSightXF, Schedule, Stage
from .serializers import StageFormSerializer, ReportSettingsSerializer
from .permissions import ReportingProjectFormsPermissions
from .models import ReportSettings
from ..fsforms.enketo_utils import CsrfExemptSessionAuthentication


class ReportingProjectFormData(APIView):
    permission_classes = [IsAuthenticated, ReportingProjectFormsPermissions]

    def get(self, request, pk, *args,  **kwargs):

        form_type = self.request.query_params.get('form_type')
        project_id = get_object_or_404(Project, pk=pk).id

        if form_type == 'general':

            generals_queryset = FieldSightXF.objects.select_related('xf')\
                .filter(is_staged=False, is_scheduled=False, is_deleted=False, project_id=project_id, is_survey=False).\
                values('xf__title', 'id')
            generals_data = [{'id': form['id'], 'title': form['xf__title']} for form in generals_queryset]

            return Response(status=status.HTTP_200_OK, data=generals_data)

        elif form_type == 'scheduled':

            schedules_queryset = Schedule.objects.select_related('project').prefetch_related('schedule_forms')\
                .filter(project_id=project_id, schedule_forms__is_deleted=False, site__isnull=True,
                        schedule_forms__isnull=False, schedule_forms__xf__isnull=False).\
                values('schedule_forms__xf__id', 'schedule_forms__xf__title')

            schedules_data = [{'id': form['schedule_forms__xf__id'], 'title': form['schedule_forms__xf__title']}
                              for form in schedules_queryset]

            return Response(status=status.HTTP_200_OK, data=schedules_data)

        elif form_type == 'stage':

            stages_queryset = Stage.objects.select_related('project').filter(stage__isnull=True, project_id=project_id,
                                                                             stage_forms__isnull=True).order_by('order')

            stages = StageFormSerializer(stages_queryset, many=True)

            return Response(status=status.HTTP_200_OK, data=stages.data)

        elif form_type == 'survey':

            surveys_queryset = FieldSightXF.objects.select_related('xf').\
                filter(is_staged=False, is_scheduled=False, is_deleted=False, project_id=project_id, is_survey=True).\
                values('id', 'xf__title')

            surveys_data = [{'id': form['id'], 'title': form['xf__title']} for form in surveys_queryset]
            return Response(status=status.HTTP_200_OK, data=surveys_data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND, data={'detail': 'form_type params is required.'})


class ReportSettingsViewSet(viewsets.ModelViewSet):
    serializer_class = ReportSettingsSerializer
    queryset = ReportSettings.objects.all()
    permission_classes = [IsAuthenticated, ReportingProjectFormsPermissions]
    authentication_classes = [BasicAuthentication, CsrfExemptSessionAuthentication]

    def get_queryset(self):
        type = self.request.query_params.get('type')
        project_id = self.kwargs.get('pk')

        if type == 'custom':
            queryset = self.queryset.filter(project_id=project_id, add_to_templates=True)

        elif type == 'shared_with_me':
            queryset = self.queryset.filter(project_id=project_id, shared_with=self.request.user,
                                            add_to_templates=False)

        else:
            queryset = self.queryset.filter(project_id=project_id, add_to_templates=False, owner=self.request.user)
        return queryset

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user, project_id=self.kwargs.get('pk'))