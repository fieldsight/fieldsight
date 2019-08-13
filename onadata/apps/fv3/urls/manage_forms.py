from django.conf.urls import url
from onadata.apps.fv3.viewsets.manage_forms import GeneralFormsVS, \
    GeneralProjectFormsVS, ScheduleFormsVS, StageFormsVS, SubStageFormsVS

manage_forms_urlpatterns = [

    url(r'^api/manage-forms/general/$',
        GeneralFormsVS.as_view({'get': 'list', 'post':'create'}),
        name='gfl'),
    url(r'^api/manage-forms/general/(?P<pk>\d+)/$',
        GeneralFormsVS.as_view({'put':'update'}),
        name='updategfl'),
    url(r'^api/manage-forms/survey/$',
        GeneralProjectFormsVS.as_view({'get': 'list', 'post':'create'}),
        name='surveyfl'),
    url(r'^api/manage-forms/survey/(?P<pk>\d+)/$',
        GeneralProjectFormsVS.as_view({'put':'update'}),
        name='updatesfl'),
    url(r'^api/manage-forms/schedule/$',
        ScheduleFormsVS.as_view({'get': 'list', 'post':'create'}),
        name='schedulefl'),
    url(r'^api/manage-forms/schedule/(?P<pk>\d+)/$',
        ScheduleFormsVS.as_view({'put': 'update'}),
        name='schedulefu'),
    url(r'^api/manage-forms/stages/$',
        StageFormsVS.as_view({'get': 'list',  'post':'create'}),
        name='stagelist'),
    url(r'^api/manage-forms/stages/(?P<pk>\d+)/$',
        StageFormsVS.as_view({'put': 'update'}),
        name='stageupdate'),
    url(r'^api/manage-forms/sub-stages/$',
        SubStageFormsVS.as_view({'get': 'list', 'post':'create'}),
        name='substagelist'),
    url(r'^api/manage-forms/sub-stages/(?P<pk>\d+)/$',
        SubStageFormsVS.as_view({'put': 'update'}),
        name='substageupdate'),


]