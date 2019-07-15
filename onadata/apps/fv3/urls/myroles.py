from django.conf.urls import url
from onadata.apps.fv3.viewsets.MyRolesViewset import my_roles, AcceptInvite, DeclineInvite, AcceptAllInvites, \
    latest_submission, map_activity

my_roles_urlpatterns = [

    url(r'^api/myroles/$', my_roles, name='my_roles'),
    url(r'^api/accept-invite/(?P<pk>\d+)/(?P<username>[^/]+)/$', AcceptInvite.as_view(), name='accept_invite'),
    url(r'^api/decline-invite/(?P<pk>\d+)/$', DeclineInvite.as_view(), name='decline_invite'),
    url(r'^api/accept-all-invites/(?P<username>[^/]+)/$', AcceptAllInvites.as_view(), name='accept_all_invites'),
    url(r'api/latestsubmissions/', latest_submission, name='latest_submissions'),
    url(r'^api/activity-map', map_activity, name='map_activity'),
]