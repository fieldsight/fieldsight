import datetime

import pandas as pd
from onadata.apps.fieldsight.models import Site, Region, Project, SiteProgressHistory
from onadata.apps.fsforms.models import FInstance, InstanceStatusChanged
from onadata.apps.reporting.utils.common import separate_metrics


def time_report(report_obj):
    if not report_obj.type == 5:
        raise ValueError("report type must be time series for Time series report")
    project_id = report_obj.project_id
    attributes = report_obj.attributes
    filters = report_obj.filter
    default_metrics, individual_form_metrics, form_information_metrics, \
        user_metrics, site_info_metrics = separate_metrics(attributes)

    start_date = "01-03-2017"
    end_date = datetime.date.today().strftime("%d-%m-%Y")
    group_by = "daily"
    if group_by == "daily":
        date_index = pd.date_range(start_date, end_date, freq='D')
        df = pd.DataFrame({}, index=date_index)
        if "num_sites" in default_metrics:
            query = Site.objects.values('id', 'date_created')
            df_site = pd.DataFrame(list(query), columns=['id', 'date_created'])
            num_sites = df_site.groupby(pd.Grouper(key='date_created', freq='1D')).size().to_frame(
                "num_sites").reset_index()
            num_sites['date_only'] = num_sites.date_created.dt.date
            del num_sites['date_created']
            num_sites = num_sites.set_index('date_only')
            df = pd.concat([df, num_sites], axis=1)
        if "num_regions" in default_metrics:
            query = Region.objects.values('id', 'date_created')
            df_region = pd.DataFrame(list(query), columns=['id', 'date_created'])
            num_regions = df_region.groupby(pd.Grouper(key='date_created', freq='1D')).size().to_frame(
                "num_regions").reset_index()
            num_regions['date_only'] = num_regions.date_created.dt.date
            del num_regions['date_created']
            num_regions = num_regions.set_index('date_only')
            df = pd.concat([df, num_regions], axis=1)
        if "num_projects" in default_metrics:
            query = Project.objects.values('id', 'date_created')
            df_project = pd.DataFrame(list(query), columns=['id', 'date_created'])
            num_projects = df_project.groupby(pd.Grouper(key='date_created', freq='1D')).size().to_frame(
                "num_projects").reset_index()
            num_projects['date_only'] = num_projects.date_created.dt.date
            del num_projects['date_created']
            num_projects = num_projects.set_index('date_only')
            df = pd.concat([df, num_projects], axis=1)
        if "sites_visited" in default_metrics:
            site_visited_query = FInstance.objects.values('instance__date_created')
            df_site_visited = pd.DataFrame(list(site_visited_query), columns=['instance__date_created'])
            sites_visited = df_site_visited.groupby(pd.Grouper(
                key='instance__date_created', freq='1D')).size().to_frame("sites_visited").reset_index()
            sites_visited['date_only'] = sites_visited.instance__date_created.dt.date
            del sites_visited['instance__date_created']
            sites_visited = sites_visited.set_index('date_only')
            df = pd.concat([df, sites_visited], axis=1)

        if "sites_reviewed" in default_metrics:
            site_reviewed_query = InstanceStatusChanged.objects.values('date')
            df_site_reviewed = pd.DataFrame(list(site_reviewed_query), columns=['date'])
            sites_reviewed = df_site_reviewed.groupby(pd.Grouper(
                key='date', freq='1D')).size().to_frame("sites_reviewed").reset_index()
            sites_reviewed['date_only'] = sites_reviewed.date.dt.date
            del sites_reviewed['date']
            sites_reviewed = sites_reviewed.set_index('date_only')
            df = pd.concat([df, sites_reviewed], axis=1)

        if set(['progress_avg', 'progress_max', 'progress_min']).intersection(set(default_metrics)):
            progress_query = SiteProgressHistory.objects.filter().values('date', 'progress')
            df_progress = pd.DataFrame(list(progress_query), columns=['date', 'progress'])
            if "progress_avg" in default_metrics:
                progress_avg = df_progress.groupby(pd.Grouper(key='date', freq='1D')).mean()
                progress_avg.columns = ['progress_avg']
                df = pd.concat([df, progress_avg], axis=1)
            if "progress_max" in default_metrics:
                progress_max = df_progress.groupby(pd.Grouper(key='date', freq='1D')).max()
                progress_max.columns = ['progress_max']
                df = pd.concat([df, progress_max], axis=1)

            if "progress_min" in default_metrics:
                progress_min = df_progress.groupby(pd.Grouper(key='date', freq='1D')).min()
                progress_min.columns = ['progress_min']
                df = pd.concat([df, progress_min], axis=1)

        df = df.fillna(0)
        df.index = df.index.date
        df.index.name = "date"
        df = df.reset_index()
        return df




