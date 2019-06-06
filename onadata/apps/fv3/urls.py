from django.conf.urls import url

from onadata.apps.fv3.views import supervisor_projects, MySuperviseSitesViewset, site_blueprints, supervisor_logs, \
    ProjectUpdateViewset, sectors_subsectors, ProjectSiteTypesViewset, SiteTypesViewset, ProjectTermsLabelsViewset, \
    TermsLabelsViewset, ProjectRegionsViewset, RegionViewset, GeoLayerView

urlpatterns = [

    url(r'^api/projects/', supervisor_projects, name='supervisor_projects'),
    url(r'^api/sites/', MySuperviseSitesViewset.as_view({'get': 'list'}),  name='supervisor_sites'),
    url(r'^api/site/blueprint/', site_blueprints, name='site_blueprints'),
    url(r'^api/user/logs/', supervisor_logs, name='supervisor_logs'),

    url(r'^api/update-project/(?P<pk>\d+)$', ProjectUpdateViewset.as_view(),
        name='update_project_api'),
    url(r'^api/sectors-subsectors/$', sectors_subsectors.as_view({'get':'list'}), name='sectors_subsectors'),
    url(r'^api/project-site-types/(?P<pk>\d+)$', ProjectSiteTypesViewset.as_view({'get': 'list', 'post':'create'}),
        name='project_site_types'),
    url(r'^api/site-types/(?P<pk>\d+)$', SiteTypesViewset.as_view(), name='site_types'),
    url(r'^api/project-terms-labels/(?P<pk>\d+)$', ProjectTermsLabelsViewset.as_view({'get': 'list', 'post':'create'}),
        name='project_terms_labels'),
    url(r'^api/terms-labels/(?P<pk>\d+)$', TermsLabelsViewset.as_view(), name='terms_labels'),
    url(r'^api/project-regions/(?P<pk>\d+)$', ProjectRegionsViewset.as_view({'get': 'list', 'post': 'create'}),
        name='project_regions'),
    url(r'^api/region/(?P<pk>\d+)$', RegionViewset.as_view(), name='region'),
    url(r'^api/geolayer/(?P<pk>\d+)$', GeoLayerView.as_view(), name='geolayer'),

]
