from django.conf.urls import url

from onadata.apps.fv3.views import supervisor_projects, MySuperviseSitesViewset, site_blueprints, supervisor_logs
from onadata.apps.fv3.viewsets.FormsViewset import MyFormsViewSet, MyProjectFormsViewSet
from onadata.apps.fv3.viewsets.SubmissionViewSet import SubmissionViewSet
from onadata.apps.fv3.viewsets.OrganizationViewSet import OrganizationViewSet
from onadata.apps.fv3.viewsets.SiteViewSet import SiteViewSet, site_map, SiteSubmissionsViewSet

urlpatterns = [

    url(r'^api/projects/', supervisor_projects, name='supervisor_projects'),
    url(r'^api/sites/', MySuperviseSitesViewset.as_view({'get': 'list'}),  name='supervisor_sites'),
    url(r'^api/site/blueprint/', site_blueprints, name='site_blueprints'),
    url(r'^api/user/logs/', supervisor_logs, name='supervisor_logs'),

    url(r'^api/myforms/', MyFormsViewSet.as_view({'get':'list'}), name='my_forms'),
    url(r'^api/myprojectforms/', MyProjectFormsViewSet.as_view({'get':'list'}), name='my_project_forms'),


    url(r'^api/submission/(?P<pk>\d+)/$', SubmissionViewSet.as_view({'get':'retrieve'}), name='submission'),
    url(r'^api/organization/(?P<pk>\d+)/$', OrganizationViewSet.as_view({'get': 'retrieve'}), name='organization'),
    url(r'^api/site/(?P<pk>\d+)/$', SiteViewSet.as_view({'get': 'retrieve'}), name='site'),
    url(r'^api/site-map/(?P<pk>\d+)/$', site_map, name='site_map'),
    url(r'^api/site-submissions/$', SiteSubmissionsViewSet.as_view({'get': 'list'}), name='site_submissions'),

]
