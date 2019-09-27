from django.conf.urls import url
from onadata.apps.fv3.viewsets.ViewFormViewset import ProjectSiteResponsesView, ProjectSiteSubmissionStatusView,\
    FormSubmissionsView, DeleteFInstanceView

view_by_forms_status_urlpatterns = [
    url(r'^api/view-by-forms/$', ProjectSiteResponsesView.as_view(), name='responses'),
    url(r'^api/view-by-status/$', ProjectSiteSubmissionStatusView.as_view(), name='submission_status'),
    url(r'^api/forms-submissions/$', FormSubmissionsView.as_view(), name='form_submissions'),
    url(r'^api/delete-submission/(?P<pk>\d+)/$', DeleteFInstanceView.as_view(), name='delete_submission'),

]


