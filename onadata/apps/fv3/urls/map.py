from django.conf.urls import url
from onadata.apps.fv3.viewsets.map import ProjectsApi, OrganizationViewset, CountriesApi, SiteViewset, \
    ProjectsInCountries, ProjectSiteMetaAttributesView, FormQuestionsView, ProjectFiltersMetrics, \
    ProjectMapFiltersListView

map_urlpatterns = [

    url(r'^api/map/projects/$', ProjectsApi.as_view(), name='projects'),
    url(r'^api/map/sites/$', SiteViewset.as_view({'get': 'list'}), name='sites'),
    url(r'^api/map/organizations/$', OrganizationViewset.as_view({'get': 'list'}), name='orgs'),
    url(r'^api/map/countries/$', CountriesApi.as_view(), name='countries'),
    url(r'^api/map/projects-countries/$', ProjectsInCountries.as_view(), name='projects_in_countries'),
    url(r'^api/project-meta-attributes/(?P<pk>\d+)/$', ProjectSiteMetaAttributesView.as_view(),
        name='project_site_meta_attributes'),
    url(r'^api/form-questions/(?P<pk>\d+)/$', FormQuestionsView.as_view(),
        name='form_questions'),
    url(r'^api/project-filters-metrics/(?P<pk>\d+)/$', ProjectFiltersMetrics.as_view({'get': 'list'}),
        name='project_filters_metrics'),
    url(r'^api/update-project-filters-metrics/(?P<pk>\d+)/$', ProjectFiltersMetrics.as_view({'put': 'update'}),
        name='update_project_filters_metrics'),
    url(r'^api/project-map-filters-list/(?P<pk>\d+)/$', ProjectMapFiltersListView.as_view(),
        name='project_map_filters_list'),

]

