from django.conf.urls import url
from onadata.apps.fv3.viewsets.manage_forms import GeneralFormsVS, \
    GeneralProjectFormsVS, ScheduleFormsVS, StageFormsVS, SubStageFormsVS, \
    DeployForm, DeleteUndeployedForm, FormSettingsVS, BreadCrumView
from onadata.apps.fsforms.viewsets.AssignedXFormListApiViewSet import \
    AssignedXFormListApi

manage_forms_urlpatterns = [

    url(r'^api/manage-forms/breadcrums/$',
        BreadCrumView.as_view(),
        name='gfl'),
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
    url(r'^api/manage-forms/deploy/$',
        DeployForm.as_view(),
        name='deploy'),
    url(r'^api/manage-forms/delete/$',
        DeleteUndeployedForm.as_view(),
        name='delete'),
    url(r'^assignedFormList/project/$', AssignedXFormListApi.as_view(
            {'get': 'multiple_project_forms'}), name='multiple-project-form-list'),
    url(r'^assignedFormList/siteLevel/$', AssignedXFormListApi.as_view(
            {'get': 'multiple_site_overide_forms'}),
            name='multiple-site-overide-form-list'),
    url(r'^api/forms/settings/$',
        FormSettingsVS.as_view({'post': 'create', 'get': 'retrieve'}),
        name='settings'),
    url(r'^api/forms/settings/(?P<pk>\d+)$',
        FormSettingsVS.as_view({'put': 'update'}),
        name='settings-edit'),

]