from django.conf.urls import url
from onadata.apps.fv3.viewsets.manage_forms import GeneralFormsVS

manage_forms_urlpatterns = [

    url(r'^api/manage-forms/$',
        GeneralFormsVS.as_view({'get':'list'}),
        name='gfl'),

]