import json
import re

from django.core.urlresolvers import reverse_lazy
from rest_framework import serializers

from onadata.apps.fieldsight.models import Site
from onadata.apps.fsforms.models import XformHistory, FORM_STATUS, InstanceStatusChanged, InstanceImages, \
    EditedSubmission, FInstance
from onadata.apps.fsforms.utils import get_version
from onadata.apps.logger.models import Instance

from django.contrib.sites.models import Site as DjangoSite
BASEURL = DjangoSite.objects.get_current().domain


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstanceImages
        fields = ('image',)


class AlterInstanceStatusSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = InstanceStatusChanged
        fields = ('finstance', 'message', 'old_status', 'new_status', 'images')
        extra_kwargs = {'images': {'write_only': True}}


class SiteSerializer(serializers.ModelSerializer):
    site_information = serializers.SerializerMethodField()
    project_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Site
        fields = ('name', 'identifier', 'id', 'logo', 'site_information', 'project_name', 'latitude', 'longitude')
        
    def get_site_information(self, obj):
        if not obj.all_ma_ans:
            return {}
        return obj.all_ma_ans

    def get_project_name(self, obj):
        if obj.region:
            return obj.region.name
        return obj.project.name


class HistorySerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = InstanceStatusChanged
        fields = ('message', 'date', 'get_new_status_display', 'user_name')

    def get_user_name(self, obj):
        return obj.user.username


class SubmissionSerializer(serializers.ModelSerializer):
    submission_data = serializers.SerializerMethodField()
    submitted_by = serializers.SerializerMethodField()
    site = serializers.SerializerMethodField()
    submission_history = serializers.SerializerMethodField()
    status_data = serializers.SerializerMethodField()
    form_type = serializers.SerializerMethodField()
    form_name = serializers.SerializerMethodField()
    edit_url = serializers.SerializerMethodField()
    download_url = serializers.SerializerMethodField()
    has_review_permission = serializers.SerializerMethodField()
    breadcrumbs = serializers.SerializerMethodField()

    class Meta:
        model = Instance
        fields = ('submission_data', 'date_created',  'submitted_by', 'site', 'submission_history',
                  'status_data', 'form_type', 'form_name', 'fieldsight_instance', 'edit_url', 'download_url',
                  'has_review_permission', 'breadcrumbs')

    def get_submitted_by(self, obj):
        return obj.user.first_name + ' ' + obj.user.last_name

    def get_status_data(self, obj):
        finstance = obj.fieldsight_instance
        return {
            'status_display': finstance.get_abr_form_status(),
            'status': finstance.form_status,
            'options': dict(FORM_STATUS),
            'comment': finstance.comment
        }

    def get_submission_history(self, obj):
        finstance = obj.fieldsight_instance
        edits = finstance.edits.all()
        comments = InstanceStatusChanged.objects.filter(finstance=finstance)
        comment_data = []
        for c in comments:
            url = c.images.first()
            if url:
                try:
                    url = url.image.url
                except:
                    url = None
            comment_data.append(
                {
                    "comment": c.message,
                    "date": c.date,
                    "get_new_status_display": c.new_status_display(),
                    "user_name": c.user.username,
                    "user_full_name": c.user.first_name + ' ' + c.user.last_name,
                    "user_profile_picture": c.user.user_profile.profile_picture.url,
                    "url": reverse_lazy("forms:instance_status_change_detail",
                                                kwargs={'pk': c.id}),
                    "media_img": url,
                },
                )
        instances_data = []
        for e in edits:
            instances_data.append(
                {"url": reverse_lazy("fv3:submission-data", args=(e.id,)),
                 "date": e.date,
                 "comment": "",
                 "get_new_status_display": "New Submission",
                 "user_name":e.user.username,
                 "user_full_name": e.user.first_name + ' ' + e.user.last_name,
                 "user_profile_picture":e.user.user_profile.profile_picture.url,
                 "media_img ": "",
                })
        # sort data past _ data
        comment_data.extend(instances_data)
        comment_data.sort(key=lambda item: item['date'], reverse=True)
        return comment_data

    def get_site(self, obj):
        finstance = obj.fieldsight_instance
        if not finstance.site:
            return {}
        return SiteSerializer(finstance.site).data

    def get_form_type(self, obj):
        finstance = obj.fieldsight_instance

        return {
            'is_staged': finstance.site_fxf.is_staged if finstance.site_fxf else finstance.project_fxf.is_staged,
            'is_scheduled': finstance.site_fxf.is_scheduled if finstance.site_fxf else finstance.project_fxf.is_scheduled,
            'is_survey': finstance.site_fxf.is_survey if finstance.site_fxf else finstance.project_fxf.is_survey,
        }

    def get_form_name(self, obj):
        return obj.xform.title

    def get_edit_url(self, obj):
        return reverse_lazy("forms:edit_data", kwargs={'id_string':obj.xform.id_string, 'data_id':obj.id})

    def get_download_url(self, obj):
        return {'main':reverse_lazy("fieldsight:instance-responses-report", kwargs={'pk':obj.id, 'remove_null_fields':0}),
                'null':reverse_lazy("fieldsight:instance-responses-report", kwargs={'pk':obj.id, 'remove_null_fields':1}),
                }

    def get_submission_data(self, instance):
        data = []
        finstance = instance.fieldsight_instance
        pattern = re.compile('\$\{(.*)\}')

        def get_answer(instance):
            return instance.json

        def get_question(instance, finstance):
            submission_version = finstance.get_version
            json_data = instance.xform.json
            xml = instance.xform.xml
            xml_version = get_version(xml)
            if submission_version and submission_version == xml_version:
                return json.loads(json_data)
            else:
                if XformHistory.objects.filter(xform=instance.xform, version=submission_version).exists():
                    xf_history = XformHistory.objects.get(xform=instance.xform, version=submission_version)
                    return json.loads(str(xf_history.json))

            return json.loads(json_data)

        json_answer = get_answer(instance)
        json_question = get_question(instance, finstance)

        base_url = BASEURL
        media_folder = instance.xform.user.username

        def parse_repeat(r_object, prev_group = None):
            repeat = dict()
            if prev_group:
                r_question = prev_group + '/' + r_object['name']
            else:
                r_question = r_object['name']
            repeat['name'] = r_object['name']
            repeat['type'] = r_object['type']
            repeat['label'] = r_object.get('label')
            repeat['elements'] = []

            if r_question in json_answer:
                for gnr_answer in json_answer[r_question]:
                    for first_children in r_object['children']:
                        question_type = first_children['type']
                        question = first_children['name']
                        # label = first_children.get('label', '')
                        group_answer = json_answer[r_question]
                        answer = ''
                        if r_question + "/" + question in gnr_answer:
                            if first_children['type'] == 'note':
                                answer = ''
                            elif first_children['type'] == 'photo' or first_children['type'] == 'audio' or \
                                    first_children['type'] == 'video':
                                answer = 'http://' + base_url + '/attachment/medium?media_file=' + media_folder + '/attachments/' + \
                                         gnr_answer[r_question + "/" + question]
                            else:
                                answer = gnr_answer[r_question + "/" + question]

                        if 'label' in first_children:
                            question = first_children['label']
                        row = {'type': question_type, 'question': question, 'answer': answer, 'label': question}
                        repeat['elements'].append(row)
            elif r_question in json_answer:
                for gnr_answer in json_answer[r_question]:
                    for first_children in r_object['children']:
                        question_type = first_children['type']
                        question = first_children['name']
                        label = first_children.get('label', '')
                        group_answer = json_answer[r_question]
                        answer = ''
                        if r_question + "/" + question in gnr_answer:
                            if first_children['type'] == 'note':
                                answer = ''
                            elif first_children['type'] == 'photo' or first_children['type'] == 'audio' or \
                                    first_children['type'] == 'video':
                                answer = 'http://' + base_url + '/attachment/medium?media_file=' + media_folder + '/attachments/' + \
                                         gnr_answer[r_question + "/" + question]
                            else:
                                answer = gnr_answer[r_question + "/" + question]

                        if 'label' in first_children:
                            question = first_children['label']
                        row = {'type': question_type, 'question': question, 'answer': answer, 'label': question}
                        repeat['elements'].append(row)
            else:
                for first_children in r_object['children']:
                    question_type = first_children['type']
                    question = first_children['name']
                    answer = ''
                    if 'label' in first_children:
                        question = first_children['label']
                    row = {'type': question_type, 'question': question, 'answer': answer, 'label':question}
                    repeat['elements'].append(row)
            return repeat

        def parse_group(prev_groupname, g_object):
            g_question = prev_groupname + g_object['name']
            if g_object['name'] == 'meta':
                for first_children in g_object['children']:
                    question = first_children['name']
                    # label = first_children.get('name', '')
                    question_type = first_children['type']
                    if question_type == 'group':
                        parse_group(g_question + "/", first_children)
                        continue
                    answer = ''
                    if g_question + "/" + question in json_answer:
                        if question_type == 'note':
                            answer = ''
                        elif question_type == 'photo' or question_type == 'audio' or question_type == 'video':
                            answer = 'http://' + base_url + '/attachment/medium?media_file=' + media_folder + '/attachments/' + \
                                     json_answer[g_question + "/" + question]
                        else:
                            answer = json_answer[g_question + "/" + question]

                    if 'label' in first_children:
                        question = first_children['label']
                    row = {'type': question_type, 'question': question, 'answer': answer, 'label': question}
                    return row
            else:
                group = dict()
                group['name'] = g_question
                group['type'] = g_object['type']
                group['label'] = g_object.get('label')
                group['elements'] = []
                # group = {'group_name': g_question, 'type': g_object['type'], 'label': g_object['label']}
                for first_children in g_object['children']:
                    question = first_children['name']
                    question_type = first_children['type']
                    if question_type == 'group':
                        group['elements'].append(parse_group(g_question + "/", first_children))
                        continue

                    if question_type == 'repeat':
                        group['elements'].append(parse_repeat(first_children, g_question))
                        continue
                    answer = ''
                    if g_question + "/" + question in json_answer:
                        if question_type == 'note':
                            answer = ''
                        elif question_type == 'photo' or question_type == 'audio' or question_type == 'video':
                            answer = 'http://' + base_url + '/attachment/medium?media_file=' + media_folder + '/attachments/' + \
                                     json_answer[g_question + "/" + question]
                        else:
                            answer = json_answer[g_question + "/" + question]

                    if 'label' in first_children:
                        question = first_children['label']
                    row = {'type': question_type, 'question': question, 'answer': answer, 'label': question}
                    group['elements'].append(row)
                return group

        def parse_individual_questions(parent_object):
            for first_children in parent_object:
                if first_children['type'] == "repeat":
                    data.append(parse_repeat(first_children))
                elif first_children['type'] == 'group':
                    group = parse_group("", first_children)
                    data.append(group)
                else:
                    question = first_children['name']
                    label = first_children.get('label','')
                    question_type = first_children['type']
                    answer = ''
                    if question in json_answer:
                        if first_children['type'] == 'note':
                            answer = ''
                        elif first_children['type'] == 'photo' or first_children['type'] == 'audio' or first_children[
                            'type'] == 'video':
                            answer = 'http://' + base_url + '/attachment/medium?media_file=' + media_folder + '/attachments/' + \
                                     json_answer[question]
                        else:
                            answer = json_answer[question]
                    if 'label' in first_children:
                        question = first_children['label']
                    if isinstance(question, dict):  # for multi language defined form field
                        for label, value in question.items():
                            m = pattern.search(value)  # check if the question field requires the value of the calculated field
                            if m:
                                field = m.group(1)  # gives the name of the calculation field
                                if field in json_answer:
                                    replace_text = json_answer[field]
                                    question[label] = value.replace(m.group(0), replace_text)  # replace variable fields in form of ${''} by the value submitted

                    else:  # for string label with value of a calculation field
                        m = pattern.search(question)
                        if m:
                            field = m.group(1)
                            if field in json_answer:
                                replace_text = json_answer[field]
                                question = question.replace(m.group(0), replace_text)

                    row = {"type": question_type, "question": question, "answer": answer, 'label':label}
                    data.append(row)

            submitted_by = {'type': 'submitted_by', 'question': 'Submitted by', 'answer': json_answer['_submitted_by'], 'label':''}
            submission_time = {
                'type': 'submission_time', 'question': 'Submission Time',
                'answer': json_answer['_submission_time'],
                'label': ''
            }
            data.append(submitted_by)
            data.append(submission_time)

        parse_individual_questions(json_question['children'])
        pattern = r"\{(.*?)\}"
        calculations_dict = [d for d in data if d['type'] == "calculate"]
        calculated_data = []
        for d in data:
            for k, v in d.items():
                if v and "${" in v:
                    calcluate_keys = re.findall(pattern, v)
                    for key in calcluate_keys:
                        for cd in calculations_dict:
                            if cd["question"] == key:
                                answer = cd['answer']
                                v = v.replace("${" + key + "}", answer)
                d[k] = v
            calculated_data.append(d)
        return calculated_data

    def get_has_review_permission(self, obj):
        finstance = obj.fieldsight_instance
        request = self.context['request']
        has_access = False

        if finstance.site:
            site = finstance.site
            if request.roles.filter(site=site, group__name="Reviewer") or request.roles.filter(region=site.region,
                                                                                               group__name="Region Reviewer"):
                has_access = True
            elif request.roles.filter(project=site.project, group__name="Project Manager") or \
                    request.roles.filter(organization=site.project.organization,
                                         group__name="Organization Admin") or request.roles.filter(
                group__name="Super Admin"):
                has_access = True
            return has_access

        return has_access

    def get_breadcrumbs(self, obj):
        finstance = obj.fieldsight_instance

        if finstance.site:
            site = finstance.site
            breadcrumbs = {'current_page': 'Submission Detail',  'name': site.name,
                           'name_url': site.get_absolute_url()}
        elif finstance.project:
            project = finstance.project
            breadcrumbs = {'current_page': 'Submission Detail', 'name': project.name,
                           'name_url': project.get_absolute_url()}
        else:
            breadcrumbs = {}

        return breadcrumbs


class EditSubmissionAnswerSerializer(serializers.ModelSerializer):
    submission_data = serializers.SerializerMethodField()
    submitted_by = serializers.SerializerMethodField()
    edit_url = serializers.SerializerMethodField()
    download_url = serializers.SerializerMethodField()
    form_name = serializers.SerializerMethodField()

    class Meta:
        model = EditedSubmission
        fields = ('submission_data', 'date', 'submitted_by', 'download_url', 'edit_url', 'form_name')

    def get_submitted_by(self, obj):
        return obj.user.first_name + ' ' + obj.user.last_name

    def get_form_name(self, obj):
        if obj.old.project_fxf:
            return obj.old.project_fxf.xf.title
        else:
            return obj.old.site_fxf.xf.title

    def get_submission_data(self, edit):
        data = []
        finstance = edit.old
        instance = finstance.instance

        def get_answer(instance):
            return instance.json

        def get_question(instance, finstance):
            submission_version = finstance.get_version
            json_data = instance.xform.json
            xml = instance.xform.xml
            xml_version = get_version(xml)
            if submission_version and submission_version == xml_version:
                return json.loads(json_data)
            else:
                if XformHistory.objects.filter(xform=instance.xform, version=submission_version).exists():
                    xf_history = XformHistory.objects.get(xform=instance.xform, version=submission_version)
                    return json.loads(str(xf_history.json))

            return json.loads(json_data)

        json_answer = get_answer(edit)
        json_question = get_question(instance, finstance)

        base_url = BASEURL
        media_folder = instance.xform.user.username

        def parse_repeat(r_object, prev_group = None):
            repeat = dict()
            if prev_group:
                r_question = prev_group + '/' + r_object['name']
            else:
                r_question = r_object['name']
            repeat['name'] = r_object['name']
            repeat['type'] = r_object['type']
            repeat['label'] = r_object.get('label')
            repeat['elements'] = []

            if r_question in json_answer:
                for gnr_answer in json_answer[r_question]:
                    for first_children in r_object['children']:
                        question_type = first_children['type']
                        question = first_children['name']
                        group_answer = json_answer[r_question]
                        answer = ''
                        if r_question + "/" + question in gnr_answer:
                            if first_children['type'] == 'note':
                                answer = ''
                            elif first_children['type'] == 'photo' or first_children['type'] == 'audio' or \
                                    first_children['type'] == 'video':
                                answer = 'http://' + base_url + '/attachment/medium?media_file=' + media_folder + '/attachments/' + \
                                         gnr_answer[r_question + "/" + question]
                            else:
                                answer = gnr_answer[r_question + "/" + question]

                        if 'label' in first_children:
                            question = first_children['label']
                        row = {'type': question_type, 'question': question, 'answer': answer}
                        repeat['elements'].append(row)
            elif r_question in json_answer:
                for gnr_answer in json_answer[r_question]:
                    for first_children in r_object['children']:
                        question_type = first_children['type']
                        question = first_children['name']
                        group_answer = json_answer[r_question]
                        answer = ''
                        if r_question + "/" + question in gnr_answer:
                            if first_children['type'] == 'note':
                                answer = ''
                            elif first_children['type'] == 'photo' or first_children['type'] == 'audio' or \
                                    first_children['type'] == 'video':
                                answer = 'http://' + base_url + '/attachment/medium?media_file=' + media_folder + '/attachments/' + \
                                         gnr_answer[r_question + "/" + question]
                            else:
                                answer = gnr_answer[r_question + "/" + question]

                        if 'label' in first_children:
                            question = first_children['label']
                        row = {'type': question_type, 'question': question, 'answer': answer}
                        repeat['elements'].append(row)
            else:
                for first_children in r_object['children']:
                    question_type = first_children['type']
                    question = first_children['name']
                    answer = ''
                    if 'label' in first_children:
                        question = first_children['label']
                    row = {'type': question_type, 'question': question, 'answer': answer}
                    repeat['elements'].append(row)
            return repeat

        def parse_group(prev_groupname, g_object):
            g_question = prev_groupname + g_object['name']
            if g_object['name'] == 'meta':
                for first_children in g_object['children']:
                    question = first_children['name']
                    question_type = first_children['type']
                    if question_type == 'group':
                        parse_group(g_question + "/", first_children)
                        continue
                    answer = ''
                    if g_question + "/" + question in json_answer:
                        if question_type == 'note':
                            answer = ''
                        elif question_type == 'photo' or question_type == 'audio' or question_type == 'video':
                            answer = 'http://' + base_url + '/attachment/medium?media_file=' + media_folder + '/attachments/' + \
                                     json_answer[g_question + "/" + question]
                        else:
                            answer = json_answer[g_question + "/" + question]

                    if 'label' in first_children:
                        question = first_children['label']
                    row = {'type': question_type, 'question': question, 'answer': answer}
                    return row
            else:
                group = dict()
                group['name'] = g_question
                group['type'] = g_object['type']
                group['label'] = g_object.get('label')
                group['elements'] = []
                # group = {'group_name': g_question, 'type': g_object['type'], 'label': g_object['label']}
                for first_children in g_object['children']:
                    question = first_children['name']
                    question_type = first_children['type']
                    if question_type == 'group':
                        group['elements'].append(parse_group(g_question + "/", first_children))
                        continue

                    if question_type == 'repeat':
                        group['elements'].append(parse_repeat(first_children, g_question))
                        continue
                    answer = ''
                    if g_question + "/" + question in json_answer:
                        if question_type == 'note':
                            answer = ''
                        elif question_type == 'photo' or question_type == 'audio' or question_type == 'video':
                            answer = 'http://' + base_url + '/attachment/medium?media_file=' + media_folder + '/attachments/' + \
                                     json_answer[g_question + "/" + question]
                        else:
                            answer = json_answer[g_question + "/" + question]

                    if 'label' in first_children:
                        question = first_children['label']
                    row = {'type': question_type, 'question': question, 'answer': answer}
                    group['elements'].append(row)
                return group

        def parse_individual_questions(parent_object):
            for first_children in parent_object:
                if first_children['type'] == "repeat":
                    data.append(parse_repeat(first_children))
                elif first_children['type'] == 'group':
                    group = parse_group("", first_children)
                    data.append(group)
                else:
                    question = first_children['name']
                    question_type = first_children['type']
                    answer = ''
                    if question in json_answer:
                        if first_children['type'] == 'note':
                            answer = ''
                        elif first_children['type'] == 'photo' or first_children['type'] == 'audio' or first_children[
                            'type'] == 'video':
                            answer = 'http://' + base_url + '/attachment/medium?media_file=' + media_folder + '/attachments/' + \
                                     json_answer[question]
                        elif first_children['type'] == 'select one':
                            for select_children in first_children['children']:
                                if json_answer[question] == select_children['name']:
                                    answer = select_children['label']
                        elif first_children['type'] == 'select all that apply':
                            answer = ''
                            for select_children in first_children['children']:
                                if select_children['name'] in json_answer[question]:
                                    answer = answer + select_children['label'] + ' '
                        else:
                            answer = json_answer[question]
                    if 'label' in first_children:
                        question = first_children['label']
                    row = {"type": question_type, "question": question, "answer": answer}
                    data.append(row)

            submitted_by = {'type': 'submitted_by', 'question': 'Submitted by', 'answer': json_answer['_submitted_by']}
            submission_time = {
                'type': 'submission_time', 'question': 'Submission Time',
                'answer': json_answer['_submission_time']
            }
            data.append(submitted_by)
            data.append(submission_time)

        parse_individual_questions(json_question['children'])
        pattern = r"\{(.*?)\}"
        calculations_dict = [d for d in data if d['type'] == "calculate"]
        calculated_data = []
        for d in data:
            for k, v in d.items():
                if "${" in v:
                    calcluate_keys = re.findall(pattern, v)
                    for key in calcluate_keys:
                        for cd in calculations_dict:
                            if cd["question"] == key:
                                answer = cd['answer']
                                v = v.replace("${"+key+"}", answer)
                d[k] = v
            calculated_data.append(d)
        return calculated_data

    def get_edit_url(self, obj):
        return None

    def get_download_url(self, obj):
        return {
                }


class MyFinstanceSerializer(serializers.ModelSerializer):
    form_name = serializers.SerializerMethodField()
    id_string = serializers.SerializerMethodField()
    site_name = serializers.CharField(source='site.name')
    site_identifier = serializers.CharField(source='site.identifier')
    project_name = serializers.CharField(source='project.name')
    status_display = serializers.SerializerMethodField()

    class Meta:
        model = FInstance
        fields = ('pk', 'project_fxf', 'site_fxf', 'project', 'site', 'form_status',
                  'form_name', 'site_name', 'site_identifier', 'project_name', 'status_display', 'version', 'id_string', 'date')

    def get_form_name(self, obj):
        if obj.project_fxf:
            return obj.project_fxf.xf.title
        return obj.site_fxf.xf.title

    def get_status_display(self, obj):
        return obj.get_abr_form_status()

    def get_id_string(self, obj):
        if obj.project_fxf:
            return obj.project_fxf.xf.id_string
        return obj.site_fxf.xf.id_string
