from __future__ import unicode_literals

import datetime

import json
from django.conf import settings
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status

from onadata.apps.api.viewsets.xform_submission_api import XFormSubmissionApi
from onadata.apps.eventlog.models import FieldSightLog
from onadata.apps.fieldsight.models import Site, SiteMetaAttrAnsHistory
from onadata.apps.fsforms.models import FieldSightXF, Stage, Schedule, SubmissionOfflineSite, FInstance, \
    EditedSubmission
from onadata.apps.fsforms.serializers.FieldSightSubmissionSerializer import FieldSightSubmissionSerializer
from ..fieldsight_logger_tools import safe_create_instance
from channels import Group as ChannelGroup
from onadata.apps.eventlog.models import CeleryTaskProgress
# 10,000,000 bytes
DEFAULT_CONTENT_LENGTH = getattr(settings, 'DEFAULT_CONTENT_LENGTH', 10000000)


def create_instance_from_xml(request, fsid, site, fs_proj_xf, proj_id, xform, flagged_instance):
    xml_file_list = request.FILES.pop('xml_submission_file', [])
    xml_file = xml_file_list[0] if len(xml_file_list) else None
    media_files = request.FILES.values()
    return safe_create_instance(fsid, xml_file, media_files, None, request, site, fs_proj_xf, proj_id, xform, flagged_instance)


class FSXFormSubmissionApi(XFormSubmissionApi):
    """
    Submit xml submissions with attachments.

    Where:

    - `pk` - fieldsight form id. A fieldsight form can be of Project level or Site Level
    - `site_id` - Site id from which form is submitted. for Project survey forms site_id is 0

    """
    serializer_class = FieldSightSubmissionSerializer
    template_name = 'fsforms/submission.xml'

    def create(self, request, *args, **kwargs):
        if self.request.user.is_anonymous():
            self.permission_denied(self.request)

        fsxfid = kwargs.get('pk', None)
        siteid = kwargs.get('site_id', None)
        if fsxfid is None or siteid is None:
            return self.error_response("Site Id Or Form ID Not Given", False, request)
        try:
            fsxfid = int(fsxfid)
            fxf = get_object_or_404(FieldSightXF, pk=kwargs.get('pk'))
            if fxf.project:
                # A form assigned from project
                if siteid == '0':
                    siteid = None
                elif Site.objects.filter(pk=siteid).exists() == False:
                    return self.error_response("siteid Invalid", False, request)
                if fsxfid is None:
                    return self.error_response("Fieldsight Form ID Not Given", False, request)
                try:
                    fs_proj_xf = fxf
                    xform = fs_proj_xf.xf
                    proj_id = fs_proj_xf.project.id
                except Exception as e:
                    return self.error_response(str(e), False, request)
                if request.method.upper() == 'HEAD':
                    return Response(status=status.HTTP_204_NO_CONTENT,
                                    headers=self.get_openrosa_headers(request),
                                    template_name=self.template_name)
                params = self.request.query_params
                flagged_instance = params.get("instance")

                error, instance = create_instance_from_xml(request, None, siteid, fs_proj_xf.id, proj_id, xform, flagged_instance)

                if error or not instance:
                    return self.error_response(error, False, request)

                fi = instance.fieldsight_instance
                fi_id = fi.id
                last_edited_date = EditedSubmission.objects.filter(
                    old__id=fi_id).last().date if EditedSubmission.objects.filter(old__id=fi_id).last() else None
                last_instance_log = FieldSightLog.objects.filter(
                    object_id=fi_id, type=16).first().date if FieldSightLog.objects.filter(object_id=fi_id, type=16).first() else None
                delta = 101  # make sure the submission is new not installment of attachment of previous submission
                if last_instance_log and last_edited_date:
                    delta = (EditedSubmission.objects.filter(old__id=fi_id).last().date - FieldSightLog.objects.filter(
                        object_id=fi_id, type=16).first().date).total_seconds()
                if (not FieldSightLog.objects.filter(object_id=fi_id, type=16).exists()) or (
                        flagged_instance and delta > 100):
                    if flagged_instance:
                        fi.form_status = None
                        fi.save()
                    if fs_proj_xf.is_survey:
                        instance.fieldsight_instance.logs.create(source=self.request.user, type=16,
                                                                 title="new Project level Submission",
                                                                 organization=fs_proj_xf.project.organization,
                                                                 project=fs_proj_xf.project,
                                                                 extra_object=fs_proj_xf.project,
                                                                 extra_message="project",
                                                                 content_object=instance.fieldsight_instance)
                    else:
                        task_obj = CeleryTaskProgress.objects.create(user=self.request.user,
                                                                     description='Change site info',
                                                                     task_type=25,
                                                                     content_object=instance.fieldsight_instance)
                        if task_obj:
                            from onadata.apps.fieldsight.tasks import update_meta_details
                            update_meta_details.apply_async((fs_proj_xf.id, instance.id, task_obj.id, siteid), countdown=1)
                        site = Site.objects.get(pk=siteid)
                        instance.fieldsight_instance.logs.create(source=self.request.user, type=16,
                                                                 title="new Site level Submission",
                                                                 organization=fs_proj_xf.project.organization,
                                                                 project=fs_proj_xf.project, site=site,
                                                                 extra_object=site,
                                                                 content_object=instance.fieldsight_instance)

                context = self.get_serializer_context()
                serializer = FieldSightSubmissionSerializer(instance, context=context)
                return Response(serializer.data,
                                headers=self.get_openrosa_headers(request),
                                status=status.HTTP_201_CREATED,
                                template_name=self.template_name)

            #  Site level forms assigned in particular site.
            fs_proj_xf = fxf.fsform.pk if fxf.fsform else None
            proj_id = fxf.fsform.project.pk if fxf.fsform else fxf.site.project.pk
            xform = fxf.xf
        except:
            return self.error_response("Site Id Or Form ID Not Vaild", False, request)
        if request.method.upper() == 'HEAD':
            return Response(status=status.HTTP_204_NO_CONTENT,
                            headers=self.get_openrosa_headers(request),
                            template_name=self.template_name)

        params = self.request.query_params
        flagged_instance = params.get("instance")
        error, instance = create_instance_from_xml(request, fsxfid, siteid, fs_proj_xf, proj_id, xform, flagged_instance)
        extra_message = ""

        if error or not instance:
            return self.error_response(error, False, request)

        if fxf.is_survey:
            extra_message = "project"
        fi = instance.fieldsight_instance
        fi_id = fi.id
        last_edited_date = EditedSubmission.objects.filter(
            old__id=fi_id).last().date if EditedSubmission.objects.filter(old__id=fi_id).last() else None
        last_instance_log = FieldSightLog.objects.filter(object_id=fi_id, type=16).first().date if FieldSightLog.objects.filter(
            object_id=fi_id, type=16).first() else None
        delta = 101
        if last_instance_log and last_edited_date:
            delta = (EditedSubmission.objects.filter(old__id=fi_id).last().date - FieldSightLog.objects.filter(
                object_id=fi_id, type=16).first().date).total_seconds()
        if (not FieldSightLog.objects.filter(object_id=fi_id, type=16).exists()) or (flagged_instance and delta > 100):
            instance.fieldsight_instance.logs.create(
                source=self.request.user, type=16, title="new Submission",
                organization=instance.fieldsight_instance.site.project.organization,
                project=instance.fieldsight_instance.site.project,
                site=instance.fieldsight_instance.site,
                extra_message=extra_message,
                extra_object=instance.fieldsight_instance.site,
                content_object=instance.fieldsight_instance)

            if flagged_instance:
                fi.form_status = None
                fi.save()
        context = self.get_serializer_context()
        serializer = FieldSightSubmissionSerializer(instance, context=context)
        return Response(serializer.data,
                        headers=self.get_openrosa_headers(request),
                        status=status.HTTP_201_CREATED,
                        template_name=self.template_name)


class ProjectFSXFormSubmissionApi(XFormSubmissionApi):
    serializer_class = FieldSightSubmissionSerializer
    template_name = 'fsforms/submission.xml'

    def create(self, request, *args, **kwargs):
        if self.request.user.is_anonymous():
            self.permission_denied(self.request)

        fsxfid = kwargs.get('pk', None)
        siteid = kwargs.get('site_id', None)
        if siteid == '0':
            siteid = None
        elif Site.objects.filter(pk=siteid).exists() == False:
            return self.error_response("siteid Invalid", False, request)
        if fsxfid is None:
            return self.error_response("Fieldsight Form ID Not Given", False, request)
        try:
            fs_proj_xf = get_object_or_404(FieldSightXF, pk=kwargs.get('pk'))
            xform = fs_proj_xf.xf
            proj_id = fs_proj_xf.project.id
            if siteid:
                site = Site.objects.get(pk=siteid)
        except Exception as e:
            return self.error_response("Site Id Or Project Form ID Not Vaild", False, request)
        if request.method.upper() == 'HEAD':
            return Response(status=status.HTTP_204_NO_CONTENT,
                            headers=self.get_openrosa_headers(request),
                            template_name=self.template_name)

        params = self.request.query_params
        flagged_instance = params.get("instance")
        error, instance = create_instance_from_xml(request, None, siteid, fs_proj_xf.id, proj_id, xform, flagged_instance)
        if error or not instance:
            return self.error_response(error, False, request)

        fi = instance.fieldsight_instance
        fi_id = fi.id
        last_edited_date = EditedSubmission.objects.filter(old__id=fi_id).last().date if EditedSubmission.objects.filter(old__id=fi_id).last() else None
        last_instance_log = FieldSightLog.objects.filter(object_id=fi_id, type=16).first().date if FieldSightLog.objects.filter(object_id=fi_id, type=16).first() else None
        delta = 101
        if last_instance_log and last_edited_date:
            delta = (EditedSubmission.objects.filter(old__id=fi_id).last().date - FieldSightLog.objects.filter(object_id=fi_id, type=16).first().date).total_seconds()
        if (not FieldSightLog.objects.filter(object_id=fi_id, type=16).exists()) or (flagged_instance and delta > 100):
            # Submission data not only attachments.

            if flagged_instance:
                fi.form_status = None
                fi.save()
            if fs_proj_xf.is_survey:
                instance.fieldsight_instance.logs.create(source=self.request.user, type=16, title="new Project level Submission",
                                           organization=fs_proj_xf.project.organization,
                                           project=fs_proj_xf.project,
                                                            extra_object=fs_proj_xf.project,
                                                            extra_message="project",
                                                            content_object=fi)
            else:
                task_obj = CeleryTaskProgress.objects.create(user=self.request.user,
                                                             description='Change site info',
                                                             task_type=25,
                                                             content_object=instance.fieldsight_instance)
                if task_obj:
                    from onadata.apps.fieldsight.tasks import update_meta_details
                    update_meta_details.apply_async((fs_proj_xf.id, instance.id, task_obj.id, siteid), countdown=1)
                site = Site.objects.get(pk=siteid)
                instance.fieldsight_instance.logs.create(source=self.request.user, type=16, title="new Site level Submission",
                                           organization=fs_proj_xf.project.organization,
                                           project=fs_proj_xf.project, site=site,
                                                            extra_object=site,
                                                            content_object=fi)

        context = self.get_serializer_context()
        serializer = FieldSightSubmissionSerializer(instance, context=context)
        return Response(serializer.data,
                        headers=self.get_openrosa_headers(request),
                        status=status.HTTP_201_CREATED,
                        template_name=self.template_name)

