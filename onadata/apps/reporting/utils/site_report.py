import pandas as pd
from django.db.models import Q

from onadata.apps.fieldsight.models import Site
from onadata.apps.fsforms.models import FInstance, InstanceStatusChanged


def generate_form_frame(form_id, df, df_submissions, df_reviews):
    form_id = str(form_id)
    df_visits = df_submissions.date.apply(lambda dt: dt.date()).groupby(
        [df_submissions.site]).nunique().to_frame('site_visited' + form_id).reset_index()
    df = df.merge(df_visits, on="site", how="left")

    df_reviews_count = df_reviews.groupby('site').size().to_frame('no_of_reviews' + form_id).reset_index()
    df_reviews_count = df_reviews_count.replace("NAN", 0)

    df = df.merge(df_reviews_count, on="site", how="left")

    # status of most recent submission
    df_mrs = df_submissions.loc[df_submissions.groupby('site').date.idxmax()][['site', 'form_status']]
    df_mrs.columns = ['site', 'status_of_most_recent_submission']
    df = df.merge(df_mrs, on="site", how="left")

    # no of submissions
    submissions_count = df_submissions.groupby(['site']).size().to_frame('submissions_count' + form_id).reset_index()
    df = df.merge(submissions_count, on="site", how="left")

    # no of submissions current
    df_submissions_status_index = df_submissions.set_index('form_status')
    submissions_pending = df_submissions_status_index.loc[0].groupby(['site']).size().to_frame(
        'submissions_pending' + form_id).reset_index()
    submissions_approved = df_submissions_status_index.loc[1].groupby(['site']).size().to_frame(
        'submissions_approved' + form_id).reset_index()
    submissions_flagged = df_submissions_status_index.loc[2].groupby(['site']).size().to_frame(
        'submissions_flagged' + form_id).reset_index()
    submissions_rejected = df_submissions_status_index.loc[3].groupby(['site']).size().to_frame(
        'submissions_rejected' + form_id).reset_index()
    df = df.merge(submissions_pending, on="site", how="left")
    df = df.merge(submissions_approved, on="site", how="left")
    df = df.merge(submissions_flagged, on="site", how="left")
    df = df.merge(submissions_rejected, on="site", how="left")

    df_reviews_old_status_index = df_reviews.set_index('old_status')

    approved_submissions = df_submissions_status_index.loc[1]
    df_flagged_or_rejected = df_reviews_old_status_index.loc[[2, 3]]
    approved_submissions_with_resolved = approved_submissions.assign(
        resolved=approved_submissions.pk.isin(df_flagged_or_rejected.finstance))
    approved_submissions_with_resolved_only = approved_submissions_with_resolved[
        approved_submissions_with_resolved["resolved"]]
    submissions_resolved_ever = approved_submissions_with_resolved_only.groupby(['site']).size().to_frame(
        'submissions_resolved_ever').reset_index()

    df = df.merge(submissions_resolved_ever, on="site", how="left")

    submissions_pending_ever = df_reviews_old_status_index.loc[0].groupby("site").size().to_frame('submissions_pending_ever' + form_id)
    submissions_approved_ever = df_reviews_old_status_index.loc[1].groupby("site").size().to_frame('submissions_approved_ever' + form_id)
    submissions_flagged_ever = df_reviews_old_status_index.loc[2].groupby("site").size().to_frame('submissions_flagged_ever' + form_id)
    submissions_rejected_ever = df_reviews_old_status_index.loc[3].groupby("site").size().to_frame('submissions_rejected_ever' + form_id)

    df = pd.concat([df, submissions_pending_ever], axis=1)
    df = pd.concat([df, submissions_approved_ever], axis=1)
    df = pd.concat([df, submissions_flagged_ever], axis=1)
    df = pd.concat([df, submissions_rejected_ever], axis=1)
    return df


def generate_answer_frame(form_id, question, df, df_sub_form_data):
    form_id = str(form_id)
    df_submissions_form_most_recent = df_sub_form_data.loc[df_sub_form_data.groupby('site').date.idxmax()]
    df_submissions_form_most_recent_question = df_submissions_form_most_recent[['site', question]]

    df_sub_form_data[question] = pd.to_numeric(
        df_sub_form_data[question], errors='coerce')

    average_value = df_sub_form_data.groupby('site')[question].mean().to_frame(form_id + question + '-average').reset_index()
    sum_value = df_sub_form_data.groupby('site')[question].sum().to_frame(form_id + question + '-sum').reset_index()
    max_value = df_sub_form_data.groupby('site')[question].max().to_frame(form_id + question + '-max').reset_index()
    min_value = df_sub_form_data.groupby('site')[question].min().to_frame(form_id + question + '-min').reset_index()
    count_value = df_sub_form_data.groupby('site')[question].size().to_frame(form_id + question + '-count').reset_index()
    count_value_distinct = df_sub_form_data.groupby('site')[question].nunique().to_frame(form_id + question + '-count-distinct').reset_index()
    common = df_sub_form_data.groupby('site')[question].apply(pd.Series.mode).to_frame(form_id + question + "-common").reset_index().head()
    df_question_distinct = df_sub_form_data.groupby(['site', question])['site', question].size().to_frame(
        form_id + question + 'dd').reset_index()
    df_question_distinct[form_id + question + "-distinct-sub"] = df_question_distinct[form_id + question + 'dd']

    df.merge(df_submissions_form_most_recent_question, on="site", how="left")
    df.merge(average_value, on="site", how="left")
    df.merge(sum_value, on="site", how="left")
    df.merge(max_value, on="site", how="left")
    df.merge(min_value, on="site", how="left")
    df.merge(count_value, on="site", how="left")
    df.merge(count_value_distinct, on="site", how="left")
    df.merge(common, on="site", how="left")
    df.merge(df_question_distinct, on="site", how="left")
    return df


def site_report(project_id):
    selected_metas = []
    selected_forms = []
    selected_forms_answer = []
    selected_questions = []
    query = Site.objects.filter(project_id=project_id).values(
        'id', 'identifier', 'name', 'current_progress', 'all_ma_ans')
    df = pd.DataFrame(list(query), columns=['id', 'identifier', 'name', 'current_progress', 'all_ma_ans'])
    df.columns = ['site', 'identifier', 'name', 'current_progress', 'all_ma_ans']
    meta_objects = [df, pd.DataFrame(df['all_ma_ans'].tolist())[selected_metas]]
    df = pd.concat(meta_objects, axis=1).drop('all_ma_ans', axis=1)

    query_submissions = FInstance.objects.filter(
        Q(project_fxf__project=project_id) |
        Q(site_fxf__site__project=project_id)
    ).values("pk", "site", "project_fxf", "form_status", "submitted_by", "date")
    df_submissions = pd.DataFrame(
        list(query_submissions), columns=["pk", "site", "project_fxf", "form_status", "submitted_by", "date"])
    query_reviews = InstanceStatusChanged.objects.all().values(
        "pk", "finstance__site", "new_status", "old_status", "user", "finstance")
    df_reviews = pd.DataFrame(list(query_reviews),
                              columns=["pk", "finstance__site", "new_status", "old_status", "user", "finstance"])
    df_reviews.columns = ["pk", "site", "new_status", "old_status", "user", "finstance"]

    df = generate_form_frame("site", df, df_submissions, df_reviews)

    df_submissions_form = df_submissions.set_index('project_fxf')

    # form submission status, approved, rejected etc
    for form_id in selected_forms:
        df = generate_form_frame(form_id, df, df_submissions_form.loc[form_id], df_reviews)

    query_submissions_form = FInstance.objects.filter(
        project_fxf__in=selected_forms_answer).select_related('instance').values("pk", "site", 'project_fxf', "date")
    df_submissions_form_answer = pd.DataFrame(list(query_submissions_form),
                                              columns=["pk", 'site', 'project_fxf', 'instance__json', "date"])
    df_submissions_form_answer = pd.concat([df_submissions_form_answer.drop('instance__json', axis=1),
                                  df_submissions_form_answer['instance__json'].apply(pd.Series)], axis=1)
    df_submissions_form_answer.set_index("project_fxf")

    # form submission answer of a question
    for form_id in selected_forms_answer:
        df_answer = df_submissions_form_answer.loc[form_id]
        for question in selected_questions:
            df = generate_answer_frame(form_id, question, df, df_answer)
