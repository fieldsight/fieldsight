from django.conf.urls import url, include

from rest_framework import routers
from onadata.apps.fv3.viewsets.ProjectDashboardViewSet import ProjectDashboardViewSet, ProjectProgressTableViewSet, \
    project_regions_types, ProjectSurveyFormsViewSet, SiteFormViewSet, SitelistForMetasLink, \
    UpdateProjectGeojson, OrganizationLibraryFormsViewSet, SupervisorProjectDashboardView, \
    ProjectFormSubmissionsChartData, ProjectLogsView

router = routers.DefaultRouter()

router.register(r'site-form', SiteFormViewSet, base_name='site_form')

project_dashboard_urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api/project/(?P<pk>\d+)/$', ProjectDashboardViewSet.as_view({'get': 'retrieve'}), name='project'),
    url(r'^api/project-chart-data/(?P<pk>\d+)/$',
        ProjectFormSubmissionsChartData.as_view(), name='project_form_submissions'),
    url(r'^api/project-logs/(?P<pk>\d+)/$', ProjectLogsView.as_view(), name='project_logs'),

    url(r'^api/project-regions-types/(?P<pk>\d+)/$', project_regions_types, name='project_regions_types'),
    url(r'^api/progress-table/(?P<pk>\d+)/$', ProjectProgressTableViewSet.as_view(),
        name='progress_table'),
    url(r'^api/project-survey-forms/(?P<pk>\d+)/$', ProjectSurveyFormsViewSet.as_view(),
        name='project_survey_forms'),
    url(r'^api/project-sites-for-metas/(?P<pk>\d+)/$', SitelistForMetasLink.as_view({'get': 'list'}),
        name='project_sites_metas'),
    url(r'^api/project-dashboard/(?P<pk>\d+)/$', SupervisorProjectDashboardView.as_view(),
        name='supervisor_project_dashboard'),
    url(r'^api/update-project-geojson/(?P<pk>\d+)/$', UpdateProjectGeojson.as_view(),
        name='update_project_geojson'),
    url(r'^api/organization-library-forms/(?P<pk>\d+)/$', OrganizationLibraryFormsViewSet.as_view({'get': 'list'}),
        name='organization_library_forms'),

]


