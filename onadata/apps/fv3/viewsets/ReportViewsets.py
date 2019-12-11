from django.contrib.gis.geos import Point
from rest_framework import viewsets, status
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from onadata.apps.fsforms.enketo_utils import CsrfExemptSessionAuthentication
from onadata.apps.fv3.serializers.ReportSerializer import ReportSerializer, ReportSyncSettingsSerializer, \
    ProjectFormSerializer
from onadata.apps.fsforms.models import ReportSyncSettings, FieldSightXF, SCHEDULED_TYPE, Stage


class ReportVs(viewsets.ModelViewSet):
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [BasicAuthentication, CsrfExemptSessionAuthentication]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=False):
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response({"message": "Your Report have been submitted. Thank You"},
                            status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        lat = float(self.request.data.get("lat", 0))
        lng = float(self.request.data.get("lng", 0))
        location = Point(round(lng, 6), round(lat, 6), srid=4326)
        serializer.save(user=self.request.user, location=location)


class ReportSyncSettingsViewSet(viewsets.ModelViewSet):
    serializer_class = ReportSyncSettingsSerializer
    queryset = ReportSyncSettings.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [BasicAuthentication, CsrfExemptSessionAuthentication]


class ReportSyncSettingsList(APIView):
    permission_classes = (IsAuthenticated,)

    def get_report_data(self, queryset):

        data = [{'title': form.xf.title,
                 'report_id': form.report_sync_settings.all()[0].id,
                 'schedule_type': SCHEDULED_TYPE[int(form.report_sync_settings.all()[0].schedule_type)][1],
                 'day': form.report_sync_settings.all()[0].day,
                 'grid_id': form.report_sync_settings.all()[0].grid_id,
                 'range': form.report_sync_settings.all()[0].range,
                 'report_type': form.report_sync_settings.all()[0].report_type,
                 'last_synced_date': form.report_sync_settings.all()[0].last_synced_date,
                 'spreadsheet_id': form.report_sync_settings.all()[0].spreadsheet_id} for form in queryset
                if form.report_sync_settings.all()]

        return data

    def get(self, request, *args, **kwargs):
        project_id = self.request.query_params.get('project_id', None)
        schedule_queryset = FieldSightXF.objects.select_related('xf').prefetch_related('report_sync_settings').\
            filter(project_id=project_id, is_scheduled=True, is_staged=False, is_survey=False)

        schedule = self.get_report_data(schedule_queryset)

        stages = Stage.objects.filter(project_id=project_id)
        mainstage = []

        for stage in stages:
            if stage.stage_id is None:
                data = [{'title': form.stage_forms.xf.title,
                         'report_id': form.stage_forms.report_sync_settings.all()[0].id,
                         'schedule_type': SCHEDULED_TYPE[int(form.stage_forms.report_sync_settings.all()[0].schedule_type)][1],
                         'day': form.stage_forms.report_sync_settings.all()[0].day,
                         'grid_id': form.stage_forms.report_sync_settings.all()[0].grid_id,
                         'range': form.stage_forms.report_sync_settings.all()[0].range,
                         'report_type': form.stage_forms.report_sync_settings.all()[0].report_type,
                         'last_synced_date': form.stage_forms.report_sync_settings.all()[0].last_synced_date,
                         'spreadsheet_id': form.stage_forms.report_sync_settings.all()[0].spreadsheet_id}
                        for form in stage.active_substages().prefetch_related('stage_forms', 'stage_forms__xf',
                                                                              'stage_forms__report_sync_settings')
                        if form.stage_forms.report_sync_settings.all()]
                stages = {'id': stage.id, 'stage': stage.name, 'sub_stages': data}
                mainstage.append(stages)

        survey_queryset = FieldSightXF.objects.select_related('xf').prefetch_related('report_sync_settings').\
            filter(project_id=project_id, is_scheduled=False, is_staged=False, is_survey=True)
        survey = self.get_report_data(survey_queryset)

        general_queryset = FieldSightXF.objects.select_related('xf').prefetch_related('report_sync_settings')\
            .filter(project_id=project_id, is_scheduled=False, is_staged=False, is_survey=False)
        general = self.get_report_data(general_queryset)

        standard_reports_queryset = ReportSyncSettings.objects.select_related('form__xf').\
            filter(project_id=project_id, report_type__in=['site_info', 'site_progress'])
        standard_reports = [
            {'report_id': report.id, 'schedule_type': SCHEDULED_TYPE[int(report.schedule_type)][1],
             'day': report.day, 'grid_id': report.grid_id,
             'range': report.range, 'report_type': report.report_type,
             'last_synced_date': report.last_synced_date, 'spreadsheet_id':
                 report.spreadsheet_id} for report in standard_reports_queryset]
        return Response(status=status.HTTP_200_OK, data={'standard_reports': standard_reports,
                                                         'general_reports': general,
                                                         'schedule_reports': schedule,
                                                         'stage_reports': mainstage,
                                                         'survey_reports': survey

                                                         })
