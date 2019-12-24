import pandas as pd
from django.contrib.auth.models import User
from django.db.models import Q

from onadata.apps.fieldsight.models import Site
from onadata.apps.fsforms.models import FInstance, InstanceStatusChanged
from onadata.apps.userrole.models import UserRole


def generate_form_metrices(form_id, df, df_submissions, df_reviews):
    form_id = str(form_id)
    df_visits = df_submissions.date.apply(lambda dt: dt.date()).groupby(
        [df_submissions.user]).nunique().to_frame('site_visited' + form_id).reset_index()
    df = df.merge(df_visits, on="user", how="left")

    df_reviews_count = df_reviews.groupby('user').size().to_frame('no_of_reviews' + form_id).reset_index()
    df_reviews_count = df_reviews_count.replace("NAN", 0)

    df = df.merge(df_reviews_count, on="user", how="left")

    # status of most recent submission
    df_mrs = df_submissions.loc[df_submissions.groupby('user').date.idxmax()][['user', 'form_status']]
    df_mrs.columns = ['user', 'status_of_most_recent_submission' + form_id]
    df = df.merge(df_mrs, on="user", how="left")

    # no of submissions
    submissions_count = df_submissions.groupby(['user']).size().to_frame('submissions_count' + form_id).reset_index()
    df = df.merge(submissions_count, on="user", how="left")

    # no of submissions current
    df_submissions_status_index = df_submissions.set_index('form_status')
    try:
        submissions_pending = df_submissions_status_index.loc[0].groupby(['user']).size().to_frame(
            'submissions_pending' + form_id).reset_index()
        df = df.merge(submissions_pending, on="user", how="left")
    except:
        df['submissions_pending' + form_id] = 0
    try:
        submissions_approved = df_submissions_status_index.loc[1].groupby(['user']).size().to_frame(
            'submissions_approved' + form_id).reset_index()
        df = df.merge(submissions_approved, on="user", how="left")
    except:
        df['submissions_approved' + form_id] = 0
    try:
        submissions_flagged = df_submissions_status_index.loc[2].groupby(['user']).size().to_frame(
            'submissions_flagged' + form_id).reset_index()
        df = df.merge(submissions_flagged, on="user", how="left")
    except:
        df['submissions_flagged' + form_id] = 0
    try:
        submissions_rejected = df_submissions_status_index.loc[3].groupby(['user']).size().to_frame(
            'submissions_rejected' + form_id).reset_index()
        df = df.merge(submissions_rejected, on="user", how="left")
    except:
        df['submissions_rejected' + form_id] = 0

    df_reviews_old_status_index = df_reviews.set_index('old_status')
    try:
        approved_submissions = df_submissions_status_index.loc[1]
        df_flagged_or_rejected = df_reviews_old_status_index.loc[[2, 3]]
        approved_submissions_with_resolved = approved_submissions.assign(
            resolved=approved_submissions.pk.isin(df_flagged_or_rejected.finstance))
        approved_submissions_with_resolved_only = approved_submissions_with_resolved[
            approved_submissions_with_resolved["resolved"]]
        submissions_resolved_ever = approved_submissions_with_resolved_only.groupby(['user']).size().to_frame(
            'submissions_resolved_ever' + form_id).reset_index()

        df = df.merge(submissions_resolved_ever, on="user", how="left")
    except:
        df['submissions_resolved_ever' + form_id] = 0

    try:
        submissions_pending_ever = df_reviews_old_status_index.loc[0].groupby("user").size().to_frame('submissions_pending_ever' + form_id).reset_index()
        df = df.merge(submissions_pending_ever, on="user", how="left")
    except:
        df['submissions_pending_ever' + form_id] = 0

    try:
        submissions_approved_ever = df_reviews_old_status_index.loc[1].groupby("user").size().to_frame('submissions_approved_ever' + form_id).reset_index()
        df = df.merge(submissions_approved_ever, on="user", how="left")
    except:
        df['submissions_approved_ever' + form_id] = 0


    try:
        submissions_flagged_ever = df_reviews_old_status_index.loc[2].groupby("user").size().to_frame('submissions_flagged_ever' + form_id).reset_index()
        df = df.merge(submissions_flagged_ever, on="user", how="left")
    except:
        df['submissions_flagged_ever' + form_id] = 0
    try:
        submissions_rejected_ever = df_reviews_old_status_index.loc[3].groupby("user").size().to_frame('submissions_rejected_ever' + form_id).reset_index()
        df = df.merge(submissions_rejected_ever, on="user", how="left")
    except:
        df['submissions_rejected_ever' + form_id] = 0
    return df


def user_report(project_id):
    form_metrics = {'form_id': 73732, 'metrices': []}
    query = User.objects.all().values('pk', 'username', 'email')
    df = pd.DataFrame(list(query), columns=['pk', 'username', 'email'])
    df.columns = ['user', 'username', 'email']
    query_role = UserRole.objects.filter(
        ended_at__isnull=True, project__isnull=False).values("user", "site", "project", "region")
    df_role = pd.DataFrame(list(query_role), columns=["user", "site", "project", "region"])

    num_of_sites = df_role.groupby('user')['site'].size().to_frame("num_of_sites").reset_index()
    num_of_projects = df_role.groupby('user')['project'].size().to_frame("num_of_projects").reset_index()
    num_of_regions = df_role.groupby('user')['region'].size().to_frame("num_of_regions").reset_index()
    df = df.merge(num_of_sites, on="user", how="left")
    df = df.merge(num_of_projects, on="user", how="left")
    df = df.merge(num_of_regions, on="user", how="left")

    query_submissions = FInstance.objects.filter(
        Q(project_fxf__project=project_id) |
        Q(site_fxf__site__project=project_id)
    ).values("pk", "site", "project_fxf", "form_status", "submitted_by", "date")
    df_submissions = pd.DataFrame(
        list(query_submissions), columns=["pk","site", "project_fxf", "form_status", "submitted_by", "date"])
    df_submissions.columns = ["pk", "site", "project_fxf", "form_status", "user", "date"]
    query_reviews = InstanceStatusChanged.objects.filter(
        Q(finstance__project_fxf__project=project_id) |
        Q(finstance__site_fxf__site__project=project_id)
    ).values(
        "pk", "finstance__site", "new_status", "old_status", "user", "finstance")
    df_reviews = pd.DataFrame(list(query_reviews),
                              columns=["pk", "new_status", "old_status", "user", "finstance"])
    df_reviews.columns = ["pk", "new_status", "old_status", "user", "finstance"]

    df = generate_form_metrices("_user", df, df_submissions, df_reviews)

    form_submissions = df_submissions[df_submissions.project_fxf == form_metrics['form_id']]
    df = generate_form_metrices(form_metrics['form_id'], df, form_submissions, df_reviews)

    query_site = Site.objects.filter(project_id=project_id).values('pk', 'current_progress')
    df_site = pd.DataFrame(list(query_site), columns=['pk', 'current_progress'])
    df_site.columns = ["site", "progress"]

    df_submissions_with_progress = df_submissions.merge(df_site, on="site", how="left")
    progress_average = df_submissions_with_progress.groupby('user').progress.mean().to_frame('progress_average')
    progress_max = df_submissions_with_progress.groupby('max').progress.mean().to_frame('progress_max')
    progress_min = df_submissions_with_progress.groupby('min').progress.mean().to_frame('progress_min')
    df = df.merge(progress_average, on="user", how="left")
    df = df.merge(progress_max, on="user", how="left")
    df = df.merge(progress_min, on="user", how="left")

    approved_submissions = df_submissions[df_submissions.form_status == 1]
    df_flagged_or_rejected = df_reviews[df_reviews.new_status.isin([2, 3])]

    approved_submissions_with_resolved = approved_submissions.assign(
        resolved=approved_submissions.pk.isin(df_flagged_or_rejected.finstance))
    approved_submissions_with_resolved_only = approved_submissions_with_resolved[
        approved_submissions_with_resolved["resolved"]]
    submission_resolves = approved_submissions_with_resolved_only.groupby(['user']).size().to_frame(
        'submission_resolves').reset_index()

    submission_approved = df_reviews[df_reviews.new_status == 1].groupby('user').size().to_frame('submission_approvals').reset_index()
    submission_flags = df_reviews[df_reviews.new_status == 2].groupby('user').size().to_frame('submission_flags').reset_index()
    submission_rejects = df_reviews[df_reviews.new_status == 3].groupby('user').size().to_frame('submission_rejects').reset_index()

    df = df.merge(submission_resolves, on="user", how="left")
    df = df.merge(submission_approved, on="user", how="left")
    df = df.merge(submission_flags, on="user", how="left")
    df = df.merge(submission_rejects, on="user", how="left")

    df = df.replace("NaN", 0)
    return df
