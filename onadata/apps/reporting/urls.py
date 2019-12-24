from django.conf.urls import url, include
from .viewsets import ReportingProjectFormData, ReportSettingsViewSet, metrics_data, GenerateStandardReports, \
    PreviewStandardReports, ReportExportView

urlpatterns = [

    url(r'project-form-data/(?P<pk>\d+)/$', ReportingProjectFormData.as_view(), name='reporting_project_form_data'),
    url(r'add-report/(?P<pk>\d+)/$', ReportSettingsViewSet.as_view({'post': 'create'}), name='report_add'),
    url(r'reports-list/(?P<pk>\d+)/$', ReportSettingsViewSet.as_view({'get': 'list'}), name='project_reports'),
    url(r'report/(?P<pk>\d+)/$', ReportSettingsViewSet.as_view({'put': 'update', 'delete': 'destroy'}),
        name='update_delete_report'),
    url(r'generate-standard-reports/(?P<pk>\d+)/$', GenerateStandardReports.as_view(),
        name='generate_standard_reports'),
    url(r'preview-standard-reports/(?P<pk>\d+)/$', PreviewStandardReports.as_view(),
        name='preview_standard_reports'),
    url(r'metrics-data/(?P<pk>\d+)/$', metrics_data, name='metrics_data'),
    url(r'export/(?P<pk>\d+)/$', ReportExportView, name='report_export')

]
