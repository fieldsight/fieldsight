from __future__ import absolute_import

from celery import shared_task
from django.contrib.auth.models import User

from django.db import transaction
from django.conf import settings
from googleapiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials

from onadata.apps.fieldsight.models import Project, Site
from onadata.apps.fsforms.management.commands.corn_sync_report import update_sheet, create_new_sheet
from onadata.apps.fsforms.models import FieldSightXF, Schedule, Stage, ReportSyncSettings
from onadata.apps.fsforms.utils import send_sub_stage_deployed_project, send_bulk_message_stage_deployed_project, \
    send_bulk_message_stages_deployed_project, send_message_un_deploy_project, notify_koboform_updated
from onadata.apps.logger.models import XForm
from onadata.apps.eventlog.models import CeleryTaskProgress
from onadata.libs.utils.fieldsight_tools import clone_kpi_form

import time
from onadata.apps.userrole.models import UserRole
from onadata.apps.fsforms.share_xform import share_form, share_forms


@shared_task(max_retries=10, soft_time_limit=60)
def copy_allstages_to_sites(pk, is_deployed=True):
    try:
        project = Project.objects.get(pk=pk)
        with transaction.atomic():
            FieldSightXF.objects.filter(is_staged=True, project=project,
                                        is_deleted=False
                                        ).update(is_deployed=is_deployed)
        send_bulk_message_stages_deployed_project(project)
    except Exception as e:
        print(e)
        num_retries = copy_allstages_to_sites.request.retries
        seconds_to_wait = 2.0 ** num_retries
        # First countdown will be 1.0, then 2.0, 4.0, etc.
        raise copy_allstages_to_sites.retry(countdown=seconds_to_wait)


@shared_task(max_retries=10, soft_time_limit=60)
def copy_stage_to_sites(main_stage, pk, is_deployed=True):
    try:
        main_stage = Stage.objects.get(pk=main_stage)
        project = Project.objects.get(pk=pk)
        project_sub_stages = Stage.objects.filter(stage__id=main_stage.pk, stage_forms__is_deleted=False)
        sub_stages_id = [s.id for s in project_sub_stages]
        project_forms = FieldSightXF.objects.filter(stage__id__in=sub_stages_id, is_deleted=False)
        project_form_ids = [p.id for p in project_forms]
        with transaction.atomic():
            FieldSightXF.objects.filter(pk__in=project_form_ids).update(
                is_deployed=is_deployed)
            send_bulk_message_stage_deployed_project(project, main_stage, 0)
    except Exception as e:
        print(str(e))
        num_retries = copy_stage_to_sites.request.retries
        seconds_to_wait = 2.0 ** num_retries
        # First countdown will be 1.0, then 2.0, 4.0, etc.
        raise copy_stage_to_sites.retry(countdown=seconds_to_wait)


@shared_task(max_retries=10, soft_time_limit=60)
def copy_sub_stage_to_sites(sub_stage, pk, is_deployed=True):
    try:
        sub_stage = Stage.objects.get(pk=sub_stage)
        project = Project.objects.get(pk=pk)
        stage_form = sub_stage.stage_forms

        with transaction.atomic():
            stage_form.is_deployed = is_deployed
            stage_form.save()
        send_sub_stage_deployed_project(project, sub_stage, 0)
    except Exception as e:
        print(str(e))
        num_retries = copy_sub_stage_to_sites.request.retries
        seconds_to_wait = 2.0 ** num_retries
        # First countdown will be 1.0, then 2.0, 4.0, etc.
        raise copy_sub_stage_to_sites.retry(countdown=seconds_to_wait)


@shared_task(max_retries=10, soft_time_limit=60)
def copy_schedule_to_sites(schedule_id, fxf_status, pk=None):
    try:
        schedule = Schedule.objects.get(pk=schedule_id)
        fxf = schedule.schedule_forms
        send_message_un_deploy_project(fxf)
    except Exception as e:
        print(str(e))
        num_retries = copy_schedule_to_sites.request.retries
        seconds_to_wait = 2.0 ** num_retries
        # First countdown will be 1.0, then 2.0, 4.0, etc.
        raise copy_schedule_to_sites.retry(countdown=seconds_to_wait)


@shared_task(max_retries=5)
def post_update_xform(xform_id, user):
    existing_xform = XForm.objects.get(pk=xform_id)
    # user = User.objects.get(pk=user)
    # existing_xform.logs.create(source=user, type=20, title="Kobo form Updated",
    #                             description="update kobo form ", ) #event_name = ??

    notify_koboform_updated(existing_xform)


@shared_task(max_retries=5)
def clone_form(project_id, task_id):
    time.sleep(10)
    project = Project.objects.get(id=project_id)

    organization = project.organization
    try:
        super_org = organization.parent
        library_forms = super_org.library_forms.filter(deleted=False, form_type__in=[0, 1])

        fsxf_list = []

        for lf in library_forms:
            if lf.form_type == 0:
                fsxf = FieldSightXF(xf=lf.xf, project=project, is_deployed=True,
                                    default_submission_status=lf.default_submission_status,
                                    organization_form_lib=lf)
                fsxf_list.append(fsxf)
            else:
                scheduled_obj = Schedule.objects.\
                    create(project=project, date_range_start=lf.date_range_start,
                           date_range_end=lf.date_range_end,
                           schedule_level_id=lf.schedule_level_id, frequency=lf.frequency,
                           month_day=lf.month_day, organization_form_lib=lf)
                scheduled_obj.selected_days.add(*lf.selected_days.values_list('id', flat=True))
                scheduled_obj.save()

                scheduled_fxf = FieldSightXF(xf=lf.xf, project=project, is_deployed=True,
                                             is_scheduled=True,
                                             default_submission_status=lf.default_submission_status,
                                             schedule=scheduled_obj, organization_form_lib=lf)
                fsxf_list.append(scheduled_fxf)

        FieldSightXF.objects.bulk_create(fsxf_list)

        CeleryTaskProgress.objects.filter(id=task_id).update(status=2)
    except Exception as e:
        CeleryTaskProgress.objects.filter(id=task_id).update(status=2, description=str(e))


# task to share the form for all the project managers of a project where the form is assigned
# used whenever a new form has been assigned to a project
@shared_task(max_retires=5)
def share_form_managers(fxf, task_id):
    fxf = FieldSightXF.objects.get(pk=fxf)
    userrole = UserRole.objects.filter(project=fxf.project, group__name='Project Manager', ended_at__isnull=True)
    users = User.objects.filter(user_roles__in=userrole)
    shared = share_form(users, fxf.xf)
    if shared:
        CeleryTaskProgress.objects.filter(id=task_id).update(status=2)
    else:
        CeleryTaskProgress.objects.filter(id=task_id).update(status=3)


# task to share forms to a single person assigned as the project manager of a project
# shares all the forms that have been assigned previously to a project
@shared_task(max_retires=5)
def created_manager_form_share(userrole, task_id):
    userrole = UserRole.objects.get(pk=userrole)
    fxf = FieldSightXF.objects.filter(project=userrole.project)
    shared = share_forms(userrole.user, fxf)
    if shared:
        CeleryTaskProgress.objects.filter(id=task_id).update(status=2)
    else:
        CeleryTaskProgress.objects.filter(id=task_id).update(status=3)


# share form to the users as specified
@shared_task(max_retries=5)
def api_share_form(xf, users, task_id):
    xf = XForm.objects.get(pk=xf)
    if isinstance(users, list):
        users = User.objects.filter(id__in=users)
    else:
        users = User.objects.filter(id=users)
    shared = share_form(users, xf)
    if shared:
        CeleryTaskProgress.objects.filter(id=task_id).update(status=2)
    else:
        CeleryTaskProgress.objects.filter(id=task_id).update(status=3)


# clone the specified form but not assign to the project
@shared_task(max_retries=5)
def api_clone_form(form_id, user_id, task_id):
    user = User.objects.get(id=user_id)
    xf = XForm.objects.get(id=form_id)

    token = user.auth_token.key

    # general clone
    clone, id_string = clone_kpi_form(xf.id_string, token, task_id, xf.title)
    if clone:
        CeleryTaskProgress.objects.filter(id=task_id).update(status=2)
    else:
        CeleryTaskProgress.objects.filter(id=task_id).update(status=3)
        raise ValueError(" Failed  clone and deploy")



# @shared_task(max_retries=10)
# def copy_to_sites(fxf):
#     try:
#         with transaction.atomic():
#             for site in fxf.project.sites.filter(is_active=True):
#                 child, created = FieldSightXF.objects.get_or_create(is_staged=False, is_scheduled=False, xf=fxf.xf, site=site, fsform=fxf)
#                 child.is_deployed = True
#                 child.default_submission_status = fxf.default_submission_status
#                 child.save()
#     except Exception as e:
#         print(str(e))
#         num_retries = copy_to_sites.request.retries
#         seconds_to_wait = 2.0 ** num_retries
#         # First countdown will be 1.0, then 2.0, 4.0, etc.
#         raise copy_to_sites.retry(countdown=seconds_to_wait)

#
#
# from __future__ import absolute_import
#
# from celery import shared_task
#
# from django.db import transaction
#
# from onadata.apps.fieldsight.models import Site, Project
# from onadata.apps.fsforms.models import FieldSightXF, Schedule, Stage, DeployEvent
# from onadata.apps.fsforms.serializers.ConfigureStagesSerializer import StageSerializer
# from onadata.apps.fsforms.serializers.FieldSightXFormSerializer import FSXFormListSerializer, StageFormSerializer
# from onadata.apps.fsforms.utils import send_sub_stage_deployed_project, send_bulk_message_stage_deployed_project, \
#     send_bulk_message_stages_deployed_project
#
#
# @shared_task(max_retries=10)
# def copy_allstages_to_sites(pk):
#     try:
#         project = Project.objects.get(pk=pk)
#         main_stages = project.stages.filter(stage__isnull=True)
#         main_stages_list = [ms for ms in main_stages]
#         if not main_stages_list:
#             return True
#         with transaction.atomic():
#
#             FieldSightXF.objects.filter(is_staged=True, site__project=project, stage__isnull=False). \
#                 update(stage=None, is_deployed=False, is_deleted=True)
#             FieldSightXF.objects.filter(is_staged=True, project=project, is_deleted=False).update(is_deployed=True)
#             Stage.objects.filter(site__project=project, project_stage_id___isnull=False).delete()
#         send_bulk_message_stages_deployed_project(project)
#     except Exception as e:
#         num_retries = copy_allstages_to_sites.request.retries
#         seconds_to_wait = 2.0 ** num_retries
#         # First countdown will be 1.0, then 2.0, 4.0, etc.
#         raise copy_allstages_to_sites.retry(countdown=seconds_to_wait)
#
#
# @shared_task(max_retries=10)
# def copy_stage_to_sites(main_stage, pk):
#     try:
#         project = Project.objects.get(pk=pk)
#         project_sub_stages = Stage.objects.filter(stage__id=main_stage.pk, stage_forms__is_deleted=False)
#         sub_stages_id = [s.id for s in project_sub_stages]
#         project_forms = FieldSightXF.objects.filter(stage__id__in=sub_stages_id, is_deleted=False)
#         project_form_ids = [p.id for p in project_forms]
#         with transaction.atomic():
#             FieldSightXF.objects.filter(pk__in=project_form_ids).update(is_deployed=True)  # deploy this stage
#
#             FieldSightXF.objects.filter(fsform__id__in=project_form_ids).update(stage=None, is_deployed=False,
#                                                                                 is_deleted=True)
#             deleted_forms = FieldSightXF.objects.filter(fsform__id__in=project_form_ids)
#             deleted_stages_id = sub_stages_id
#             if main_stage.id:
#                 deleted_stages_id.append(main_stage.id)
#             deleted_stages = Stage.objects.filter(project_stage_id__in=deleted_stages_id)
#             Stage.objects.filter(project_stage_id=main_stage.id).delete()
#             Stage.objects.filter(project_stage_id__in=sub_stages_id).delete()
#             sites_affected = []
#             deploy_data = {
#                 'project_stage': StageSerializer(main_stage).data,
#                 'project_sub_stages': StageSerializer(project_sub_stages, many=True).data,
#                 'project_forms': StageFormSerializer(project_forms, many=True).data,
#                 'deleted_forms': StageFormSerializer(deleted_forms, many=True).data,
#                 'deleted_stages': StageSerializer(deleted_stages, many=True).data,
#                 'sites_affected': sites_affected,
#             }
#             d = DeployEvent(project=project, data=deploy_data)
#             d.save()
#             send_bulk_message_stage_deployed_project(project, main_stage, d.id)
#     except Exception as e:
#         print(str(e))
#         num_retries = copy_stage_to_sites.request.retries
#         seconds_to_wait = 2.0 ** num_retries
#         # First countdown will be 1.0, then 2.0, 4.0, etc.
#         raise copy_stage_to_sites.retry(countdown=seconds_to_wait)
#
# @shared_task(max_retries=10)
# def copy_sub_stage_to_sites(sub_stage, pk):
#     try:
#         project = Project.objects.get(pk=pk)
#         sites = project.sites.filter(is_active=True)
#         site_ids = []
#         main_stage = sub_stage.stage
#         stage_form = sub_stage.stage_forms
#
#         with transaction.atomic():
#             FieldSightXF.objects.filter(pk=stage_form.pk).update(is_deployed=True)
#             stage_form.is_deployed = True
#             stage_form.save()
#
#             FieldSightXF.objects.filter(fsform__id=stage_form.id).update(stage=None, is_deployed=False, is_deleted=True)
#
#             deleted_forms = FieldSightXF.objects.filter(fsform__id=stage_form.id)
#             deleted_stages = Stage.objects.filter(project_stage_id=sub_stage.id, stage__isnull=False)
#
#             Stage.objects.filter(project_stage_id=sub_stage.id, stage__isnull=False).delete()
#             deploy_data = {'project_forms': [StageFormSerializer(stage_form).data],
#                        'project_stage': StageSerializer(main_stage).data,
#                        'project_sub_stages': [StageSerializer(sub_stage).data],
#                        'deleted_forms': StageFormSerializer(deleted_forms, many=True).data,
#                        'deleted_stages': StageSerializer(deleted_stages, many=True).data,
#                        'sites_affected': [],
#                        }
#         d = DeployEvent(project=project, data=deploy_data)
#         d.save()
#         send_sub_stage_deployed_project(project, sub_stage, d.id)
#     except Exception as e:
#         print(str(e))
#         num_retries = copy_sub_stage_to_sites.request.retries
#         seconds_to_wait = 2.0 ** num_retries
#         # First countdown will be 1.0, then 2.0, 4.0, etc.
#         raise copy_sub_stage_to_sites.retry(countdown=seconds_to_wait)
#
# @shared_task(max_retries=10)
# def copy_schedule_to_sites(schedule, fxf_status, pk):
#     try:
#         fxf = schedule.schedule_forms
#         selected_days = tuple(schedule.selected_days.all())
#         with transaction.atomic():
#             if not fxf_status:
#                 # deployed case
#                 fxf.is_deployed = True
#                 fxf.save()
#                 FieldSightXF.objects.filter(fsform=fxf, is_scheduled=True, site__project__id=pk).update(is_deployed=True,
#                                                                                                         is_deleted=False)
#
#             else:
#                 # undeploy
#                 fxf.is_deployed = False
#                 fxf.save()
#                 FieldSightXF.objects.filter(fsform=fxf, is_scheduled=True, site__project_id=pk).update(is_deployed=False,
#                                                                                                        is_deleted=True)
#     except Exception as e:
#         print(str(e))
#         num_retries = copy_schedule_to_sites.request.retries
#         seconds_to_wait = 2.0 ** num_retries
#         # First countdown will be 1.0, then 2.0, 4.0, etc.
#         raise copy_schedule_to_sites.retry(countdown=seconds_to_wait)
#
#


@shared_task(max_retries=5)
def update_progress(site_id, project_fxf_id, submission_answer={}):
    time.sleep(5)
    try:
        site = Site.objects.get(pk=site_id)
        project_fxf = FieldSightXF.objects.get(pk=project_fxf_id)
        project_settings = site.project.progress_settings.filter(
            deployed=True, active=True).order_by("-date").first()
        site_saved = False
        progress = 0
        if project_settings:
            if project_settings.source == 0 and project_fxf.is_staged:
                progress = site.progress()
                site.current_progress = progress
                site.save()
                site_saved = True
            elif project_settings.source == 1 and project_fxf.is_staged:
                from onadata.apps.fieldsight.utils.progress import advance_stage_approved
                progress = advance_stage_approved(site, site.project)
                if progress:
                    site.current_progress = progress
                    site.save()
                    site_saved = True

            elif project_settings.source == 2 and (
                    project_settings.pull_integer_form == project_fxf.pk or
                    project_settings.pull_integer_form == str(project_fxf.pk)):
                xform_question = project_settings.pull_integer_form_question
                from onadata.apps.fieldsight.utils.progress import pull_integer_answer
                progress = pull_integer_answer(project_fxf, xform_question, site, submission_answer)
                try:
                    progress = int(progress)
                    if progress and progress > 99:
                        progress = 100
                    site.current_progress = progress
                    site.save()
                    site_saved = True
                except Exception as e:
                    progress = 0
                    print("progress error", str(e))
            elif project_settings.source == 4 and (
                    project_settings.no_submissions_form == project_fxf.pk or
                    project_settings.no_submissions_form == str(project_fxf.pk)):
                progress = ("%.0f" % (site.site_instances.filter(
                    project_fxf_id=project_fxf_id, form_status=3).count() / (
                                       project_settings.no_submissions_total_count * 0.01)))
                progress = int(progress)
                if progress > 99:
                    progress = 100
                site.current_progress = progress
                site.save()
                site_saved = True
            elif project_settings.source == 3:
                progress = ("%.0f" % (site.site_instances.filter(form_status=3).count() / (
                            project_settings.no_submissions_total_count * 0.01)))
                progress = int(progress)
                if progress > 99:
                    progress = 100
                site.current_progress = progress
                site.save()
                site_saved = True
        if site_saved:
            print(progress, site_id, "progress , site id")
            from onadata.apps.fieldsight.models import SiteProgressHistory
            if not SiteProgressHistory.objects.filter(site=site, progress=progress,
                                                      setting=project_settings).exists():
                history = SiteProgressHistory(site=site, progress=progress,
                                              setting=project_settings)
                history.save()
    except Exception as e:
        print("error progess update in submission", str(e))


@shared_task(max_retries=5, soft_time_limit=300)
def sync_sheet(sheet_id):
    time.sleep(2)

    sheet = ReportSyncSettings.objects.get(id=sheet_id)

    report_type = sheet.report_type
    project = sheet.project
    form_id = sheet.form_id if sheet.form else 0
    spreadsheet_id = sheet.spreadsheet_id
    grid_id = sheet.grid_id
    sheet_range = sheet.range

    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive',
             'https://www.googleapis.com/auth/spreadsheets']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        settings.SERVICE_ACCOUNT_JSON, scope)

    service = discovery.build('sheets', 'v4', credentials=credentials,
                              cache_discovery=False)
    if spreadsheet_id:  # Already Have file in Drive
        update_sheet(service, sheet,
                     report_type, project, form_id, spreadsheet_id, grid_id, sheet_range)
    else:
        create_new_sheet(sheet)
