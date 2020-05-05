from __future__ import unicode_literals
import json
import uuid
from base64 import b64decode

import datetime
from bson import json_util
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse, reverse_lazy
from django.db import transaction
from django.db.models import Q, Sum, F, Max
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.views.generic import ListView, DetailView, TemplateView, View
from django.http import HttpResponse, HttpResponseForbidden, Http404, HttpResponseBadRequest

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, parser_classes, \
    authentication_classes
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
from rest_framework.response import Response

from onadata.apps.fieldsight.models import Site, Project

from onadata.apps.fsforms.enketo_utils import enketo_view_url, \
    enketo_url_new_submission, enketo_preview_url, \
    CsrfExemptSessionAuthentication
from onadata.apps.users.models import UserProfile
from onadata.apps.fsforms.reports_util import delete_form_instance, get_images_for_site_all, get_instances_for_field_sight_form, build_export_context, \
    get_xform_and_perms, query_mongo, get_instance, update_status, get_instances_for_project_field_sight_form
from onadata.apps.fsforms.serializers.ConfigureStagesSerializer import StageSerializer, SubStageSerializer, \
    SubStageDetailSerializer
from onadata.apps.fsforms.serializers.FieldSightXFormSerializer import FSXFormListSerializer, StageFormSerializer
from onadata.apps.fsforms.serializers.StageSerializer import EMSerializer
from onadata.apps.fsforms.utils import send_message, send_message_stages, send_message_xf_changed, \
    send_bulk_message_stages, \
    send_message_un_deploy, send_bulk_message_stages_deployed_project, send_bulk_message_stages_deployed_site, \
    send_bulk_message_stage_deployed_project, send_bulk_message_stage_deployed_site, send_sub_stage_deployed_project, \
    send_sub_stage_deployed_site, send_message_flagged, send_message_un_deploy_project, get_version, image_urls_dict, \
    inject_instanceid, has_change_form_permission
from onadata.apps.logger.models import XForm, Attachment, Instance
from onadata.apps.main.models import MetaData
from onadata.apps.main.views import set_xform_owner_data
from onadata.apps.viewer.models.parsed_instance import update_mongo_instance
from onadata.libs.utils.user_auth import add_cors_headers
from onadata.libs.utils.user_auth import helper_auth_helper
from onadata.libs.utils.log import audit_log, Actions
from onadata.libs.utils.logger_tools import response_with_mimetype_and_name
from onadata.apps.fieldsight.mixins import group_required, LoginRequiredMixin, ProjectMixin, \
    CreateView, UpdateView, DeleteView, KoboFormsMixin, SiteMixin, SuperAdminMixin
from onadata.libs.utils.viewer_tools import _get_form_url, enketo_url
from .forms import AssignSettingsForm, FSFormForm, FormTypeForm, FormStageDetailsForm, FormScheduleDetailsForm, \
    StageForm, ScheduleForm, GroupForm, AddSubSTageForm, AssignFormToStageForm, AssignFormToScheduleForm, \
    AlterAnswerStatus, MainStageEditForm, SubStageEditForm, GeneralFSForm, GroupEditForm, GeneralForm, KoScheduleForm, \
    EducationalmaterialForm
from .models import DeletedXForm, FieldSightXF, Stage, Schedule, FormGroup, FieldSightFormLibrary, \
    InstanceStatusChanged, FInstance, \
    EducationMaterial, EducationalImages, InstanceImages, DeployEvent, XformHistory
from django.db.models import Q
from onadata.apps.fieldsight.rolemixins import FInstanceRoleMixin, MyFormMixin, ConditionalFormMixin, ReadonlyFormMixin, SPFmixin, FormMixin, ReviewerRoleMixin, ProjectRoleMixin, ReadonlyProjectLevelRoleMixin, ReadonlySiteLevelRoleMixin
from onadata.apps.fsforms.XFormMediaAttributes import get_questions_and_media_attributes
from .fieldsight_logger_tools import save_submission

from onadata.apps.fsforms.tasks import copy_schedule_to_sites, copy_sub_stage_to_sites, copy_stage_to_sites, \
    copy_allstages_to_sites

import requests



TYPE_CHOICES = {3, 'Normal Form', 2, 'Schedule Form', 1, 'Stage Form'}


class UniqueXformMixin(object):
    def get_queryset(self):
        return FieldSightXF.objects.order_by('xf__id').distinct('xf__id')


class FSFormView(object):
    model = XForm
    paginate_by = 50
    success_url = reverse_lazy('forms:library-forms-list')
    form_class = FSFormForm


class OwnListView(ListView):

    def get_template_names(self):
        return ['fsforms/my_form_list.html']

    def get_queryset(self):
        search_xform_key = self.request.GET.get('q', None)
        if search_xform_key is not None:
            return XForm.objects.filter(user=self.request.user, deleted_xform=None, title__icontains=search_xform_key).order_by('-date_modified')
        return XForm.objects.filter(user=self.request.user, deleted_xform=None).order_by('-date_modified')


class LibraryFormView(object):
    model = FieldSightFormLibrary
    success_url = reverse_lazy('forms:library-forms-list')


class MyLibraryListView(ListView):

    def get_queryset(self):
        if self.request.project:
            return super(MyLibraryListView, self).\
                get_queryset().filter(Q(is_global=True)
                                      | Q(project=self.request.project)
                                      |Q(organization=self.request.organization))
        elif self.request.organization:
            return super(MyLibraryListView, self).\
                get_queryset().filter(Q(is_global=True)
                                      |Q(organization=self.request.organization))
        else:
            return super(MyLibraryListView, self).get_queryset()

    def get_template_names(self):
        return ['fsforms/library_form_list.html']


class LibraryFormsListView(LibraryFormView, MyLibraryListView, ProjectMixin):
    pass


class MyOwnFormsListView(LoginRequiredMixin, FSFormView, OwnListView):

    def dispatch(self, request, *args, **kwargs):
        return HttpResponseRedirect('/fieldsight/application/#/forms/myform')

class FormView(object):
    model = FieldSightXF
    success_url = reverse_lazy('forms:forms-list')
    form_class = FSFormForm


@login_required
@require_POST
def share_level(request, id, counter):
    xf = XForm.objects.get(id_string=id)
    # sl = dict(request.POST).get('sl')[int(counter)-1]
    sl = request.POST.get('sl')
    if not FieldSightFormLibrary.objects.filter(xf__id_string=id).exists():
        form = FieldSightFormLibrary()
        form.xf= xf
    else:
        form = FieldSightFormLibrary.objects.get(xf__id_string=id)
    if not sl:
        if form.pk:
            form.delete()
            messages.add_message(request, messages.WARNING, u'{0} Form Shared Removed'.format(xf.title))
    else:
        if sl == '0':
            form.is_global = True
            form.organization = None
            form.project = None
            form.save()
            messages.add_message(request, messages.INFO, u'{0} Shared '
                                                         u'Globally '.format(xf.title))
        elif sl == '1':
            form.is_global = False
            if hasattr(request,"project") and request.project:
                form.organization = request.project.organization
                form.project = None
                form.save()
                messages.add_message(request, messages.INFO, u'{0} Shared To '
                                                             u'Organization Level'.format(xf.title))
            elif hasattr(request,"organization") and request.organization:
                form.organization = request.organization
                form.project = None
                form.save()
                messages.add_message(request, messages.INFO, u'{0} Shared To '
                                                             u'Organization Level'.format(xf.title))
            else:
                messages.add_message(request, messages.WARNING, u'{0} Not '
                                                                u'Shared. You Cannot Share to Organization Level'.
                                     format(xf.title))
        elif sl == '2':
            if hasattr(request,"project") and request.project:
                form.is_global  = False
                form.organization = None
                form.project = request.project
                form.save()
                messages.add_message(request, messages.INFO, u'{0} Shared to '
                                                             u'Project Level '.format(xf.title))
            else:
                messages.add_message(request, messages.WARNING, u'{0} Form '
                                                                u'Not Shared. You Cannot Share to Project Level'
                                     .format(xf.title))

    return HttpResponseRedirect(reverse('forms:forms-list'))


class MyProjectListView(ListView):
    def get_template_names(self):
        return ['fsforms/my_project_form_list.html']

    def get_queryset(self):
        if self.request.site:
            return FieldSightXF.objects.filter(site__id=self.request.site.id)
        elif self.request.project:
            return FieldSightXF.objects.filter(site__project__id=self.request.project.id)
        elif self.request.organization:
            return FieldSightXF.objects.filter(site__project__organization__id=self.request.organization.id)
        else: return FieldSightXF.objects.filter(site__isnull=False)


class AssignedFormListView(ListView):
    def get_template_names(self):
        return ['fsforms/assigned_form_list.html']

    def get_queryset(self):
        return FieldSightXF.objects.filter(site__id=self.request.site.id)


class FormsListView(FormView, LoginRequiredMixin, SiteMixin, MyProjectListView):
    pass


class AssignedFormsListView(FormView, LoginRequiredMixin, SiteMixin, AssignedFormListView):
    pass


class StageView(object):
    model = Stage
    success_url = reverse_lazy('forms:stages-list')
    form_class = StageForm


class MainStagesOnly(ListView):
    def get_queryset(self):
        return Stage.objects.filter(stage=None)


class StageListView(StageView, LoginRequiredMixin, MainStagesOnly):
    pass


class StageCreateView(StageView, LoginRequiredMixin, KoboFormsMixin, CreateView):
    pass


class StageUpdateView(StageView, LoginRequiredMixin, KoboFormsMixin, UpdateView):
    pass


class StageDeleteView(StageView, LoginRequiredMixin, KoboFormsMixin, DeleteView):
    pass


@group_required("Project")
def add_sub_stage(request, pk=None):
    stage = get_object_or_404(
        Stage, pk=pk)
    if request.method == 'POST':
        form = AddSubSTageForm(data=request.POST, request=request)
        if form.is_valid():
            child_stage = form.save(commit=False)
            child_stage.stage = stage
            child_stage.project = stage.project
            child_stage.site = stage.site
            child_stage.group = stage.group
            child_stage.save()
            form = int(form.cleaned_data.get('form',0))
            if form:
                if stage.site:
                    FieldSightXF.objects.create(xf_id=form, is_staged=True, stage=child_stage,site=stage.site)
                else:
                    FieldSightXF.objects.create(xf_id=form, is_staged=True, stage=child_stage,project=stage.project)
            messages.info(request, u'Sub Stage {} Saved.'.format(
                child_stage.name))
            return HttpResponseRedirect(reverse("forms:stages-detail", kwargs={'pk': stage.id}))
    order = Stage.objects.filter(stage=stage).count() + 1
    instance = Stage(name="Sub Stage"+str(order), order=order)
    form = AddSubSTageForm(instance=instance, request=request)
    return render(request, "fsforms/add_sub_stage.html", {'form': form, 'obj': stage})


@group_required("Project")
def stage_add(request, site_id=None):
    site = get_object_or_404(
        Site, pk=site_id)
    if request.method == 'POST':
        form = StageForm(data=request.POST)
        if form.is_valid():
            stage = form.save()
            stage.site = site
            stage.save()
            messages.info(request, u'Stage {} Saved.'.format(stage.name))
            return HttpResponseRedirect(reverse("forms:setup-site-stages", kwargs={'site_id': site.id}))
    order = Stage.objects.filter(site=site,stage__isnull=True).count() + 1
    instance = Stage(name="Stage"+str(order), order=order)
    form = StageForm(instance=instance)
    return render(request, "fsforms/stage_form.html", {'form': form, 'obj': site})

class ProjectResponses(ReadonlyProjectLevelRoleMixin, View): 
    def get(self,request, pk=None, **kwargs):
        obj = get_object_or_404(Project, pk=pk)
        schedules = Schedule.objects.filter(project_id=pk, schedule_forms__is_deleted=False, site__isnull=True, schedule_forms__isnull=False, schedule_forms__xf__isnull=False)
        stages = Stage.objects.filter(stage__isnull=True, project_id=pk, stage_forms__isnull=True).order_by('order')
        generals = FieldSightXF.objects.filter(is_staged=False, is_scheduled=False, is_deleted=False, project_id=pk, is_survey=False)
        surveys = FieldSightXF.objects.filter(is_staged=False, is_scheduled=False, is_deleted=False, project_id=pk, is_survey=True)
        stage_deleted_forms = FieldSightXF.objects.filter(is_staged=True,  is_scheduled=False, is_survey=False ,is_deleted=True, project_id=pk)
        general_deleted_forms = FieldSightXF.objects.filter(is_staged=False, is_scheduled=False, is_survey=False, is_deleted=True, project_id=pk)
        schedule_deleted_forms = FieldSightXF.objects.filter(is_staged=False, site__isnull=True, is_survey=False, is_scheduled=True, is_deleted=True, project_id=pk)
        survey_deleted_forms = FieldSightXF.objects.filter(is_staged=False, is_survey=True, is_scheduled=False, is_deleted=True, project_id=pk)
        return render(request, "fsforms/project/project_responses_list.html",
                      {'is_donor_only': kwargs.get('is_donor_only', False), 'obj': obj, 'schedules': schedules, 'stages':stages, 'generals':generals, 'surveys': surveys,
                       "stage_deleted_forms":stage_deleted_forms, "survey_deleted_forms":survey_deleted_forms, "general_deleted_forms":general_deleted_forms, "schedule_deleted_forms":schedule_deleted_forms, 'project': pk})


class Responses(ReadonlySiteLevelRoleMixin, View):
    def get(self, request, pk=None, **kwargs):
        obj = get_object_or_404(Site, pk=pk)
        project_id = get_object_or_404(Site, pk=pk).project.id
        schedules = Schedule.objects.filter(schedule_forms__is_deleted=False,
                                            schedule_forms__isnull=False).filter(
            Q(site__id=pk, schedule_forms__from_project=False)
                                       | Q(project__id=project_id))
        stages = Stage.objects.filter(
            stage__isnull=True
        ).filter(Q(site__id=pk,
                   project_stage_id=0
                   ) | Q(
            project__id=project_id
        )).order_by('order', 'date_created')
        generals = FieldSightXF.objects.filter(is_staged=False, is_deleted=False, is_scheduled=False,  is_survey=False).\
            filter(Q(site__id=pk, from_project=False)| Q(project__id=project_id))
        
        stage_deleted_forms = FieldSightXF.objects.filter(is_staged=True,
                                                          is_scheduled=False,
                                                          is_survey=False ,
                                                          is_deleted=True).filter(Q(site__id=pk, from_project=False)| Q(project__id=project_id))
        general_deleted_forms = FieldSightXF.objects.filter(is_staged=False,
                                                            is_scheduled=False,
                                                            is_survey=False,
                                                            is_deleted=True).filter(Q(site__id=pk, from_project=False)| Q(project__id=project_id))
        schedule_deleted_forms = FieldSightXF.objects.filter(
            is_staged=False,
            project__isnull=True,
            is_survey=False,
            is_scheduled=True,
            is_deleted=True
        ).filter(Q(site__id=pk, from_project=False)| Q(project__id=project_id))
        
        return render(request, "fsforms/responses_list.html",
                      {'is_donor_only': kwargs.get('is_donor_only', False),'obj': obj, 'schedules': schedules, 'stages':stages,'generals':generals,
                        "stage_deleted_forms":stage_deleted_forms, "general_deleted_forms":general_deleted_forms, "schedule_deleted_forms":schedule_deleted_forms,'site': pk})


@group_required("Project")
def project_stage_add(request, id=None):
    project = get_object_or_404(
        Project, pk=id)
    if request.method == 'POST':
        form = StageForm(data=request.POST)
        if form.is_valid():
            stage = form.save()
            stage.project = project
            stage.save()
            messages.info(request, u'Stage {} Saved.'.format(stage.name))
            return HttpResponseRedirect(reverse("forms:setup-project-stages", kwargs={'id': project.id}))
    order = Stage.objects.filter(project=project,stage__isnull=True).count() + 1
    instance = Stage(name="Stage"+str(order), order=order)
    form = StageForm(instance=instance)
    return render(request, "fsforms/project/stage_form.html", {'form': form, 'obj': project})


@group_required("Project")
def stage_details(request, pk=None):
    stage = get_object_or_404(
        Stage, pk=pk)
    object_list = Stage.objects.filter(stage__id=stage.id).order_by('order')
    order = Stage.objects.filter(stage=stage).count() + 1
    instance = Stage(name="Sub Stage"+str(order), order=order)
    form = AddSubSTageForm(instance=instance, request=request)
    return render(request, "fsforms/stage_detail.html", {'obj': stage, 'object_list':object_list, 'form':form})


@group_required("Project")
def stage_add_form(request, pk=None):
    stage = get_object_or_404(
        Stage, pk=pk)
    if stage.stage.site:
        instance = FieldSightXF(site=stage.stage.site, is_staged=True, is_scheduled=False, stage=stage)
        if request.method == 'POST':
            form = AssignFormToStageForm(request.POST, instance=instance)
            if form.is_valid():
                form.save()
                messages.add_message(request, messages.INFO, 'Form Assigned Successfully.')
                return HttpResponseRedirect(reverse("forms:stages-detail", kwargs={'pk': stage.stage.id}))
        else:
            form = AssignFormToStageForm(instance=instance)
        return render(request, "fsforms/stage_add_form.html", {'form': form, 'obj': stage})
    else:
        if request.method == 'POST':
            form = AssignFormToStageForm(request.POST)
            if form.is_valid():
                form.save()
                messages.add_message(request, messages.INFO, 'Form Assigned Successfully.')
                return HttpResponseRedirect(reverse("forms:stages-detail", kwargs={'pk': stage.stage.id}))
        else:
            form = AssignFormToStageForm()
        return render(request, "fsforms/stage_add_form.html", {'form': form, 'obj': stage})


@group_required("Project")
def edit_main_stage(request, stage, id, is_project):
    stage = get_object_or_404(Stage, pk=stage)
    if request.method == 'POST':
        form = MainStageEditForm(instance=stage, data=request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, 'Stage Updated.')
            if is_project == '1':
                return HttpResponseRedirect(reverse("forms:setup-project-stages", kwargs={'id': id}))
            else:
                return HttpResponseRedirect(reverse("forms:setup-site-stages", kwargs={'site_id': id}))
    form = MainStageEditForm(instance=stage)
    return render(request, "fsforms/main_stage_edit.html", {'form': form, 'id': id, 'is_project':is_project,'scenario':"Update"})


@group_required("Project")
def edit_sub_stage(request, stage, id, is_project):
    stage = get_object_or_404(Stage, pk=stage)
    if request.method == 'POST':
        form = SubStageEditForm(instance=stage, data=request.POST, request=request)
        if form.is_valid():
            form.save()
            form = int(form.cleaned_data.get('form', 0))
            if form:
                if is_project:
                    if FieldSightXF.objects.filter(project=stage.project, stage=stage, is_staged=True).exists():
                        fs_xform = FieldSightXF.objects.get(project=stage.project, stage=stage, is_staged=True)
                        fs_xform.xf_id = form
                        fs_xform.save()
                    else:
                        FieldSightXF.objects.create(xf_id=form, is_staged=True,stage=stage, project=stage.project)
                else:
                    if FieldSightXF.objects.filter(site=stage.site, stage=stage, is_staged=True).exists():
                        fs_xform = FieldSightXF.objects.get(site=stage.site, stage=stage, is_staged=True)
                        if fs_xform.xf.id != form:
                            fs_xform.xf_id = form
                            fs_xform.save()
                            if fs_xform.is_deployed:
                                send_message_xf_changed(fs_xform, "Stage", id)

                    else:
                        FieldSightXF.objects.create(xf_id=form, is_staged=True,stage=stage,site=stage.site)
            messages.info(request, u'Stage {} Updated.'.format(stage.name))
            return HttpResponseRedirect(reverse("forms:stages-detail", kwargs={'pk': stage.stage.id}))
    form = SubStageEditForm(instance=stage, request=request)
    if FieldSightXF.objects.filter(stage=stage).exists():
        if FieldSightXF.objects.get(stage=stage).xf:
            form.fields['form'].initial= FieldSightXF.objects.get(stage=stage).xf.id
    return render(request, "fsforms/sub_stage_edit.html", {'form': form, 'id': id, 'is_project':is_project,
                                                           'scenario':"Update"})


@group_required("Project")
def create_schedule(request, site_id):
    form = ScheduleForm(request=request)
    site = get_object_or_404(
        Site, pk=site_id)
    if request.method == 'POST':
        form = ScheduleForm(data=request.POST , request=request)
        if form.is_valid():
            form_type = int(form.cleaned_data.get('form_type',0))
            xf = int(form.cleaned_data.get('form', 0))
            if not form_type:
                if xf:
                    fxf, created = FieldSightXF.objects.get_or_create(xf_id=xf, is_scheduled=False,
                                                                    is_staged=False, site=site)
                    fxf.is_deployed= True
                    fxf.save()
                    messages.info(request, 'General Form  Saved.')
                return HttpResponseRedirect(reverse("forms:site-general", kwargs={'site_id': site.id}))
            schedule = form.save()
            schedule.site = site
            schedule.save()
            if xf:
                FieldSightXF.objects.create(xf_id=xf, is_scheduled=True,schedule=schedule,site=site, is_deployed=True)
            messages.info(request, u'Schedule {} Saved.'.format(schedule.name))
            return HttpResponseRedirect(reverse("forms:site-survey", kwargs={'site_id': site.id}))
    return render(request, "fsforms/schedule_form.html", {'form': form, 'obj': site, 'is_general':True})


@group_required("Project")
def site_survey(request, site_id):
    objlist = Schedule.objects.filter(site__id=site_id)
    if not len(objlist):
        return HttpResponseRedirect(reverse("forms:schedule-add", kwargs={'site_id': site_id}))
    return render(request, "fsforms/schedule_list.html", {'object_list': objlist, 'site':Site.objects.get(pk=site_id)})


@group_required("Project")
def site_general(request, site_id):
    objlist = FieldSightXF.objects.filter(site__id=site_id, is_staged=False, is_scheduled=False)
    if not len(objlist):
        return HttpResponseRedirect(reverse("forms:schedule-add", kwargs={'site_id': site_id}))
    return render(request, "fsforms/general_list.html", {'object_list': objlist, 'site':Site.objects.get(pk=site_id)})


@group_required("Project")
def project_general(request, project_id):
    objlist = FieldSightXF.objects.filter(project__id=project_id, is_staged=False, is_scheduled=False)
    if not len(objlist):
        return HttpResponseRedirect(reverse("forms:project-schedule-add", kwargs={'id': project_id}))
    return render(request, "fsforms/general_list.html", {'object_list': objlist, 'project':Project.objects.get(pk=project_id)})


@group_required("Project")
def project_create_schedule(request, id):
    project = get_object_or_404(
        Project, pk=id)
    if request.method == 'POST':
        form = ScheduleForm(data=request.POST, request=request)
        if form.is_valid():
            form_type = int(form.cleaned_data.get('form_type',0))
            xf = int(form.cleaned_data.get('form',0))
            if not form_type:
                if xf:
                    fxf, created = FieldSightXF.objects.get_or_create(
                        xf_id=xf, is_scheduled=False, is_staged=False, project=project)
                    fxf.is_deployed = True
                    fxf.save()
                    messages.info(request, 'General Form  Saved.')
                return HttpResponseRedirect(reverse("forms:project-general", kwargs={'project_id': project.id}))
            schedule = form.save()
            schedule.project = project
            schedule.save()
            if xf:
                FieldSightXF.objects.create(
                    xf_id=xf, is_scheduled=True,schedule=schedule,project=project, is_deployed=True)
            messages.info(request, u'Schedule {} Saved.'.format(schedule.name))
            return HttpResponseRedirect(reverse("forms:project-survey", kwargs={'project_id': project.id}))
    form = ScheduleForm(request=request)
    return render(request, "fsforms/schedule_form.html",
                  {'form': form, 'obj': project, 'is_project':True, 'is_general':True})


@group_required("Project")
def project_edit_schedule(request, id):
    schedule = get_object_or_404(
        Schedule, pk=id)
    if request.method == 'POST':
        form = ScheduleForm(data=request.POST, instance=schedule, request=request)
        if form.is_valid():
            form.save()
            xf = int(form.cleaned_data.get('form', 0))
            if xf:
                if FieldSightXF.objects.filter(project=schedule.project, schedule=schedule, is_scheduled=True).exists():
                    fs_xform = FieldSightXF.objects.get(project=schedule.project, schedule=schedule, is_scheduled=True)
                    if fs_xform.xf.id != xf:
                        fs_xform.xf_id = xf
                        fs_xform.save()
                else:
                    FieldSightXF.objects.create(
                        xf_id=xf, is_scheduled=True,schedule=schedule,project=schedule.project, is_deployed=True)
            messages.info(request, u'Schedule {} Saved.'.format(schedule.name))
            return HttpResponseRedirect(reverse("forms:project-survey", kwargs={'project_id': schedule.project.id}))
    form = ScheduleForm(instance=schedule, request=request)
    if FieldSightXF.objects.filter(schedule=schedule).exists():
        if FieldSightXF.objects.get(schedule=schedule).xf:
            form.fields['form'].initial= FieldSightXF.objects.get(schedule=schedule).xf.id
    return render(request, "fsforms/schedule_form.html",
                  {'form': form, 'obj': schedule.project, 'is_project':True, 'is_general':False, 'is_edit':True})


@group_required("Project")
def edit_schedule(request, id):
    schedule = get_object_or_404(Schedule, pk=id)
    if request.method == 'POST':
        form = ScheduleForm(data=request.POST, instance=schedule, request=request)
        if form.is_valid():
            form.save()
            xf = int(form.cleaned_data.get('form', 0))
            if xf:
                if FieldSightXF.objects.filter(site=schedule.site, schedule=schedule, is_scheduled=True).exists():
                    fs_xform = FieldSightXF.objects.get(site=schedule.site, schedule=schedule, is_scheduled=True)
                    if fs_xform.xf.id != xf:
                        fs_xform.xf_id = xf
                        fs_xform.save()
                        send_message_xf_changed(fs_xform, "Schedule", id)

                else:
                    FieldSightXF.objects.create(
                        xf_id=xf, is_scheduled=True,schedule=schedule,site=schedule.site, is_deployed=True)
            messages.info(request, u'Schedule {} Saved.'.format(schedule.name))
            return HttpResponseRedirect(reverse("forms:site-survey", kwargs={'site_id': schedule.site.id}))
    form = ScheduleForm(instance=schedule, request=request)
    if FieldSightXF.objects.filter(schedule=schedule, site=schedule.site, is_scheduled=True).exists():
        if FieldSightXF.objects.get(schedule=schedule, site=schedule.site, is_scheduled=True).xf:
            form.fields['form'].initial= FieldSightXF.objects.get(schedule=schedule,
                                                                  site=schedule.site, is_scheduled=True).xf.id
    return render(request, "fsforms/schedule_form.html",
                  {'form': form, 'obj': schedule.site, 'is_project': False, 'is_general': False, 'is_edit': True})


@api_view(['POST'])
def set_deploy_stages(request, is_project, pk):
    try:
        if is_project == "1":
            project = Project.objects.get(pk=pk)
            sites = project.sites.filter(is_active=True)
            main_stages = project.stages.filter(stage__isnull=True)
            with transaction.atomic():

                FieldSightXF.objects.filter(is_staged=True, site__project=project, stage__isnull=False).\
                    update(stage=None, is_deployed=False, is_deleted=True)
                FieldSightXF.objects.filter(is_staged=True, project=project,is_deleted=False).update(is_deployed=True)
                Stage.objects.filter(site__project=project).delete()
                for main_stage in main_stages:
                    # sites = []
                    for site in sites:
                        # sites.append(site.id)
                        # send_message_stages(site)
                        site_main_stage = Stage(name=main_stage.name, order=main_stage.order, site=site,
                                           description=main_stage.description, project_stage_id=main_stage.id)
                        site_main_stage.save()
                        project_sub_stages = Stage.objects.filter(stage__id=main_stage.pk, stage_forms__is_deleted=False)
                        for project_sub_stage in project_sub_stages:
                            site_sub_stage = Stage(name=project_sub_stage.name, order=project_sub_stage.order, site=site,
                                           description=project_sub_stage.description, stage=site_main_stage, project_stage_id=project_sub_stage.id, weight=project_sub_stage.weight)
                            site_sub_stage.save()
                            if FieldSightXF.objects.filter(stage=project_sub_stage).exists():
                                fsxf = FieldSightXF.objects.filter(stage=project_sub_stage)[0]
                                site_fsxf, created = FieldSightXF.objects.get_or_create(is_staged=True, default_submission_status=fsxf.default_submission_status, xf=fsxf.xf, site=site,
                                                                   fsform=fsxf, stage=site_sub_stage)
                                site_fsxf.is_deleted = False
                                site_fsxf.is_deployed = True
                                site_fsxf.save()
            return HttpResponse({'msg': 'ok'}, status=status.HTTP_200_OK)
        else:
            site = Site.objects.get(pk=pk)
            site.site_forms.filter(is_staged=True, xf__isnull=False, is_deployed=False, is_deleted=False).update(is_deployed=True)
            send_message_stages(site)
            return HttpResponse({'msg': 'ok'}, status=status.HTTP_200_OK)
    except Exception as e:
        return HttpResponse({'error':e.message}, status=status.HTTP_400_BAD_REQUEST)

class Rearrange_stages(SPFmixin, View):
    def post(self, request, is_project, pk):
        try:
            data = json.loads(self.request.body)
            with transaction.atomic():
                for order, stage in enumerate(data.get('orders')):
                    Stage.objects.filter(pk=stage.get('id')).update(order=order+1)
            return HttpResponse({'msg': 'ok'}, status=status.HTTP_200_OK)
        except Exception as e:
            return HttpResponse({'error':e.message}, status=status.HTTP_400_BAD_REQUEST)



@group_required("Project")
def edit_share_stages(request, id):
    fgroup = get_object_or_404(
        FormGroup, pk=id)
    if request.method == 'POST':
        form = GroupEditForm(data=request.POST,instance=fgroup)
        if form.is_valid():
            group = form.save()
            sl = form.data['sl']
            if sl == '':
                group.is_global=False
                group.organization=None
                group.project=None
                group.save()

            if sl == '0':
                group.is_global= True
                group.organization=None
                group.project=None
                group.save()

            elif sl == '1':
                group.is_global = False
                if hasattr(request,"project") and request.project:
                    group.organization = request.project.organization
                    group.project = None
                    group.save()
                    messages.add_message(request, messages.INFO, u'{0} Shared To Organization Level'.format(group.name))
                elif hasattr(request,"organization") and request.organization:
                    group.organization = request.organization
                    group.project = None
                    group.save()
                    messages.add_message(request, messages.INFO, u'{0} Shared To Organization Level'.format(group.name))
                else:
                    messages.add_message(request, messages.WARNING, u'{0} Not Shared. You Cannot Share to Organization Level'.
                                       format(group.name))
            elif sl == '2':
                if hasattr(request,"project") and request.project:
                    group.is_global  = False
                    group.organization = None
                    group.project = request.project
                    group.save()
                    messages.add_message(request, messages.INFO, u'{0} Shared to Project Level '.format(group.name))
                else:
                    messages.add_message(request, messages.WARNING,
                                         u'{0} Form Not Shared. You Cannot Share to Project Level'
                                         .format(group.name))

            return HttpResponseRedirect(reverse("forms:group-list"))
    sl = ''
    if fgroup.is_global:
        sl =  0
    elif fgroup.project:
        sl = 2
    elif fgroup.organization:
        sl = 1
    fgroup.shared_level = sl
    form = GroupEditForm(instance=fgroup)
    return render(request, "fsforms/edit_formgroup_form.html", {'form': form,'shared':sl})


@group_required("Project")
def share_stages(request, id, is_project):
    if request.method == 'POST':
        form = GroupForm(data=request.POST)
        if form.is_valid():
            with transaction.atomic():
                group = form.save(commit=False)
                group.creator=request.user
                sl = form.cleaned_data['shared_level']
                if sl == '':
                    group.is_global=False
                    group.organization=None
                    group.project=None
                    group.save()

                if sl == '0':
                    group.is_global= True
                    group.organization=None
                    group.project=None
                    group.save()

                if sl == '1':
                    group.is_global= False
                    if is_project == '1':
                        group.organization = Project(pk=id).organization
                    else:
                        group.organization = Site(pk=id).project.organization
                    group.project=None
                    group.save()
                if sl == '2':
                    group.is_global= False
                    if is_project == '1':
                        group.project = Project(pk=id)
                    else:
                        group.project = Site(pk=id).project
                    group.organization=None
                    group.save()
                if is_project == '1':
                    Stage.objects.filter(stage__isnull=True,project_id=id).update(group=group)
                    messages.info(request, 'Project Stages Shared')
                    return HttpResponseRedirect(reverse("forms:setup-project-stages", kwargs={'id': id}))
                else:
                    Stage.objects.filter(stage__isnull=True,site_id=id).update(group=group)
                    messages.info(request, 'Site Stages Shared')
                    return HttpResponseRedirect(reverse("forms:setup-site-stages", kwargs={'site_id': id}))
    else:
        form = GroupForm()
    return render(request, "fsforms/formgroup_form.html", {'form': form,'is_project':is_project, 'id':id})


@group_required("Project")
def deploy_stages(request, id):
    project = Project(pk=id)
    sites = project.sites.all()
    main_stages = project.stages.filter(stage__isnull=True)
    with transaction.atomic():
        Stage.objects.filter(site__project=project).delete()
        FieldSightXF.objects.filter(is_staged=True, site__project=project).delete()
        for main_stage in main_stages:
            for site in sites:
                send_message_stages(site)
                site_main_stage = Stage(name=main_stage.name, order=main_stage.order, site=site,
                                   description=main_stage.description)
                site_main_stage.save()
                project_sub_stages = Stage.objects.filter(stage__id=main_stage.pk)
                for project_sub_stage in project_sub_stages:
                    site_sub_stage = Stage(name=project_sub_stage.name, order=project_sub_stage.order, site=site,
                                   description=project_sub_stage.description, stage=site_main_stage)
                    site_sub_stage.save()
                    if FieldSightXF.objects.filter(stage=project_sub_stage).exists():
                        fsxf = FieldSightXF.objects.filter(stage=project_sub_stage)[0]
                        FieldSightXF.objects.get_or_create(is_staged=True, xf=fsxf.xf, site=site,
                                                           fsform=fsxf, stage=site_sub_stage, is_deployed=True)

    messages.info(request, 'Stages Form Deployed to Sites')
    return HttpResponseRedirect(reverse("forms:setup-project-stages", kwargs={'id': id}))


class Deploy_general(SPFmixin, View):
    def post(self, request, is_project, pk):
        data = json.loads(self.request.body)
        fxf_id = data.get('id')
        fxf_status = data.get('is_deployed')
        
        try:
            if is_project == "1":
                with transaction.atomic():
                    fxf = FieldSightXF.objects.get(pk=fxf_id)
                    if fxf_status:
                        fxf.is_deployed = False
                        fxf.save()
                        send_message_un_deploy_project(fxf)
                        # FieldSightXF.objects.filter(fsform=fxf, is_scheduled=False, is_staged=False).update(is_deployed=False, is_deleted=True)
                    else:
                        fxf.is_deployed = True
                        fxf.save()
                        send_message_un_deploy_project(fxf)
                return HttpResponse({'msg': 'ok'}, status=status.HTTP_200_OK)
            else:
                fxf = FieldSightXF.objects.get(pk=fxf_id)
                if fxf_status:
                    fxf.is_deployed = False
                    fxf.save()
                    send_message_un_deploy(fxf)
                else:
                    fxf.is_deployed = True
                    fxf.is_deleted = False
                    fxf.save()
                    send_message_un_deploy(fxf)
                return HttpResponse({'msg': 'ok'}, status=status.HTTP_200_OK)
        except Exception as e:
            return HttpResponse({'error':e.message}, status=status.HTTP_400_BAD_REQUEST)

@group_required("Project")
@api_view(['POST', 'GET'])
def deploy_general_remaining_sites(request, is_project, pk):
    fxf_id = request.data.get('id')
    fxf_status = request.data.get('is_deployed')
    try:
        if is_project == "1":
            with transaction.atomic():
                fxf = FieldSightXF.objects.get(pk=fxf_id)
                if fxf_status:
                    site_ids=[]
                    for site in fxf.project.sites.filter(is_active=True):
                        child, created = FieldSightXF.objects.get_or_create(is_staged=False, is_scheduled=False, xf=fxf.xf, site=site, fsform_id=fxf_id)
                        child.is_deployed = True
                        child.save()
                        if created:
                            site_ids.append(site.id)
                    send_bulk_message_stages(site_ids)
                else:
                    return Response({'error':"Deploy Form First and deploy to remaining.."}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'msg': 'ok'}, status=status.HTTP_200_OK)
        else:
            return Response({'error':"Site level Deploy to remaining Not permitted."}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error':e.message}, status=status.HTTP_400_BAD_REQUEST)



# @group_required("Project")
# @api_view([])
# def deploy_general(request, fxf_id):
#     with transaction.atomic():
#         fxf = FieldSightXF.objects.get(pk=fxf_id)
#         FieldSightXF.objects.filter(fsform=fxf, is_scheduled=False, is_staged=False).delete()
#         for site in fxf.project.sites.filter(is_active=True):
#             # cloning from parent
#             child = FieldSightXF(is_staged=False, is_scheduled=False, xf=fxf.xf, site=site, fsform_id=fxf_id,
#                                  is_deployed=True)
#             child.save()
#     messages.info(request, 'General Form {} Deployed to Sites'.format(fxf.xf.title))
#     return HttpResponseRedirect(reverse("forms:project-general", kwargs={'project_id': fxf.project.pk}))

@group_required("Project")
def deploy_general_part(request, fxf_id):
    with transaction.atomic():
        fxf = FieldSightXF.objects.get(pk=fxf_id)
        for site in fxf.project.sites.filter(is_active=True):
            # cloning from parent
            child, created = FieldSightXF.objects.get_or_create(is_staged=False, is_scheduled=False, xf=fxf.xf,
                                site=site, fsform_id=fxf_id)
            child.is_deployed = True
            child.save()
    messages.info(request, u'General Form {} Deployed to Sites'.format(
        fxf.xf.title))
    return HttpResponseRedirect(reverse("forms:project-general", kwargs={'project_id': fxf.project.pk}))


@group_required("Project")
def un_deploy_general(request, fxf_id):
    fxf = FieldSightXF.objects.get(pk=fxf_id)
    fxf.is_deployed = False if fxf.is_deployed else True
    label = "Deployed" if fxf.is_deployed else "Undeployed"
    fxf.save()
    send_message_un_deploy(fxf)
    messages.info(request, u'General Form {} has been {}'.format(
        fxf.xf.title, label))
    return HttpResponseRedirect(reverse("forms:site-general", kwargs={'site_id': fxf.site.pk}))


class Deploy_survey(SPFmixin, View):
    def post(self, request, is_project, pk):
        data = json.loads(self.request.body)
        id = data.get('id')
        fxf_status = data.get('is_deployed',)
        try:
            schedule = Schedule.objects.get(pk=id)
            if is_project == "1":
                arguments = {'schedule_id': schedule.id,  'fxf_status':fxf_status, 'pk':pk}
                copy_schedule_to_sites.apply_async((), arguments, countdown=2)
                return HttpResponse({'msg': 'ok'}, status=status.HTTP_200_OK)
            else:
                flag = False if fxf_status else True
                form = schedule.schedule_forms
                form.is_deployed = flag
                form.save()
                send_message_un_deploy(form)
                return HttpResponse({'msg': 'ok'}, status=status.HTTP_200_OK)
        except Exception as e:
            print("dddddddddddd",str(e))
            return HttpResponse({'error':e.message}, status=status.HTTP_400_BAD_REQUEST)


@group_required("Project")
def un_deploy_survey(request, id):
    schedule = Schedule.objects.get(pk=id)
    fxf = FieldSightXF.objects.get(schedule=schedule)
    fxf.is_deployed = False if fxf.is_deployed else True
    fxf.save()
    send_message_un_deploy(fxf)
    label = "Deployed" if fxf.is_deployed else "Undeployed"
    messages.info(request, u'Schedule {} with  Form Named {} Form {}'.format(
        schedule.name,fxf.xf.title, label))
    return HttpResponseRedirect(reverse("forms:site-survey", kwargs={'site_id': fxf.site.id}))


@group_required("Project")
def edit_general(request, fxf_id):
    fs_xform = get_object_or_404(
        FieldSightXF, pk=fxf_id)
    form = GeneralFSForm(instance=fs_xform, request=request)
    if request.method == 'POST':
        form = GeneralFSForm(data=request.POST, instance=fs_xform, request=request)
        if form.is_valid():
            form.save()
            messages.info(request, 'General Form Updated')
            if fs_xform.site:
                return HttpResponseRedirect(reverse("forms:site-general", kwargs={'site_id': fs_xform.site.id}))
            return HttpResponseRedirect(reverse("forms:project-general", kwargs={'project_id': fs_xform.project.id}))
    is_project = True if fs_xform.project else False
    return render(request, "fsforms/general_form.html", {'form': form,'is_project':is_project})


@group_required("Project")
def schedule_add_form(request, pk=None):
    schedule = get_object_or_404(
        Schedule, pk=pk)
    instance = FieldSightXF(site=schedule.site, is_staged=False, is_scheduled=True, schedule=schedule)
    if request.method == 'POST':
        form = AssignFormToScheduleForm(request.POST, instance=instance, request=request)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, 'Form Assigned Successfully.')
            return HttpResponseRedirect(reverse("forms:site-survey", kwargs={'site_id': schedule.site.id}))
    form = AssignFormToScheduleForm(instance=instance, request=request)
    return render(request, "fsforms/schedule_add_form.html", {'form': form, 'obj': schedule})


class FormGroupView(object):
    model = FormGroup
    success_url = reverse_lazy('forms:group-list')
    form_class = GroupForm


class GroupListView(FormGroupView, LoginRequiredMixin, ListView):

    def get_queryset(self):
        if self.request.project:
            return super(GroupListView, self).\
                get_queryset().filter(Q(is_global=True)
                                      | Q(project=self.request.project)
                                      |Q(organization=self.request.organization))
        elif self.request.organization:
            return super(GroupListView, self).\
                get_queryset().filter(Q(is_global=True)
                                      |Q(organization=self.request.organization))
        else:
            return super(GroupListView, self).get_queryset()


class CreateViewWithUser(CreateView):
    def dispatch(self, *args, **kwargs):
        return super(CreateViewWithUser, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.creator = self.request.user
        obj.save()
        return HttpResponseRedirect(self.success_url)


class GroupCreateView(FormGroupView, LoginRequiredMixin, KoboFormsMixin, CreateViewWithUser):
    pass


class GroupUpdateView(FormGroupView, LoginRequiredMixin, KoboFormsMixin, UpdateView):
    pass


class GroupDeleteView(FormGroupView, LoginRequiredMixin, KoboFormsMixin, DeleteView):
    pass


@group_required("Project")
def site_forms(request, site_id=None):
    return render(request, "fsforms/site_forms_ng.html", {'site_id': site_id, 'angular_url':settings.ANGULAR_URL})


@group_required("Project")
def site_stages(request, site_id=None):
    return render(request, "fsforms/site_stages_ng.html", {'site_id': site_id, 'angular_url':settings.ANGULAR_URL})


@group_required("Project")
def assign(request, pk=None):
    if request.method == 'POST':
        field_sight_form = get_object_or_404(
        FieldSightXF, pk=pk)
        form = AssignSettingsForm(request.POST, instance=field_sight_form)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, 'Form Assigned Successfully.')
            return HttpResponseRedirect(reverse("forms:fill_form_type", kwargs={'pk': form.instance.id}))
    else:
        field_sight_form = FieldSightXF.objects.create(xf=XForm.objects.get(pk=int(pk)))
        project = request.project.id if request.project is not None else None
        form = AssignSettingsForm(instance=field_sight_form, project=project)
    return render(request, "fsforms/assign.html", {'form': form})


@group_required("Project")
def fill_form_type(request, pk=None):
    field_sight_form = get_object_or_404(
        FieldSightXF, pk=pk)
    if request.method == 'POST':
        form = FormTypeForm(request.POST)
        if form.is_valid():
            form_type = form.cleaned_data.get('form_type', '3')
            form_type = int(form_type)
            messages.info(request, 'Form Type Saved.')
            if form_type == 3:
                return HttpResponseRedirect(reverse("forms:library-forms-list"))
            elif form_type == 2:
                field_sight_form.is_scheduled = True
                field_sight_form.save()
                return HttpResponseRedirect(reverse("forms:fill_details_schedule", kwargs={'pk': field_sight_form.id}))
            else:
                field_sight_form.is_staged = True
                field_sight_form.save()
                return HttpResponseRedirect(reverse("forms:fill_details_stage", kwargs={'pk': field_sight_form.id}))
    else:
        form = FormTypeForm()
    return render(request, "fsforms/stage_or_schedule.html", {'form': form, 'obj': field_sight_form})


@group_required("Project")
def fill_details_stage(request, pk=None):
    field_sight_form = get_object_or_404(
        FieldSightXF, pk=pk)
    if request.method == 'POST':
        form = FormStageDetailsForm(request.POST, instance=field_sight_form)
        if form.is_valid():
            form.save()
            messages.info(request, 'Form Stage Saved.')
            return HttpResponseRedirect(reverse("forms:stages-detail", kwargs={'pk': form.instance.stage.stage.id}))
    else:
        form = FormStageDetailsForm(instance=field_sight_form)
    return render(request, "fsforms/form_details_stage.html", {'form': form})


@group_required("Project")
def fill_details_schedule(request, pk=None):
    field_sight_form = get_object_or_404(
        FieldSightXF, pk=pk)
    if request.method == 'POST':
        form = FormScheduleDetailsForm(request.POST, instance=field_sight_form)
        if form.is_valid():
            form.save()
            messages.info(request, 'Form Schedule Saved.')
            return HttpResponseRedirect(reverse("forms:schedules-list"))
    else:
        form = FormScheduleDetailsForm(instance=field_sight_form)
    return render(request, "fsforms/form_details_schedule.html", {'form': form})


@group_required("Project")
def setup_site_stages(request, site_id):
    objlist = Stage.objects.filter(stage_forms__isnull=True, stage__isnull=True,site__id=site_id)
    order = Stage.objects.filter(site__id=site_id,stage__isnull=True).count() + 1
    instance = Stage(name="Stage"+str(order), order=order)
    form = StageForm(instance=instance)
    return render(request, "fsforms/main_stages.html",
                  {'objlist': objlist, 'site':Site(pk=site_id),'form': form})


@group_required("Project")
def library_stages(request, id):
    objlist = Stage.objects.filter(stage_forms__isnull=True, stage__isnull=True, group__id=id).order_by('order')
    return render(request, "fsforms/library_stage_detail.html", {'stages': objlist})


@group_required("Project")
def setup_project_stages(request, id):
    objlist = Stage.objects.filter(stage_forms__isnull=True, stage__isnull=True,project__id=id)
    order = Stage.objects.filter(project__id=id,stage__isnull=True).count() + 1
    instance = Stage(name="Stage"+str(order), order=order)
    form = StageForm(instance=instance)
    return render(request, "fsforms/project/project_main_stages.html",
                  {'objlist': objlist, 'obj':Project(pk=id), 'form': form})


@group_required("Project")
def project_survey(request, project_id):
    objlist = Schedule.objects.filter(project__id=project_id)
    if not len(objlist):
        return HttpResponseRedirect(reverse("forms:project-schedule-add", kwargs={'id': project_id}))
    return render(request, "fsforms/project/schedule_list.html", {'object_list': objlist, 'project': Project(id=project_id)})


class AssignFormDefaultStatus(FormMixin, View):
    def post(self, request, fsxf_id, status_code):
        fsform = FieldSightXF.objects.get(pk=fsxf_id)
        if int(status_code) >= 0 and int(status_code) < 5: 
            fsform.default_submission_status = status_code
            fsform.save()
            
            for childform in fsform.parent.all():
                childform.default_submission_status = status_code
                childform.save()
        return HttpResponse({'responseJSON':'success'}, status=status.HTTP_200_OK)


class Setup_forms(SPFmixin, View):
    def get(self, request, *args, **kwargs):
        is_project = False
        if self.kwargs.get('is_project') == '1':
            is_project = True
            obj = Project.objects.get(pk=self.kwargs.get('pk'))
        else:
            obj = Site.objects.get(pk=self.kwargs.get('pk'))
        return render(request, "fsforms/manage_forms.html",
                  {'obj': obj, 'is_project': self.kwargs.get('is_project'), 'pk': self.kwargs.get('pk'), 'form': GeneralForm(request=request,  project_or_site=obj, is_project=is_project),
                   'schedule_form': KoScheduleForm(request=request,  project_or_site=obj, is_project=is_project)})


class FormPreviewView(View):
    def get(self, request, *args, **kwargs):
        id_string = self.kwargs.get('id_string')
        xform = XForm.objects.get(id_string=id_string)
        form_url = _get_form_url(request, xform.user.username, settings.ENKETO_PROTOCOL)
        print(form_url)

        try:
            url = enketo_preview_url(
                form_url, xform.id_string
            )
        except Exception as e:
            return HttpResponse("This form cannot be viewed in enketo. Please Report")
        else:
            if url:
                return HttpResponseRedirect(url)
        return HttpResponse("This form cannot be viewed in enketo. Please Report")


class FormFillView(FormMixin, View):
    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('fsxf_id')
        site_id = self.kwargs.get('site_id', None)
        sub_pk = self.kwargs.get('instance_pk')

        fieldsight_xf = FieldSightXF.objects.get(pk=pk)
        xform = fieldsight_xf.xf
        data = {
            'xform': xform.xml
        }
        media_list = MetaData.objects.filter(data_type='media', xform=xform)
        for m in media_list:
            data.update({
                'media[' + m.data_value + ']': m.data_file.url
            })
        finstance = FInstance.objects.get(instance_id=sub_pk) if sub_pk else None

        result = requests.post(
            'http://localhost:8085/transform',
            data=data
        ).json()

        return render(request, 'fsforms/form.html', {
            'xform': xform,
            'html_form': result['form'],
            'model_str': result['model'],
            'existing': finstance,
            'site_id': site_id,
        })

    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('fsxf_id')
        site_id = self.kwargs.get('site_id')
        sub_pk = self.kwargs.get('instance_pk')

        fs_xf = FieldSightXF.objects.get(pk=pk)
        xform = fs_xf.xf
        finstance = FInstance.objects.get(instance_id=sub_pk) if sub_pk else None

        xml = request.POST['enketo_xml_data']
        media_files = request.FILES.values()
        new_uuid = finstance.instance.uuid if finstance else str(uuid.uuid4())

        if fs_xf.site:
            site_id = fs_xf.site_id
        else:
            if finstance and finstance.site:
                site_id = finstance.site_id
        with transaction.atomic():
            if fs_xf.is_survey:
                instance = save_submission(
                    xform=xform,
                    xml=xml,
                    media_files=media_files,
                    new_uuid=new_uuid,
                    submitted_by=request.user,
                    status='submitted_via_web',
                    date_created_override=None,
                    fxid=None,
                    site=None,
                    fs_poj_id=fs_xf.id,
                    project=fs_xf.project.id,
                )
            else:
                if fs_xf.site:
                    instance = save_submission(
                        xform=xform,
                        xml=xml,
                        media_files=media_files,
                        new_uuid=new_uuid,
                        submitted_by=request.user,
                        status='submitted_via_web',
                        date_created_override=None,
                        fxid=fs_xf.id,
                        site=site_id,
                    )
                else:
                    instance = save_submission(
                        xform=xform,
                        xml=xml,
                        media_files=media_files,
                        new_uuid=new_uuid,
                        submitted_by=request.user,
                        status='submitted_via_web',
                        date_created_override=None,
                        fxid=None,
                        site=site_id,
                        fs_poj_id=fs_xf.id,
                        project=fs_xf.project.id,
                    )
            if finstance:
                noti_type=31
                title = "editing submission"
            else:
                noti_type=16
                title = "new submission"

            if instance.fieldsight_instance.site:
                extra_object=instance.fieldsight_instance.site
                extra_message=""
                project=extra_object.project
                site = extra_object
                organization=extra_object.project.organization

            else:
                extra_object=instance.fieldsight_instance.project
                extra_message="project"
                project=extra_object
                site = None
                organization=extra_object.organization
            
            instance.fieldsight_instance.logs.create(source=self.request.user, type=noti_type, title=title,

                                       organization=organization,
                                       project=project,
                                                        site=site,
                                                        extra_object=extra_object,
                                                        extra_message=extra_message,
                                                        content_object=instance.fieldsight_instance)
        if site_id:
            return HttpResponseRedirect(reverse("forms:site-responses",
                                        kwargs={'pk': site_id}))
        else:
            return HttpResponseRedirect(reverse("forms:project-responses",
                                        kwargs={'pk': fs_xf.project_id}))


class Configure_forms(SPFmixin, View):
    def get(self, request, *args, **kwargs):
        if self.kwargs.get('is_project') == '1':
            obj = Project.objects.get(pk=self.kwargs.get('pk'))
        else:
            obj = Site.objects.get(pk=self.kwargs.get('pk'))
        return render(request, "fsforms/configure_stages.html",
                  {'obj': obj, 'is_project': self.kwargs.get('is_project'), 'pk': self.kwargs.get('pk')})

# kobo form related

def download_xform(request, pk):
    # if request.user.is_anonymous():
        # raises a permission denied exception, forces authentication
        # response= JsonResponse({'code': 401, 'message': 'Unauthorized User'})
        # return response
    fs_xform = get_object_or_404(FieldSightXF, pk__exact=pk)

    audit = {
        "xform": fs_xform.pk
    }

    audit_log(
        Actions.FORM_XML_DOWNLOADED, request.user, fs_xform.xf.user,
        _("Downloaded XML for form '%(pk)s'.") %
        {
            "pk": pk
        }, audit, request)
    response = response_with_mimetype_and_name('xml', str(fs_xform.id),  show_date=False)
    response.content = fs_xform.xf.xml

    return response


class FullResponseTable(ReadonlyFormMixin, View):
    def get(self, request, fsxf_id):
        limit = int(request.GET.get('limit', 100))
        fsxf_id = int(fsxf_id)
        fsxf = FieldSightXF.objects.get(pk=fsxf_id)
        json_question = json.loads(fsxf.xf.json)
        
        parsedQuestions = get_questions_and_media_attributes(json_question['children'])
        
        xform = fsxf.xf
        id_string = xform.id_string
        if fsxf.site is None:
            cursor = get_instances_for_project_field_sight_form(fsxf_id)
        else:
            cursor = get_instances_for_field_sight_form(fsxf_id)
        cursor = list(cursor)
        for index, doc in enumerate(cursor):
            medias = []
            for media in cursor[index].get('_attachments', []):
                if media:
                    medias.append(media.get('download_url', ''))
            cursor[index].update({'medias': medias})
        paginator = Paginator(cursor, limit, request=request)

        try:
            page = paginator.page(request.GET.get('page', 1))
        except (EmptyPage, PageNotAnInteger):
            try:
                page = paginator.page(1)
            except (EmptyPage, PageNotAnInteger):
                raise Http404('This report has no submissions')

        data = [("v1", page.object_list)]
        context = build_export_context(request, xform, id_string)

        context.update({
            'page': page,
            'table': [],
            'title': id,
        })

        export = context['export']
        sections = list(export.labels.items())
        # question_names = export.sections.items()[0][1]
        # section, labels = sections[0]
        
        # id_index = labels.index('_id')

        # generator dublicating the "_id" to allow to make a link to each
        # submission
        # def make_table(submissions):
        #     for chunk in export.parse_submissions(submissions):
        #         for section_name, rows in chunk.items():
        #             section1=section_name
        #             if section == section_name:
        #                 rows1 = rows
        #                 for row in rows:
        #                     return renders(request, 'fsforms/full_response_table.html', context)

        def make_table(submissions):
            for section_name, submission in submissions:
                for row in submission:
                    row_data=[]

                    for indv_question in parsedQuestions.get('questions'):
                        if indv_question.get('question') in row:
                            if indv_question.get('type') in ['photo', 'audio', 'video']:
                                row_data.append('<a href="/attachment/medium?media_file='+fsxf.xf.user.username+'/attachments/'+row[indv_question.get('question')]+'" target="_blank">'+row[indv_question.get('question')]+'</a>')
                            else:
                                row_data.append(row[indv_question.get('question')])
                        else:
                            row_data.append('')
                    yield row['_id'], row_data

        context['labels'] = parsedQuestions.get('questions')
        context['data'] = make_table(data)
        context['owner_username'] = fsxf.xf.user.username
        context['obj'] = fsxf
        return render(request, 'fsforms/full_response_table.html', context)

# @group_required('KoboForms')
# def html_export(request, fsxf_id):
#
#     cursor = FInstance.objects.filter(site_fxf=fsxf)
#     context={}
#     context['is_site_data'] = True
#     context['site_data'] = cursor
#     context['form_name'] = fsxf.xf.title
#     context['fsxfid'] = fsxf_id
#     context['obj'] = fsxf
#     return render(request, 'fsforms/fieldsight_export_html.html', context)

class Html_export(ReadonlyFormMixin, ListView):
    model =   FInstance
    paginate_by = 100
    template_name = "fsforms/fieldsight_export_html.html"

    def get_context_data(self, **kwargs):
        context = super(Html_export, self).get_context_data(**kwargs)
        fsxf_id = int(self.kwargs.get('fsxf_id'))
        site_id = int(self.kwargs.get('site_id'), 0)
        fsxf = FieldSightXF.objects.get(pk=fsxf_id)
        # context['pk'] = self.kwargs.get('pk')
        context['is_site_data'] = True
        context['form_name'] = fsxf.xf.title
        context['fsxfid'] = fsxf_id
        context['obj'] = fsxf
        if site_id != 0:
            context['site_id'] = site_id
        if fsxf.site is not None:
            project = fsxf.site.project
        else:
            project = fsxf.project
        organization_roles = self.request.roles.filter(organization_id=project.organization_id, group__name="Organization Admin")
        if organization_roles:
            context['is_read_only'] = False
        elif self.request.roles.filter(project_id=project, group__name="Project Manager"):
            context['is_read_only'] = False
        elif self.request.roles.filter(group__name="Super Admin"):
            context['is_read_only'] = False
        else:
            context['is_read_only'] = True
        return context

    def get_queryset(self, **kwargs):
        fsxf_id = int(self.kwargs.get('fsxf_id'))
        site_id = int(self.kwargs.get('site_id'), 0)
        fsxf = FieldSightXF.objects.get(pk=fsxf_id)
        query = self.request.GET.get("q", None)
        if not fsxf.from_project:
            queryset = FInstance.objects.filter(site_fxf=fsxf_id)
        else:
            queryset = FInstance.objects.filter(project_fxf=fsxf_id, site_id=site_id)
        if query:
            if not fsxf.from_project:
                new_queryset = FInstance.objects.filter(
                    Q(site_fxf=fsxf_id) &
                    (
                        Q(submitted_by__first_name__icontains=query)|
                        Q(submitted_by__last_name__icontains=query)
                    )
                    )
            else:
                new_queryset = FInstance.objects.filter(
                    Q(project_fxf=fsxf_id) &
                    (
                        Q(submitted_by__first_name__icontains=query)|
                        Q(submitted_by__last_name__icontains=query)
                    )
                    )

        else:
            new_queryset = queryset.order_by('-id')
        return new_queryset


class Project_html_export(ReadonlyFormMixin, ListView):
    model = FInstance
    paginate_by = 100
    template_name = "fsforms/fieldsight_export_html.html"

    def get_context_data(self, **kwargs):
        context = super(Project_html_export, self).get_context_data(**kwargs)
        fsxf_id = int(self.kwargs.get('fsxf_id'))
        fsxf = FieldSightXF.objects.get(pk=fsxf_id)
        # context['pk'] = self.kwargs.get('pk')
        context['is_project_data'] = True
        context['form_name'] = fsxf.xf.title
        context['fsxfid'] = fsxf_id
        context['obj'] = fsxf
        project = fsxf.project
        organization_roles = self.request.roles.filter(organization_id=project.organization_id, group__name="Organization Admin")
        if organization_roles:
            context['is_read_only'] = False
        elif self.request.roles.filter(project_id=project, group__name="Project Manager"):
            context['is_read_only'] = False
        elif self.request.roles.filter(group__name="Super Admin"):
            context['is_read_only'] = False
        else:
            context['is_read_only'] = True
        return context

    def get_queryset(self, **kwargs):
        fsxf_id = int(self.kwargs.get('fsxf_id'))
        query = self.request.GET.get("q", None)
        queryset = FInstance.objects.filter(project_fxf=fsxf_id)
        if query:
            new_queryset = FInstance.objects.filter(
                Q(project_fxf=fsxf_id) &
                (
                    Q(site__name__icontains=query) |
                    Q(site__identifier__icontains=query) |
                    Q(submitted_by__first_name__icontains=query)|
                    Q(submitted_by__last_name__icontains=query)
                )
                )
        else:
            new_queryset = queryset.order_by('-id')
        return new_queryset

@group_required('KoboForms')
def project_html_export(request, fsxf_id):
    fsxf_id = int(fsxf_id)
    fsxf = FieldSightXF.objects.get(pk=fsxf_id)
    cursor = FInstance.objects.filter(project_fxf=fsxf) 
    context={}
    context['project_data'] = cursor
    context['is_project_data'] = True
    context['form_name'] = fsxf.xf.title
    context['fsxfid'] = fsxf_id
    context['obj'] = fsxf
    # return JsonResponse({'data': cursor})
    return render(request, 'fsforms/fieldsight_export_html.html', context)

class Instance_detail(FormMixin, View):
    def get(self, request, fsxf_id, instance_id):
        fsxf = FieldSightXF.objects.get(pk=fsxf_id)
        cursor = get_instance(instance_id)
        cursor = list(cursor)
        obj = cursor[0]
        _keys = ['_notes', 'meta/instanceID', 'end', '_uuid', '_bamboo_dataset_id', '_tags', 'start',
                 '_geolocation', '_xform_id_string', '_userform_id', '_status', '__version__', 'formhub/uuid',
                 '_id', 'fs_uuid', 'fs_site', 'fs_project_uuid']
        data = {}
        medias = []
        status = 0
        for key in obj.keys():
            if key not in _keys:
                if key == "_attachments":
                    for media in obj[key]:
                        if media:
                            medias.append(media.get('download_url', ''))
                elif key == "fs_status":
                    status = obj[key]
                else:
                    data.update({str(key): str(obj[key])})
        return render(request, 'fsforms/fieldsight_instance_export_html.html',
                      {'obj': fsxf, 'answer': instance_id, 'status': status, 'data': data, 'medias': medias})


@api_view(['GET'])
def delete_substage(request, id):
    try:
        sub_stage = Stage.objects.get(pk=id)
        old_fsxf = sub_stage.stage_forms
        old_fsxf.is_deleted = True
        # old_fsxf.stage = None
        old_fsxf.save()
        return Response({}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error':e.message}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def delete_mainstage(request, id):
    try:
        with transaction.atomic():
            stage = Stage.objects.get(pk=id)
            org = stage.site.project.organization if stage.site else stage.project.organization
            substages = Stage.objects.filter(stage=stage)
            for sub_stage in substages:
                if hasattr(sub_stage, 'stage_forms'):
                    old_fsxf = sub_stage.stage_forms
                    old_fsxf.is_deleted = True
                    old_fsxf.stage = None
                    old_fsxf.save()
                sub_stage.delete()
            stage.delete()
        return Response({}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error':e.message}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def instance_status(request, instance):
    message = None
    comment_url = None
    try:
        if not FInstance.objects.filter(instance__id=instance).exists():
            return Response({'error': "This Detail Data is missing in Postgres DB"}, status=status.HTTP_400_BAD_REQUEST)
        fi = FInstance.objects.get(instance__id=instance)
        if request.method == 'POST':
            site = fi.site
            if site:
                has_acess = False
                if request.roles.filter(site=site, group__name="Reviewer") or request.roles.filter(region=site.region, group__name="Region Reviewer"):
                    has_acess = True
                elif request.roles.filter(project=site.project, group__name="Project Manager") or \
                    request.roles.filter(organization=site.project.organization, group__name="Organization Admin") or request.roles.filter(group__name="Super Admin"):
                    has_acess = True
                if not has_acess:
                    return Response({'error': "You are not permitted to change Status of this Submission"}, status=status.HTTP_400_BAD_REQUEST)

            with transaction.atomic():
                submission_status = request.data.get("status", 0)
                message = request.data.get("message", "")
                status_changed = InstanceStatusChanged(finstance=fi, message=message, old_status=fi.form_status,
                                                     new_status=submission_status, user=request.user)
                status_changed.save()
                for key in request.FILES.keys():
                    if "new_images_" in key:
                        img = request.FILES.get(key)
                        obj = InstanceImages(image=img, instance_status=status_changed)
                        obj.save()
                fi.form_status = int(submission_status)
                fi.date = datetime.date.today()
                fi.save()
                comment_url = reverse("forms:instance_status_change_detail",
                                                kwargs={'pk': status_changed.id})
                if fi.site:
                    extra_object=fi.site
                    extra_message=""
                else:
                    extra_object=fi.project
                    extra_message="project"

                    
                org = fi.project.organization if fi.project else fi.site.project.organization
                noti = status_changed.logs.create(source=request.user, type=17, title="form status changed",
                                          organization=org,
                                          project=fi.project,
                                          site = fi.site,
                                          content_object=fi,
                                          extra_object=extra_object,
                                          extra_message=extra_message
                                          )
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    else:
        if request.method == 'POST':
            try:
                send_message_flagged(fi, message, comment_url)
            except Exception as e:
                print(str(e))
                # send_message(fi.site_fxf, fi.form_status, message, comment_url)
        if fi.site:
            site_name = fi.site.name
            site_id = fi.site.id
        else:
            site_name = "Survey Form"
            site_id = 0
        return Response({'formStatus': str(fi.form_status), 'site_name': site_name, 'site_id': site_id}, status=status.HTTP_200_OK)


class AlterStatusDetailView(DetailView):
    model = InstanceStatusChanged

@login_required
@group_required("Reviewer")
def alter_answer_status(request, instance_id, status, fsid):
    if request.method == 'POST':
        form = AlterAnswerStatus(request.POST)
        if form.is_valid():
            status = int(form.cleaned_data['status'])
            update_status(instance_id, status)
            fsxf = FieldSightXF.objects.get(pk=fsid)
            fsxf.form_status = status
            fsxf.save()
            comment = form.cleaned_data['comment']
            if comment:
                # comment save
                pass
            send_message(fsxf, status, comment)
            return HttpResponseRedirect(reverse("forms:instance_detail",
                                                kwargs={'fsxf_id': fsid, 'instance_id':instance_id}))

    else:
        form = AlterAnswerStatus(initial={'status':status})

    return render(request, 'fsforms/alter_answer_status.html',
                  {'form': form, 'answer':instance_id, 'status':status, 'fsid':fsid})


# @group_required('KoboForms')
class InstanceKobo(ConditionalFormMixin, View):
    def get(self, request, fsxf_id, is_read_only=True, is_doner=False, site_id=None):
        fxf = FieldSightXF.objects.get(pk=fsxf_id)
        xform, is_owner, can_edit, can_view = fxf.xf, True, False, True
        audit = {
            "xform": xform.id_string,
        }
        audit_log(
            Actions.FORM_DATA_VIEWED, request.user, xform.user,
            _("Requested instance view for '%(id_string)s'.") %
            {
                'id_string': xform.id_string,
            }, audit, request)
        kwargs = {
            'username': xform.user,
            'fxf': fxf,
            'can_edit': can_edit,
            'is_readonly': is_read_only,
            'is_doner': is_doner
        }
        if site_id is not None:
            kwargs['site_id'] = site_id
        return render(request, 'fs_instance.html', kwargs)


@require_http_methods(["GET", "OPTIONS"])
def api(request, fsxf_id=None, site_id=None):
    """
    Returns all results as JSON.  If a parameter string is passed,
    it takes the 'query' parameter, converts this string to a dictionary, an
    that is then used as a MongoDB query string.

    NOTE: only a specific set of operators are allow, currently $or and $and.
    Please send a request if you'd like another operator to be enabled.

    NOTE: Your query must be valid JSON, double check it here,
    http://json.parser.online.fr/

    E.g. api?query='{"last_name": "Smith"}'
    """
    if request.method == "OPTIONS":
        response = HttpResponse()
        add_cors_headers(response)
        return response
    helper_auth_helper(request)
    fs_xform = FieldSightXF.objects.get(pk=fsxf_id)
    xform = fs_xform.xf
    # owner = request.user

    if not xform:
        return HttpResponseForbidden(_(u'Not shared.'))
    # if not request.GET.get('query', False):
    #     response = HttpResponse( json_util.dumps([{"count": 1}]), content_type='application/json')
    #     add_cors_headers(response)
    #     return response

    try:
        args = {
            'username': xform.user.username,
            'id_string': xform.id_string,
            'query': request.GET.get('query'),
            'fields': request.GET.get('fields'),
            'sort': request.GET.get('sort')
        }
        if 'start' in request.GET:
            args["start"] = int(request.GET.get('start'))
        if 'limit' in request.GET:
            args["limit"] = int(request.GET.get('limit'))
        if 'count' in request.GET:
            args["count"] = True if int(request.GET.get('count')) > 0\
                else False
        if xform:
            if fs_xform.project:
                args["fs_project_uuid"] = fs_xform.id
                if site_id is not None:
                    args['site_id'] = site_id
            else:
                args["fs_uuid"] = fs_xform.id
        cursor = query_mongo(**args)
    except ValueError as e:
        return HttpResponseBadRequest(e.__str__())
    records = list(record for record in cursor)
    response_text = json_util.dumps(records)

    if 'callback' in request.GET and request.GET.get('callback') != '':
        callback = request.GET.get('callback')
        response_text = ("%s(%s)" % (callback, response_text))

    response = HttpResponse(response_text, content_type='application/json')
    add_cors_headers(response)
    return response


@require_GET
@group_required("Reviewer")
def show(request, fsxf_id):
    fxf = FieldSightXF.objects.get(pk=fsxf_id)
    xform, is_owner, can_edit, can_view = fxf.xf, False, False, False
    # no access

    data = {}
    data['cloned'] = len(
        XForm.objects.filter(user__username__iexact=request.user.username,
                             id_string__exact=fxf.xf.id_string + XForm.CLONED_SUFFIX)
    ) > 0
    data['public_link'] = MetaData.public_link(xform)
    data['is_owner'] = is_owner
    data['can_edit'] = can_edit
    data['can_view'] = can_view or request.session.get('public_link')
    data['xform'] = xform
    data['fxf'] = fxf
    data['content_user'] = xform.user
    data['base_url'] = "https://%s" % request.get_host()
    data['source'] = MetaData.source(xform)
    data['form_license'] = MetaData.form_license(xform).data_value
    data['data_license'] = MetaData.data_license(xform).data_value
    data['supporting_docs'] = MetaData.supporting_docs(xform)
    data['media_upload'] = MetaData.media_upload(xform)
    data['mapbox_layer'] = MetaData.mapbox_layer_upload(xform)
    data['external_export'] = MetaData.external_export(xform)


    if is_owner:
        set_xform_owner_data(data, xform, request, xform.user.username, xform.id_string)

    return render(request, "fieldsight_show.html", data)


# @group_required('KoboForms')
def download_jsonform(request,  fsxf_id):
    json = None
    try:
        instance_id = request.get_full_path().split("/")[-1]
        instance_id = int(instance_id)
        finstance = FInstance.objects.get(instance=instance_id)
        #hack
        xform =  finstance.instance.xform #hack version less
        json = xform.json #hack version less
        # end hack
        # fs_xform = finstance.fsxf
        # version = finstance.version
        # xform = fs_xform.xf
        # try:
        #     history = XformHistory.objects.get(xform=xform, version=version)
        #     json = history.json
        #     # print("his", json)
        # except Exception as e:
        #     json = xform.json
    except Exception as e:
        # no instance id in url
        fs_xform = FieldSightXF.objects.get(pk=fsxf_id)
        xform = fs_xform.xf
        json = xform.json
    if request.method == "OPTIONS":
        response = HttpResponse()
        add_cors_headers(response)
        return response
    helper_auth_helper(request)
    response = response_with_mimetype_and_name('json', xform.id_string,
                                               show_date=False)
    if 'callback' in request.GET and request.GET.get('callback') != '':
        callback = request.GET.get('callback')
        response.content = "%s(%s)" % (callback, json)
    else:
        add_cors_headers(response)
        response.content = json
    return response


@require_POST
@login_required
def delete_data(request, fsxf_id=None):
    pass
    # xform, owner = check_and_set_user_and_form(username, id_string, request)
    # response_text = u''
    # if not xform or not has_edit_permission(
    #     xform, owner, request, xform.shared
    # ):
    #     return HttpResponseForbidden(_(u'Not shared.'))
    #
    # data_id = request.POST.get('id')
    # if not data_id:
    #     return HttpResponseBadRequest(_(u"id must be specified"))
    #
    # Instance.set_deleted_at(data_id)
    # audit = {
    #     'xform': xform.id_string
    # }
    # audit_log(
    #     Actions.SUBMISSION_DELETED, request.user, owner,
    #     _("Deleted submission with id '%(record_id)s' "
    #         "on '%(id_string)s'.") %
    #     {
    #         'id_string': xform.id_string,
    #         'record_id': data_id
    #     }, audit, request)
    # response_text = json.dumps({"success": "Deleted data %s" % data_id})
    # if 'callback' in request.GET and request.GET.get('callback') != '':
    #     callback = request.GET.get('callback')
    #     response_text = ("%s(%s)" % (callback, response_text))
    #
    # return HttpResponse(response_text, content_type='application/json')



def data_view(request, fsxf_id):
    fs_xform = FieldSightXF.objects.get(pk=fsxf_id)
    xform = fs_xform.xf
    data = {
        'fsxf_id': fsxf_id,
        'owner': xform.user,
        'xform': xform,
        'obj': fs_xform
    }
    audit = {
        "xform": xform.id_string,
    }
    audit_log(
        Actions.FORM_DATA_VIEWED, request.user, xform.user,
        _("Requested data view for '%(id_string)s'.") %
        {
            'id_string': xform.id_string,
        }, audit, request)

    return render(request, "fieldsight_data_view.html", data)

class XFormView(object):
    model = XForm


class XformDetailView(LoginRequiredMixin, SuperAdminMixin, XFormView, DetailView):
    pass

@api_view(['POST'])
@authentication_classes([CsrfExemptSessionAuthentication, BasicAuthentication])
def save_educational_material(request):
    id = request.POST.get('id', False)
    stage = request.POST.get('stage', False)
    if stage:
        if EducationMaterial.objects.filter(Q(stage_id=stage) | Q(fsxf__stage_id=stage)).exists():
            id = EducationMaterial.objects.filter(Q(stage_id=stage) | Q(fsxf__stage_id=stage))[0].id
    print(id)
    if id:
        instance = EducationMaterial.objects.get(pk=id)
        form = EducationalmaterialForm(request.POST, request.FILES, instance=instance)
    else:
        form = EducationalmaterialForm(request.POST, request.FILES)
    if form.is_valid():
        em = form.save()
        for key in request.FILES.keys():
            if "new_images_" in key:
                img = request.FILES.get(key)
                ei = EducationalImages(image=img, educational_material=em)
                ei.save()
        serializer = EMSerializer(em)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({'error': 'Invalid Educational Material Data', 'errors': form.errors}, status=status.HTTP_400_BAD_REQUEST)

@login_required
@api_view(['POST'])
def stages_reorder(request):
    try:
        stages = request.data.get("stages")
        qs_list = []
        for i, stage in enumerate(stages):
            obj = Stage.objects.get(pk=stage.get("id"))
            obj.order = i+1
            obj.save()
            qs_list.append(obj.id)
        serializer = StageSerializer(Stage.objects.filter(pk__in=qs_list).annotate(
            sub_stage_weight=Sum(F('parent__weight'))), many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@login_required
@api_view(['POST'])
def substages_reorder(request):
    try:
        stages = request.data.get("stages")
        qs = []
        for i, stage in  enumerate(stages):
            obj = Stage.objects.get(pk=stage.get("id"))
            obj.order = i+1
            obj.save()
            qs.append(obj)
        serializer = SubStageSerializer(qs, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class DeleteMyForm(MyFormMixin, View):
    def get(self, request, xf_id):
        obj, created = DeletedXForm.objects.get_or_create(xf_id=xf_id)
        messages.success(request, 'Form Sucessfully Deleted.')
        return HttpResponseRedirect(reverse("forms:forms-list"))


@login_required
@api_view(['POST'])
@parser_classes([FormParser, MultiPartParser])
def save_edumaterial(request, stageid):
    try:
        data = request.data
        is_pdf = data.get("is_pdf", False)
        stage = Stage.objects.get(pk=stageid)
        try:
            em = stage.em
        except:
            em = EducationMaterial(stage=stage)
        if is_pdf:
            em.pdf = data.get('pdf')
            em.is_pdf = True
            em.save()
        else:
            em.save()
            for key in data.keys():
                if "new_images_" in key:
                    img = data.get(key)
                    ei = EducationalImages(image=img, educational_material=em)
                    ei.save()
        response_data = EMSerializer(em).data
        return Response({"em":response_data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@login_required
@api_view(['POST'])
def save_edumaterial_details(request, stageid):
    try:
        data = request.data
        stage = Stage.objects.get(pk=stageid)
        try:
            em = stage.em
        except:
            em = EducationMaterial(stage=stage)
        title = data.get('title', False)
        text = data.get('text', False)
        if title:
            em.title = title
        if text:
            em.text = text
        em.save()
        response_data = EMSerializer(em).data
        return Response({"em":response_data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def set_deploy_all_stages(request, is_project, pk):
    try:
        if is_project == "1":
            copy_allstages_to_sites.apply_async((), {'pk': pk}, countdown=2)
            return Response({'msg': 'ok'}, status=status.HTTP_200_OK)
        else:
            site = Site.objects.get(pk=pk)
            site.site_forms.filter(is_staged=True, xf__isnull=False, is_deployed=False, is_deleted=False).update(is_deployed=True)
            send_bulk_message_stages_deployed_site(site)
            return HttpResponse({'msg': 'ok'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error':e.message}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def set_deploy_main_stage(request, is_project, pk, stage_id):
    if True:
        if is_project == "1":
            main_stage = Stage.objects.get(pk=stage_id)
            copy_stage_to_sites.apply_async((), {'main_stage': main_stage.id, 'pk': pk}, countdown=2)
            serializer = StageSerializer(main_stage)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            site = Site.objects.get(pk=pk)
            main_stage = Stage.objects.get(pk=stage_id)
            FieldSightXF.objects.filter(stage__stage__id=main_stage.pk, is_deleted=False).update(is_deployed=True)
            send_bulk_message_stage_deployed_site(site, main_stage, 0)
            serializer = StageSerializer(main_stage)
            return Response(serializer.data, status=status.HTTP_200_OK)
    # except Exception as e:
    #     return HttpResponse({'error':e.message}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def set_deploy_sub_stage(request, is_project, pk, stage_id):
    try:
        sub_stage = Stage.objects.get(pk=stage_id)
        if is_project == "1":
            copy_sub_stage_to_sites.apply_async((), {'sub_stage':sub_stage.id, 'pk':pk},  countdown=2)
            serializer = SubStageDetailSerializer(sub_stage)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            site = Site.objects.get(pk=pk)
            stage_form = FieldSightXF.objects.get(stage__id=sub_stage.pk, is_deleted=False)
            stage_form.is_deployed = True
            stage_form.save()
            serializer = SubStageDetailSerializer(sub_stage)
            send_sub_stage_deployed_site(site, sub_stage, 0)
            return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CreateKoboFormView(TemplateView, LoginRequiredMixin):
    template_name = "fsforms/create_form.html"

    def get_context_data(self, **kwargs):
        data = super(CreateKoboFormView, self).get_context_data(**kwargs)
        token, created = Token.objects.get_or_create(user=self.request.user)
        data["token_key"] = token
        data["kpi_url"] = settings.KPI_URL
        data['has_user_profile'] = UserProfile.objects.filter(user=self.request.user).exists()

        return data


class DeleteFInstance(View):
    def get(self, request, *args, **kwargs):
        finstance = FInstance.objects.get(instance_id=self.kwargs.get('instance_pk'))
        form = finstance.fsxf
        if not has_change_form_permission(request, form, "delete"):
            raise PermissionDenied
        try:

            finstance.is_deleted = True
            finstance.save()
            instance = finstance.instance
            instance.deleted_at = datetime.datetime.now()
            instance.save()
            delete_form_instance(int(self.kwargs.get('instance_pk')))


            if finstance.site:
                extra_object=finstance.site
                site_id=extra_object.id
                project_id = extra_object.project_id
                organization_id = extra_object.project.organization_id
                extra_message="site"
            else:
                extra_object=finstance.project
                site_id=None
                project_id = extra_object.id
                organization_id = extra_object.organization_id
                extra_message="project"
            extra_json = {}

            extra_json['submitted_by'] = finstance.submitted_by.user_profile.getname()
            noti = finstance.logs.create(source=self.request.user, type=33, title="deleted response" + self.kwargs.get('instance_pk'),
                                         organization_id=organization_id,
                                         project_id=project_id,
                                         site_id=site_id,
                                         extra_json=extra_json,
                                         extra_object=extra_object,
                                         extra_message=extra_message,
                                         content_object=finstance)
            messages.success(request, 'Response sucessfully Deleted.')

        except Exception as e:
            messages.warning(request, 'Response deleted unsuccessfull.' + str(e))

        next_url = request.GET.get('next', '/')
        return HttpResponseRedirect(next_url)

class DeleteFieldsightXF(FormMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            fsform = FieldSightXF.objects.get(pk=self.kwargs.get('fsxf_id'))
            fsform.is_deleted = True
            fsform.save()

            extra_json = {}
            if fsform.site:
                if fsform.site_form_instances.count():
                    messages.warning(request, 'Form deleted unsuccessfull. Form have submissions' )
                    next_url = request.GET.get('next', '/')
                    return HttpResponseRedirect(next_url)

                extra_object=fsform.site
                site_id=extra_object.id
                project_id = extra_object.project_id
                organization_id = extra_object.project.organization_id
                extra_message="site"
                extra_json['submission_count'] = fsform.site_form_instances.all().count() 
            
            else:
                if fsform.project_form_instances.count():
                    messages.warning(request, 'Form deleted unsuccessfull. Form have submissions' )
                    next_url = request.GET.get('next', '/')
                    return HttpResponseRedirect(next_url)
                extra_object=fsform.project
                extra_message="project"
                site_id=None
                project_id = extra_object.id
                organization_id = extra_object.organization_id
                extra_json['submission_count'] = fsform.project_form_instances.all().count() 
            
            noti = fsform.logs.create(source=self.request.user, type=34, title="deleted form" + self.kwargs.get('fsxf_id'),
                                       organization_id=organization_id,
                                       project_id=project_id,
                                                        site_id=site_id,
                                                        extra_json=extra_json,
                                                        extra_object=extra_object,
                                                        extra_message=extra_message,
                                                        content_object=fsform)
            messages.success(request, 'Form sucessfully Deleted.')

        except Exception as e:
            messages.warning(request, 'Form deleted unsuccessfull.' + str(e))

        next_url = request.GET.get('next', '/')
        return HttpResponseRedirect(next_url)


        # <a class="btn btn-xs btn-danger" href="{% url 'users:end_user_role' role.pk %}?next={{ request.path|urlencode }}">Remove</a>

@api_view(['GET'])
def repair_mongo(request, instance):
    finstance = FInstance.objects.get(instance=instance)
    i = finstance.instance
    d = i.parsed_instance.to_dict_for_mongo()
    try:
        d.update(
            {'fs_project_uuid': str(finstance.project_fxf_id), 'fs_project': finstance.project_id, 'fs_status': 0, 'fs_site': finstance.site_id,
             'fs_uuid': finstance.site_fxf_id})
        try:
            synced = update_mongo_instance(d, i.id)
        except Exception as e:
            return Response({'error':"Failed to sync "+ str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': "Failed to sync mongo"}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'success': "synced mongo"}, status=status.HTTP_200_OK)

def download_submission(request, pk):
    finstance = get_object_or_404(FInstance, pk__exact=pk)
    response = response_with_mimetype_and_name('xml',  str(finstance.instance.id), show_date=False)
    response.content = finstance.instance.xml
    return response

def download_xml_version(request, pk):
    finstance = get_object_or_404(FInstance, pk__exact=pk)
    response = response_with_mimetype_and_name('xml',  str(finstance.instance.id),  show_date=False)
    submission_version = finstance.get_version
    xml = None
    if finstance.project_fxf:
        xml = finstance.project_fxf.xf.xml
        xf = finstance.project_fxf.xf
    else:
        xml = finstance.site_fxf.xf.xml
        xf = finstance.site_fxf.xf
    xml_version = get_version(xml)
    if submission_version and submission_version == xml_version:
        response.content = xml
    elif XformHistory.objects.filter(xform=xf,
                                    version=submission_version).exists():
            xf_history = XformHistory.objects.get(
                xform=xf, version=submission_version)
            response.content = xf_history.xml
    else:
        response.content = xml
    return response

@api_view(['GET'])
def get_attachments_of_finstance(request,pk):
    instance = FInstance.objects.get(pk=pk).instance
    instance_attachments = image_urls_dict(instance)

    return Response(instance_attachments, status=status.HTTP_200_OK)


def edit_data(request,  id_string, data_id):
    context = RequestContext(request)
    xform = get_object_or_404(
        XForm, id_string__exact=id_string)
    instance = get_object_or_404(
        Instance, pk=data_id, xform=xform)
    form = instance.fieldsight_instance.fsxf
    if not has_change_form_permission(request, form, 'edit'):
        raise PermissionDenied


    instance_attachments = image_urls_dict(instance)
    # check permission
    # if not has_edit_permission(xform, owner, request, xform.shared):
    #     return HttpResponseForbidden(_(u'Not shared.'))
    if not hasattr(settings, 'ENKETO_URL'):
        response = render_to_response('enketo_error.html', {},
                                      context_instance=RequestContext(request))
        response.status_code = 500
        return response

    injected_xml = inject_instanceid(instance.xml, instance.uuid)

    form_url = _get_form_url(request, xform.user.username, settings.ENKETO_PROTOCOL)

    try:
        url = enketo_url(
            form_url, xform.id_string, instance_xml=injected_xml,
            instance_id=instance.uuid, return_url="",
            instance_attachments=instance_attachments
        )
    except Exception as e:
        context.message = {
            'type': 'alert-error',
            'text': u"Enketo error, reason: %s" % e}
        messages.add_message(
            request, messages.WARNING,
            _("Enketo error: enketo replied %s") % e, fail_silently=True)
    else:
        if url:
            context.enketo = url
            return HttpResponseRedirect(url)

    response = render_to_response('enketo_error.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response


def view_data(request,  id_string, data_id):
    context = RequestContext(request)
    xform = get_object_or_404(
        XForm, id_string__exact=id_string)
    instance = get_object_or_404(
        Instance, pk=data_id, xform=xform)
    instance_attachments = image_urls_dict(instance)
    if not hasattr(settings, 'ENKETO_URL'):
        response = render_to_response('enketo_error.html', {},
                                      context_instance=RequestContext(request))
        response.status_code = 500
        return response

    injected_xml = inject_instanceid(instance.xml, instance.uuid)
    form_url = _get_form_url(request, xform.user.username, settings.ENKETO_PROTOCOL)

    try:
        url = enketo_view_url(
            form_url, xform.id_string, instance_xml=injected_xml,
            instance_id=instance.uuid, return_url="",
            instance_attachments=instance_attachments
        )
    except Exception as e:
        context.message = {
            'type': 'alert-error',
            'text': u"Enketo error, reason: %s" % e}
        messages.add_message(
            request, messages.WARNING,
            _("Enketo error: enketo replied %s") % e, fail_silently=True)
    else:
        if url:
            context.enketo = url
            return HttpResponseRedirect(url)
    response = render_to_response('enketo_error.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response


class FormVersions(LoginRequiredMixin, View):

    def dispatch(self, request, *args, **kwargs):
        is_project = kwargs.get("is_project")
        fsfid = kwargs.get("fsfid")
        fsf = FieldSightXF.objects.get(pk=fsfid)
        site = self.kwargs.get('site', 0)
        if is_project == "1":
            project = fsf.project
        else:
            site_obj = Site.objects.get(pk=site)
            project = site_obj.project
        project_id = project.id
        kwargs['project'] = project_id
        kwargs['obj'] = project
        kwargs['fsf'] = fsf
        kwargs['site'] = site

        kwargs['versions'] = XformHistory.objects.filter(xform=fsf.xf).order_by('-date')
        kwargs['latest'] = fsf.xf


        if request.is_super_admin:
            return super(FormVersions, self).dispatch(request, is_donor_only=False, *args, **kwargs)
        user_role = request.roles.filter(project_id=project_id, group_id=2)

        if user_role:
            return super(FormVersions, self).dispatch(request, is_donor_only=False, *args, **kwargs)

        organization_id = Project.objects.get(pk=project_id).organization.id
        user_role_asorgadmin = request.roles.filter(organization_id=organization_id, group_id=1)

        if user_role_asorgadmin:
            return super(FormVersions, self).dispatch(request, is_donor_only=False, *args, **kwargs)

        user_role_asdonor = request.roles.filter(project_id=project_id, group_id=7)
        if user_role_asdonor:
            return super(FormVersions, self).dispatch(request, is_donor_only=True, *args, **kwargs)

        raise PermissionDenied()

    def get(self,request, **kwargs):
        data = {'is_donor_only': kwargs.get('is_donor_only', False),
                       }
        data.update(**kwargs)
        return render(request, "fsforms/form_versions.html",
                      data)


def new_data(request,  site, form):
    context = RequestContext(request)
    xform = FieldSightXF.objects.get(pk=form).xf
    if not hasattr(settings, 'ENKETO_URL'):
        response = render_to_response('enketo_error.html', {},
                                      context_instance=RequestContext(request))
        response.status_code = 500
        return response

    form_url = _get_form_url(request, xform.user.username, settings.ENKETO_PROTOCOL)

    try:
        url = enketo_url_new_submission(
            form_url, xform.id_string, site=site,
            form=form, return_url="",
        )
    except Exception as e:
        context.message = {
            'type': 'alert-error',
            'text': u"Enketo error, reason: %s" % e}
        messages.add_message(
            request, messages.WARNING,
            _("Enketo error: enketo replied %s") % e, fail_silently=True)
    else:
        if url:
            context.enketo = url
            return HttpResponseRedirect(url)

    response = render_to_response('enketo_error.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response