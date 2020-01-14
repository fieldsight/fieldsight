import pandas as pd
from django.contrib.auth.models import User
from django.db.models import Q

from onadata.apps.fieldsight.models import Site
from onadata.apps.fsforms.models import FInstance, InstanceStatusChanged
from onadata.apps.reporting.utils.common import separate_metrics, generate_default_metrices, generate_form_metrices
from onadata.apps.userrole.models import UserRole


def user_report(report_obj):
    project_id = report_obj.project_id
    attributes = report_obj.attributes
    filters = report_obj.filter
    default_metrics, individual_form_metrics, form_information_metrics, \
        user_metrics, site_info_metrics = separate_metrics(attributes)

    query = User.objects.filter(
        user_roles__project=project_id, user_roles__ended_at__isnull=project_id)\
        .distinct().values('pk', 'username', 'email')
    df = pd.DataFrame(list(query), columns=['pk', 'username', 'email'])
    df.columns = ['user', 'username', 'email']
    query_role = UserRole.objects.filter(
        ended_at__isnull=True, project=project_id).values("user", "site", "project", "region")
    df_role = pd.DataFrame(list(query_role), columns=["user", "site", "project", "region"])

    if "num_sites" in default_metrics:
        num_of_sites = df_role.groupby(['user']).agg({'site': lambda x: x.nunique()}).reset_index()
        num_of_sites.columns = ["user", "num_sites"]
        df = df.merge(num_of_sites, on="user", how="left")
    if "num_projects" in default_metrics:
        num_of_projects = df_role.groupby(['user']).agg({'project': lambda x: x.nunique()}).reset_index()
        num_of_projects.columns = ["user", "num_projects"]
        df = df.merge(num_of_projects, on="user", how="left")
    if "num_regions" in default_metrics:
        num_of_regions = df_role.groupby(['user']).agg({'region': lambda x: x.nunique()}).reset_index()
        num_of_regions.columns = ["user", "num_regions"]
        df = df.merge(num_of_regions, on="user", how="left")

    query_submissions = FInstance.objects.filter(
        Q(project_fxf__project=project_id) |
        Q(site_fxf__site__project=project_id)
    ).values("pk", "site", "project_fxf", "form_status", "submitted_by", "date")
    df_submissions = pd.DataFrame(
        list(query_submissions), columns=["pk", "site", "project_fxf", "form_status", "submitted_by", "date"])
    df_submissions.columns = ["pk", "site", "project_fxf", "form_status", "user", "date"]
    query_reviews = InstanceStatusChanged.objects.filter(
        Q(finstance__project_fxf__project=project_id) |
        Q(finstance__site_fxf__site__project=project_id)
    ).values(
        "pk", "finstance__site", "new_status", "old_status", "user", "finstance")
    df_reviews = pd.DataFrame(list(query_reviews),
                              columns=["pk", "new_status", "old_status", "user", "finstance"])
    df_reviews.columns = ["pk", "new_status", "old_status", "user", "finstance"]

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
        form_name = individual_form_name_dict[form_id]
        df = generate_form_metrices(form_name, df, form_submissions, df_reviews, metrices_list, "site")

    df = df.replace("NaN", 0)
    return df
