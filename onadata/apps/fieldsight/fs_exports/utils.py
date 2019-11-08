from datetime import date, timedelta

import pandas as pd
import numpy as np

from onadata.apps.fieldsight.models import Site, Project
from onadata.apps.fsforms.models import FInstance, InstanceStatusChanged


def site_report():
    query_sites = Site.objects.all().values("pk", "name", "identifier", "region", "project", "current_progress")
    query_submissions = FInstance.objects.all().values("pk", "site", "form_status", "submitted_by", "date")
    query_submissions_reviewed = InstanceStatusChanged.objects.all().values(
        "pk", "finstance__site", "new_status", "old_status", "user", "finstance")

    df_sites = pd.DataFrame(list(query_sites), columns=["pk", "name", "identifier", "region", "project", "current_progress"])
    df_sites.rename(columns={'pk': 'site'}, inplace=True)
    df_submissions = pd.DataFrame(list(query_submissions),
                                  columns=["pk", "site", "form_status", "submitted_by", "date"])
    df_submissions_reviewed = pd.DataFrame(list(query_submissions_reviewed),
                                           columns=["pk", "finstance__site", "new_status", "old_status", "user", "finstance"])
    df_submissions_reviewed.rename(columns={'finstance__site': 'site'}, inplace=True)

    no__of_submissions = df_submissions.groupby(['site']).size().to_frame('no__of_submissions').reset_index()
    no__of_pending_submissions = df_submissions[df_submissions['form_status'] == 0].groupby(['site']).size().to_frame('no__of_pending_submissions').reset_index()
    no__of_approved_submissions = df_submissions[df_submissions['form_status'] == 1].groupby(['site']).size().to_frame('no__of_approved_submissions').reset_index()
    no__of_flagged_submissions = df_submissions[df_submissions['form_status'] == 2].groupby(['site']).size().to_frame('no__of_flagged_submissions').reset_index()
    no__of_rejected_submissions = df_submissions[df_submissions['form_status'] == 3].groupby(['site']).size().to_frame('no__of_rejected_submissions').reset_index()

    no_of_reviews = df_submissions_reviewed.groupby(['site']).size().to_frame(
        'no_of_reviews').reset_index()
    no_of_submissions_reviewed = df_submissions_reviewed.finstance.groupby([df_submissions_reviewed.site]).nunique().to_frame(
        'no_of_submissions_reviewed').reset_index()

    no_of_submissions_flagged = df_submissions_reviewed[df_submissions_reviewed['new_status'] == 2].finstance.groupby(
        [df_submissions_reviewed.site]).nunique().to_frame('no_of_submissions_flagged').reset_index()

    no_of_submissions_approved = df_submissions_reviewed[df_submissions_reviewed['new_status'] == 1].finstance.groupby(
        [df_submissions_reviewed.site]).nunique().to_frame('no_of_submissions_approved').reset_index()
    no_of_submissions_rejected = df_submissions_reviewed[df_submissions_reviewed['new_status'] == 3].finstance.groupby(
        [df_submissions_reviewed.site]).nunique().to_frame('no_of_submissions_flagged').reset_index()

    # df_visits_per_site = df_submissions.groupby(['site'])['date'].apply(lambda s: s.dt.date.nunique()).to_frame('site_visited').reset_index() #slow
    df_visits_per_site = df_submissions.date.apply(lambda dt: dt.date()).groupby([df_submissions.site]).nunique().to_frame('site_visited').reset_index()
    df_site_with_site_visited = pd.merge(df_sites, df_visits_per_site, on='site', how="left", sort=False)


    df_site_with_site_visited_reviewed = pd.merge(
        df_site_with_site_visited, no_of_reviews, on='site', how="left", sort=False)
    # df_most_recent_submission = df_submissions.loc[df_submissions.groupby('site').date.idxmax()]
    # df_most_recent_submission = df_submissions.groupby('site').date.apply(lambda x: max(x)).to_frame('most_recent_submission').reset_index()
    df_most_recent_submission = df_submissions.groupby('site').date.max().to_frame('most_recent_submission').reset_index()
    # df_date_most_recent = df_most_recent_submission[['site', 'most_recent_submission']].copy()
    # df_status_most_recent = df_most_recent_submission[['site', 'form_status']].copy()
    # df_site_with_site_recent_submission = pd.merge(df_sites, df_site_with_site_visited_reviewed, on='site', how="left", sort=False)

    # resolved
    approved_submissions = df_submissions[df_submissions['form_status'] == 1]
    once_flaged_submission_history = df_submissions_reviewed[df_submissions_reviewed['new_status'] == 2]
    approved_submissions_with_resolved = approved_submissions.assign(resolved=approved_submissions.pk.isin(once_flaged_submission_history.finstance))

    approved_submissions_with_resolved_only = approved_submissions_with_resolved[
        approved_submissions_with_resolved["resolved"]]

    no_of_resolved_submissions_in_site = approved_submissions_with_resolved_only.groupby(['site']).size().to_frame('no_of_resolved').reset_index()

    submissions_resolved = once_flaged_submission_history.groupby('finstance').size().to_frame('no_of').reset_index()


    # history resolved
    resolved_history = df_submissions_reviewed[df_submissions_reviewed['new_status'] == 2][
        df_submissions_reviewed['old_status'] == 1]
    finstance_resolved_count = resolved_history.groupby('finstance').size().to_frame(
        'no__of_resolved_submissions').reset_index()

    submissions_with_resolved_count = pd.merge(df_submissions, finstance_resolved_count, left_on='pk', right_on='finstance', how='left', sort=False)
    submissions_with_resolved_count = submissions_with_resolved_count.fillna(0)
    df_sites['no_of_resolved'] = submissions_with_resolved_count.groupby(['site'])['no__of_resolved_submissions'].sum


    fieldsight_form_id = 73732
    df_submissions_per_form = df_submissions[df_submissions['project_fxf'] == fieldsight_form_id]

    #  add project_fxf in reviewed data
    df_submissions_reviewed["project_fxf"] = []
    df_submissions_reviewed_per_form = df_submissions_reviewed[df_submissions_reviewed['project_fxf'] == fieldsight_form_id]


    return df_sites


def project_map_data():
    query_project = Project.objects.select_related("organization").exclude(location__isnull=True).\
        values("pk", "name", "location", "address", "organization", "organization__country")
    df_project = pd.DataFrame(list(query_project), columns=["pk", "name", "location", "address", "organization", "organization__country"])

    query_site = Site.objects.values("pk", "project")
    df_site = pd.DataFrame(list(query_site), columns=["pk", "project"])

    query_submission = FInstance.objects.select_related("site", "instance").values("pk", "site__project", "form_status", "instance__date_created")
    df_submissions = pd.DataFrame(list(query_submission), columns=["pk", "site__project", "form_status", "instance__date_created"])

    df_project_site_count = df_site.groupby("project").size().to_frame("sites_count").reset_index()
    project_with_sites_count = pd.merge(df_project, df_project_site_count, how="left", left_on='pk', right_on="project",
                                        sort=False)
    del project_with_sites_count['project']
    last_wek = (date.today() - timedelta(days=7)).strftime("%Y-%m-%d")
    today = date.today().strftime("%Y-%m-%d")
    last_seven_days_submissions = df_submissions[(df_submissions['instance__date_created'] > last_wek) & (
                df_submissions['instance__date_created'] < today)].head()
    last_7_days_count = last_seven_days_submissions.groupby('site__project').size().to_frame(
        "submissions_in_last_7days").reset_index()
    project_site_7days = project_with_sites_count.merge(last_7_days_count, left_on="pk", right_on="site__project", how="left")
    del project_site_7days['site__project']
    approved_count = df_submissions[df_submissions['form_status'] == 3].groupby(
        'site__project').size().to_frame('approved_count').reset_index()
    pending_count = df_submissions[df_submissions['form_status'] == 0].groupby(
        'site__project').size().to_frame('pending_count').reset_index()
    project_site_7days_approved = project_site_7days.merge(approved_count, how='left', left_on='pk', right_on='site__project')
    del project_site_7days_approved['site__project']
    project_site_7days_approved_pending = project_site_7days_approved.merge(pending_count, how='left', left_on='pk', right_on='site__project')
    del project_site_7days_approved_pending['site__project']
    project_site_7days_approved_pending['latlng'] = project_site_7days_approved_pending.location.apply(lambda x: [x.y, x.x])
    del project_site_7days_approved_pending['location']
    project_site_7days_approved_pending.fillna(0, inplace=True)
    return project_site_7days_approved_pending


