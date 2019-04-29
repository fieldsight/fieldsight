from django.conf.urls import url

from onadata.apps.fv3.views import supervisor_projects

urlpatterns = [

    url(r'^api/supervisor/projects/', supervisor_projects, name='supervisor_projects'),
    ]
