from onadata.apps.fieldsight.models import Site
from onadata.apps.fsforms.models import FieldSightXF

"""
This module is used to get the site meta attributes answers of a specified site.
The site meta attributes answers that are to be selected from forms are not directly stored in the database.
To remove the overhead computation of calculating such answers repeatedly, it would be a lot easier if they are saved 
in the database directly. 

To be used in the future this module provides site meta attributes answers in a format to be saved in the database directly.
"""


def get_form_answer(site_id, meta):
    fxf = FieldSightXF.objects.filter(pk=int(meta.get('form_id', "0")))
    if fxf:
        sub = fxf[0].project_form_instances.filter(site_id=site_id).order_by('-instance_id')[:1]
        if sub:
            if meta['question']['type'] == 'repeat':
                return ""

            sub_answers = sub[0].instance.json
            if meta['question']['type'] == "repeat":
                answer = ""
            else:
                answer = sub_answers.get(meta.get('question').get('name'), '')

            if meta['question']['type'] in ['photo', 'video', 'audio'] and answer is not "":
                answer = 'http://app.fieldsight.org/attachment/medium?media_file=' + fxf.xf.user.username + '/attachments/' + answer
        else:
            answer = ""
    else:
        answer = ""
    return answer


def get_form_sub_status(site_id, meta):
    fxf = FieldSightXF.objects.filter(pk=int(meta.get('form_id', "0")))
    if fxf:
        sub_date = fxf[0].project_form_instances.filter(site_id=site_id).order_by('-instance_id').values('date')[:1]
        if sub_date:
            answer = "Last submitted on " + sub_date[0]['date'].strftime("%d %b %Y %I:%M %P")
        else:
            answer = ""
    else:
        answer = ""
    return answer


def get_form_ques_ans_status(site_id, meta):
    fxf = FieldSightXF.objects.filter(pk=int(meta.get('form_id', "0")))
    if fxf:
        sub = fxf[0].project_form_instances.filter(site_id=site_id).order_by('-instance_id')[:1]
        if sub:

            sub_answers = sub[0].instance.json
            get_answer = sub_answers.get(meta.get('question').get('name'), None)

            if get_answer:
                answer = "Answered"
            else:
                answer = ""

        else:
            answer = ""
    else:
        answer = ""
    return answer


def get_form_submission_count(site_id, meta):
    fxf = FieldSightXF.objects.filter(pk=int(meta.get('form_id', "0")))
    if fxf:
        answer = fxf[0].project_form_instances.filter(site_id=site_id).count()
    else:
        # answer = "No Form"
        answer = ""
    return answer


def get_site_meta_ans(site_id):
    metas = {}
    site = Site.objects.get(pk=site_id)
    project = site.project
    main_project = project.id

    def generate_ans(metas, project_id, metas_to_parse, meta_answer, parent_selected_metas, project_metas):

        for meta in metas_to_parse:
            # if project_metas and meta not in project_metas:
            #     continue
            if meta.get('question_type') == "Link":
                if parent_selected_metas:
                    selected_metas = parent_selected_metas
                else:
                    selected_metas = meta.get('metas')
                if meta.get('project_id') == main_project:
                    continue
                sitenew = Site.objects.filter(identifier=meta_answer.get(meta.get('question_name'), None),
                                              project_id=meta.get('project_id'))
                if sitenew and str(sitenew[0].project_id) in selected_metas:
                    answer = meta_answer.get(meta.get('question_name'))
                    sub_metas = []
                    generate_ans(sub_metas,
                                 sitenew[0].project_id,
                                 selected_metas[str(sitenew[0].project_id)],
                                 sitenew[0].site_meta_attributes_ans,
                                 selected_metas,
                                 sitenew[0].project.site_meta_attributes)
                    metas[meta.get('question_text')] = answer

                else:
                    answer = "No site referenced"
                    metas[meta.get('question_text')] = answer

            else:
                if meta.get('question_type') == "Form":
                    answer = get_form_answer(site_id, meta)

                elif meta.get('question_type') == "FormSubStat":
                    answer = get_form_sub_status(site_id, meta)

                elif meta.get('question_type') == "FormQuestionAnswerStatus":
                    answer = get_form_ques_ans_status(site_id, meta)

                elif meta.get('question_type') == "FormSubCountQuestion":
                    answer = get_form_submission_count(site_id, meta)

                else:
                    answer = meta_answer.get(meta.get('question_name'), "")

                metas[meta.get('question_text')] = answer

    generate_ans(metas, project.id, project.site_meta_attributes, site.site_meta_attributes_ans, None, None)

    return metas
