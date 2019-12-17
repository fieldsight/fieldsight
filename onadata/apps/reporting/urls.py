from django.conf.urls import url, include
from .viewsets import ReportingProjectFormData, ReportSettingsViewSet

urlpatterns = [

    url(r'project-form-data/(?P<pk>\d+)/$', ReportingProjectFormData.as_view(), name='reporting_project_form_data'),
    url(r'add-report/(?P<pk>\d+)/$', ReportSettingsViewSet.as_view({'post': 'create'}), name='report_add'),

]

