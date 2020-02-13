import os
import re
import requests
from django.conf import settings
from rest_framework.authentication import SessionAuthentication

from onadata.libs.utils.viewer_tools import EnketoError


def get_attachment(key):
    p = re.compile('instance_attachments\[(.*)\]')
    m = p.search(key)
    if m:
        return m.group(1)
    return None


def get_attachment_strings_to_be_replace(attachment_file_name, instance_xml, attachment_file_extension):
    p = re.compile(attachment_file_name+'(.*)' + attachment_file_extension)
    m = p.findall(instance_xml)
    if m:
        return [attachment_file_name + i + attachment_file_extension for i in m]
    return []


def trim_after_last_hyphen(a):
    return "_".join(a.split("_")[:-1])


def replace_attachmnt_name(attachment_file_name, instance_xml, attachment_file_extension, attachment_alias):
    file_names_to_be_replaced_in_xml = get_attachment_strings_to_be_replace(attachment_file_name, instance_xml,
                                                                           attachment_file_extension)
    if file_names_to_be_replaced_in_xml:
        for file_name_to_be_replaced_in_xml in file_names_to_be_replaced_in_xml:
            instance_xml = instance_xml.replace(file_name_to_be_replaced_in_xml, attachment_alias)
    return instance_xml


#attachments_keys = [k for k in values.keys() if "instance_attachments" in k]
#instance_xml = values['instance']


def clean_xml_for_enketo(attachments_keys, instance_xml):
    return instance_xml
    for attachment_key in attachments_keys:
        attachment = get_attachment(attachment_key)
        attachment_file_name = os.path.splitext(attachment)[0]
        attachment_file_extension = os.path.splitext(attachment)[1]
        if attachment_file_name in instance_xml:
            instance_xml = replace_attachmnt_name(attachment_file_name, instance_xml, attachment_file_extension, attachment)
        else:
            #     attachment file name have changed trim the kobocat aded text from attachment key
            trimmed_file_name = trim_after_last_hyphen(attachment_file_name)
            if trimmed_file_name in instance_xml:
                instance_xml = replace_attachmnt_name(trimmed_file_name, instance_xml, attachment_file_extension, attachment)
    return instance_xml



def enketo_view_url(form_url, id_string, instance_xml=None,
               instance_id=None, return_url=None, instance_attachments=None):
    if not hasattr(settings, 'ENKETO_URL')\
            and not hasattr(settings, 'ENKETO_API_SURVEY_PATH'):
        return False

    if instance_attachments is None:
        instance_attachments = {}


    values = {
        'form_id': id_string,
        'server_url': form_url
    }
    if instance_id is not None and instance_xml is not None:
        url = settings.ENKETO_URL + '/api/v2/instance'
        url = url + "/view"
        values.update({
            'instance': instance_xml,
            'instance_id': instance_id,
            'return_url': return_url
        })
        for key, value in instance_attachments.iteritems():
            values.update({
                'instance_attachments[' + key + ']': value
            })
        values['instance'] = clean_xml_for_enketo(
            [k for k in values.keys() if "instance_attachments" in k],
            values['instance'])
        req = requests.post(url, data=values,
                            auth=(settings.ENKETO_API_TOKEN, ''), verify=False)

        if req.status_code in [200, 201]:
            try:
                response = req.json()
            except ValueError:
                pass
            else:
                if 'view_url' in response:
                    return response['view_url']
                if settings.ENKETO_OFFLINE_SURVEYS and ('offline_url' in response):
                    return response['offline_url']
                if 'url' in response:
                    return response['url']
        else:
            try:
                response = req.json()
            except ValueError:
                pass
            else:
                if 'message' in response:
                    raise EnketoError(response['message'])
    return False


def enketo_preview_url(form_url, id_string, return_url=None):
    if not hasattr(settings, 'ENKETO_URL')\
            and not hasattr(settings, 'ENKETO_API_SURVEY_PATH'):
        return False

    values = {
        'form_id': id_string,
        'server_url': form_url,
        'return_url': return_url
    }
    url = settings.ENKETO_URL + '/api/v2/survey/preview/iframe'

    req = requests.post(url, data=values,
                        auth=(settings.ENKETO_API_TOKEN, ''), verify=False)

    if req.status_code in [200, 201]:
        try:
            response = req.json()
            if 'preview_url' in response:
                preview_url = response['preview_url']
                if settings.ENKETO_PROTOCOL not in preview_url:
                    preview_url = preview_url.replace("http", settings.ENKETO_PROTOCOL)
                    return preview_url
                return response['preview_url']
        except ValueError:
            pass
        else:
            if 'preview_url' in response:
                return response['preview_url']
    else:
        try:
            response = req.json()
        except ValueError:
            pass
        else:
            if 'message' in response:
                raise EnketoError(response['message'])
    return False

def enketo_url_new_submission(form_url, id_string, site=None,
               form=None, return_url=None):

    if not hasattr(settings, 'ENKETO_URL')\
            and not hasattr(settings, 'ENKETO_API_SURVEY_PATH'):
        return False


    url = settings.ENKETO_URL + '/api/v2/survey/single'

    values = {
        'form_id': id_string,
        'server_url': form_url,
        'return_url': ''
    }

    req = requests.post(url, data=values,
                        auth=(settings.ENKETO_API_TOKEN, ''), verify=False)
    if req.status_code in [200, 201]:
        try:
            response = req.json()
        except ValueError:
            pass
        else:
            if 'single_url' in response:
                return response['single_url'] + '?ref={}_{}'.format(
        site, form)
    else:
        try:
            response = req.json()
        except ValueError:
            pass
        else:
            if 'message' in response:
                raise EnketoError(response['message'])
    return False




class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return

