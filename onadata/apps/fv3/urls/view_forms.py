from django.conf.urls import url
from onadata.apps.fv3.viewsets.ViewFormViewset import ProjectSiteResponsesView

view_forms_urlpatterns = [
    url(r'^api/responses/$', ProjectSiteResponsesView.as_view(), name='responses'),

]


