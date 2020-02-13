from django.conf.urls import url

from onadata.apps.fv3.viewsets.TeamViewSet import TeamDashboardViewSet, TeamProjectsViewSet, \
    AddTeamProjectViewset, team_regions_types

team_dashboard_urlpatterns = [
    url(r'^api/team/(?P<pk>\d+)/$', TeamDashboardViewSet.as_view({'get': 'retrieve'}), name='team'),
    url(r'^api/team-projects/(?P<pk>\d+)/$', TeamProjectsViewSet.as_view({'get': 'list'}), name='team'),
    url(r'^api/add-project/(?P<pk>\d+)/$', AddTeamProjectViewset.as_view({'get': 'list', 'post': 'create'}),
        name='add_project'),
    url(r'^api/team-regions-types/(?P<pk>\d+)/$', team_regions_types, name='team_regions_types'),

]


