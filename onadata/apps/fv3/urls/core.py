from django.conf.urls import url, include
from rest_framework import routers

from onadata.apps.fv3.urls.project_settings import progress_urlpatterns
from onadata.apps.fv3.views import supervisor_projects, MySuperviseSitesViewset, site_blueprints, supervisor_logs, \
    ProjectUpdateViewset, sectors_subsectors, ProjectSiteTypesViewset, ProjectTermsLabelsViewset, \
    ProjectRegionsViewset, GeoLayerView, ProjectDefineSiteMeta, ProjectSitesViewset, organization_geolayer

from onadata.apps.fv3.viewsets.OrganizationViewSet import OrganizationViewSet
from onadata.apps.fv3.viewsets.SiteViewSet import SiteViewSet, site_map, SiteSubmissionsViewSet
from onadata.apps.fv3.viewsets.FormsViewset import MyFormsViewSet, MyProjectFormsViewSet, ShareFormViewSet, \
    ShareProjectFormViewSet, ShareTeamFormViewSet, ShareGlobalFormViewSet, FormAddLanguageViewSet, CloneFormViewSet, \
    MyFormDeleteViewSet, ShareUserListViewSet, ShareTeamListViewSet, ShareProjectListViewSet

from onadata.apps.fv3.viewsets.ReportViewsets import ReportVs

from onadata.apps.fv3.viewsets.SubmissionViewSet import AlterSubmissionStatusViewSet, SubmissionAnswerViewSet, \
    SubmissionViewSet
from onadata.apps.fv3.viewsets.ProjectSitesListViewset import ProjectSitesListViewSet


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
    url(r'^api/organization/(?P<pk>\d+)/$', OrganizationViewSet.as_view({'get': 'retrieve'}), name='organization'),
    url(r'^api/site/(?P<pk>\d+)/$', SiteViewSet.as_view({'get': 'retrieve'}), name='site'),
    url(r'^api/site-map/(?P<pk>\d+)/$', site_map, name='site_map'),
    url(r'^api/site-submissions/$', SiteSubmissionsViewSet.as_view({'get': 'list'}), name='site_submissions'),
    url(r'^api/submission-answers/(?P<pk>\d+)/$', SubmissionAnswerViewSet.as_view({'get':'retrieve'}), name='submission-data'),
    url(r'^api/change/submission/status/$', AlterSubmissionStatusViewSet.as_view({'post':'create'}), name='submission-flag'),


    url(r'^api/share/$', ShareFormViewSet.as_view(), name='share_form'),
    url(r'^api/share/project/$', ShareProjectFormViewSet.as_view(), name='share_project_form'),
    url(r'^api/share/team/$', ShareTeamFormViewSet.as_view(), name='share_team_form'),
    url(r'^api/share/global/$', ShareGlobalFormViewSet.as_view(), name='share_global_form'),
    url(r'^api/clone/$', CloneFormViewSet.as_view(), name='clone_form'),

    url(r'^api/report/$', ReportVs.as_view({'post':'create'}), name='report'),

    url(r'^api/add-language/$', FormAddLanguageViewSet.as_view(), name='add_language'),
    url(r'^api/form/delete/$', MyFormDeleteViewSet.as_view(), name='myform-delete'),
    url(r'^api/form/users/$', ShareUserListViewSet.as_view({'get': 'list'}), name='shareable-users'),
    url(r'api/form/teams/$', ShareTeamListViewSet.as_view({'get': 'list'}), name='shareable-team'),
    url(r'api/form/projects/$', ShareProjectListViewSet.as_view({'get': 'list'}), name='shareable-project'),

    url(r'^api/project-site-list/', ProjectSitesListViewSet.as_view({'get': 'list'}), name='project_sites_list'),
]

urlpatterns += progress_urlpatterns