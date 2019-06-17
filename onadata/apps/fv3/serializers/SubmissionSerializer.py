import datetime

import json
import re
from django.core.urlresolvers import reverse_lazy, reverse
from rest_framework import serializers

from onadata.apps.fieldsight.models import Site
from onadata.apps.fsforms.models import XformHistory, FORM_STATUS, InstanceStatusChanged, InstanceImages
from onadata.apps.fsforms.utils import get_version, send_message_flagged
from onadata.apps.logger.models import Instance

from django.contrib.sites.models import Site as DjangoSite
BASEURL = DjangoSite.objects.get_current().domain


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstanceImages
        fields = ('image',)


class AlterInstanceStatusSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True)

    class Meta:
        model = InstanceStatusChanged
        fields = ('finstance', 'message', 'old_status', 'new_status', 'images')
        extra_kwargs = {'images': {'write_only': True}}

    def create(self, validated_data):
        images = self.context['images']
        validated_data.pop("images")
        instance_status = InstanceStatusChanged.objects.create(**validated_data)
        for image in images:
            InstanceImages.objects.create(instance_status=instance_status, image=image)
        fi = instance_status.finstance
        fi.form_status = instance_status.new_status
        fi.date = datetime.date.today()
        fi.save()
        if fi.site:
            fi.site.update_current_progress()
            extra_object = fi.site
            extra_message = ""
        else:
            extra_object = fi.project
            extra_message = "project"

        org = fi.project.organization if fi.project else fi.site.project.organization
        instance_status.logs.create(source=self.context['request'].user,
                                    type=17,
                                    title="form status changed",
                                      organization=org,
                                      project=fi.project,
                                      site=fi.site,
                                      content_object=fi,
                                      extra_object=extra_object,
                                      extra_message=extra_message
                                      )
        comment_url = reverse("forms:instance_status_change_detail",
                              kwargs={'pk': instance_status.id})
        send_message_flagged(fi, instance_status.message, comment_url)
        return instance_status


class SiteSerializer(serializers.ModelSerializer):
    site_information = serializers.SerializerMethodField()
    
    class Meta:
        model = Site
        fields = ('name', 'identifier', 'id', 'logo', 'site_information')
        
    def get_site_information(self, obj):
        if not obj.site_meta_attributes_ans:
            return {}
        return obj.site_meta_attributes_ans


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
    submmition_history = serializers.SerializerMethodField()
    status_data = serializers.SerializerMethodField()
    form_type = serializers.SerializerMethodField()
    form_name = serializers.SerializerMethodField()

    class Meta:
        model = Instance
        fields = ('submission_data', 'date_created',  'submitted_by', 'site', 'submmition_history',
                  'status_data', 'form_type','form_name','fieldsight_instance')

    def get_submitted_by(self, obj):
        return obj.user.username

    def get_status_data(self, obj):
        finstance = obj.fieldsight_instance
        return {
            'status_display': finstance.get_abr_form_status(),
            'status': finstance.form_status,
            'options': dict(FORM_STATUS),
            'comment': finstance.comment
        }

    def get_submmition_history(self, obj):
        finstance = obj.fieldsight_instance
        pk_list = [finstance.id]
        finstances = []
        previous = finstance.new_edits.all()
        if len(previous):
            previous_edit = previous[0].old
            pk_list.append(previous_edit.id)
            finstances.append(previous_edit)
            p_previous = previous_edit.new_edits.all()
            if len(p_previous):
                p_previous_edit = p_previous[0].old
                pk_list.append(p_previous_edit.id)
                finstances.append(p_previous_edit)
                p_p_previous = p_previous_edit.new_edits.all()
                if len(p_p_previous):
                    p_p_previous_edit = p_p_previous[0].old
                    pk_list.append(p_p_previous_edit.id)
                    finstances.append(p_p_previous_edit)

        comments = InstanceStatusChanged.objects.filter(finstance__id__in=pk_list)
        comment_data = []
        for c in comments:
            comment_data.append(
                {
                    "comment": c.message,
                    "date": c.date,
                    "get_new_status_display": "Rejected",
                    "user_name": c.user.user_name,
                    "url": reverse_lazy("forms:instance_status_change_detail",
                                                kwargs={'pk': c.id}),
                },
                )
        instances_data = []
        for fi in finstances:
            instances_data.append(
                {"url": reverse_lazy("fv3:submission", args=(fi.id,)),
                 "date": fi.date,
                 "comment": "",
                 "get_new_status_display": "New Submission",
                 "user_name":fi.submitted_by.username})
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
    def get_submission_data(self, instance):
        data = []
        finstance = instance.fieldsight_instance

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
                                v = v.replace("${" + key + "}", answer)
                d[k] = v
            calculated_data.append(d)
        return calculated_data


class SubmissionAnswerSerializer(serializers.ModelSerializer):
    submission_data = serializers.SerializerMethodField()
    submitted_by = serializers.SerializerMethodField()

    class Meta:
        model = Instance
        fields = ('submission_data', 'date_created',  'submitted_by')

    def get_submitted_by(self, obj):
        return obj.user.username

    def get_submission_data(self, instance):
        data = []
        finstance = instance.fieldsight_instance

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
