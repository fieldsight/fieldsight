from django.conf.urls import url

from onadata.apps.fv3.views import supervisor_projects, MySuperviseSitesViewset, site_blueprints, supervisor_logs
from onadata.apps.fv3.viewsets.FormsViewset import MyFormsViewSet, MyProjectFormsViewSet, ShareFormViewSet, \
    ShareProjectFormViewSet, ShareTeamFormViewSet
from onadata.apps.fv3.viewsets.ReportViewsets import ReportVs
from onadata.apps.fv3.viewsets.SubmissionViewSet import SubmissionViewSet, AlterSubmissionStatusViewSet, \
    SubmissionAnswerViewSet, SubmissionViewSet


urlpatterns = [

    url(r'^api/projects/', supervisor_projects, name='supervisor_projects'),
    url(r'^api/sites/', MySuperviseSitesViewset.as_view({'get': 'list'}),  name='supervisor_sites'),
    url(r'^api/site/blueprint/', site_blueprints, name='site_blueprints'),
    url(r'^api/user/logs/', supervisor_logs, name='supervisor_logs'),

    url(r'^api/myforms/', MyFormsViewSet.as_view({'get':'list'}), name='my_forms'),
    url(r'^api/myprojectforms/', MyProjectFormsViewSet.as_view({'get':'list'}), name='my_project_forms'),


    url(r'^api/submission/(?P<pk>\d+)/$', SubmissionViewSet.as_view({'get':'retrieve'}), name='submission'),
    url(r'^api/submission-answers/(?P<pk>\d+)/$', SubmissionAnswerViewSet.as_view({'get':'retrieve'}), name='submission-data'),
    url(r'^api/change/submission/status/$', AlterSubmissionStatusViewSet.as_view({'post':'create'}), name='submission-flag'),


    url(r'^api/share/(?P<pk>\d+)/$', ShareFormViewSet.as_view(), name='share_form'),
    url(r'^api/share/project/(?P<pk>\d+)/$', ShareProjectFormViewSet.as_view(), name='share_project_form'),
    url(r'^api/share/team/(?P<pk>\d+)/$', ShareTeamFormViewSet.as_view(), name='share_team_form'),


    url(r'^api/report/$', ReportVs.as_view({'post':'create'}), name='report'),

    ]


