from django.conf.urls import url
from onadata.apps.fv3.viewsets.MyRolesViewset import my_roles, accept_invite, decline_invite, accept_all_invites, \
    latest_submission, map_activity

my_roles_urlpatterns = [

    url(r'^api/myroles/$', my_roles, name='my_roles'),
    url(r'^api/accept-invite/(?P<pk>\d+)/(?P<username>[^/]+)/$', accept_invite, name='accept_invite'),
    url(r'^api/decline-invite/(?P<pk>\d+)/$', decline_invite, name='decline_invite'),
    url(r'^api/accept-all-invites/(?P<username>[^/]+)/$', accept_all_invites, name='accept_all_invites'),
    url(r'^api/activity-map', map_activity, name='map_activity'),
]