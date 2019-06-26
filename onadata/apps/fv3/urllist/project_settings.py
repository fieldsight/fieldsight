from django.conf.urls import url
from onadata.apps.fv3.viewsets.project_settings_vs import ProjectSettingsOptions, ProjectProgressSettings

urlpatterns = [

    url(r'^api/project/progress/options/$', ProjectSettingsOptions.as_view(), name='progress_options'),
    url(r'^api/project/progress/options/add/(?P<pk>\d+)/$',
        ProjectProgressSettings.as_view({'post':'create', 'get':'list'}),
        name='progress_add'),
    ]


