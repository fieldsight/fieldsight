from django.conf.urls import url, include
from rest_framework import routers

from onadata.apps.fv3.urls.project_settings import progress_urlpatterns
from onadata.apps.fv3.urls.myroles import my_roles_urlpatterns
from onadata.apps.fv3.urls.site_dashboard import site_dashboard_urlpatterns
from onadata.apps.fv3.urls.manage_forms import manage_forms_urlpatterns
from onadata.apps.fv3.views import supervisor_projects, MySuperviseSitesViewset, site_blueprints, supervisor_logs, \
    ProjectDefineSiteMeta, ProjectSitesViewset, check_region
from onadata.apps.fv3.viewsets.OrganizationViewSet import OrganizationViewSet
from onadata.apps.fv3.viewsets.FormsViewset import MyFormsViewSet, MyProjectFormsViewSet, ShareFormViewSet, \
    ShareProjectFormViewSet, ShareTeamFormViewSet, ShareGlobalFormViewSet, FormAddLanguageViewSet, CloneFormViewSet, \
    MyFormDeleteViewSet, ShareUserListViewSet, ShareTeamListViewSet, ShareProjectListViewSet, MySharedFormViewSet

from onadata.apps.fv3.viewsets.ReportViewsets import ReportVs

from onadata.apps.fv3.viewsets.SubmissionViewSet import AlterSubmissionStatusViewSet, SubmissionAnswerViewSet, \
    SubmissionViewSet
from onadata.apps.fv3.viewsets.ProjectSitesListViewset import \
    ProjectSitesListViewSet, SubSitesListViewSet

from onadata.apps.fv3.views import RegionalSites, sub_regions

router = routers.DefaultRouter()

router.register(r'project-sites', ProjectSitesViewset, base_name='project-sites')


urlpatterns = [

    url(r'^api/', include(router.urls)),
    url(r'^api/projects/', supervisor_projects, name='supervisor_projects'),
    url(r'^api/sites/', MySuperviseSitesViewset.as_view({'get': 'list'}),  name='supervisor_sites'),
    url(r'^api/site/blueprint/', site_blueprints, name='site_blueprints'),
    url(r'^api/user/logs/', supervisor_logs, name='supervisor_logs'),
    url(r'^api/check-region/(?P<project_id>\d+)/$', check_region, name='check_region'),

    url(r'^api/project-define-site-meta/(?P<pk>\d+)/$', ProjectDefineSiteMeta.as_view(), name='project_define_site_meta'),

    url(r'^api/myforms/', MyFormsViewSet.as_view({'get':'list'}), name='my_forms'),
    url(r'^api/sharedforms/', MySharedFormViewSet.as_view({'get':'list'}), name='my_shared_forms'),
    url(r'^api/myprojectforms/', MyProjectFormsViewSet.as_view({'get':'list'}), name='my_project_forms'),


    url(r'^api/submission/(?P<pk>\d+)/$', SubmissionViewSet.as_view({'get':'retrieve'}), name='submission'),
    url(r'^api/organization/(?P<pk>\d+)/$', OrganizationViewSet.as_view({'get': 'retrieve'}), name='organization'),

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

    url(r'^api/project-site-list/$', ProjectSitesListViewSet.as_view({'get': 'list'}), name='project_sites_list'),
    url(r'^api/sub-site-list/$', SubSitesListViewSet.as_view(
        {'get': 'list'}), name='sub_sites_list'),
    url(r'^api/regional-sites/$', RegionalSites.as_view({'get' : 'list'}), name='regional_sites'),
    url(r'^api/sub-regions/$', sub_regions, name='sub_regions'),

]

urlpatterns += progress_urlpatterns
urlpatterns += my_roles_urlpatterns
urlpatterns += site_dashboard_urlpatterns
urlpatterns += manage_forms_urlpatterns