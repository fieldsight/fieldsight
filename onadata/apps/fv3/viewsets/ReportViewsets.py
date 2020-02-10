import calendar
import datetime

from django.contrib.gis.geos import Point
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from rest_framework import viewsets, status
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient import discovery

from onadata.apps.fieldsight.models import Project
from onadata.apps.fsforms.enketo_utils import CsrfExemptSessionAuthentication
from onadata.apps.fsforms.tasks import sync_sheet
from onadata.apps.fsforms.management.commands.corn_sync_report import update_sheet, create_new_sheet
from onadata.apps.fv3.serializers.ReportSerializer import ReportSerializer, ReportSyncSettingsSerializer, \
    ProjectFormSerializer
from onadata.apps.fsforms.models import ReportSyncSettings, FieldSightXF, SCHEDULED_TYPE, Stage, SCHEDULED_LEVEL
from onadata.apps.fv3.permissions.reports import ReportSyncPermission, check_manager_or_admin_perm, \
    ReportSyncSettingsViewPermission


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
    permission_classes = [IsAuthenticated, ReportSyncSettingsViewPermission]
    authentication_classes = [BasicAuthentication, CsrfExemptSessionAuthentication]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)

        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        data = serializer.data
        if not data.get('spreadsheet_id') and data.get('schedule_type') != 0:
            sync_sheet.delay(instance.id)
        data.update({'schedule_type': SCHEDULED_TYPE[int(serializer.data.get('schedule_type'))][1]})
        return Response(data, status=status.HTTP_200_OK)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user, updated_at=datetime.datetime.now())


class ReportSyncSettingsList(APIView):
    permission_classes = (IsAuthenticated, ReportSyncSettingsViewPermission)

    def get_report_data(self, queryset):
        data = []
        for form in queryset:
            if form.report_sync_settings.all().exists():

                data.append({'title': form.xf.title,
                             'form_id': form.id,
                             'report_id': form.report_sync_settings.all()[0].id,
                             'schedule_type': SCHEDULED_TYPE[int(form.report_sync_settings.all()[0].schedule_type)][1],
                             'day': form.report_sync_settings.all()[0].day,
                             'grid_id': form.report_sync_settings.all()[0].grid_id,
                             'range': form.report_sync_settings.all()[0].range,
                             'report_type': form.report_sync_settings.all()[0].report_type,
                             'last_synced_date': form.report_sync_settings.all()[0].last_synced_date,
                             'spreadsheet_id': form.report_sync_settings.all()[0].spreadsheet_id})
            elif form.organization_form_lib:
                data.append({'title': form.xf.title,
                             'form_id': form.id,
                             'report_id': None,
                             'schedule_type': 'Manual',
                             'day': None,
                             'grid_id': None,
                             'range': None,
                             'report_type': 'form',
                             'last_synced_date': None,
                             'spreadsheet_id': None,

                             })

        return data

    def get(self, request, *args, **kwargs):
        project_id = self.request.query_params.get('project_id', None)
        main_queryset = FieldSightXF.objects.select_related('xf', 'schedule').prefetch_related('report_sync_settings')
        schedule_queryset = main_queryset.filter(project_id=project_id, is_scheduled=True, is_staged=False,
                                                 is_survey=False, is_deleted=False)

        schedule = self.get_report_data(schedule_queryset)

        stages = Stage.objects.filter(project_id=project_id)
        mainstage = []

        for stage in stages:
            if stage.stage_id is None:
                data = [{'title': form.stage_forms.xf.title,
                         'form_id': form.stage_forms.id,
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
                        if form.stage_forms.report_sync_settings.all().exists()]
                stages = {'id': stage.id, 'stage': stage.name, 'sub_stages': data}
                mainstage.append(stages)

        survey_queryset = main_queryset.filter(project_id=project_id, is_scheduled=False, is_staged=False,
                                               is_survey=True, is_deleted=False)
        survey = self.get_report_data(survey_queryset)

        general_queryset = main_queryset.filter(project_id=project_id, is_scheduled=False, is_staged=False,
                                                is_survey=False, is_deleted=False)
        general = self.get_report_data(general_queryset)

        standard_reports_queryset = ReportSyncSettings.objects.select_related('form__xf').\
            filter(project_id=project_id, report_type__in=['site_info', 'site_progress'])
        standard_reports = [
            {'report_id': report.id, 'schedule_type': SCHEDULED_TYPE[int(report.schedule_type)][1],
             'day': report.day, 'grid_id': report.grid_id,
             'range': report.range, 'report_type': report.report_type,
             'last_synced_date': report.last_synced_date, 'spreadsheet_id':
                 report.spreadsheet_id} for report in standard_reports_queryset]
        
        project = Project.objects.get(id=project_id)

        breadcrumbs = {'project': project.name, 'project_url': project.get_absolute_url(), 'current_page': 'Reports'}
        return Response(status=status.HTTP_200_OK, data={'standard_reports': standard_reports,
                                                         'general_reports': general,
                                                         'schedule_reports': schedule,
                                                         'stage_reports': mainstage,
                                                         'survey_reports': survey,
                                                         'can_edit_or_sync': check_manager_or_admin_perm(request,
                                                                                                         project_id),
                                                         'breadcrumbs': breadcrumbs

                                                         })


class ReportSyncSettingsToday(viewsets.ReadOnlyModelViewSet):
    serializer_class = ReportSyncSettingsSerializer
    queryset = ReportSyncSettings.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        week_day = int(datetime.datetime.today().strftime('%w'))
        day = datetime.datetime.today().day
        _start, _end = calendar.monthrange(datetime.datetime.today().year, datetime.datetime.today().month)
        if day == _end:
            sheet_list = ReportSyncSettings.objects.exclude(schedule_type=0).filter(Q(schedule_type=1)
                            | Q(schedule_type=2, day=week_day)
                            | Q(schedule_type=3, day=0)
                            )

        else:
            sheet_list = ReportSyncSettings.objects.exclude(schedule_type=0).filter(Q(schedule_type=1)
                            | Q(schedule_type=2, day=week_day)
                            | Q(schedule_type=3, day=day))
        return sheet_list


class ReportSyncView(APIView):
    authentication_classes = [BasicAuthentication, CsrfExemptSessionAuthentication]
    permission_classes = (IsAuthenticated, ReportSyncPermission)

    def post(self, request, *args, **kwargs):
        sheet_id = self.kwargs.get('pk', None)
        sync_sheet.delay(sheet_id)
        return Response(status=status.HTTP_200_OK, data={'detail': 'This report is being synced with google sheets.'})


class OrganizationFormReportSyncView(APIView):
    authentication_classes = [BasicAuthentication, CsrfExemptSessionAuthentication]
    permission_classes = (IsAuthenticated, ReportSyncSettingsViewPermission)

    def post(self, request, *args, **kwargs):
        serializer = ReportSyncSettingsSerializer(data=request.data)
        if serializer.is_valid():
            obj = serializer.save(user=self.request.user)
            sheet_id = obj.id
            sync_sheet.delay(sheet_id)
            return Response(status=status.HTTP_200_OK,
                            data={'detail': 'This report is being synced with google sheets.'})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

