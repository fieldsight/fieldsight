from django.conf.urls import url
from onadata.apps.fv3.viewsets.map import ProjectsApi

map_urlpatterns = [

    url(r'^api/map/projects/$', ProjectsApi.as_view(), name='projects'),
]