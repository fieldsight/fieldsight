from django.conf.urls import url, include

from onadata.apps.fv3.viewsets.ProjectDashboardViewSet import ProjectDashboardViewSet, ProjectProgressTableViewSet, \
    project_regions_types


project_dashboard_urlpatterns = [
    url(r'^api/project/(?P<pk>\d+)/$', ProjectDashboardViewSet.as_view({'get': 'retrieve'}), name='project'),
    url(r'^api/project-regions-types/(?P<project_id>\d+)/$', project_regions_types, name='project_regions_types'),
    url(r'^api/progress-table/(?P<pk>\d+)/$', ProjectProgressTableViewSet.as_view(),
        name='progress_table'),

]


