from django.conf.urls import url, include
from .viewsets import ReportingProjectForms

urlpatterns = [

    url(r'project-forms/(?P<pk>\d+)/$', ReportingProjectForms.as_view(), name='reporting_project_forms'),
]

