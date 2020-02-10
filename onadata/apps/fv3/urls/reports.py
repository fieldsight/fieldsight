from django.conf.urls import url
from onadata.apps.fv3.viewsets.ReportViewsets import ReportSyncSettingsViewSet, ReportSyncSettingsList, \
    ReportSyncView, ReportSyncSettingsToday, OrganizationFormReportSyncView

reports_urlpatterns = [
    url(r'^api/report-sync-settings-list/$', ReportSyncSettingsList.as_view(), name='report_sync_settings_list'),
    url(r'^api/add-report-sync-settings/$', ReportSyncSettingsViewSet.as_view({'post': 'create'}),
        name='add_report_sync_settings'),
    url(r'^api/report-sync-settings-today/$', ReportSyncSettingsToday.as_view({'get':'list'}),
        name='report_sync_settings_today'),
    url(r'^api/update-report-sync-settings/(?P<pk>\d+)/$', ReportSyncSettingsViewSet.as_view({'put': 'update'}),
        name='report_sync_settings'),
    url(r'^api/report-sync/(?P<pk>\d+)/$', ReportSyncView.as_view(), name='report_sync'),
    url(r'^api/organization-form-report-sync/$', OrganizationFormReportSyncView.as_view(),
        name='org_form_report_sync'),

]