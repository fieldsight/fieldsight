import datetime

import pandas as pd
from django.db.models import Q

from onadata.apps.fieldsight.models import Site, Region, Project, SiteProgressHistory
from onadata.apps.fsforms.models import FInstance, InstanceStatusChanged
from onadata.apps.reporting.utils.common import separate_metrics, ordered_columns_from_metrics
from onadata.apps.userrole.models import UserRole


def generate_form_metrices_time_report(form_name, df, df_submissions, df_reviews, metrices_list):
    form_name = form_name + "/"

    if "form_no_submissions" in metrices_list:
        form_no_submissions = df_submissions.groupby(pd.Grouper(key='date', freq='1D')).size().to_frame(
            form_name + 'form_no_submissions').reset_index()
        form_no_submissions['date_only'] = form_no_submissions.date.dt.date
        del form_no_submissions['date']
        form_no_submissions = form_no_submissions.set_index('date_only')
        df = pd.concat([df, form_no_submissions], axis=1)

    df_submissions_status_index = df_submissions.set_index('form_status')
    df_reviews_old_status_index = df_reviews.set_index('old_status')
    try:
        approved_submissions = df_submissions[df_submissions.new_status == 3]
        approved_submissions_with_resolved = approved_submissions.assign(
            resolved=approved_submissions.pk.isin(df_submissions_status_index.finstance))
        approved_submissions_with_resolved_only = approved_submissions_with_resolved[
            approved_submissions_with_resolved["resolved"]]
        submissions_resolved_ever = approved_submissions_with_resolved_only.groupby(pd.Grouper(
            key='date', freq='1D')).size().to_frame(form_name + "no_resolved_submissions_ever").reset_index()
        submissions_resolved_ever['date_only'] = submissions_resolved_ever.date.dt.date
        del submissions_resolved_ever['date']
        submissions_resolved_ever = submissions_resolved_ever.set_index('date_only')
        df = pd.concat([df, submissions_resolved_ever], axis=1)
    except:
        df['no_resolved_submissions_ever'] = 0

    if "form_no_submissions_reviewed" in metrices_list:
        try:
            submissions_pending_ever = df_reviews_old_status_index.groupby(pd.Grouper(
             key='date', freq='1D')).size().to_frame(form_name + "form_no_submissions_reviewed").reset_index()
            submissions_pending_ever['date_only'] = submissions_pending_ever.date.dt.date
            del submissions_pending_ever['date']
            submissions_pending_ever = submissions_pending_ever.set_index('date_only')
            df = pd.concat([df, submissions_pending_ever], axis=1)
        except:
            df[form_name + 'form_no_submissions_reviewed'] = 0

    if "form_submissions_approved_ever" in metrices_list:
        try:
            submissions_approved_ever = df_reviews_old_status_index.loc[3].groupby(pd.Grouper(
                key='date', freq='1D')).size().to_frame(form_name + "form_submissions_approved_ever").reset_index()
            submissions_approved_ever['date_only'] = submissions_approved_ever.date.dt.date
            del submissions_approved_ever['date']
            submissions_approved_ever = submissions_approved_ever.set_index('date_only')
            df = pd.concat([df, submissions_approved_ever], axis=1)
        except:
            df['form_submissions_approved_ever'] = 0

    if "form_no_submissions_flagged_ever" in metrices_list:
        try:
            form_no_submissions_flagged_ever = df_reviews_old_status_index.loc[2].groupby(pd.Grouper(
                key='date', freq='1D')).size().to_frame(form_name + "form_no_submissions_flagged_ever").reset_index()
            form_no_submissions_flagged_ever['date_only'] = form_no_submissions_flagged_ever.date.dt.date
            del form_no_submissions_flagged_ever['date']
            form_no_submissions_flagged_ever = form_no_submissions_flagged_ever.set_index('date_only')
            df = pd.concat([df, form_no_submissions_flagged_ever], axis=1)
        except:
            df['form_no_submissions_flagged_ever'] = 0

    if "form_submissions_rejected_ever" in metrices_list:
        try:
            form_submissions_rejected_ever = df_reviews_old_status_index.loc[1].groupby(pd.Grouper(
                key='date', freq='1D')).size().to_frame(form_name + "form_submissions_rejected_ever").reset_index()
            form_submissions_rejected_ever['date_only'] = form_submissions_rejected_ever.date.dt.date
            del form_submissions_rejected_ever['date']
            form_submissions_rejected_ever = form_submissions_rejected_ever.set_index('date_only')
            df = pd.concat([df, form_submissions_rejected_ever], axis=1)
        except:
            df['form_submissions_rejected_ever'] = 0
    return df


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
        query_role = UserRole.objects.filter().filter(
            project=report_obj.project_id,).values("group", "started_at", "ended_at")
        df_role = pd.DataFrame(list(query_role), columns=["group", "started_at", "ended_at"])
        active_df = df_role[~df_role.ended_at.isnull()]
        if 'active_users' in user_metrics:
            active_users = active_df.groupby(pd.Grouper(key='started_at', freq='1D')).size().to_frame(
                "active_users").reset_index()
            active_users['date_only'] = active_users.started_at.dt.date
            del active_users['started_at']
            active_users = active_users.set_index('date_only')
            df = pd.concat([df, active_users], axis=1)
        if 'no_of_site_supervisor' in user_metrics:
            users_site_sup = df_role[df_role.group == 4].groupby(pd.Grouper(key='started_at', freq='1D')).size().to_frame(
                "no_of_site_supervisor").reset_index()
            users_site_sup['date_only'] = users_site_sup.started_at.dt.date
            del users_site_sup['started_at']
            users_site_sup = users_site_sup.set_index('date_only')
            df = pd.concat([df, users_site_sup], axis=1)
        if 'no_of_site_reviewer' in user_metrics:
            users_site_rev = df_role[df_role.group == 3].groupby(pd.Grouper(key='started_at', freq='1D')).size().to_frame(
                "no_of_site_reviewer").reset_index()
            users_site_rev['date_only'] = users_site_rev.started_at.dt.date
            del users_site_rev['started_at']
            users_site_rev = users_site_rev.set_index('date_only')
            df = pd.concat([df, users_site_rev], axis=1)
        if 'no_of_active_site_supervisor' in user_metrics:
            active_users_site_sup = active_df[active_df.group == 4].groupby(pd.Grouper(key='started_at', freq='1D')).size().to_frame(
                "no_of_active_site_supervisor").reset_index()
            active_users_site_sup['date_only'] = active_users_site_sup.started_at.dt.date
            del active_users_site_sup['started_at']
            active_users_site_sup = active_users_site_sup.set_index('date_only')
            df = pd.concat([df, active_users_site_sup], axis=1)

        if 'no_of_active_site_reviewer' in user_metrics:
            active_users_site_rev = active_df[active_df.group == 3].groupby(pd.Grouper(key='started_at', freq='1D')).size().to_frame(
                "active_users_site_rev").reset_index()
            active_users_site_rev['date_only'] = active_users_site_rev.started_at.dt.date
            del active_users_site_rev['started_at']
            active_users_site_rev = active_users_site_rev.set_index('date_only')
            df = pd.concat([df, active_users_site_rev], axis=1)

        if 'no_of_project_manager' in user_metrics:
            active_users_project_manager = df_role[df_role.group == 2].groupby(pd.Grouper(key='started_at', freq='1D')).size().to_frame(
                "no_of_project_manager").reset_index()
            active_users_project_manager['date_only'] = active_users_project_manager.started_at.dt.date
            del active_users_project_manager['started_at']
            active_users_project_manager = active_users_project_manager.set_index('date_only')
            df = pd.concat([df, active_users_project_manager], axis=1)

        if 'no_of_project_donor' in user_metrics:
            no_of_project_donor = df_role[df_role.group == 7].groupby(pd.Grouper(key='started_at', freq='1D')).size().to_frame(
                "active_users_site_rev").reset_index()
            no_of_project_donor['date_only'] = no_of_project_donor.started_at.dt.date
            del no_of_project_donor['started_at']
            no_of_project_donor = no_of_project_donor.set_index('date_only')
            df = pd.concat([df, no_of_project_donor], axis=1)

        if 'no_of_active_project_manager' in user_metrics:
            no_of_active_project_manager = active_df[active_df.group == 2].groupby(pd.Grouper(key='started_at', freq='1D')).size().to_frame(
                "no_of_active_project_manager").reset_index()
            no_of_active_project_manager['date_only'] = no_of_active_project_manager.started_at.dt.date
            del no_of_active_project_manager['started_at']
            no_of_active_project_manager = no_of_active_project_manager.set_index('date_only')
            df = pd.concat([df, no_of_active_project_manager], axis=1)

        if 'no_of_active_project_donor' in user_metrics:
            no_of_active_project_donor = active_df[active_df.group == 7].groupby(pd.Grouper(key='started_at', freq='1D')).size().to_frame(
                "no_of_active_project_donor").reset_index()
            no_of_active_project_donor['date_only'] = no_of_active_project_donor.started_at.dt.date
            del no_of_active_project_donor['started_at']
            no_of_active_project_donor = no_of_active_project_donor.set_index('date_only')
            df = pd.concat([df, no_of_active_project_donor], axis=1)

        if 'no_of_active_region_supervisor' in user_metrics:
            no_of_active_region_supervisor = active_df[active_df.group == 9].groupby(pd.Grouper(key='started_at', freq='1D')).size().to_frame(
                "no_of_active_region_supervisor").reset_index()
            no_of_active_region_supervisor['date_only'] = no_of_active_region_supervisor.started_at.dt.date
            del no_of_active_region_supervisor['started_at']
            no_of_active_region_supervisor = no_of_active_region_supervisor.set_index('date_only')
            df = pd.concat([df, no_of_active_region_supervisor], axis=1)

        if 'no_of_active_region_reviewer' in user_metrics:
            no_of_active_region_reviewer = active_df[active_df.group == 10].groupby(pd.Grouper(key='started_at', freq='1D')).size().to_frame(
                "no_of_active_region_reviewer").reset_index()
            no_of_active_region_reviewer['date_only'] = no_of_active_region_reviewer.started_at.dt.date
            del no_of_active_region_reviewer['started_at']
            no_of_active_region_reviewer = no_of_active_region_reviewer.set_index('date_only')
            df = pd.concat([df, no_of_active_region_reviewer], axis=1)

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
                progress_avg.index = progress_avg.index.date

                df = pd.concat([df, progress_avg], axis=1)
            if "progress_max" in default_metrics:
                progress_max = df_progress.groupby(pd.Grouper(key='date', freq='1D')).max()
                progress_max.columns = ['progress_max']
                progress_max.index = progress_max.index.date
                df = pd.concat([df, progress_max], axis=1)

            if "progress_min" in default_metrics:
                progress_min = df_progress.groupby(pd.Grouper(key='date', freq='1D')).min()
                progress_min.columns = ['progress_min']
                progress_min.index = progress_min.index.date
                df = pd.concat([df, progress_min], axis=1)
            query_submissions = FInstance.objects.filter().filter(
                Q(project_fxf__project=report_obj.project_id) |
                Q(site_fxf__site__project=report_obj.project_id)
            ).values("pk",  "date", "instance__date_created", "form_status", "project_fxf")
            df_submissions = pd.DataFrame(
                list(query_submissions), columns=["pk", "date", "instance__date_created", "form_status", "project_fxf"])

            query_reviews = InstanceStatusChanged.objects.filter(
                finstance__project=report_obj.project_id, old_status__in=[2, 3]).filter(
                Q(finstance__project_fxf__project=project_id) |
                Q(finstance__site_fxf__site__project=project_id)
            ).values("old_status", "date", "finstance", "finstance__project_fxf")

            df_reviews = pd.DataFrame(list(query_reviews), columns=["old_status", "date", "finstance", "finstance__project_fxf"])

            if 'no_submissions' in default_metrics:
                df_no_submissions = df_submissions
                no_submissions = df_no_submissions.groupby(pd.Grouper(
                    key='instance__date_created', freq='1D')).size().to_frame("no_submissions").reset_index()
                no_submissions['date_only'] = no_submissions.instance__date_created.dt.date
                del no_submissions['instance__date_created']
                no_submissions = no_submissions.set_index('date_only')
                df = pd.concat([df, no_submissions], axis=1)

            if "no_pending_submissions_ever" in default_metrics:
                
                df_no_pending_submissions_ever = df_submissions[df_submissions.form_status == 0]
                no_pending_submissions_ever = df_no_pending_submissions_ever.groupby(pd.Grouper(
                    key='date', freq='1D')).size().to_frame("no_pending_submissions_ever").reset_index()
                no_pending_submissions_ever['date_only'] = no_pending_submissions_ever.date.dt.date
                del no_pending_submissions_ever['date']
                no_pending_submissions_ever = no_pending_submissions_ever.set_index('date_only')
                df = pd.concat([df, no_pending_submissions_ever], axis=1)

            if "no_approved_submissions_ever" in default_metrics:
                df_no_approved_submissions_ever = df_submissions[df_submissions.form_status == 3]
                no_approved_submissions_ever = df_no_approved_submissions_ever.groupby(pd.Grouper(
                    key='date', freq='1D')).size().to_frame("no_approved_submissions_ever").reset_index()
                no_approved_submissions_ever['date_only'] = no_approved_submissions_ever.date.dt.date
                del no_approved_submissions_ever['date']
                no_approved_submissions_ever = no_approved_submissions_ever.set_index('date_only')
                df = pd.concat([df, no_approved_submissions_ever], axis=1)
            if "no_flagged_submissions_ever" in default_metrics:
                df_no_flagged_submissions_ever = df_submissions[df_submissions.form_status == 3]
                no_flagged_submissions_ever = df_no_flagged_submissions_ever.groupby(pd.Grouper(
                    key='date', freq='1D')).size().to_frame("no_flagged_submissions_ever").reset_index()
                no_flagged_submissions_ever['date_only'] = no_flagged_submissions_ever.date.dt.date
                del no_flagged_submissions_ever['date']
                no_flagged_submissions_ever = no_flagged_submissions_ever.set_index('date_only')
                df = pd.concat([df, no_flagged_submissions_ever], axis=1)
            if "no_rejected_submissions_ever" in default_metrics:
                df_no_rejected_submissions_ever = df_submissions[df_submissions.form_status == 2]
                no_rejected_submissions_ever = df_no_rejected_submissions_ever.groupby(pd.Grouper(
                    key='date', freq='1D')).size().to_frame("no_rejected_submissions_ever").reset_index()
                no_rejected_submissions_ever['date_only'] = no_rejected_submissions_ever.date.dt.date
                del no_rejected_submissions_ever['date']
                no_rejected_submissions_ever = no_rejected_submissions_ever.set_index('date_only')
                df = pd.concat([df, no_rejected_submissions_ever], axis=1)

            if "no_resolved_submissions_ever" in default_metrics:
                try:

                    df_flagged_or_rejected = df_reviews.set_index('old_status')
                    approved_submissions = df_submissions[df_submissions.new_status == 3]
                    approved_submissions_with_resolved = approved_submissions.assign(
                        resolved=approved_submissions.pk.isin(df_flagged_or_rejected.finstance))
                    approved_submissions_with_resolved_only = approved_submissions_with_resolved[
                        approved_submissions_with_resolved["resolved"]]
                    submissions_resolved_ever = approved_submissions_with_resolved_only.groupby(pd.Grouper(
                        key='date', freq='1D')).size().to_frame("no_resolved_submissions_ever").reset_index()
                    submissions_resolved_ever['date_only'] = submissions_resolved_ever.date.dt.date
                    del submissions_resolved_ever['date']
                    submissions_resolved_ever = submissions_resolved_ever.set_index('date_only')
                    df = pd.concat([df, submissions_resolved_ever], axis=1)
                except:
                    df['no_resolved_submissions_ever'] = 0
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
                df = generate_form_metrices_time_report(form_name, df, form_submissions, form_reviews, metrices_list)
        columns_name = ordered_columns_from_metrics(report_obj)  # ordered metrices codes
        df = df[columns_name]
        df = df.fillna(0)
        df.index = df.index.date
        df.index.name = "date"
        df.reset_index(level="date", inplace=True)
        return df




