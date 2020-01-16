from __future__ import unicode_literals
import json
from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from jsonfield import JSONField

from onadata.apps.fieldsight.models import Organization, Project, Site, SuperOrganization
from onadata.apps.users.models import UserProfile

from celery.result import AsyncResult
from django.contrib.contenttypes.fields import GenericRelation


class FieldSightLog(models.Model):
    ACTION_TYPES = (
        (1, 'User was added as the Team Admin of Organization Name by Invitor Full Name.'),
        (2, 'User was added as the Project Manager of Project Name by Invitor Full Name.'),
        (3, 'User was added as Reviewer of Site Name by Invitor Full Name.'),
        (4, 'User was added as Site Supervisor of Site Name by Invitor Full Name.'),
        (5, 'User was assigned as an Team Admin in Organization Name.'),
        (6, 'User was assigned as a Project Manager in Project Name.'),
        (7, 'User was assigned as a Reviewer in Site Name.'),
        (8, 'User was assigned as a Site Supervisor in Site Name.'),
        (9, 'User created a new Team named Organization Name'),
        (10, 'User created a new project named Project Name.'),
        (11, 'User created a new site named Site Name in Project Name.'),
        (110, 'User created a new Sub site named Site Name in Site Name.'),
        (12, 'User created number + sites in Project Name.'),
        (13, 'User changed the details of Organization Name.'),
        (14, 'User changed the details of Project Name.'),
        (15, 'User changed the details of Site Name.'),
        (16, 'User submitted a response for Form Type Form Name in Site Name.'),
        (17, 'User reviewed a response for Form Type Form Name in Site Name.'),
        (18, 'User assigned a new Form Type Form Name in Project Name.'),
        (19, 'User assigned a new Form Type Form Name to Site Name.'),
        (20, 'User edited Form Name form.'),
        (21, 'User assign successful in Team.'),
        (22, 'User assign sucessfull in project.'),
        (23, 'Users were already assigned.'),
        (24, 'User was added as unassigned.'),
        (25, 'User was added as partner in project.'),
        (26, 'User was added as the Project Manager in count project of org by Invitor Full Name.'),
        (27, 'User was added as Reviewer in count site of project by Invitor Full Name.'),
        (28, 'User was added as Site Supervisor in count site of project by Invitor Full Name.'),
        (29, 'Project SIte Import From Project Name Completed SuccessFully'),
        (30, 'Project SIte Import From number of region in Project Name Completed SuccessFully'),
        (31, 'User edited a response for Form Type Form Name in Site Name.'),
        (32, 'Report generated sucessfull.'),
        (33, 'Response Delete sucessfull.'),
        (34, 'Delete form sucessful.'),
        (341, 'Delete stages sucessful.'),
        (343, 'Delete substages sucessful.'),
        (342, 'Delete stage sucessful.'),
        (35, 'Remove roles.'),
        (36, 'Delete project/site/org/ .. etc.'),
        (37, 'User was added as Region Reviewer of Region Name by Invitor Full Name.'),
        (38, 'User was added as Region Supervisor of Region Name by Invitor Full Name.'),
        (39, 'User was added as Region Reviewer in count regions of project by Invitor Full Name.'),
        (40, 'User was added as Region Supervisor in count regions of project by Invitor Full Name.'),
        (41, 'User was added as the Super Organization Admin of Organization Name by Invitor Full Name.'),
        (412, 'Bulk upload of number + sites in Project Name failed.'),
        (421, 'User assign unsuccessful in Team.'),
        (422, 'User assign unsucessfull in project.'),
        (429, 'Project SIte Import From Project Name Completed SuccessFully'),
        (430, 'Project SIte Import From number of region in Project Name Completed SuccessFully'),
        (432, 'Report generation failed.'),
    )
    
    type = models.IntegerField(default=0, choices=ACTION_TYPES)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)
    seen_by = models.ManyToManyField(User)
    source = models.ForeignKey(User, related_name='log', null=True)
    super_organization = models.ForeignKey(SuperOrganization, related_name="logs", null=True, blank=True)
    organization = models.ForeignKey(Organization, related_name="logs", null=True)
    project = models.ForeignKey(Project, related_name="logs", null=True)
    site = models.ForeignKey(Site, related_name="logs", null=True)
    extra_message = models.TextField(blank=True, null=True)
    extra_json = JSONField(blank=True, null=True, default=None)
    
    recipient = models.ForeignKey(User, related_name='recipent_log', null=True)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    event_name = models.CharField(max_length=255, blank=True)
    event_url = models.CharField(max_length=500, blank=True)

    extra_content_type = models.ForeignKey(ContentType, related_name='notify_object', blank=True, null=True)
    extra_object_id = models.CharField(max_length=255, blank=True, null=True)
    extra_object = GenericForeignKey('extra_content_type', 'extra_object_id')
    extra_obj_name = models.CharField(max_length=255, blank=True)    
    extra_obj_url = models.CharField(max_length=500, blank=True)

    class Meta:
        get_latest_by = "-date"
        ordering = ["-date"]

    def get_absolute_url(self):
        return reverse('eventlog:notification-detail', kwargs={'pk': self.pk})

    def get_event_url(self):
        try:
            return self.content_object.get_absolute_url()
        except:
            return None

    def get_event_name(self):
        try:
            return self.content_object.getname()
        except:
            return None
            
    def get_extraobj_url(self):
        if self.extra_object is None:
            return None

        if self.extra_content_type.model == "user":
            if self.extra_object.user_profile:
                return self.extra_object.user_profile.get_absolute_url()
            return "#"
        return self.extra_object.get_absolute_url()

    def get_extraobj_name(self):
        if self.extra_object is None:
            return None
        if self.extra_content_type.model == "user":
            if self.extra_object.user_profile:
                return self.extra_object.user_profile.getname()
            return self.extra_object.email
        return self.extra_object.getname()

    def get_source_url(self):
        try:
            profile = self.source.user_profile
        except UserProfile.DoesNotExist:
            return None
        else:
            return profile.get_absolute_url()

    def get_source_name(self):
        return self.source.first_name + ' ' + self.source.last_name

    def get_org_url(self):
        if self.organization is None:
            return None
        return self.organization.get_absolute_url()

    def get_project_url(self):
        if self.project is None:
            return None
        return self.project.get_absolute_url()

    def get_site_url(self):
        if self.site is None:
            return None
        return self.site.get_absolute_url()

    def get_extra_json_string(self):
        return json.dumps(self.extra_json)

    def __str__(self):
        return str(self.get_type_display())

    def save(self, *args, **kwargs):
        self.event_name = self.get_event_name()
        self.event_url = self.get_event_url()
        if self.extra_object:
            self.extra_obj_name = self.get_extraobj_name()
            self.extra_obj_url = self.get_extraobj_url()

        super(FieldSightLog, self).save(*args, **kwargs)  # Call the "real" save() method.


class FieldSightMessage(models.Model):
    sender = models.ForeignKey(User, related_name="sender")
    receiver = models.ForeignKey(User, related_name="receiver")
    msg_content = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)

    class Meta:
        ordering = ["-date"]

    @classmethod
    def inbox(cls, user):
        return FieldSightMessage.objects.filter(receiver=user, is_seen=False)

    @classmethod
    def outbox(cls, user):
        return FieldSightMessage.objects.filter(sender=user)

    @classmethod
    def user_messages(cls, user):
        return FieldSightMessage.objects.filter(Q(sender=user) | Q(receiver=user))


class CeleryTaskProgress(models.Model):
    Task_Status = (
        (0, 'Pending'),
        (1, 'In Progress'),
        (2, 'Completed'),
        (3, 'Failed'),
        )
    Task_Type = (
        (0, 'Bulk Site Update'),
        (1, 'User Assign to Project'),
        (2, 'User Assign to Site'),
        (3, 'Site Response Xls Report'),
        (4, 'Site Import'),
        (6, 'Zip Site Images'),
        (7, 'Remove Roles'),
        (8, 'Site Data Export'),
        (9, 'Response Pdf Report'),
        (10, 'Site Progress Xls Report'),
        (11, 'Project Statstics Report'),
        (12, 'Log Report'),
        (13, 'User Assign to Region'),
        (14, 'User Assign to an entire project'),
        (15, 'Auto Clone and Deploy General Form'),
        (16, 'User Activity Xls Report'),
        (17, 'Share XForm'),
        (18, 'Share XForm to Created Manager'),
        (19, 'Share XForm to Individuals'),
        (20, 'Share XForm to Project Managers and Admin of Project'),
        (21, 'Share XForm to team'),
        (22, 'Clone Form'),
        (22, 'Update Sites Progress'),
        (23, 'Update Site Progress'),
        (24, 'Update and Create History of Site Meta-attributes Answers'),
        (25, 'Update Site Information on Submission'),
        (26, 'Export Report in excel'),
        (27, 'Add default forms in Projects'),

    )
    task_id = models.CharField(max_length=255, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updateded = models.DateTimeField(auto_now=True, blank=True, null=True)
    user = models.ForeignKey(User, related_name="task_owner")
    file = models.FileField(
        upload_to="celeryFiles", max_length=755, blank=True, null=True)
    status = models.IntegerField(default=0, choices=Task_Status)
    description = models.CharField(max_length=755, blank=True)
    task_type = models.IntegerField(default=0, choices=Task_Type)
    content_type = models.ForeignKey(ContentType, related_name='task_object', blank=True, null=True)
    object_id = models.IntegerField(blank=True, null=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    logs = GenericRelation('eventlog.FieldSightLog')
    other_fields = JSONField(default={})

    def getname(self):
        return self.file.name
    
    def get_absolute_url(self):
        if self.file:
            return self.file.url
        else:
            return ""
    
    def get_source_url(self):
        try:
            profile = self.user.user_profile
        except UserProfile.DoesNotExist:
            return None
        else:
            return profile.get_absolute_url()

    def get_source_name(self):
        return self.user.first_name + ' ' + self.user.last_name

    def get_event_url(self):
        try:
            return self.content_object.get_absolute_url()
        except:
            return None

    def get_event_name(self):
        try:
            return self.content_object.getname()
        except:
            return None

    def get_progress(self):
        if self.status == 1:
            if self.task_id:
                task = AsyncResult(self.task_id)
                data = task.result or task.state
                return json.dumps(data)
            else:
                return None
        return None

    def __str__(self):
        return str(self.pk) + " (" + str(self.task_type) + ") " + "-->" + str(self.status) +\
               "--->" + str(self.user) + " | Date_last_updated =" +\
               str(self.date_updateded) + " | Added_On ="+str(self.date_added)

