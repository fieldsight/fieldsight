from django.conf.urls import url
from onadata.apps.fv3.viewsets.project_settings_vs import ProjectSettings


urlpatterns = [

    url(r'^api/project/progress/options', ProjectSettings.as_view(), name='progress_options'),
    ]


