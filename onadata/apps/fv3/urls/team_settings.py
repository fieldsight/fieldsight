from django.conf.urls import url, include
from rest_framework import routers
from onadata.apps.fv3.viewsets.TeamSettingsViewset import TeamViewset, team_types_countries, TeamGeoLayerViewset, \
    TeamOwnerAccount

router = routers.DefaultRouter()

router.register(r'team-settings', TeamViewset, base_name='team')
router.register(r'team-geolayer', TeamGeoLayerViewset, base_name='team_geolayer')

team_settings_urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api/team-types-countries', team_types_countries, name="team_types"),
    url(r'^api/team-owner-account/(?P<pk>\d+)/$', TeamOwnerAccount.as_view(), name="team_owner_account"),

]


