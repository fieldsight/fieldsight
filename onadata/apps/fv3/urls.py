from django.conf.urls import url, include
from rest_framework import routers

from onadata.apps.fv3.views import supervisor_projects, MySuperviseSitesViewset, site_blueprints, supervisor_logs, \
    ProjectUpdateViewset, sectors_subsectors, ProjectSiteTypesViewset, ProjectTermsLabelsViewset, \
    ProjectRegionsViewset, GeoLayerView, ProjectDefineSiteMeta


router = routers.DefaultRouter()

router.register(r'project-terms-labels', ProjectTermsLabelsViewset, base_name='project-terms-labels')
router.register(r'project-regions', ProjectRegionsViewset, base_name='project-regions')
router.register(r'project-site-types', ProjectSiteTypesViewset, base_name='project-site-types')


urlpatterns = [

    url(r'^api/', include(router.urls)),
    url(r'^api/projects/', supervisor_projects, name='supervisor_projects'),
    url(r'^api/sites/', MySuperviseSitesViewset.as_view({'get': 'list'}),  name='supervisor_sites'),
    url(r'^api/site/blueprint/', site_blueprints, name='site_blueprints'),
    url(r'^api/user/logs/', supervisor_logs, name='supervisor_logs'),

    url(r'^api/update-project/(?P<pk>\d+)/$', ProjectUpdateViewset.as_view(),
        name='update_project_api'),
    url(r'^api/sectors-subsectors/$', sectors_subsectors.as_view({'get':'list'}), name='sectors_subsectors'),
    url(r'^api/geolayer/$', GeoLayerView.as_view(), name='geolayer'),
    url(r'^api/project-define-site-meta/(?P<pk>\d+)/$', ProjectDefineSiteMeta.as_view(), name='project_define_site_meta'),

]
