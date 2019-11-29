from django.conf.urls import url
from onadata.apps.fv3.viewsets.map import ProjectsApi, OrganizationViewset, CountriesApi, SiteViewset, \
    ProjectsInCountries

map_urlpatterns = [

    url(r'^api/map/projects/$', ProjectsApi.as_view(), name='projects'),
    url(r'^api/map/sites/$', SiteViewset.as_view({'get': 'list'}), name='sites'),
    url(r'^api/map/organizations/$', OrganizationViewset.as_view({'get': 'list'}), name='orgs'),
    url(r'^api/map/countries/$', CountriesApi.as_view(), name='countries'),
    url(r'^api/map/projects-countries/$', ProjectsInCountries.as_view(), name='projects_in_countries'),

]

