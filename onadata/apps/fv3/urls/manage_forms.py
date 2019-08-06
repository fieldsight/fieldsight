from django.conf.urls import url
from onadata.apps.fv3.viewsets.manage_forms import GeneralFormsVS, \
    GeneralProjectFormsVS

manage_forms_urlpatterns = [

    url(r'^api/manage-forms/general/$',
        GeneralFormsVS.as_view({'get':'list'}),
        name='gfl'),
    url(r'^api/manage-forms/survey/$',
        GeneralProjectFormsVS.as_view({'get':'list'}),
        name='gpfl'),

]