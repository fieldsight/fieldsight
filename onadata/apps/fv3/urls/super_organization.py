from django.conf.urls import url, include

from rest_framework import routers

from onadata.apps.fv3.viewsets.SuperOrganizationViewset import SuperOrganizationListView, ManageTeamsView, \
    OrganizationViewSet, OrganizationFormLibraryVS


router = routers.DefaultRouter()
router.register(r'super-organizations', OrganizationViewSet,
                base_name='super-organizations')

super_organization_urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api/super_organizations/', OrganizationViewSet.as_view({'post': 'create', 'get': 'list'}),
        name='super_organizations'),
    url(r'^api/super-organizations-list/', SuperOrganizationListView.as_view(), name='super_organizations_list'),
    url(r'^api/manage-teams/(?P<pk>\d+)/$', ManageTeamsView.as_view(), name='manage_teams'),
    url(r'^api/super_organizations_library/', OrganizationFormLibraryVS.as_view({'post': 'create', 'get': 'list'}),
        name='super_organizations_lib'),
    url(r'^api/super_organizations_library/(?P<pk>\d+)/$', OrganizationFormLibraryVS.as_view({'post': 'destroy'}),
        name='super_organizations_lib_del'),
]
