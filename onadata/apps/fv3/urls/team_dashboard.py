from django.conf.urls import url

from onadata.apps.fv3.viewsets.TeamViewSet import TeamDashboardViewSet, TeamProjectsViewSet, StripeSubscriptions


team_dashboard_urlpatterns = [
    url(r'^api/team/(?P<pk>\d+)/$', TeamDashboardViewSet.as_view({'get': 'retrieve'}), name='team'),
    url(r'^api/team-projects/(?P<pk>\d+)/$', TeamProjectsViewSet.as_view({'get': 'list'}), name='team'),
    url(r'^api/subscriptions/(?P<org_id>\d+)/$', StripeSubscriptions.as_view(), name='subscriptions'),

]


