from __future__ import unicode_literals
import datetime
import os
import json
import re
from xml.dom import Node
from jsonfield import JSONField
from shortuuid import ShortUUID
from pyxform.xform2json import create_survey_element_from_xml
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Max
from django.db.models.signals import post_save, pre_delete
from django.utils.translation import ugettext_lazy as _
from django.dispatch import receiver
from django.contrib.sites.models import Site as DjangoSite
from pyxform import create_survey_from_xls, SurveyElementBuilder
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from onadata.apps.fieldsight.models import Site, Project, Organization, \
    ProgressSettings, SuperOrganization
from onadata.apps.fsforms.fieldsight_models import IntegerRangeField
from onadata.apps.fsforms.utils import send_message, send_message_project_form,\
    check_version
from onadata.apps.logger.models import XForm, Instance
from onadata.apps.logger.xform_instance_parser import clean_and_parse_xml
from onadata.apps.viewer.models import ParsedInstance
from onadata.apps.fsforms.fsxform_responses import \
    get_instances_for_field_sight_form
from onadata.settings.local_settings import XML_VERSION_MAX_ITER
from django.db import transaction, IntegrityError


SHARED_LEVEL = [(0, 'Global'), (1, 'Organization'), (2, 'Project')]
SCHEDULED_LEVEL = [(0, 'Daily'), (1, 'Weekly'), (2, 'Monthly')]
FORM_STATUS = [(0, 'Pending'), (1, 'Rejected'),
               (2, 'Flagged'), (3, 'Approved')]

REPORT_TYPE = [('site_info', 'Site Info'), ('site_progress', 'Site Progress'), ('form', 'Form'),  ('custom', 'Custom')]
SCHEDULED_TYPE = [(0, 'Manual'), (1, 'Daily'), (2, 'Weekly'), (3, 'Monthly')]
FORM_TYPE = [(0, 'General'), (1, 'Scheduled')]


class Days(models.Model):
    day = models.CharField(max_length=9)
    index = models.IntegerField()

    def __unicode__(self):
        return getattr(self, "day", "")


class FormGroup(models.Model):
    name = models.CharField(max_length=256, unique=True)
    description = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, related_name="form_group")
    is_global = models.BooleanField(default=False)
    organization = models.ForeignKey(Organization, null=True, blank=True)
    project = models.ForeignKey(Project, null=True, blank=True)
    logs = GenericRelation('eventlog.FieldSightLog')

    class Meta:
        db_table = 'fieldsight_forms_group'
        verbose_name = _("FieldSight Form Group")
        verbose_name_plural = _("FieldSight Form Groups")
        ordering = ("-date_modified",)

    def __unicode__(self):
        return getattr(self, "name", "")


class ActiveStagesManager(models.Manager):
    def get_queryset(self):
        return super(ActiveStagesManager, self).get_queryset(

        ).filter(is_deleted=False)


class ActiveOrgLibs(models.Manager):
    def get_queryset(self):
        return super(ActiveOrgLibs, self).get_queryset(

        ).filter(deleted=False)


class OrganizationFormLibrary(models.Model):
    xf = models.ForeignKey(XForm, related_name="library_forms")
    organization = models.ForeignKey(SuperOrganization, related_name="library_forms")
    form_type = models.IntegerField(default=0, choices=FORM_TYPE)
    date_range_start = models.DateField(default=datetime.date.today, null=True, blank=True)
    date_range_end = models.DateField(default=datetime.date.today, null=True, blank=True)
    selected_days = models.ManyToManyField(Days,
                                           related_name='library_forms', blank=True)
    schedule_level_id = models.IntegerField(default=0, choices=SCHEDULED_LEVEL, null=True, blank=True)
    default_submission_status = models.IntegerField(default=0,
                                                    choices=FORM_STATUS)
    frequency = models.IntegerField(default=0, null=True, blank=True)
    month_day = models.IntegerField(default=0, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)
    is_form_library = models.BooleanField(default=False)
    objects = ActiveOrgLibs()


class Stage(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField(blank=True, null=True)
    group = models.ForeignKey(FormGroup,related_name="stage", null=True,
                              blank=True)
    order = IntegerRangeField(min_value=0, max_value=30,default=0)
    stage = models.ForeignKey('self', blank=True, null=True,
                              related_name="parent")
    shared_level = models.IntegerField(default=2, choices=SHARED_LEVEL)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    site = models.ForeignKey(Site, related_name="stages", null=True, blank=True)
    project = models.ForeignKey(Project, related_name="stages",
                                null=True, blank=True)
    ready = models.BooleanField(default=False)
    project_stage_id = models.IntegerField(default=0)
    weight = models.IntegerField(default=0)
    tags = ArrayField(models.IntegerField(), default=[])
    regions = ArrayField(models.IntegerField(), default=[])
    is_deleted = models.BooleanField(default=False)
    objects = ActiveStagesManager()
    logs = GenericRelation('eventlog.FieldSightLog')

    class Meta:
        db_table = 'fieldsight_forms_stage'
        verbose_name = _("FieldSight Form Stage")
        verbose_name_plural = _("FieldSight Form Stages")
        ordering = ("order",)

    def save(self, *args, **kwargs):
        if self.stage:
            self.group = self.stage.group
        super(Stage, self).save(*args, **kwargs)

    def get_display_name(self):
        return "Stage" if not self.stage  else "SubStage"

    def is_main_stage(self):
        return True if not self.stage else False

    def sub_stage_count(self):
        if not self.stage:
            return Stage.objects.filter(stage=self).count()
        return 0

    def form_exists(self):
        return True if FieldSightXF.objects.filter(stage=self).count() > 0\
            else False

    def form_name(self):
        if not FieldSightXF.objects.filter(stage=self).count():
            return ""
        return FieldSightXF.objects.filter(stage=self)[0].xf.title

    def form(self):
        if not FieldSightXF.objects.filter(stage=self).count():
            return None
        return FieldSightXF.objects.filter(stage=self)[0]

    def active_substages(self):
        return self.parent.filter(stage_forms__isnull=False)

    def get_sub_stage_list(self, sync_details=False, values_list=False):
        if not self.stage:
            qs= Stage.objects.select_related(
                'stage_forms__xf').filter(stage=self)
            if sync_details:
                if values_list:
                    return qs.select_related(
                        'stage_forms__sync_schedule').filter(
                        stage_forms__sync_schedule__isnull=False).values(
                        'stage_forms__sync_schedule__id',
                        'stage_forms__xf__title',
                        'stage_forms__sync_schedule__schedule',
                        'stage_forms__sync_schedule__date',
                        'stage_forms__sync_schedule__end_of_month')
                else:
                    return qs.select_related(
                        'stage_forms__sync_schedule').filter(
                        stage_forms__sync_schedule__isnull=False)

            return qs.values('stage_forms__id','name','stage_id',
                             'stage_forms__xf__id_string',
                             'stage_forms__xf__user__username')
        return []


    @property
    def xf(self):
        return FieldSightXF.objects.filter(stage=self)[0].xf.pk\
            if self.form_exists() else None

    @property
    def form_status(self):
        status = 0
        if self.stage_forms.site_form_instances.filter(form_status=3).exists():
            status = 1
        return status

    @property
    def form_count(self):
        return self.stage_forms.site_form_instances.all().count()
    
    @staticmethod
    def site_submission_count(id, site_id):
        return Stage.objects.get(
            pk=id).stage_forms.project_form_instances.filter(
            site_id=site_id).count()
    
    
    @staticmethod
    def rejected_submission_count(id, site_id):
        return Stage.objects.get(
            pk=id).stage_forms.project_form_instances.filter(
            form_status=1, site_id=site_id).count()
    
    @staticmethod
    def flagged_submission_count(id, site_id):
        return Stage.objects.get(
            pk=id).stage_forms.project_form_instances.filter(
            form_status=2, site_id=site_id).count()
    
        
    @classmethod
    def get_order(cls, site, project, stage):
        if site:
            if not Stage.objects.filter(site=site).exists():
                return 1
            elif stage is not None:
                if not Stage.objects.filter(stage=stage).exists():
                    return 1
                else:
                    mo = Stage.objects.filter(
                        stage=stage).aggregate(Max('order'))
                    order = mo.get('order__max', 0)
                    return order + 1
            else:
                mo = Stage.objects.filter(
                    site=site, stage__isnull=True).aggregate(Max('order'))
                order = mo.get('order__max', 0)
                return order + 1
        else:
            if not Stage.objects.filter(project=project).exists():
                return 1
            elif stage is not None:
                if not Stage.objects.filter(stage=stage).exists():
                    return 1
                else:
                    mo = Stage.objects.filter(
                        stage=stage).aggregate(Max('order'))
                    order = mo.get('order__max', 0)
                    return order + 1
            else:
                mo = Stage.objects.filter(
                    project=project, stage__isnull=True).aggregate(Max('order'))
                order = mo.get('order__max', 0)
                return order + 1

    def __unicode__(self):
        return getattr(self, "name", "")


class ScheduleManager(models.Manager):
    def get_queryset(self):
        return super(ScheduleManager, self).get_queryset().filter(is_deleted=False)


class Schedule(models.Model):
    name = models.CharField("Schedule Name",
                            max_length=256, blank=True, null=True)
    site = models.ForeignKey(Site,
                             related_name="schedules", null=True, blank=True)
    project = models.ForeignKey(Project,
                                related_name="schedules", null=True, blank=True)
    organization_form_lib = models.ForeignKey(OrganizationFormLibrary, related_name="schedules",
                                              null=True, blank=True)
    date_range_start = models.DateField(default=datetime.date.today)
    date_range_end = models.DateField(default=datetime.date.today)
    selected_days = models.ManyToManyField(Days,
                                           related_name='days', blank=True)
    shared_level = models.IntegerField(default=2, choices=SHARED_LEVEL)
    schedule_level_id = models.IntegerField(default=0, choices=SCHEDULED_LEVEL)
    frequency = models.IntegerField(default=0)
    month_day = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False)
    objects = ScheduleManager()
    date_created = models.DateTimeField(auto_now_add=True)

    logs = GenericRelation('eventlog.FieldSightLog')

    class Meta:
        db_table = 'fieldsight_forms_schedule'
        verbose_name = _("Form Schedule")
        verbose_name_plural = _("Form Schedules")
        ordering = ('-date_range_start', 'date_range_end')

    def form_exists(self):
        return True if FieldSightXF.objects.filter(schedule=self).count()\
                       > 0 else False

    def form(self):
        return FieldSightXF.objects.filter(schedule=self)[0] \
            if self.form_exists() else None

    @property
    def xf(self):
        return FieldSightXF.objects.filter(schedule=self)[0].xf.pk\
            if self.form_exists() else None

    def __unicode__(self):
        return "--"


class DeletedXForm(models.Model):
    xf = models.OneToOneField(XForm, related_name="deleted_xform")
    date_created = models.DateTimeField(auto_now=True)


class FieldSightXF(models.Model):
    xf = models.ForeignKey(XForm, related_name="field_sight_form")
    site = models.ForeignKey(Site, related_name="site_forms", null=True,
                             blank=True)
    project = models.ForeignKey(Project, related_name="project_forms",
                                null=True, blank=True)
    organization_form_lib = models.ForeignKey(OrganizationFormLibrary, related_name="organization_forms",
                                              null=True, blank=True)
    is_staged = models.BooleanField(default=False)
    is_scheduled = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now=True)
    date_modified = models.DateTimeField(auto_now=True)
    schedule = models.OneToOneField(Schedule, blank=True, null=True,
                                    related_name="schedule_forms")
    stage = models.OneToOneField(Stage, blank=True, null=True,
                                 related_name="stage_forms")
    shared_level = models.IntegerField(default=2, choices=SHARED_LEVEL)
    form_status = models.IntegerField(default=0, choices=FORM_STATUS)
    fsform = models.ForeignKey('self', blank=True, null=True,
                               related_name="parent")
    is_deployed = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    is_survey = models.BooleanField(default=False)
    from_project = models.BooleanField(default=True)
    default_submission_status = models.IntegerField(default=0,
                                                    choices=FORM_STATUS)
    logs = GenericRelation('eventlog.FieldSightLog')

    class Meta:
        db_table = 'fieldsight_forms_data'
        verbose_name = _("XForm")
        verbose_name_plural = _("XForms")
        ordering = ("-date_created",)

    def url(self):
        return reverse(
            "download_fild_sight_form",
            kwargs={
                "site": self.site.username,
                "id_string": self.id_string
            }
        )

    def getname(self):
        return '{0} form {1}'.format(self.form_type(),
                                           self.xf.title,)
    def getresponces(self):
        return get_instances_for_field_sight_form(self.pk)

    def getlatestsubmittiondate(self):
        if self.site is not None:
            return self.site_form_instances.order_by('-pk').values('date')[:1]
        else:
            return self.project_form_instances.order_by('-pk').values(
                'date')[:1]

    def get_absolute_url(self):
        if self.project:
            return reverse('forms:setup-forms',
                           kwargs={'is_project':1, 'pk':self.project_id})
        else:
            return reverse('forms:setup-forms',
                           kwargs={'is_project':0, 'pk':self.site_id})
            
    def form_type(self):
        if self.is_scheduled:
            return "scheduled"
        if self.is_staged:
            return "staged"
        if self.is_survey:
            return "survey"
        if not self.is_scheduled and not self.is_staged:
            return "general"

    def form_type_id(self):
        if self.is_scheduled and self.schedule: return self.schedule.id
        if self.is_staged and self.stage: return self.stage.id
        return None

    def stage_name(self):
        if self.stage: return self.stage.name

    def schedule_name(self):
        if self.schedule: return self.schedule.name

    def clean(self):
        if self.is_staged:
            if FieldSightXF.objects.filter(stage=self.stage).exists():
                if not FieldSightXF.objects.filter(
                        stage=self.stage).pk == self.pk:
                    raise ValidationError({
                        'xf': ValidationError(_('Duplicate Stage Data')),
                    })
        if self.is_scheduled:
            if FieldSightXF.objects.filter(schedule=self.schedule).exists():
                if not FieldSightXF.objects.filter(
                        schedule=self.schedule)[0].pk == self.pk:
                    raise ValidationError({
                        'xf': ValidationError(_('Duplicate Schedule Data')),
                    })
        if not self.is_scheduled and not self.is_staged:
            if self.site:
                if FieldSightXF.objects.filter(xf=self.xf, is_scheduled=False,
                                               is_staged=False,
                                               project=self.site.project
                                               ).exists():
                    raise ValidationError({
                        'xf': ValidationError(
                            _('Form Already Used in Project Level')),
                    })
            else:
                if FieldSightXF.objects.filter(
                        xf=self.xf, is_scheduled=False, is_staged=False,
                        site=self.site, project=self.project,
                        is_deleted=False).exists():
                    if not FieldSightXF.objects.filter(xf=self.xf,
                                                       is_scheduled=False,
                                                       is_staged=False,
                                                       site=self.site,
                                                       project=self.project
                                                       )[0].pk == self.pk:
                        raise ValidationError({
                            'xf': ValidationError(
                                _('Duplicate General Form Data')),
                        })

    @staticmethod
    def get_xform_id_list(site_id):
        fs_form_list = FieldSightXF.objects.filter(
            site__id=site_id).order_by('xf__id').distinct('xf__id')
        return [fsform.xf.pk for fsform in fs_form_list]

    @property
    def site_name(self):
        if self.site is not None:
            return u'{}'.format(self.site.name)\

    @property
    def site_or_project_display(self):
        if self.site is not None:
            return u'{}'.format(self.site.name)
        return u'{}'.format(self.project.name)

    @property
    def project_info(self):
        if self.fsform:
            self.fsform.pk
        return None

    @property
    def has_versions(self):
        return self.xf.fshistory.exists()

    def __unicode__(self): 
        return u'{}- {}- {}'.format(self.xf, self.site, self.is_staged)


# @receiver(post_save, sender=OrganizationFormLibrary)
# def create_org_forms_in_projects(sender, instance, created,  **kwargs):
#     projects = Project.objects.filter(organization__parent=instance.organization)
#     fsxf_list = []
#     for p in projects:    
#         fsxf = FieldSightXF(xf=instance.xf, project=p, is_deployed=True)
#         fsxf_list.append(fsxf)
#     FieldSightXF.objects.bulk_create(fsxf_list)


class FormSettings(models.Model):
    form = models.OneToOneField(FieldSightXF, related_name="settings")
    types = ArrayField(models.IntegerField(), default=[])
    regions = ArrayField(models.IntegerField(), default=[])
    notify_incomplete_schedule = models.BooleanField(default=False)
    donor_visibility = models.BooleanField(default=False)
    can_edit = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)

    @property
    def default_submission_status(self):
        return self.form.default_submission_status

    @property
    def weight(self):
        try:
            return self.form.stage.weight
        except:
            return 0

    def __unicode__(self):
        return getattr(self, "name", "")


@receiver(post_save, sender=FieldSightXF)
def create_messages(sender, instance, created,  **kwargs):
    if instance.project and created:
        sync_settings = ReportSyncSettings(project=instance.project, form=instance, report_type="form", schedule_type=0)
        sync_settings.save()
    if instance.project is not None and created and not instance.is_staged and not instance.is_scheduled:
        send_message_project_form(instance)
    elif created and instance.site is not None and not instance.is_staged and not instance.is_scheduled:
        send_message(instance)

    if instance.project is not None and created:
        from onadata.apps.fsforms.tasks import share_form_managers
        from onadata.apps.eventlog.models import CeleryTaskProgress
        task_obj = CeleryTaskProgress.objects.create(user=instance.xf.user,
                                                     description="Share Forms",
                                                     task_type=17, content_object=instance)
        if task_obj:
            try:
                with transaction.atomic():
                    share_form_managers.apply_async(kwargs={'fxf': instance.id, 'task_id': task_obj.id}, countdown=5)
            except IntegrityError as e:
                print(e)


@receiver(post_save, sender=Stage)
def update_site_progress(sender, instance, *args, **kwargs):
    try:
        fsxf = instance.stage_forms
        if fsxf.is_deployed:
            if instance.project:
                if ProgressSettings.objects.filter(project=instance.project, active=True, deployed=True).exists():
                    progress_settings = ProgressSettings.objects.filter(
                        project=fsxf.project, active=True, deployed=True)[0]
                    if progress_settings.status in [0, 1]:
                        from onadata.apps.fieldsight.tasks import update_sites_progress
                        from onadata.apps.eventlog.models import CeleryTaskProgress
                        task_obj = CeleryTaskProgress.objects.create(user=instance.xf.user,
                                                                     description='Update site progress',
                                                                     task_type=23, content_object=instance)
                        if task_obj:
                            try:
                                with transaction.atomic():
                                    update_sites_progress.apply_async(
                                        kwargs={'pk': progress_settings.id, 'task_id': task_obj.id}, countdown=5)
                            except IntegrityError as e:
                                print(e)
            else:
                if not instance.site.enable_subsites:
                    from onadata.apps.fieldsight.utils.progress import set_site_progress
                    set_site_progress(instance.site,instance.site.project)
    except:
        pass


@receiver(pre_delete, sender=FieldSightXF)
def send_delete_message(sender, instance, using, **kwargs):
    if instance.project is not None:
        pass
    elif instance.is_staged:
        pass
    else:
        fxf = instance
        send_message(fxf)


post_save.connect(create_messages, sender=FieldSightXF)


class SyncSchedule(models.Model):
    MANUAL = "NA"
    DAILY = "D"
    WEEKLY = "W"
    FORTNIGHT = "F"
    MONTHLY = "M"
    SCHEDULES = [
        (MANUAL, "Manual"),
        (DAILY, "Daily"),
        (WEEKLY, "Weekly"),
        (FORTNIGHT, "Fortnightly"),
        (MONTHLY, "Monthly"),
    ]
    fxf = models.OneToOneField(FieldSightXF, related_name="sync_schedule")
    schedule = models.CharField(choices=SCHEDULES,
                                default=MONTHLY, max_length=2)
    date = models.DateField(blank=True, null=True)
    end_of_month = models.BooleanField(default=False)


class FieldSightParsedInstance(ParsedInstance):
    _update_fs_data = None

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self._update_fs_data = kwargs.pop('update_fs_data', {})
        super(FieldSightParsedInstance, self).save(*args, **kwargs)

    def to_dict_for_mongo(self):
        mongo_dict = super(FieldSightParsedInstance, self).to_dict_for_mongo()
        mongo_dict.update(self._update_fs_data)
        return mongo_dict

    @staticmethod
    def get_or_create(instance, update_data=None):
        if update_data is None:
            update_data = {}
        created = False
        try:
            fspi = FieldSightParsedInstance.objects.get(instance__pk=instance.pk)
            fspi.save(update_fs_data=update_data, async=False)
        except FieldSightParsedInstance.DoesNotExist:
            created = True
            fspi = FieldSightParsedInstance(instance=instance)
            fspi.save(update_fs_data=update_data, async=False)
        return fspi, created




class FInstanceManager(models.Manager):
    def get_queryset(self):
        return super(FInstanceManager, self).get_queryset().filter(is_deleted=False)


class FInstanceDeletedManager(models.Manager):
    def get_queryset(self):
        return super(FInstanceDeletedManager, self).get_queryset().filter(is_deleted=True)


class FInstance(models.Model):
    instance = models.OneToOneField(Instance,
                                    related_name='fieldsight_instance')
    site = models.ForeignKey(Site, null=True, related_name='site_instances')
    project = models.ForeignKey(Project, null=True,
                                related_name='project_instances')
    organization = models.ForeignKey(SuperOrganization, null=True, blank=True,
                                     related_name='organization_instances')
    team = models.ForeignKey(Organization, null=True, blank=True,
                             related_name='team_instances')
    site_fxf = models.ForeignKey(FieldSightXF, null=True,
                                 related_name='site_form_instances',
                                 on_delete=models.SET_NULL)
    project_fxf = models.ForeignKey(FieldSightXF, null=True, blank=True,
                                    related_name='project_form_instances')

    organization_form_lib = models.ForeignKey(OrganizationFormLibrary, related_name="organization_form_instances",
                                              null=True, blank=True)

    form_status = models.IntegerField(null=True,
                                      blank=True, choices=FORM_STATUS)
    comment = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now=True)
    submitted_by = models.ForeignKey(User, related_name="supervisor")
    is_deleted = models.BooleanField(default=False)
    version = models.CharField(max_length=255, default=u'')
    objects = FInstanceManager()
    deleted_objects = FInstanceDeletedManager()
    logs = GenericRelation('eventlog.FieldSightLog')

    @property
    def get_version(self):
        n = XML_VERSION_MAX_ITER
        for i in range(n, 0, -1):
            tag = "_version__00{0}".format(i)
            if self.instance.json.get(tag):
                return self.instance.json.get(tag)
        if self.instance.json.get('_version_'):
            return self.instance.json.get('_version_')
        else:
            return self.instance.json.get('__version__')

    def save(self, *args, **kwargs):
        self.version = self.get_version
        if self.form_status is None:
            if self.site_fxf:
                self.form_status = self.site_fxf.default_submission_status
            else:
                self.form_status = self.project_fxf.default_submission_status

        if self.project_fxf is not None:
            if self.project_fxf.organization_form_lib is not None:
                self.organization_form_lib = self.project_fxf.organization_form_lib
                self.organization = self.project_fxf.organization_form_lib.organization
        self.team = self.project.organization
        super(FInstance, self).save(*args, **kwargs)  # Call the "real" save() method.
        
    @property
    def fsxfid(self):
        if self.project_fxf:
            return self.project_fxf.id
        else:
            return self.site_fxf.id\

    @property
    def fsxf(self):
        if self.project_fxf:
            return self.project_fxf
        else:
            return self.site_fxf

    def get_absolute_url(self):

        if self.site_fxf:
            fxf_id = self.site_fxf_id
        else:
            fxf_id = self.project_fxf_id
            
        return "/fieldsight/application/?submission=" + str(self.instance.id) + "#/submission-details"

 
    def get_abr_form_status(self):
        return dict(FORM_STATUS)[self.form_status]    


    def getname(self):
        if self.site_fxf is None:
        
            return u'{0} form {1}'.format(self.project_fxf.form_type(),
                                          self.project_fxf.xf.title,)
        
        return u'{0} form {1}'.format(self.site_fxf.form_type(),
                                           self.site_fxf.xf.title,)
    def __unicode__(self):
        if self.site_fxf is None:
            return u"%s" % str(self.submitted_by) + "---" + self.project_fxf.xf.title
        return u"%s" % str(self.submitted_by) + "---" + self.site_fxf.xf.title

    def instance_json(self):
        return json.dumps(self.instance.json)

    def get_responces(self):
        data=[]
        json_answer = self.instance.json
        json_question = json.loads(self.instance.xform.json)
        base_url = DjangoSite.objects.get_current().domain
        media_folder = self.instance.xform.user.username
        def parse_repeat(r_object):
            r_question = r_object['name']
            
            if r_question in json_answer:
                for gnr_answer in json_answer[r_question]:
                    for first_children in r_object['children']:
                        question_type = first_children['type']
                        question = first_children['name']
                        group_answer = json_answer[r_question]
                        answer = ''
                        if r_question+"/"+question in gnr_answer:
                            if first_children['type'] == 'note':
                                answer= ''
                            elif first_children['type'] == 'photo' or first_children['type'] == 'audio' or first_children['type'] == 'video':
                                answer = 'http://'+base_url+'/attachment/medium?media_file=/'+ media_folder +'attachments/'+gnr_answer[r_question+"/"+question]
                            else:
                                answer = gnr_answer[r_question+"/"+question]
                                
                        if 'label' in first_children:
                            question = first_children['label']
                        row={'type':question_type, 'question':question, 'answer':answer}
                        data.append(row)
            else:
                for first_children in r_object['children']:
                        question_type = first_children['type']
                        question = first_children['name']
                        answer = ''
                        if 'label' in first_children:
                            question = first_children['label']
                        row={'type':question_type, 'question':question, 'answer':answer}
                        data.append(row)


        def parse_group(prev_groupname, g_object):
            g_question = prev_groupname+g_object['name']
            for first_children in g_object['children']:
                question = first_children['name']
                question_type = first_children['type']
                if question_type == 'group':
                    parse_group(g_question+"/",first_children)
                    continue
                answer = ''
                if g_question+"/"+question in json_answer:
                    if question_type == 'note':
                        answer= '' 
                    elif question_type == 'photo' or question_type == 'audio' or question_type == 'video':
                        answer = 'http://'+base_url+'/attachment/medium?media_file=/'+ media_folder +'attachments/'+json_answer[g_question+"/"+question]
                    else:
                        answer = json_answer[g_question+"/"+question]

                if 'label' in first_children:
                    question = first_children['label']
                row={'type':question_type, 'question':question, 'answer':answer}
                data.append(row)
                

        def parse_individual_questions(parent_object):
            for first_children in parent_object:
                if first_children['type'] == "repeat":
                    parse_repeat(first_children)
                elif first_children['type'] == 'group':
                    parse_group("",first_children)
                else:
                    question = first_children['name']
                    question_type = first_children['type']
                    answer= ''
                    if question in json_answer:
                        if first_children['type'] == 'note':
                            answer= '' 
                        elif first_children['type'] == 'photo' or first_children['type'] == 'audio' or first_children['type'] == 'video':
                            answer = 'http://'+base_url+'/attachment/medium?media_file=/'+ media_folder +'attachments/'+json_answer[question]
                        else:
                            answer = json_answer[question]
                    if 'label' in first_children:
                        question = first_children['label']
                    row={"type":question_type, "question":question, "answer":answer}
                    data.append(row)

            submitted_by={'type':'submitted_by','question':'Submitted by', 'answer':json_answer['_submitted_by']}
            submittion_time={'type':'submittion_time','question':'Submittion Time', 'answer':json_answer['_submission_time']}
            data.append(submitted_by)
            data.append(submittion_time)
        parse_individual_questions(json_question['children'])
        return data


@receiver(post_save, sender=FInstance)
def submission_saved(sender, instance, created,  **kwargs):
    if instance.project_fxf is not None and instance.site is not None and instance.form_status == 3:
        instance.site.current_status = instance.form_status
        instance.site.save()
        from onadata.apps.fsforms.tasks import update_progress
        update_progress.delay(instance.site_id, instance.project_fxf_id, instance.instance.json)

    elif instance.site is not None:
        instance.site.current_status = instance.form_status
        instance.site.save()



class EditedSubmission(models.Model):
    old = models.ForeignKey(FInstance, related_name="edits")
    json = JSONField(default={}, null=False)
    date = models.DateTimeField(auto_now=True, null=True, blank=True)
    user = models.ForeignKey(User)
    status = models.BooleanField(default=False)


class InstanceStatusChanged(models.Model):
    finstance = models.ForeignKey(FInstance, related_name="comments")
    message = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now=True)
    old_status = models.IntegerField(default=0, choices=FORM_STATUS)
    new_status = models.IntegerField(default=0, choices=FORM_STATUS)
    user = models.ForeignKey(User, related_name="submission_comments")
    logs = GenericRelation('eventlog.FieldSightLog')

    class Meta:
        ordering = ['-date']

    def get_absolute_url(self):
        return reverse('forms:alter-status-detail', kwargs={'pk': self.pk})

    def getname(self):
        return u'{0} form {1}'.format(self.finstance.site_fxf.form_type(),
                                      self.finstance.site_fxf.xf.title)

    def new_status_display(self):
        return dict(FORM_STATUS)[self.new_status]


class InstanceImages(models.Model):
    instance_status = models.ForeignKey(InstanceStatusChanged,
                                        related_name="images")
    image = models.ImageField(upload_to="submission-feedback-images",
                              verbose_name='Status Changed Images',)



class FieldSightFormLibrary(models.Model):
    xf = models.ForeignKey(XForm)
    is_global = models.BooleanField(default=False)
    shared_date = models.DateTimeField(auto_now=True)
    organization = models.ForeignKey(Organization, null=True, blank=True)
    project = models.ForeignKey(Project, null=True, blank=True)
    logs = GenericRelation('eventlog.FieldSightLog')

    class Meta:
        verbose_name = _("Library")
        verbose_name_plural = _("Library")
        ordering = ("-shared_date",)


class EducationMaterial(models.Model):
    is_pdf = models.BooleanField(default=False)
    pdf = models.FileField(upload_to="education-material-pdf",
                           null=True, blank=True)
    title = models.CharField(max_length=31, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    stage = models.OneToOneField(Stage, related_name="em",
                                 null=True, blank=True)
    fsxf = models.OneToOneField(FieldSightXF, related_name="em",
                                null=True, blank=True)


class EducationalImages(models.Model):
    educational_material = models.ForeignKey(EducationMaterial,
                                             related_name="em_images")
    image = models.ImageField(upload_to="education-material-images",
                              verbose_name='Education Images',)


class DeployEvent(models.Model):
    form_changed = models.BooleanField(default=True)
    data = JSONField(default={})
    date = models.DateTimeField(auto_now=True)
    site = models.ForeignKey(Site, related_name="deploy_data", null=True)
    project = models.ForeignKey(Project, related_name="deploy_data", null=True)


def upload_to(instance, filename):
    return os.path.join(
        'versions', str(instance.pk),
        'xls',
        os.path.split(filename)[1])


class XformHistory(models.Model):
    class Meta:
        unique_together = ('xform', 'version')
        
    def _set_uuid_in_xml(self, file_name=None):
        """
        Add bind to automatically set UUID node in XML.
        """
        if not file_name:
            file_name = self.file_name()
        file_name, file_ext = os.path.splitext(file_name)

        doc = clean_and_parse_xml(self.xml)
        model_nodes = doc.getElementsByTagName("model")
        if len(model_nodes) != 1:
            raise Exception(u"xml contains multiple model nodes")

        model_node = model_nodes[0]
        instance_nodes = [node for node in model_node.childNodes if
                          node.nodeType == Node.ELEMENT_NODE and
                          node.tagName.lower() == "instance" and
                          not node.hasAttribute("id")]

        if len(instance_nodes) != 1:
            raise Exception(u"Multiple instance nodes without the id "
                            u"attribute, can't tell which is the main one")

        instance_node = instance_nodes[0]

        # get the first child whose id attribute matches our id_string
        survey_nodes = [node for node in instance_node.childNodes
                        if node.nodeType == Node.ELEMENT_NODE and
                        (node.tagName == file_name or
                         node.attributes.get('id'))]

        if len(survey_nodes) != 1:
            raise Exception(
                u"Multiple survey nodes with the id '%s'" % self.id_string)

        survey_node = survey_nodes[0]
        formhub_nodes = [n for n in survey_node.childNodes
                         if n.nodeType == Node.ELEMENT_NODE and
                         n.tagName == "formhub"]

        if len(formhub_nodes) > 1:
            raise Exception(
                u"Multiple formhub nodes within main instance node")
        elif len(formhub_nodes) == 1:
            formhub_node = formhub_nodes[0]
        else:
            formhub_node = survey_node.insertBefore(
                doc.createElement("formhub"), survey_node.firstChild)

        uuid_nodes = [node for node in formhub_node.childNodes if
                      node.nodeType == Node.ELEMENT_NODE and
                      node.tagName == "uuid"]

        if len(uuid_nodes) == 0:
            formhub_node.appendChild(doc.createElement("uuid"))
        if len(formhub_nodes) == 0:
            # append the calculate bind node
            calculate_node = doc.createElement("bind")
            calculate_node.setAttribute(
                "nodeset", "/%s/formhub/uuid" % file_name)
            calculate_node.setAttribute("type", "string")
            calculate_node.setAttribute("calculate", "'%s'" % self.uuid)
            model_node.appendChild(calculate_node)

        self.xml = doc.toprettyxml(indent="  ", encoding='utf-8')
        
        # hack
        # http://ronrothman.com/public/leftbraned/xml-dom-minidom-toprettyxml-\
        # and-silly-whitespace/
        text_re = re.compile('>\n\s+([^<>\s].*?)\n\s+</', re.DOTALL)
        output_re = re.compile('\n.*(<output.*>)\n(  )*')
        prettyXml = text_re.sub('>\g<1></', self.xml.decode('utf-8'))
        inlineOutput = output_re.sub('\g<1>', prettyXml)
        inlineOutput = re.compile('<label>\s*\n*\s*\n*\s*</label>').sub(
            '<label></label>', inlineOutput)
        self.xml = inlineOutput

    xform = models.ForeignKey(XForm, related_name="fshistory")
    date = models.DateTimeField(auto_now=True)
    xls = models.FileField(upload_to=upload_to, null=True)
    json = models.TextField(default=u'')
    description = models.TextField(default=u'', null=True)
    xml = models.TextField()
    id_string = models.CharField(editable=False, max_length=255)
    title = models.CharField(editable=False, max_length=255)
    uuid = models.CharField(max_length=32, default=u'')
    version = models.CharField(max_length=255, default=u'')

    @property
    def get_version(self):
        import re
        n = XML_VERSION_MAX_ITER
        xml = self.xml
        p = re.compile('version="(.*)">')
        m = p.search(xml)
        if m:
            return m.group(1)
        
        version = check_version(xml, n)
        
        if version:
            return version
        
        else:
            p = re.compile("""<bind calculate="\'(.*)\'" nodeset="/(.*)/_version_" """)
            m = p.search(xml)
            if m:
                return m.group(1)
            
            p1 = re.compile("""<bind calculate="(.*)" nodeset="/(.*)/_version_" """)
            m1 = p1.search(xml)
            if m1:
                return m1.group(1)
            
            p1 = re.compile("""<bind calculate="\'(.*)\'" nodeset="/(.*)/__version__" """)
            m1 = p1.search(xml)
            if m1:
                return m1.group(1)
            
            p1 = re.compile("""<bind calculate="(.*)" nodeset="/(.*)/__version__" """)
            m1 = p1.search(xml)
            if m1:
                return m1.group(1)
        return None

    def save(self, *args, **kwargs):
        if self.xls and not self.xml:
            survey = create_survey_from_xls(self.xls)
            self.json = survey.to_json()
            self.xml = survey.to_xml()
            self._mark_start_time_boolean()
            # set_uuid(self)
            # self._set_uuid_in_xml()
        if not self.version:
            self.version = self.get_version
        super(XformHistory, self).save(*args, **kwargs)

    def file_name(self):
        return os.path.split(self.xls.name)[-1]

    def _mark_start_time_boolean(self):
        starttime_substring = 'jr:preloadParams="start"'
        if self.xml.find(starttime_substring) != -1:
            self.has_start_time = True
        else:
            self.has_start_time = False

    def get_survey(self):
        if not hasattr(self, "_survey"):
            try:
                builder = SurveyElementBuilder()
                self._survey = \
                    builder.create_survey_element_from_json(self.json)
            except ValueError:
                xml = bytes(bytearray(self.xml, encoding='utf-8'))
                self._survey = create_survey_element_from_xml(xml)
        return self._survey

    survey = property(get_survey)


class SubmissionOfflineSite(models.Model):
    offline_site_id = models.CharField(max_length=20)
    temporary_site = models.ForeignKey(Site, related_name="offline_submissions")
    instance = models.OneToOneField(FInstance, blank=True,
                                    null=True,
                                    related_name="offline_submission")
    fieldsight_form = models.ForeignKey(FieldSightXF,
                                        related_name="offline_submissiob",
                                        null=True, blank=True)

    def __unicode__(self):
        if self.instance:
            return u"%s ---------------%s" % (str(self.instance.id) ,self.offline_site_id)
        return u"%s" % str(self.offline_site_id)


UUID_LENGTH = 21


class KpiUidField(models.CharField):
    ''' If empty, automatically populates itself with a UID before saving '''
    def __init__(self, uid_prefix):
        self.uid_prefix = uid_prefix
        total_length = len(uid_prefix) + UUID_LENGTH
        super(KpiUidField, self).__init__(max_length=total_length, unique=True)

    def deconstruct(self):
        name, path, args, kwargs = super(KpiUidField, self).deconstruct()
        kwargs['uid_prefix'] = self.uid_prefix
        del kwargs['max_length']
        del kwargs['unique']
        return name, path, args, kwargs

    def generate_uid(self):
        return self.uid_prefix + ShortUUID().random(UUID_LENGTH)
        # When UID_LENGTH is 22, that should be changed to:
        # return self.uid_prefix + shortuuid.uuid()

    def pre_save(self, model_instance, add):
        value = getattr(model_instance, self.attname)
        if value == '':
            value = self.generate_uid()
            setattr(model_instance, self.attname, value)
        return value


# A kpi permission class that defines the permissions of an user in a form.
# Used to replicate the sharing behaviour of kpi forms in fieldsight.
# Make sure the content type matches that of the model asset of app kpi(for asset permissions).
# object_id is the object_od of asset(for asset permissions).
# if the asset is shared by an user then: inherited=False, deny=False
class ObjectPermission(models.Model):
    ''' An application of an auth.Permission instance to a specific
    content_object. Call ObjectPermission.objects.get_for_object() or
    filter_for_object() to run queries using the content_object field. '''
    user = models.ForeignKey('auth.User')
    permission = models.ForeignKey('auth.Permission')
    deny = models.BooleanField(
        default=False,
        help_text='Blocks inheritance of this permission when set to True'
    )
    inherited = models.BooleanField(default=False)
    object_id = models.PositiveIntegerField()
    # We can't do something like GenericForeignKey('permission__content_type'),
    # so duplicate the content_type field here.
    content_type = models.ForeignKey(ContentType)
    content_object = GenericForeignKey('content_type', 'object_id')
    uid = KpiUidField(uid_prefix='p')

    @property
    def kind(self):
        return 'objectpermission'

    class Meta:
        db_table = 'kpi_objectpermission'
        managed = False

    def save(self, *args, **kwargs):
        if self.permission.content_type_id is not self.content_type_id:
            raise ValidationError('The content type of the permission does '
                'not match that of the object.')
        super(ObjectPermission, self).save(*args, **kwargs)

    def __unicode__(self):
        for required_field in ('user', 'permission'):
            if not hasattr(self, required_field):
                return u'incomplete ObjectPermission'
        return u'{}{} {} {}'.format(
            'inherited ' if self.inherited else '',
            unicode(self.permission.codename),
            'denied from' if self.deny else 'granted to',
            unicode(self.user)
        )


# A replicated class of the kpi asset.
# Asset uid = xform id_string
class Asset(models.Model):
    uid = KpiUidField(uid_prefix='a')
    owner = models.ForeignKey('auth.User', related_name='assets', null=True)
    content = JSONField(null=True)

    class Meta:
        db_table = 'kpi_asset'
        managed = False


# Store the shared status of forms if the forms are shared globally
class SharedFieldSightForm(models.Model):
    xf = models.OneToOneField(XForm, null=True)
    shared = models.BooleanField(default=False)

    def get_shareable_link(self):
        return settings.KPI_URL + '#/forms/' + self.xf.id_string


class ReportSyncManager(models.Manager):
    def get_queryset(self):
        return super(ReportSyncManager, self).get_queryset().filter(is_deleted=False)


class ReportSyncSettings(models.Model):
    user = models.ForeignKey(User, related_name='report_sync_settings', on_delete=models.CASCADE, null=True, blank=True)
    project = models.ForeignKey(Project, related_name="report_sync_settings", on_delete=models.CASCADE)
    form = models.ForeignKey(FieldSightXF, related_name="report_sync_settings", on_delete=models.CASCADE,
                             null=True, blank=True)
    report = models.ForeignKey('reporting.ReportSettings', related_name="report_sync_settings", on_delete=models.CASCADE,
                               null=True, blank=True)
    schedule_type = models.CharField(choices=SCHEDULED_TYPE, default=0, max_length=50)
    day = models.IntegerField(null=True, blank=True)
    spreadsheet_id = models.CharField(max_length=250, null=True, blank=True)
    grid_id = models.IntegerField(null=True, blank=True)
    range = models.CharField(max_length=250, null=True, blank=True)
    report_type = models.CharField(choices=REPORT_TYPE, default='site_info', max_length=50)
    description = models.TextField(null=True, blank=True)
    last_synced_date = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    objects = ReportSyncManager()


