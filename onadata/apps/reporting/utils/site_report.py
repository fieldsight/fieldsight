import pandas as pd
from django.db.models import Q

from onadata.apps.fieldsight.models import Site
from onadata.apps.fsforms.models import FInstance, InstanceStatusChanged
from onadata.apps.reporting.utils.common import separate_metrics, generate_default_metrices, generate_form_metrices, \
    generate_form_information
from onadata.apps.userrole.models import UserRole


def site_report(report_obj):
    project_id = report_obj.project_id
    attributes = report_obj.attributes
    filters = report_obj.filter
    regions = filters.get('regions')
    site_types = filters.get('site_types')
    region_filters = []
    if regions:
        if isinstance(regions, list):
            for r in regions:
                region_filters.append(r['id'])
        elif isinstance(regions, dict):
            region_filters.append(regions['id'])
    type_filters = []
    if site_types:
        if isinstance(site_types, list):
            for t in site_types:
                type_filters.append(t['id'])
        elif isinstance(regions, dict):
            type_filters.append(site_types['id'])

    site_filter = {}
    foreign_key_site_filter = {}
    review_site_filter = {}
    if region_filters:
        site_filter['region__id__in'] = region_filters
        foreign_key_site_filter['site__region__id__in'] = region_filters
        review_site_filter['finstance__site__region__id__in'] = region_filters
    if type_filters:
        site_filter['type__id__in'] = type_filters
        foreign_key_site_filter['site__type__id__in'] = type_filters
        review_site_filter['finstance__site__region__id__in'] = type_filters
    default_metrics, individual_form_metrics, form_information_metrics,\
        user_metrics, site_info_metrics = separate_metrics(attributes)
    selected_metas = []
    for meta in site_info_metrics:
        selected_metas.append(meta['code'])

    if selected_metas:
        query = Site.objects.filter(**site_filter).filter(project_id=project_id).values(
            'id', 'identifier', 'name', 'current_progress', 'all_ma_ans')
        df = pd.DataFrame(list(query), columns=['id', 'identifier', 'name', 'current_progress', 'all_ma_ans'])
        df.columns = ['site', 'identifier', 'name', 'progress', 'all_ma_ans']
        meta_objects = [df, pd.DataFrame(df['all_ma_ans'].tolist())[selected_metas]]
        df = pd.concat(meta_objects, axis=1).drop('all_ma_ans', axis=1)
    else:
        query = Site.objects.filter(**site_filter).filter(project_id=project_id).values(
            'id', 'identifier', 'name', 'current_progress')
        df = pd.DataFrame(list(query), columns=['id', 'identifier', 'name', 'current_progress'])
        df.columns = ['site', 'identifier', 'name', 'progress']
    if "progress" not in default_metrics:
        del df['progress']

    query_role = UserRole.objects.filter(**foreign_key_site_filter).filter(
        project=report_obj.project_id, site__isnull=False).values("site", "group", "ended_at")
    df_role = pd.DataFrame(list(query_role), columns=["site", "group", "ended_at"])
    active_df = df_role[~df_role.ended_at.isnull()]
    if 'active_users' in user_metrics:
        active_users = active_df.groupby('site').size().to_frame("active_users").reset_index()
        df = df.merge(active_users, on="site", how="left")
    if 'no_of_site_supervisor' in user_metrics:
        users_site_sup = df_role[df_role.group == 4].groupby('site').size().to_frame("no_of_site_supervisor").reset_index()
        df = df.merge(users_site_sup, on="site", how="left")
    if 'no_of_site_reviewer' in user_metrics:
        users_site_rev = df_role[df_role.group == 3].groupby('site').size().to_frame("no_of_site_reviewer").reset_index()
        df = df.merge(users_site_rev, on="site", how="left")
    if 'no_of_active_site_supervisor' in user_metrics:
        active_users_site_sup = active_df[active_df.group == 4].groupby('site').size().to_frame(
            "no_of_active_site_supervisor").reset_index()
        df = df.merge(active_users_site_sup, on="site", how="left")
    if 'no_of_active_site_reviewer' in user_metrics:
        active_users_site_rev = active_df[active_df.group == 3].groupby('site').size().to_frame(
            "active_users_rev").reset_index()
        df = df.merge(active_users_site_rev, on="site", how="left")

    query_submissions = FInstance.objects.filter(**foreign_key_site_filter).filter(
        Q(project_fxf__project=project_id) |
        Q(site_fxf__site__project=project_id)
    ).values("pk", "site", "project_fxf", "form_status", "date")
    df_submissions = pd.DataFrame(
        list(query_submissions), columns=["pk", "site", "project_fxf", "form_status", "date"])
    query_reviews = InstanceStatusChanged.objects.filter(**review_site_filter).filter(
        Q(finstance__project_fxf__project=project_id) |
        Q(finstance__site_fxf__site__project=project_id)
    ).values(
        "pk", "finstance__site", "new_status", "old_status", "user", "finstance")
    df_reviews = pd.DataFrame(list(query_reviews),
                              columns=["pk", "finstance__site", "new_status", "old_status", "user", "finstance"])
    df_reviews.columns = ["pk", "site", "new_status", "old_status", "user", "finstance"]

    df = generate_default_metrices(df, df_submissions, df_reviews, default_metrics, "site")

    individual_form_dict = {}
    individual_form_name_dict = {}
    for individual_form_metric in individual_form_metrics:
        code = individual_form_metric['value']['selectedIndividualForm']['code']
        key = individual_form_metric['value']['selectedForm']['id']
        form_name = individual_form_metric['value']['selectedForm']['title']
        if key not in individual_form_dict:
            individual_form_dict[key] = [code]
        else:
            individual_form_dict[key].append(code)
        individual_form_name_dict[key] = form_name

    for form_id, metrices_list in individual_form_dict.items():
        form_submissions = df_submissions[df_submissions.project_fxf == form_id]
        form_name = individual_form_name_dict[form_id]
        df = generate_form_metrices(form_name, df, form_submissions, df_reviews, metrices_list, "site")

    information_form_dict = {}
    information_form_name_dict = {}
    for individual_form_metric in form_information_metrics:
        code = individual_form_metric['value']['selectedQuestion']['form']['code']
        question = individual_form_metric['value']['selectedQuestion']['name']
        key = individual_form_metric['value']['selectedForm']['id']
        form_name = individual_form_metric['value']['selectedForm']['title']
        if key not in information_form_dict:
            information_form_dict[key] = {question: [code]}
        else:
            if question not in information_form_dict[key]:
                information_form_dict[key][question] = [code]
            else:
                information_form_dict[key][question].append(code)

        information_form_name_dict[key] = form_name

    query_submissions_form = FInstance.objects.filter(**foreign_key_site_filter).filter(
       project_fxf__in=information_form_dict.keys()).select_related(
       'instance').values("pk", "site", 'project_fxf', "instance__json", "date")
    df_submissions_form_answers = pd.DataFrame(list(query_submissions_form),
                                               columns=["pk", 'site', 'project_fxf', 'instance__json', "date"])
    for form_id, question_dict in information_form_dict.items():
        form_label = information_form_name_dict[form_id] + "/"
        form_submissions = df_submissions_form_answers[df_submissions_form_answers.project_fxf == int(form_id)]
        if not form_submissions.empty:
            question_objects = [form_submissions, pd.DataFrame(form_submissions['instance__json'].tolist())[question_dict.keys()]]
            form_submissions = pd.concat(question_objects, axis=1).drop('instance__json', axis=1)
        for question, metrices_codes in question_dict.items():
            df = generate_form_information(form_label, question, df, form_submissions, metrices_codes, "site")


    #reorder cols
    columns_name = list(df.columns)  #ordered metrices codes
    df = df[columns_name]

    df = df.replace("Nan", 0)
    return df
