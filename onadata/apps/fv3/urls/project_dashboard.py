from django.conf.urls import url, include

from onadata.apps.fv3.viewsets.ProjectDashboardViewSet import ProjectDashboardViewSet


project_dashboard_urlpatterns = [
    url(r'^api/project/(?P<pk>\d+)/$', ProjectDashboardViewSet.as_view({'get': 'retrieve'}), name='project'),
]


