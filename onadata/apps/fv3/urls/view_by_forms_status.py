from django.conf.urls import url
from onadata.apps.fv3.viewsets.ViewFormViewset import ProjectSiteResponsesViewSet, ProjectSiteSubmissionStatusViewSet,\
    FormSubmissionsViewSet

view_by_forms_status_urlpatterns = [
    url(r'^api/view-by-forms/$', ProjectSiteResponsesViewSet.as_view(), name='responses'),
    url(r'^api/view-by-status/$', ProjectSiteSubmissionStatusViewSet.as_view(), name='submission_status'),
    url(r'^api/forms-submissions/$', FormSubmissionsViewSet.as_view(), name='form_submissions'),

]


