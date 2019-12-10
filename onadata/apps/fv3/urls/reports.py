from django.conf.urls import url
from onadata.apps.fv3.viewsets.ReportViewsets import ReportSyncSettingsViewSet, ProjectFormsViewSet, \
    ReportSyncSettingsList

reports_urlpatterns = [
    url(r'^api/report-sync-settings-list/$', ReportSyncSettingsList.as_view(), name='report_sync_settings_list'),
    url(r'^api/report-sync-settings/$', ReportSyncSettingsViewSet.as_view({'post': 'create'}),
        name='report_sync_settings'),
    url(r'^api/project-forms/(?P<pk>\d+)/$', ProjectFormsViewSet.as_view({'get': 'list'}), name='project_forms'),

]