from django.conf.urls import url, include
from rest_framework import routers

from onadata.apps.fv3.views import supervisor_projects, MySuperviseSitesViewset, site_blueprints, supervisor_logs, \
    ProjectUpdateViewset, sectors_subsectors, ProjectSiteTypesViewset, ProjectTermsLabelsViewset, \
    ProjectRegionsViewset, GeoLayerView, ProjectDefineSiteMeta, ProjectSitesViewset, organization_geolayer

from onadata.apps.fv3.views import supervisor_projects, MySuperviseSitesViewset, site_blueprints, supervisor_logs
from onadata.apps.fv3.viewsets.FormsViewset import MyFormsViewSet, MyProjectFormsViewSet, ShareFormViewSet, \
    ShareProjectFormViewSet, ShareTeamFormViewSet
from onadata.apps.fv3.viewsets.SubmissionViewSet import SubmissionViewSet, AlterSubmissionStatusViewSet, \
    SubmissionAnswerViewSet, SubmissionViewSet


router = routers.DefaultRouter()

router.register(r'project-terms-labels', ProjectTermsLabelsViewset, base_name='project-terms-labels')
router.register(r'project-regions', ProjectRegionsViewset, base_name='project-regions')
router.register(r'project-sites', ProjectSitesViewset, base_name='project-sites')
router.register(r'project-site-types', ProjectSiteTypesViewset, base_name='project-site-types')





urlpatterns = [

    url(r'^api/', include(router.urls)),
    url(r'^api/projects/', supervisor_projects, name='supervisor_projects'),
    url(r'^api/sites/', MySuperviseSitesViewset.as_view({'get': 'list'}),  name='supervisor_sites'),
    url(r'^api/site/blueprint/', site_blueprints, name='site_blueprints'),
    url(r'^api/user/logs/', supervisor_logs, name='supervisor_logs'),


    url(r'^api/update-project/(?P<pk>\d+)/$', ProjectUpdateViewset.as_view(),
        name='update_project_api'),
    url(r'^api/organization-geolayer/$', organization_geolayer, name='organization_geolayer'),
    url(r'^api/sectors-subsectors/$', sectors_subsectors.as_view({'get':'list'}), name='sectors_subsectors'),
    url(r'^api/geolayer/$', GeoLayerView.as_view(), name='geolayer'),
    url(r'^api/project-define-site-meta/(?P<pk>\d+)/$', ProjectDefineSiteMeta.as_view(), name='project_define_site_meta'),

    url(r'^api/myforms/', MyFormsViewSet.as_view({'get':'list'}), name='my_forms'),
    url(r'^api/myprojectforms/', MyProjectFormsViewSet.as_view({'get':'list'}), name='my_project_forms'),


    url(r'^api/submission/(?P<pk>\d+)/$', SubmissionViewSet.as_view({'get':'retrieve'}), name='submission'),
    url(r'^api/submission-answers/(?P<pk>\d+)/$', SubmissionAnswerViewSet.as_view({'get':'retrieve'}), name='submission-data'),
    url(r'^api/change/submission/status/$', AlterSubmissionStatusViewSet.as_view({'post':'create'}), name='submission-flag'),


    url(r'^api/share/(?P<pk>\d+)/$', ShareFormViewSet.as_view(), name='share_form'),
    url(r'^api/share/project/(?P<pk>\d+)/$', ShareProjectFormViewSet.as_view(), name='share_project_form'),
    url(r'^api/share/team/(?P<pk>\d+)/$', ShareTeamFormViewSet.as_view(), name='share_team_form'),
    ]



