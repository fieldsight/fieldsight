from django.conf.urls import url, include
from rest_framework import routers

from onadata.apps.fv3.viewsets.project_settings_vs import ProjectSettingsOptions, ProjectProgressSettings, \
    ProjectSiteTypesViewset, ProjectTermsLabelsViewset, ProjectRegionsViewset
from onadata.apps.fv3.views import ProjectUpdateViewset, sectors_subsectors, GeoLayerView, organization_geolayer, \
    EnableClusterSitesView
router = routers.DefaultRouter()

router.register(r'project-terms-labels', ProjectTermsLabelsViewset, base_name='project-terms-labels')
router.register(r'project-regions', ProjectRegionsViewset, base_name='project-regions')
router.register(r'project-site-types', ProjectSiteTypesViewset, base_name='project-site-types')

progress_urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api/project/progress/options/$', ProjectSettingsOptions.as_view(), name='progress_options'),
    url(r'^api/project/progress/add/(?P<pk>\d+)/$',
        ProjectProgressSettings.as_view({'post':'create', 'get':'list'}),
        name='progress_add'),
    url(r'^api/update-project/(?P<pk>\d+)/$', ProjectUpdateViewset.as_view(),
        name='update_project_api'),
    url(r'^api/sectors-subsectors/$', sectors_subsectors.as_view({'get': 'list'}), name='sectors_subsectors'),
    url(r'^api/geolayer/$', GeoLayerView.as_view(), name='geolayer'),
    url(r'^api/organization-geolayer/$', organization_geolayer, name='organization_geolayer'),
    url(r'^api/enable-project-cluster-sites/(?P<pk>\d+)/$', EnableClusterSitesView.as_view(),
        name='enable_project_cluster_sites'),

]


