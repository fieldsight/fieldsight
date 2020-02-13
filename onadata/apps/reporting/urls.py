from django.conf.urls import url, include
from .viewsets import ReportingProjectFormData, ReportSettingsViewSet, metrics_data, GenerateStandardReports, \
    PreviewStandardReports, ReportExportView, ReportActionView, ReportTaskLogViewset, CustomReportPreviewView, \
    ProjectReportFilterView, ProjectDataExportView, StandardReportsExportXlsView

urlpatterns = [

    url(r'project-form-data/(?P<pk>\d+)/$', ReportingProjectFormData.as_view(), name='reporting_project_form_data'),
    url(r'preview-custom-report/(?P<pk>\d+)/$', CustomReportPreviewView.as_view(), name='custom_report_preview'),
    url(r'add-report/(?P<pk>\d+)/$', ReportSettingsViewSet.as_view({'post': 'create'}), name='report_add'),
    url(r'reports-list/(?P<pk>\d+)/$', ReportSettingsViewSet.as_view({'get': 'list'}), name='project_reports'),
    url(r'report/(?P<pk>\d+)/$', ReportSettingsViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),
        name='update_delete_report'),
    url(r'generate-standard-reports/(?P<pk>\d+)/$', GenerateStandardReports.as_view(),
        name='generate_standard_reports'),
    url(r'preview-standard-reports/(?P<pk>\d+)/$', PreviewStandardReports.as_view(),
        name='preview_standard_reports'),
    url(r'metrics-data/(?P<pk>\d+)/$', metrics_data, name='metrics_data'),
    url(r'export/(?P<pk>\d+)/$', ReportExportView.as_view(), name='report_export'),
    url(r'report-action/(?P<pk>\d+)/$', ReportActionView.as_view(), name='report_action'),
    url(r'export/logs/$', ReportTaskLogViewset.as_view({'get': 'list'}), name="task_list"),
    url(r'project-report-filter/(?P<pk>\d+)/$', ProjectReportFilterView.as_view(),
        name="project_report_filter"),
    url(r'xls-project-responses/(?P<pk>\d+)/$', ProjectDataExportView.as_view(), name="project_data_export"),
    url(r'standard-reports-export-xls/(?P<pk>\d+)/$', StandardReportsExportXlsView.as_view(),
        name="standard_reports_export_xls"),

]
