import pandas as pd


def separate_metrics(attributes):
    default_metrics = []
    user_metrics_code = []
    default_metrics_code = []
    individual_form_metrics = []
    form_information_metrics = []
    user_metrics = []
    site_info_metrics = []
    for a in attributes:
        category = a.get('category')
        if category:
            if a['category'] == 'default':
                default_metrics.append(a)
            elif a['category'] == 'users':
                user_metrics.append(a)
        elif a.get('value'):
            value = a['value']
            if value.get('selectedQuestion'):
                if value['selectedQuestion']['form']['category'] == "form_information":
                    form_information_metrics.append(a)
                else:
                    raise ValueError
            elif value.get('selectedIndividualForm'):
                if value['selectedIndividualForm']['category'] == "individual_form":
                    individual_form_metrics.append(a)
                else:
                    raise ValueError
            elif value.get('category') == "site_information":
                site_info_metrics.append(a)

            else:
                raise ValueError
        else:
            raise ValueError
    for d in default_metrics:
        default_metrics_code.append(d['code'])
    for d in user_metrics:
        user_metrics_code.append(d['code'])
    return default_metrics_code, individual_form_metrics, form_information_metrics, user_metrics_code, site_info_metrics


def generate_default_metrices(df, df_submissions, df_reviews, metrices_list, report_type):
    if "sites_visited" in metrices_list:
        df_visits = df_submissions.date.apply(lambda dt: dt.date()).groupby(
            [df_submissions[report_type]]).nunique().to_frame('site_visited').reset_index()
        df = df.merge(df_visits, on=report_type, how="left")

    if "sites_reviewed" in metrices_list:
        df_reviews_count = df_reviews.groupby(report_type).size().to_frame('sites_reviewed').reset_index()
        df_reviews_count = df_reviews_count.replace("NAN", 0)

        df = df.merge(df_reviews_count, on=report_type, how="left")

    if "status_most_recent_submission" in metrices_list:
        df_mrs = df_submissions.loc[df_submissions.groupby(report_type).date.idxmax()][[report_type, 'form_status']]
        df_mrs.columns = [report_type, 'status_most_recent_submission']
        df = df.merge(df_mrs, on=report_type, how="left")

    if "no_submissions" in metrices_list:
        submissions_count = df_submissions.groupby([report_type]).size().to_frame('no_submissions').reset_index()
        df = df.merge(submissions_count, on=report_type, how="left")

    # no of submissions current
    df_submissions_status_index = df_submissions.set_index('form_status')
    if "no_pending_submissions_current" in metrices_list:
        try:
            submissions_pending = df_submissions_status_index.loc[0].groupby([report_type]).size().to_frame(
                'no_pending_submissions_current').reset_index()
            df = df.merge(submissions_pending, on=report_type, how="left")
        except:
            df['no_pending_submissions_current'] = 0
    if "no_approved_submissions_current" in metrices_list:
        try:
            submissions_approved = df_submissions_status_index.loc[1].groupby([report_type]).size().to_frame(
                'no_approved_submissions_current').reset_index()
            df = df.merge(submissions_approved, on=report_type, how="left")
        except:
            df['no_approved_submissions_current'] = 0
    if "no_flagged_submissions_current" in metrices_list:
        try:
            submissions_flagged = df_submissions_status_index.loc[2].groupby([report_type]).size().to_frame(
                'no_flagged_submissions_current').reset_index()
            df = df.merge(submissions_flagged, on=report_type, how="left")
        except:
            df['no_flagged_submissions_current'] = 0
    if "no_rejected_submissions_current" in metrices_list:
        try:
            submissions_rejected = df_submissions_status_index.loc[3].groupby([report_type]).size().to_frame(
                'no_rejected_submissions_current').reset_index()
            df = df.merge(submissions_rejected, on=report_type, how="left")
        except:
            df['no_rejected_submissions_current'] = 0

    df_reviews_old_status_index = df_reviews.set_index('old_status')
    if "no_resolved_submissions_ever" in metrices_list:
        try:
            approved_submissions = df_submissions_status_index.loc[1]
            df_flagged_or_rejected = df_reviews_old_status_index.loc[[2, 3]]
            approved_submissions_with_resolved = approved_submissions.assign(
                resolved=approved_submissions.pk.isin(df_flagged_or_rejected.finstance))
            approved_submissions_with_resolved_only = approved_submissions_with_resolved[
                approved_submissions_with_resolved["resolved"]]
            submissions_resolved_ever = approved_submissions_with_resolved_only.groupby([report_type]).size().to_frame(
                'no_resolved_submissions_ever').reset_index()

            df = df.merge(submissions_resolved_ever, on=report_type, how="left")
        except:
            df['no_resolved_submissions_ever'] = 0

    if "no_pending_submissions_ever" in metrices_list:
        try:
            submissions_pending_ever = df_reviews_old_status_index.loc[0].groupby(report_type).size().to_frame('no_pending_submissions_ever').reset_index()
            df = df.merge(submissions_pending_ever, on=report_type, how="left")
        except:
            df['no_pending_submissions_ever'] = 0

    if "no_approved_submissions_ever" in metrices_list:
        try:
            submissions_approved_ever = df_reviews_old_status_index.loc[1].groupby(report_type).size().to_frame('no_approved_submissions_ever').reset_index()
            df = df.merge(submissions_approved_ever, on=report_type, how="left")
        except:
            df['no_approved_submissions_ever'] = 0

    if "no_flagged_submissions_ever" in metrices_list:
        try:
            submissions_flagged_ever = df_reviews_old_status_index.loc[2].groupby(report_type).size().to_frame('no_flagged_submissions_ever').reset_index()
            df = df.merge(submissions_flagged_ever, on=report_type, how="left")
        except:
            df['no_flagged_submissions_ever'] = 0
    if "no_rejected_submissions_ever" in metrices_list:
        try:
            submissions_rejected_ever = df_reviews_old_status_index.loc[3].groupby(report_type).size().to_frame('no_rejected_submissions_ever').reset_index()
            df = df.merge(submissions_rejected_ever, on=report_type, how="left")
        except:
            df['no_rejected_submissions_ever'] = 0
    return df


def generate_form_metrices(form_name, df, df_submissions, df_reviews, metrices_list, report_type):
    form_name = form_name + "/"

    if "form_no_submissions" in metrices_list:
        submissions_count = df_submissions.groupby([report_type]).size().to_frame(form_name + 'form_no_submissions').reset_index()
        df = df.merge(submissions_count, on=report_type, how="left")

    df_submissions_status_index = df_submissions.set_index('form_status')
    if "form_no_pending_submissions_current" in metrices_list:
        try:
            submissions_pending = df_submissions_status_index.loc[0].groupby([report_type]).size().to_frame(
                form_name + 'form_no_pending_submissions_current').reset_index()
            df = df.merge(submissions_pending, on=report_type, how="left")
        except:
            df[form_name + 'no_pending_submissions_current'] = 0
    if "form_no_approved_submissions_current" in metrices_list:
        try:
            submissions_approved = df_submissions_status_index.loc[1].groupby([report_type]).size().to_frame(
                form_name + 'form_no_approved_submissions_current').reset_index()
            df = df.merge(submissions_approved, on=report_type, how="left")
        except:
            df[form_name + 'form_no_approved_submissions_current'] = 0
    if "form_no_flagged_submissions_current" in metrices_list:
        try:
            submissions_flagged = df_submissions_status_index.loc[2].groupby([report_type]).size().to_frame(
                form_name + 'form_no_flagged_submissions_current').reset_index()
            df = df.merge(submissions_flagged, on=report_type, how="left")
        except:
            df[form_name + 'form_no_flagged_submissions_current'] = 0
    if "form_no_rejected_submissions_current" in metrices_list:
        try:
            submissions_rejected = df_submissions_status_index.loc[3].groupby([report_type]).size().to_frame(
                form_name + 'form_no_rejected_submissions_current').reset_index()
            df = df.merge(submissions_rejected, on=report_type, how="left")
        except:
            df[form_name + 'form_no_rejected_submissions_current'] = 0

    df_reviews_old_status_index = df_reviews.set_index('old_status')
    if "form_submissions_resolutions_ever" in metrices_list:
        try:
            approved_submissions = df_submissions_status_index.loc[1]
            df_flagged_or_rejected = df_reviews_old_status_index.loc[[2, 3]]
            approved_submissions_with_resolved = approved_submissions.assign(
                resolved=approved_submissions.pk.isin(df_flagged_or_rejected.finstance))
            approved_submissions_with_resolved_only = approved_submissions_with_resolved[
                approved_submissions_with_resolved["resolved"]]
            submissions_resolved_ever = approved_submissions_with_resolved_only.groupby([report_type]).size().to_frame(
                form_name + 'form_submissions_resolutions_ever').reset_index()

            df = df.merge(submissions_resolved_ever, on=report_type, how="left")
        except:
            df[form_name + 'form_submissions_resolutions_ever'] = 0

    if "form_no_submissions_reviewed" in metrices_list:
        try:
            submissions_pending_ever = df_reviews_old_status_index.groupby(report_type).size().to_frame(form_name + 'form_no_submissions_reviewed').reset_index()
            df = df.merge(submissions_pending_ever, on=report_type, how="left")
        except:
            df[form_name + 'form_no_submissions_reviewed'] = 0

    if "form_submissions_approved_ever" in metrices_list:
        try:
            submissions_approved_ever = df_reviews_old_status_index.loc[1].groupby(report_type).size().to_frame(form_name +'form_submissions_approved_ever').reset_index()
            df = df.merge(submissions_approved_ever, on=report_type, how="left")
        except:
            df['form_submissions_approved_ever'] = 0

    if "form_no_submissions_flagged_ever" in metrices_list:
        try:
            submissions_flagged_ever = df_reviews_old_status_index.loc[2].groupby(report_type).size().to_frame(form_name +'form_no_submissions_flagged_ever').reset_index()
            df = df.merge(submissions_flagged_ever, on=report_type, how="left")
        except:
            df[form_name + 'form_no_submissions_flagged_ever'] = 0
    if "form_submissions_rejected_ever" in metrices_list:
        try:
            submissions_rejected_ever = df_reviews_old_status_index.loc[3].groupby(report_type).size().to_frame(form_name +'form_submissions_rejected_ever').reset_index()
            df = df.merge(submissions_rejected_ever, on=report_type, how="left")
        except:
            df[form_name + 'form_submissions_rejected_ever'] = 0
    return df


def generate_form_information(form_label, question, df, df_sub_form_data, metrice_codes, report_type):
    if "form_info_most_recent" in metrice_codes:
        if df_sub_form_data.empty:
            df[form_label + question + "/form_info_most_recent"] = "no submission"
        else:
            df_submissions_form_most_recent = df_sub_form_data.loc[df_sub_form_data.groupby(report_type).date.idxmax()]
            df_submissions_form_most_recent_question = df_submissions_form_most_recent[[report_type, question]]
            df_submissions_form_most_recent_question.columns = [form_label + question + "/form_info_most_recent"]
            df = df.merge(df_submissions_form_most_recent_question, on=report_type, how="left")
    if "form_info_most_common" in metrice_codes:
        if df_sub_form_data.empty:
            df[form_label + question + "/form_info_most_common"] = "no submission"
        else:
            common = df_sub_form_data.groupby(report_type)[question].apply(pd.Series.mode).to_frame(form_label + question + "form_info_most_common").reset_index()
            df = df.merge(common, on=report_type, how="left")
    # if "form_info_all_values" in metrice_codes:
    #     df_question_distinct = df_sub_form_data.groupby([report_type, question])[report_type, question].size().to_frame(
    #         form_label + question + 'dd').reset_index()
    #     df_question_distinct[form_label + question + "/form_info_all_values"] = df_question_distinct[form_label + question + 'dd']
    #     df = df.merge(df_question_distinct, on=report_type, how="left")

    if df_sub_form_data.empty:
        if "form_info_average" in metrice_codes:
            df[form_label + question + "/form_info_average"] = 0
        if "form_info_sum" in metrice_codes:
            df[form_label + question + "/form_info_sum"] = 0
        if "form_info_maximum" in metrice_codes:
            df[form_label + question + "/form_info_maximum"] = 0
        if "form_info_minimum" in metrice_codes:
            df[form_label + question + "/form_info_minimum"] = 0
        if "form_info_count" in metrice_codes:
            df[form_label + question + "/form_info_count"] = 0
        if "form_info_count_distinct" in metrice_codes:
            df[form_label + question + "/form_info_count_distinct"] = 0
    else:
        int_metrices = set(["form_info_average", "form_info_sum", "form_info_maximum", "form_info_minimum", "form_info_count", "form_info_count_distinct"])
        set_selected_metrices = set(metrice_codes)
        if int_metrices.intersection(set_selected_metrices):
            df_sub_form_data[question] = pd.to_numeric(df_sub_form_data[question], errors='coerce')
            if "form_info_average" in metrice_codes:
                average_value = df_sub_form_data.groupby(report_type)[question].mean().to_frame(form_label + question + '/form_info_average').reset_index()
                df = df.merge(average_value, on=report_type, how="left")
            if "form_info_sum" in metrice_codes:
                sum_value = df_sub_form_data.groupby(report_type)[question].sum().to_frame(form_label + question + '/form_info_sum').reset_index()
                df = df.merge(sum_value, on=report_type, how="left")
            if "form_info_maximum" in metrice_codes:
                max_value = df_sub_form_data.groupby(report_type)[question].max().to_frame(form_label + question + '/form_info_maximum').reset_index()
                df = df.merge(max_value, on=report_type, how="left")
            if "form_info_minimum" in metrice_codes:
                min_value = df_sub_form_data.groupby(report_type)[question].min().to_frame(form_label + question + '/form_info_minimum').reset_index()
                df = df.merge(min_value, on=report_type, how="left")
            if "form_info_count" in metrice_codes:
                count_value = df_sub_form_data.groupby(report_type)[question].size().to_frame(form_label + question + '/form_info_count').reset_index()
                df = df.merge(count_value, on=report_type, how="left")
            if "form_info_count_distinct" in metrice_codes:
                count_value_distinct = df_sub_form_data.groupby(report_type)[question].nunique().to_frame(
                    form_label + question + '/form_info_count_distinct').reset_index()
                df = df.merge(count_value_distinct, on=report_type, how="left")

    return df


def ordered_columns_from_metrics(attributes):
    columns = []
    for a in attributes:
        category = a.get('category')
        if category:
            if a['category'] == 'default':
                columns.append(a['code'])
            elif a['category'] == 'users':
                columns.append(a['code'])
        elif a.get('value'):
            value = a['value']
            if value.get('selectedQuestion'):
                if value['selectedQuestion']['form']['category'] == "form_information":
                    code = value['selectedQuestion']['code']
                    question = value['selectedQuestion']['name']
                    form_title = value['selectedForm']['title']
                    columns.append(form_title + "/" + question + "/" + code)
                else:
                    raise ValueError
            elif value.get('selectedIndividualForm'):
                code = value['selectedIndividualForm']['code']
                form_title = value['selectedForm']['title']
                columns.append(form_title + "/" + code)
            elif value.get('category') == "site_information":
                columns.append(a['code'])

            else:
                raise ValueError
        else:
            raise ValueError
    return columns
import pandas as pd


def separate_metrics(attributes):
    default_metrics = []
    user_metrics_code = []
    default_metrics_code = []
    individual_form_metrics = []
    form_information_metrics = []
    user_metrics = []
    site_info_metrics = []
    for a in attributes:
        category = a.get('category')
        if category:
            if a['category'] == 'default':
                default_metrics.append(a)
            elif a['category'] == 'users':
                user_metrics.append(a)
        elif a.get('value'):
            value = a['value']
            if value.get('selectedQuestion'):
                if value['selectedQuestion']['form']['category'] == "form_information":
                    form_information_metrics.append(a)
                else:
                    raise ValueError
            elif value.get('selectedIndividualForm'):
                if value['selectedIndividualForm']['category'] == "individual_form":
                    individual_form_metrics.append(a)
                else:
                    raise ValueError
            elif value.get('category') == "site_information":
                site_info_metrics.append(a)

            else:
                raise ValueError
        else:
            raise ValueError
    for d in default_metrics:
        default_metrics_code.append(d['code'])
    for d in user_metrics:
        user_metrics_code.append(d['code'])
    return default_metrics_code, individual_form_metrics, form_information_metrics, user_metrics_code, site_info_metrics


def generate_default_metrices(df, df_submissions, df_reviews, metrices_list, report_type):
    if "sites_visited" in metrices_list:
        df_visits = df_submissions.date.apply(lambda dt: dt.date()).groupby(
            [df_submissions[report_type]]).nunique().to_frame('site_visited').reset_index()
        df = df.merge(df_visits, on=report_type, how="left")

    if "sites_reviewed" in metrices_list:
        df_reviews_count = df_reviews.groupby(report_type).size().to_frame('sites_reviewed').reset_index()
        df_reviews_count = df_reviews_count.replace("NAN", 0)

        df = df.merge(df_reviews_count, on=report_type, how="left")

    if "status_most_recent_submission" in metrices_list:
        df_mrs = df_submissions.loc[df_submissions.groupby(report_type).date.idxmax()][[report_type, 'form_status']]
        df_mrs.columns = [report_type, 'status_most_recent_submission']
        df = df.merge(df_mrs, on=report_type, how="left")

    if "no_submissions" in metrices_list:
        submissions_count = df_submissions.groupby([report_type]).size().to_frame('no_submissions').reset_index()
        df = df.merge(submissions_count, on=report_type, how="left")

    # no of submissions current
    df_submissions_status_index = df_submissions.set_index('form_status')
    if "no_pending_submissions_current" in metrices_list:
        try:
            submissions_pending = df_submissions_status_index.loc[0].groupby([report_type]).size().to_frame(
                'no_pending_submissions_current').reset_index()
            df = df.merge(submissions_pending, on=report_type, how="left")
        except:
            df['no_pending_submissions_current'] = 0
    if "no_approved_submissions_current" in metrices_list:
        try:
            submissions_approved = df_submissions_status_index.loc[1].groupby([report_type]).size().to_frame(
                'no_approved_submissions_current').reset_index()
            df = df.merge(submissions_approved, on=report_type, how="left")
        except:
            df['no_approved_submissions_current'] = 0
    if "no_flagged_submissions_current" in metrices_list:
        try:
            submissions_flagged = df_submissions_status_index.loc[2].groupby([report_type]).size().to_frame(
                'no_flagged_submissions_current').reset_index()
            df = df.merge(submissions_flagged, on=report_type, how="left")
        except:
            df['no_flagged_submissions_current'] = 0
    if "no_rejected_submissions_current" in metrices_list:
        try:
            submissions_rejected = df_submissions_status_index.loc[3].groupby([report_type]).size().to_frame(
                'no_rejected_submissions_current').reset_index()
            df = df.merge(submissions_rejected, on=report_type, how="left")
        except:
            df['no_rejected_submissions_current'] = 0

    df_reviews_old_status_index = df_reviews.set_index('old_status')
    if "no_resolved_submissions_ever" in metrices_list:
        try:
            approved_submissions = df_submissions_status_index.loc[1]
            df_flagged_or_rejected = df_reviews_old_status_index.loc[[2, 3]]
            approved_submissions_with_resolved = approved_submissions.assign(
                resolved=approved_submissions.pk.isin(df_flagged_or_rejected.finstance))
            approved_submissions_with_resolved_only = approved_submissions_with_resolved[
                approved_submissions_with_resolved["resolved"]]
            submissions_resolved_ever = approved_submissions_with_resolved_only.groupby([report_type]).size().to_frame(
                'no_resolved_submissions_ever').reset_index()

            df = df.merge(submissions_resolved_ever, on=report_type, how="left")
        except:
            df['no_resolved_submissions_ever'] = 0

    if "no_pending_submissions_ever" in metrices_list:
        try:
            submissions_pending_ever = df_reviews_old_status_index.loc[0].groupby(report_type).size().to_frame('no_pending_submissions_ever').reset_index()
            df = df.merge(submissions_pending_ever, on=report_type, how="left")
        except:
            df['no_pending_submissions_ever'] = 0

    if "no_approved_submissions_ever" in metrices_list:
        try:
            submissions_approved_ever = df_reviews_old_status_index.loc[1].groupby(report_type).size().to_frame('no_approved_submissions_ever').reset_index()
            df = df.merge(submissions_approved_ever, on=report_type, how="left")
        except:
            df['no_approved_submissions_ever'] = 0

    if "no_flagged_submissions_ever" in metrices_list:
        try:
            submissions_flagged_ever = df_reviews_old_status_index.loc[2].groupby(report_type).size().to_frame('no_flagged_submissions_ever').reset_index()
            df = df.merge(submissions_flagged_ever, on=report_type, how="left")
        except:
            df['no_flagged_submissions_ever'] = 0
    if "no_rejected_submissions_ever" in metrices_list:
        try:
            submissions_rejected_ever = df_reviews_old_status_index.loc[3].groupby(report_type).size().to_frame('no_rejected_submissions_ever').reset_index()
            df = df.merge(submissions_rejected_ever, on=report_type, how="left")
        except:
            df['no_rejected_submissions_ever'] = 0
    return df


def generate_form_metrices(form_name, df, df_submissions, df_reviews, metrices_list, report_type):
    form_name = form_name + "/"

    if "form_no_submissions" in metrices_list:
        submissions_count = df_submissions.groupby([report_type]).size().to_frame(form_name + 'form_no_submissions').reset_index()
        df = df.merge(submissions_count, on=report_type, how="left")

    df_submissions_status_index = df_submissions.set_index('form_status')
    if "form_no_pending_submissions_current" in metrices_list:
        try:
            submissions_pending = df_submissions_status_index.loc[0].groupby([report_type]).size().to_frame(
                form_name + 'form_no_pending_submissions_current').reset_index()
            df = df.merge(submissions_pending, on=report_type, how="left")
        except:
            df[form_name + 'no_pending_submissions_current'] = 0
    if "form_no_approved_submissions_current" in metrices_list:
        try:
            submissions_approved = df_submissions_status_index.loc[1].groupby([report_type]).size().to_frame(
                form_name + 'form_no_approved_submissions_current').reset_index()
            df = df.merge(submissions_approved, on=report_type, how="left")
        except:
            df[form_name + 'form_no_approved_submissions_current'] = 0
    if "form_no_flagged_submissions_current" in metrices_list:
        try:
            submissions_flagged = df_submissions_status_index.loc[2].groupby([report_type]).size().to_frame(
                form_name + 'form_no_flagged_submissions_current').reset_index()
            df = df.merge(submissions_flagged, on=report_type, how="left")
        except:
            df[form_name + 'form_no_flagged_submissions_current'] = 0
    if "form_no_rejected_submissions_current" in metrices_list:
        try:
            submissions_rejected = df_submissions_status_index.loc[3].groupby([report_type]).size().to_frame(
                form_name + 'form_no_rejected_submissions_current').reset_index()
            df = df.merge(submissions_rejected, on=report_type, how="left")
        except:
            df[form_name + 'form_no_rejected_submissions_current'] = 0

    df_reviews_old_status_index = df_reviews.set_index('old_status')
    if "form_submissions_resolutions_ever" in metrices_list:
        try:
            approved_submissions = df_submissions_status_index.loc[1]
            df_flagged_or_rejected = df_reviews_old_status_index.loc[[2, 3]]
            approved_submissions_with_resolved = approved_submissions.assign(
                resolved=approved_submissions.pk.isin(df_flagged_or_rejected.finstance))
            approved_submissions_with_resolved_only = approved_submissions_with_resolved[
                approved_submissions_with_resolved["resolved"]]
            submissions_resolved_ever = approved_submissions_with_resolved_only.groupby([report_type]).size().to_frame(
                form_name + 'form_submissions_resolutions_ever').reset_index()

            df = df.merge(submissions_resolved_ever, on=report_type, how="left")
        except:
            df[form_name + 'form_submissions_resolutions_ever'] = 0

    if "form_no_submissions_reviewed" in metrices_list:
        try:
            submissions_pending_ever = df_reviews_old_status_index.groupby(report_type).size().to_frame(form_name + 'form_no_submissions_reviewed').reset_index()
            df = df.merge(submissions_pending_ever, on=report_type, how="left")
        except:
            df[form_name + 'form_no_submissions_reviewed'] = 0

    if "form_submissions_approved_ever" in metrices_list:
        try:
            submissions_approved_ever = df_reviews_old_status_index.loc[1].groupby(report_type).size().to_frame(form_name +'form_submissions_approved_ever').reset_index()
            df = df.merge(submissions_approved_ever, on=report_type, how="left")
        except:
            df['form_submissions_approved_ever'] = 0

    if "form_no_submissions_flagged_ever" in metrices_list:
        try:
            submissions_flagged_ever = df_reviews_old_status_index.loc[2].groupby(report_type).size().to_frame(form_name +'form_no_submissions_flagged_ever').reset_index()
            df = df.merge(submissions_flagged_ever, on=report_type, how="left")
        except:
            df[form_name + 'form_no_submissions_flagged_ever'] = 0
    if "form_submissions_rejected_ever" in metrices_list:
        try:
            submissions_rejected_ever = df_reviews_old_status_index.loc[3].groupby(report_type).size().to_frame(form_name +'form_submissions_rejected_ever').reset_index()
            df = df.merge(submissions_rejected_ever, on=report_type, how="left")
        except:
            df[form_name + 'form_submissions_rejected_ever'] = 0
    return df


def generate_form_information(form_label, question, df, df_sub_form_data, metrice_codes, report_type):
    if "form_info_most_recent" in metrice_codes:
        if df_sub_form_data.empty:
            df[form_label + question + "/form_info_most_recent"] = "no submission"
        else:
            df_submissions_form_most_recent = df_sub_form_data.loc[df_sub_form_data.groupby(report_type).date.idxmax()]
            df_submissions_form_most_recent_question = df_submissions_form_most_recent[[report_type, question]]
            df_submissions_form_most_recent_question.columns = [form_label + question + "/form_info_most_recent"]
            df = df.merge(df_submissions_form_most_recent_question, on=report_type, how="left")
    if "form_info_most_common" in metrice_codes:
        if df_sub_form_data.empty:
            df[form_label + question + "/form_info_most_common"] = "no submission"
        else:
            common = df_sub_form_data.groupby(report_type)[question].apply(pd.Series.mode).to_frame(form_label + question + "form_info_most_common").reset_index()
            df = df.merge(common, on=report_type, how="left")
    # if "form_info_all_values" in metrice_codes:
    #     df_question_distinct = df_sub_form_data.groupby([report_type, question])[report_type, question].size().to_frame(
    #         form_label + question + 'dd').reset_index()
    #     df_question_distinct[form_label + question + "/form_info_all_values"] = df_question_distinct[form_label + question + 'dd']
    #     df = df.merge(df_question_distinct, on=report_type, how="left")

    if df_sub_form_data.empty:
        if "form_info_average" in metrice_codes:
            df[form_label + question + "/form_info_average"] = 0
        if "form_info_sum" in metrice_codes:
            df[form_label + question + "/form_info_sum"] = 0
        if "form_info_maximum" in metrice_codes:
            df[form_label + question + "/form_info_maximum"] = 0
        if "form_info_minimum" in metrice_codes:
            df[form_label + question + "/form_info_minimum"] = 0
        if "form_info_count" in metrice_codes:
            df[form_label + question + "/form_info_count"] = 0
        if "form_info_count_distinct" in metrice_codes:
            df[form_label + question + "/form_info_count_distinct"] = 0
    else:
        int_metrices = set(["form_info_average", "form_info_sum", "form_info_maximum", "form_info_minimum", "form_info_count", "form_info_count_distinct"])
        set_selected_metrices = set(metrice_codes)
        if int_metrices.intersection(set_selected_metrices):
            df_sub_form_data[question] = pd.to_numeric(df_sub_form_data[question], errors='coerce')
            if "form_info_average" in metrice_codes:
                average_value = df_sub_form_data.groupby(report_type)[question].mean().to_frame(form_label + question + '/form_info_average').reset_index()
                df = df.merge(average_value, on=report_type, how="left")
            if "form_info_sum" in metrice_codes:
                sum_value = df_sub_form_data.groupby(report_type)[question].sum().to_frame(form_label + question + '/form_info_sum').reset_index()
                df = df.merge(sum_value, on=report_type, how="left")
            if "form_info_maximum" in metrice_codes:
                max_value = df_sub_form_data.groupby(report_type)[question].max().to_frame(form_label + question + '/form_info_maximum').reset_index()
                df = df.merge(max_value, on=report_type, how="left")
            if "form_info_minimum" in metrice_codes:
                min_value = df_sub_form_data.groupby(report_type)[question].min().to_frame(form_label + question + '/form_info_minimum').reset_index()
                df = df.merge(min_value, on=report_type, how="left")
            if "form_info_count" in metrice_codes:
                count_value = df_sub_form_data.groupby(report_type)[question].size().to_frame(form_label + question + '/form_info_count').reset_index()
                df = df.merge(count_value, on=report_type, how="left")
            if "form_info_count_distinct" in metrice_codes:
                count_value_distinct = df_sub_form_data.groupby(report_type)[question].nunique().to_frame(
                    form_label + question + '/form_info_count_distinct').reset_index()
                df = df.merge(count_value_distinct, on=report_type, how="left")

    return df


def ordered_columns_from_metrics(attributes):
    columns = []
    for a in attributes:
        category = a.get('category')
        if category:
            if a['category'] == 'default':
                columns.append(a['code'])
            elif a['category'] == 'users':
                columns.append(a['code'])
        elif a.get('value'):
            value = a['value']
            if value.get('selectedQuestion'):
                if value['selectedQuestion']['form']['category'] == "form_information":
                    code = value['selectedQuestion']['form']['code']
                    question = value['selectedQuestion']['name']
                    form_title = value['selectedForm']['title']
                    columns.append(form_title + "/" + question + "/" + code)
                else:
                    raise ValueError
            elif value.get('selectedIndividualForm'):
                code = value['selectedIndividualForm']['code']
                form_title = value['selectedForm']['title']
                columns.append(form_title + "/" + code)
            elif value.get('category') == "site_information":
                columns.append(a['code'])

            else:
                raise ValueError
        else:
            raise ValueError
    return columns
