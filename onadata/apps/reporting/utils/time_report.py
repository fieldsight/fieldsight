import datetime

import pandas as pd
from onadata.apps.fieldsight.models import Site
from onadata.apps.reporting.utils.common import separate_metrics


def time_report(report_obj):
    if not report_obj.type == 5:
        raise ValueError("report type must be time series for Time series report")
    project_id = report_obj.project_id
    attributes = report_obj.attributes
    filters = report_obj.filter
    default_metrics, individual_form_metrics, form_information_metrics, \
        user_metrics, site_info_metrics = separate_metrics(attributes)
    query = Site.objects.values('id', 'date_created')
    df_site = pd.DataFrame(list(query), columns=['id', 'date_created'])
    start_date = "01-06-2016"
    end_date = datetime.date.today().strftime("%d-%m-%Y")
    group_by = "daily"
    if group_by == "daily":
        date_index = pd.date_range(start_date, end_date, freq='D')
        df = pd.DataFrame({}, index=date_index)
        if "num_sites" in default_metrics:
            num_sites = df_site.groupby(pd.Grouper(key='date_created', freq='1D')).size().to_frame("num_sites").reset_index()
            num_sites['date_only'] = num_sites.date_created.dt.date
            num_sites = num_sites.set_index('date_only')
            df = pd.concat([df, num_sites], axis=1)
        return df




