from django.contrib.gis.geos import Point
from rest_framework import viewsets, status
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from onadata.apps.fsforms.enketo_utils import CsrfExemptSessionAuthentication
from onadata.apps.fv3.serializers.ReportSerializer import ReportSerializer, ReportSyncSettingsSerializer, \
    ProjectFormSerializer
from onadata.apps.fsforms.models import ReportSyncSettings, FieldSightXF, SCHEDULED_TYPE


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

    def get_queryset(self):
        project_id = self.request.query_params.get('project_id', None)
        if project_id is not None:
            return self.queryset.filter(project_id=project_id)


class ProjectFormsViewSet(viewsets.ModelViewSet):

    queryset = FieldSightXF.objects.select_related('xf').filter(is_deleted=False)
    serializer_class = ProjectFormSerializer

    def filter_queryset(self, queryset):
        return queryset.filter(project_id=self.kwargs.get('pk'))


class ReportSyncSettingsList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        project_id = self.request.query_params.get('project_id', None)
        report_sync_queryset = ReportSyncSettings.objects.filter(project_id=project_id)
        report_sync_list = [{'id': report.id, 'form': report.form.xf.title, 'schedule_type':
            SCHEDULED_TYPE[int(report.schedule_type)][1], 'day': report.day} for report in report_sync_queryset]

        report_sync_form_ids = ReportSyncSettings.objects.filter(project_id=project_id).values_list('form__xf_id',
                                                                                                    flat=True)

        project_forms_queryset = FieldSightXF.objects.select_related('xf').filter(is_deleted=False,
                                                                                  project_id=self.kwargs.get('pk')).\
            exclude(xf_id__in=report_sync_form_ids)
        project_forms = [{'id': None, 'form': form.xf.title, 'schedule_type': 'Manual', 'day': None}
                         for form in project_forms_queryset]
        report_sync_list.extend(project_forms)

        return Response(status=status.HTTP_200_OK, data=report_sync_list)
