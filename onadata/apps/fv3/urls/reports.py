from django.conf.urls import url
from onadata.apps.fv3.viewsets.ReportViewsets import ReportSyncSettingsViewSet, ReportSyncSettingsList, \
    ReportSyncView

reports_urlpatterns = [
    url(r'^api/report-sync-settings-list/$', ReportSyncSettingsList.as_view(), name='report_sync_settings_list'),
    url(r'^api/update-report-sync-settings/(?P<pk>\d+)/$', ReportSyncSettingsViewSet.as_view({'put': 'update'}),
        name='report_sync_settings'),
    url(r'^api/report-sync/(?P<pk>\d+)/$', ReportSyncView.as_view(), name='report_sync'),
]