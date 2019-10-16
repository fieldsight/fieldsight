import pandas as pd
import numpy as np

from onadata.apps.fieldsight.models import Site
from onadata.apps.fsforms.models import FInstance, InstanceStatusChanged


def site_report():
    query_sites = Site.objects.all().values("pk", "name", "identifier", "region", "project")
    query_submissions = FInstance.objects.all().values("pk", "site", "form_status", "submitted_by")
    query_submissions_reviewed = InstanceStatusChanged.objects.all().values(
        "pk", "finstance__site", "new_status", "old_status", "user")

    df_sites = pd.DataFrame(list(query_sites), columns=["pk", "name", "identifier", "region", "project"])
    df_sites.rename(columns={'pk': 'site'}, inplace=True)
    df_submissions = pd.DataFrame(list(query_submissions),
                                  columns=["pk", "site", "form_status", "submitted_by"])
    df_submissions_reviewed = pd.DataFrame(list(query_submissions_reviewed),
                                           columns=["pk", "finstance__site", "new_status", "old_status", "user"])
    df_submissions_reviewed.rename(columns={'finstance__site': 'site'}, inplace=True)

    df_submission_per_site = df_submissions.groupby(['site']).size().to_frame('site_visited').reset_index()
    df_site_with_site_visited = pd.merge(df_sites, df_submission_per_site, left_on='site', right_on='site')

    df_reviewed_per_site = df_submissions_reviewed.groupby(['site']).size().to_frame(
        'site_reviewed').reset_index()
    df_site_with_site_visited_reviewed = pd.merge(
        df_site_with_site_visited, df_reviewed_per_site, left_on='site', right_on='site')
    return df_site_with_site_visited_reviewed

