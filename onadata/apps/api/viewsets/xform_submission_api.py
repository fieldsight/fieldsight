import re
import StringIO
import uuid

from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from django.utils.decorators import method_decorator
from django.db import transaction
from django.db.models import Q

from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.authentication import (
    BasicAuthentication,
    TokenAuthentication,
    SessionAuthentication,)
from rest_framework.response import Response
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer

from onadata.apps.eventlog.models import CeleryTaskProgress
from onadata.apps.fsforms.fieldsight_logger_tools import save_submission, save_attachments
from onadata.apps.fsforms.models import FieldSightXF, FInstance
from onadata.apps.logger.models import Instance
from onadata.apps.logger.xform_instance_parser import \
    get_deprecated_uuid_from_xml, get_uuid_from_xml, DuplicateInstance
from onadata.apps.main.models.user_profile import UserProfile
from onadata.apps.viewer.models.parsed_instance import update_mongo_instance
from onadata.libs import filters
from onadata.libs.authentication import DigestAuthentication
from onadata.libs.mixins.openrosa_headers_mixin import OpenRosaHeadersMixin
from onadata.libs.renderers.renderers import TemplateXMLRenderer
from onadata.libs.serializers.data_serializer import SubmissionSerializer
from onadata.libs.utils.logger_tools import dict2xform, safe_create_instance


# 10,000,000 bytes
DEFAULT_CONTENT_LENGTH = getattr(settings, 'DEFAULT_CONTENT_LENGTH', 10000000)
xml_error_re = re.compile('>(.*)<')


def is_json(request):
    return 'application/json' in request.content_type.lower()


def dict_lists2strings(d):
    """Convert lists in a dict to joined strings.

    :param d: The dict to convert.
    :returns: The converted dict."""
    for k, v in d.items():
        if isinstance(v, list) and all([isinstance(e, basestring) for e in v]):
            d[k] = ' '.join(v)
        elif isinstance(v, dict):
            d[k] = dict_lists2strings(v)

    return d


def create_instance_from_xml(username, request):
    xml_file_list = request.FILES.pop('xml_submission_file', [])
    xml_file = xml_file_list[0] if len(xml_file_list) else None

    media_files = request.FILES.values()

    return safe_create_instance(username, xml_file, media_files, None, request)


def create_instance_from_json(username, request):
    request.accepted_renderer = JSONRenderer()
    request.accepted_media_type = JSONRenderer.media_type
    dict_form = request.data
    submission = dict_form.get('submission')

    if submission is None:
        # return an error
        return [_(u"No submission key provided."), None]

    # convert lists in submission dict to joined strings
    submission_joined = dict_lists2strings(submission)
    xml_string = dict2xform(submission_joined, dict_form.get('id'))

    xml_file = StringIO.StringIO(xml_string)

    return safe_create_instance(username, xml_file, [], None, request)


def update_mongo(i):
    """ Update the instance data to mongo database when a existing submission is submitted from enketo

    Args:
        i: Instance object

    Returns: None

    """
    d = i.parsed_instance.to_dict_for_mongo()
    try:
        x = i.fieldsight_instance
        d.update(
            {'fs_project_uuid': str(x.project_fxf_id),
             'fs_project': x.project_id,
             'fs_status': 0,
             'fs_site': x.site_id,
             'fs_organization': None,
             'fs_organization_uuid': None,
             'fs_team': x.project.organization_id,

             })
        if x.project_fxf:
            d['fs_project_uuid'] = str(x.project_fxf_id)
            if x.project_fxf.organization_form_lib:
                d['fs_organization'] = str(x.project_fxf.organization_form_lib.organization_id)
                d['fs_organization_uuid'] = str(x.project_fxf.organization_form_lib_id)

        if x.site_fxf:
            d['fs_uuid'] = str(x.site_fxf_id)

        try:
            synced = update_mongo_instance(d, i.id)
        except Exception as e:
            print(str(e))
    except Exception as e:
        print(str(e))


def update_meta(instance):
    if instance.fieldsight_instance.project_fxf and \
            instance.fieldsight_instance.site:
        task_obj = CeleryTaskProgress.objects.create(user=instance.user,
                                                     description='Change site info',
                                                     task_type=25,
                                                     content_object=instance.fieldsight_instance)
        if task_obj:
            from onadata.apps.fieldsight.tasks import update_meta_details
            update_meta_details.apply_async(
                (instance.fieldsight_instance.project_fxf.id, instance.id,
                 task_obj.id, instance.fieldsight_instance.site.id),
                countdown=1)


def update_default_status(instance):
    fieldsight_instance = instance.fieldsight_instance
    if fieldsight_instance.project_fxf:
        status = fieldsight_instance.project_fxf.default_submission_status
    else:
        status = fieldsight_instance.site_fxf.default_submission_status
    FInstance.objects.filter(
        pk=fieldsight_instance.pk).update(form_status=status)

class XFormSubmissionApi(OpenRosaHeadersMixin,
                         mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
Implements OpenRosa Api [FormSubmissionAPI](\
    https://bitbucket.org/javarosa/javarosa/wiki/FormSubmissionAPI)

## Submit an XML XForm submission

<pre class="prettyprint">
<b>POST</b> /api/v1/submissions</pre>
> Example
>
>       curl -X POST -F xml_submission_file=@/path/to/submission.xml \
https://example.com/api/v1/submissions

## Submit an JSON XForm submission

<pre class="prettyprint">
<b>POST</b> /api/v1/submissions</pre>
> Example
>
>       curl -X POST -d '{"id": "[form ID]", "submission": [the JSON]} \
http://localhost:8000/api/v1/submissions -u user:pass -H "Content-Type: \
application/json"

Here is some example JSON, it would replace `[the JSON]` above:
>       {
>           "transport": {
>               "available_transportation_types_to_referral_facility": \
["ambulance", "bicycle"],
>               "loop_over_transport_types_frequency": {
>                   "ambulance": {
>                       "frequency_to_referral_facility": "daily"
>                   },
>                   "bicycle": {
>                       "frequency_to_referral_facility": "weekly"
>                   },
>                   "boat_canoe": null,
>                   "bus": null,
>                   "donkey_mule_cart": null,
>                   "keke_pepe": null,
>                   "lorry": null,
>                   "motorbike": null,
>                   "taxi": null,
>                   "other": null
>               }
>           }
>           "meta": {
>               "instanceID": "uuid:f3d8dc65-91a6-4d0f-9e97-802128083390"
>           }
>       }
"""
    filter_backends = (filters.AnonDjangoObjectPermissionFilter,)
    model = Instance
    permission_classes = (permissions.AllowAny,)
    renderer_classes = (TemplateXMLRenderer,
                        JSONRenderer,
                        BrowsableAPIRenderer)
    serializer_class = SubmissionSerializer
    template_name = 'submission.xml'

    def __init__(self, *args, **kwargs):
        super(XFormSubmissionApi, self).__init__(*args, **kwargs)
        # Respect DEFAULT_AUTHENTICATION_CLASSES, but also ensure that the
        # previously hard-coded authentication classes are included first.
        # We include BasicAuthentication here to allow submissions using basic
        # authentication over unencrypted HTTP. REST framework stops after the
        # first class that successfully authenticates, so
        # HttpsOnlyBasicAuthentication will be ignored even if included by
        # DEFAULT_AUTHENTICATION_CLASSES.
        authentication_classes = [
            DigestAuthentication,
            BasicAuthentication,
            TokenAuthentication
        ]
        # Do not use `SessionAuthentication`, which implicitly requires CSRF prevention
        # (which in turn requires that the CSRF token be submitted as a cookie and in the
        # body of any "unsafe" requests).
        self.authentication_classes = authentication_classes + [
            auth_class for auth_class in self.authentication_classes
                if not auth_class in authentication_classes and \
                    not issubclass(auth_class, SessionAuthentication)
        ]

    def create(self, request, *args, **kwargs):
        username = self.kwargs.get('username')
        site = self.request.query_params.get('site')
        form = self.request.query_params.get('form')
        dep = self.request.query_params.get('dep', False)
        if request.method.upper() == 'HEAD':
            return Response(status=status.HTTP_204_NO_CONTENT,
                            headers=self.get_openrosa_headers(request),
                            template_name=self.template_name)
        if form and form != "undefined" and not dep:

            return self.create_new_submission(request, site, form)

        elif dep:
            uuid_value = dep.replace("uuid:", "")
            if not Instance.objects.filter(uuid=uuid_value).exists():
                return Response({'error': "Cannot edit this submission"},
                                headers=self.get_openrosa_headers(request),
                                status=status.HTTP_400_BAD_REQUEST)
            is_json_request = is_json(request)
            #
            error, instance = (create_instance_from_json if is_json_request else
                               create_instance_from_xml)(username, request)

            if error or not instance:
                return self.error_response(error, is_json_request, request)
            update_mongo(instance)
            update_meta(instance)
            update_default_status(instance)
            context = self.get_serializer_context()
            serializer = SubmissionSerializer(instance, context=context)

            return Response(serializer.data,
                            headers=self.get_openrosa_headers(request),
                            status=status.HTTP_201_CREATED,
                            template_name=self.template_name)
        else:
            return Response({'error': "submission not implemented"},
                            headers=self.get_openrosa_headers(request),
                            status=status.HTTP_400_BAD_REQUEST)

    def error_response(self, error, is_json_request, request):
        if not error:
            error_msg = _(u"Unable to create submission.")
            status_code = status.HTTP_400_BAD_REQUEST
        elif isinstance(error, basestring):
            error_msg = error
            status_code = status.HTTP_400_BAD_REQUEST
        elif not is_json_request:
            return error
        else:
            error_msg = xml_error_re.search(error.content).groups()[0]
            status_code = error.status_code

        return Response({'error': error_msg},
                        headers=self.get_openrosa_headers(request),
                        status=status_code)

    def create_new_submission(self, request, site, form):
        fs_xf = FieldSightXF.objects.get(pk=form)
        xform = fs_xf.xf
        xml_file_list = self.request.FILES.pop('xml_submission_file', [])
        xml_file = xml_file_list[0] if len(xml_file_list) else None
        xml = xml_file.read()
        username = self.kwargs.get('username')
        user = get_object_or_404(User, username=username)
        media_files = request.FILES.values()
        new_uuid = get_uuid_from_xml(xml)
        site_id = site

        xml_hash = Instance.get_hash(xml)

        if xform.has_start_time:
            # XML matches are identified by identical content hash OR, when a
            # content hash is not present, by string comparison of the full
            # content, which is slow! Use the management command
            # `populate_xml_hashes_for_instances` to hash existing submissions
            existing_instance = Instance.objects.filter(
                Q(xml_hash=xml_hash) |
                Q(xml_hash=Instance.DEFAULT_XML_HASH, xml=xml),
                xform__user=xform.user,
            ).first()
        else:
            existing_instance = None

        if existing_instance:
            # ensure we have saved the extra attachments
            any_new_attachment = save_attachments(existing_instance, media_files)

            if not any_new_attachment:
                raise DuplicateInstance()
            else:
                context = self.get_serializer_context()
                serializer = SubmissionSerializer(existing_instance, context=context)
                return Response(serializer.data,
                                headers=self.get_openrosa_headers(request),
                                status=status.HTTP_201_CREATED,
                                template_name=self.template_name)
        with transaction.atomic():
            if fs_xf.is_survey:
                instance = save_submission(
                    xform=xform,
                    xml=xml,
                    media_files=media_files,
                    new_uuid=new_uuid,
                    submitted_by=user,
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
                        submitted_by=user,
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
                        submitted_by=user,
                        status='submitted_via_web',
                        date_created_override=None,
                        fxid=None,
                        site=site_id,
                        fs_poj_id=fs_xf.id,
                        project=fs_xf.project.id,
                    )
                    task_obj = CeleryTaskProgress.objects.create(
                        user=user,
                        description='Change site info',
                        task_type=25,
                        content_object=instance.fieldsight_instance)
                    if task_obj:
                        from onadata.apps.fieldsight.tasks import \
                            update_meta_details
                        update_meta_details.apply_async(
                            (fs_xf.id, instance.id, task_obj.id, site_id),
                            countdown=1)
                    else:
                        from onadata.apps.fieldsight.tasks import \
                            update_meta_details
                        update_meta_details.apply_async(
                            (fs_xf.id, instance.id, 0, site_id),
                            countdown=1)

            noti_type = 16
            title = "new submission"

            if instance.fieldsight_instance.site:
                extra_object = instance.fieldsight_instance.site
                extra_message = ""
                project = extra_object.project
                site = extra_object
                organization = extra_object.project.organization

            else:
                extra_object = instance.fieldsight_instance.project
                extra_message = "project"
                project = extra_object
                site = None
                organization = extra_object.organization

            instance.fieldsight_instance.logs.create(source=user,
                                                     type=noti_type,
                                                     title=title,

                                                     organization=organization,
                                                     project=project,
                                                     site=site,
                                                     extra_object=extra_object,
                                                     extra_message=extra_message,
                                                     content_object=instance.fieldsight_instance)

        context = self.get_serializer_context()
        serializer = SubmissionSerializer(instance, context=context)
        return Response(serializer.data,
                        headers=self.get_openrosa_headers(request),
                        status=status.HTTP_201_CREATED,
                        template_name=self.template_name)
