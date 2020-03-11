import pandas as pd
import numpy as np
from django.contrib.auth.models import User
from django.db.models import Q

from onadata.apps.fieldsight.models import Site
from onadata.apps.fsforms.models import FInstance, InstanceStatusChanged
from onadata.apps.reporting.utils.common import separate_metrics, generate_default_metrices, generate_form_metrices, \
    ordered_columns_from_metrics
from onadata.apps.userrole.models import UserRole


def user_report(report_obj, preview=False):
    if not report_obj.type == 4:
        raise ValueError("report type must be user for user report")
    project_id = report_obj.project_id
    attributes = report_obj.attributes
    filters = report_obj.filter
    user_roles = filters.get('user_roles')
    report_user_roles_filters = []
    if user_roles:
        if isinstance(user_roles, list):
            [report_user_roles_filters.append(user['name']) for user in user_roles]
        elif isinstance(user_roles, dict):
            report_user_roles_filters.append(user_roles['name'])

    user_filter = {}
    user_roles_filter = {}
    instance_status_changed_filter = {}
    finstance_filter = {}

    user_filter['user_roles__project'] = project_id
    user_filter['user_roles__ended_at__isnull'] = True

    user_roles_filter['ended_at__isnull'] = True
    user_roles_filter['project'] = project_id

    if report_user_roles_filters:
        user_filter['user_roles__group__name__in'] = report_user_roles_filters
        user_roles_filter['group__name__in'] = report_user_roles_filters
        finstance_filter['submitted_by__user_roles__group__name__in'] = report_user_roles_filters
        finstance_filter['submitted_by__user_roles__ended_at__isnull'] = True
        instance_status_changed_filter['user__user_roles__group__name__in'] = report_user_roles_filters
        instance_status_changed_filter['user__user_roles__ended_at__isnull'] = True

    default_metrics, individual_form_metrics, form_information_metrics, \
        user_metrics, site_info_metrics = separate_metrics(attributes)

    if preview:
        query = User.objects.filter(**user_filter).distinct().values('pk', 'username', 'email')[:10]
    else:
        query = User.objects.filter(**user_filter).distinct().values('pk', 'username', 'email')
    df = pd.DataFrame(list(query), columns=['pk', 'username', 'email'])
    df.columns = ['user', 'username', 'email']

    if preview:
        query_role = UserRole.objects.filter(**user_roles_filter).values("user", "site", "project", "region")[:10]
    else:
        query_role = UserRole.objects.filter(**user_roles_filter).values("user", "site", "project", "region")

    df_role = pd.DataFrame(list(query_role), columns=["user", "site", "project", "region"])

    if "num_sites" in default_metrics:
        num_of_sites = df_role.groupby('user').site.count().to_frame("num_sites").reset_index()
        num_of_sites.columns = ["user", "num_sites"]
        df = df.merge(num_of_sites, on="user", how="left")
    if "num_projects" in default_metrics:
        num_projects = df_role.dropna(subset=['site', 'region']).groupby("user").project.count().to_frame(
            "num_projects").reset_index()
        df = df.merge(num_projects, on="user", how="left")
    if "num_regions" in default_metrics:
        # df_role[~np.isfinite(df_role['site'])]
        num_of_regions = df_role.dropna(subset=['site']).groupby("user").region.count().to_frame("num_regions").reset_index()
        df = df.merge(num_of_regions, on="user", how="left")

    if preview:
        query_submissions = FInstance.objects.filter(**finstance_filter).filter(
            Q(project_fxf__project=project_id) |
            Q(site_fxf__site__project=project_id)
        ).distinct().values("pk", "site", "project_fxf", "form_status", "submitted_by", "date",
                            "site__current_progress")[:10]
    else:
        query_submissions = FInstance.objects.filter(**finstance_filter).filter(
            Q(project_fxf__project=project_id) |
            Q(site_fxf__site__project=project_id)
        ).distinct().values("pk", "site", "project_fxf", "form_status", "submitted_by", "date",
                            "site__current_progress")

    df_submissions = pd.DataFrame(
        list(query_submissions), columns=["pk", "site", "project_fxf", "form_status", "submitted_by", "date",
                                          "site__current_progress"])
    df_submissions.columns = ["pk", "site", "project_fxf", "form_status", "user", "date", "progress"]

    if "progress_avg" in default_metrics:
        try:
            progress_avg = df_submissions.groupby('user').progress.mean().to_frame("progress_avg").reset_index()
            df = df.merge(progress_avg, on="user", how="left")
        except:
            df['progress_avg'] = 0

    if "progress_max" in default_metrics:
        try:
            progress_max = df_submissions.groupby('user').progress.max().to_frame("progress_max").reset_index()
            df = df.merge(progress_max, on="user", how="left")
        except:
            df['progress_max'] = 0

    if "progress_min" in default_metrics:
        try:
            progress_min = df_submissions.groupby('user').progress.min().to_frame("progress_min").reset_index()
            df = df.merge(progress_min, on="user", how="left")
        except:
            df['progress_min'] = 0

    if preview:
        query_reviews = InstanceStatusChanged.objects.filter(**instance_status_changed_filter).filter(
            Q(finstance__project_fxf__project=project_id) |
            Q(finstance__site_fxf__site__project=project_id)
        ).distinct().values(
            "pk", "finstance__site", "new_status", "old_status", "user", "finstance")[:10]
    else:
        query_reviews = InstanceStatusChanged.objects.filter(**instance_status_changed_filter).filter(
            Q(finstance__project_fxf__project=project_id) |
            Q(finstance__site_fxf__site__project=project_id)
        ).distinct().values(
            "pk", "finstance__site", "new_status", "old_status", "user", "finstance")
    df_reviews = pd.DataFrame(list(query_reviews),
                              columns=["pk", "new_status", "old_status", "user", "finstance", "finstance__project_fxf"])
    df_reviews.columns = ["pk", "new_status", "old_status", "user", "finstance", "finstance__project_fxf"]
    df_reviews_old_status_index = df_reviews.set_index('old_status')
    df_submissions_status_index = df_submissions.set_index('form_status')

    if "submissions_flagged_by_user" in default_metrics:
        try:
            _submissions = df_submissions_status_index.loc[2]
            submissions_flagged_by_user =_submissions.groupby(
                'user').size().to_frame("submissions_flagged_by_user").reset_index()
            df = df.merge(submissions_flagged_by_user, on="user", how="left")
        except:
            df["submissions_flagged_by_user"] = 0

    if "submissions_rejected_by_user" in default_metrics:
        try:
            _submissions = df_submissions_status_index.loc[1]
            submissions_rejected_by_user = _submissions.groupby(
                'user').size().to_frame("submissions_rejected_by_user").reset_index()
            df = df.merge(submissions_rejected_by_user, on="user", how="left")
        except:
            df["submissions_rejected_by_user"] = 0

    if "submissions_approved_by_user" in default_metrics:
        try:
            _submissions = df_submissions_status_index.loc[3]
            submissions_approved_by_user = _submissions.groupby(
                'user').size().to_frame("submissions_approved_by_user").reset_index()
            df = df.merge(submissions_approved_by_user, on="user", how="left")
        except:
            df["submissions_approved_by_user"] = 0

    if "submissions_resolved_by_user" in default_metrics:
        try:

            approved_submissions = df_submissions_status_index.loc[3]
            df_flagged_or_rejected = df_reviews_old_status_index.loc[[2, 1]]
            submissions_resolved_ever = df_flagged_or_rejected[
                df_flagged_or_rejected.finstance.isin(approved_submissions.pk)].groupby('user').size().to_frame(
                'submissions_resolved_by_user').reset_index()

            df = df.merge(submissions_resolved_ever, on="user", how="left")
        except:
            df['submissions_resolved_by_user'] = 0

    df = generate_default_metrices(df, df_submissions, df_reviews, default_metrics, "user")

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
        form_reviews = df_reviews[df_reviews.finstance__project_fxf == form_id]
        form_name = individual_form_name_dict[form_id]
        df = generate_form_metrices(form_name, df, form_submissions, form_reviews, metrices_list, "user")

    df = df.replace("NaN", 0)
    # reorder cols
    columns_name = ordered_columns_from_metrics(report_obj)  # ordered metrices codes
    # code to label column
    df = df[columns_name]
    return df
