import json

import pandas as pd

import datetime
from django.core.files.temp import NamedTemporaryFile

from django.db.models import Sum, Case, When, IntegerField
from django.conf import settings

from onadata.apps.fieldsight.models import Project, Site
from onadata.apps.fsforms.models import FInstance, FieldSightXF
from onadata.apps.reporting.utils.site_report import site_report
from onadata.apps.reporting.utils.time_report import time_report
from onadata.apps.reporting.utils.user_report import user_report

form_status_map = ["Pending", "Rejected", "Flagged", "Approved"]

group_delimiter = '/'


def site_information(project_id):
    project = Project.objects.get(pk=project_id)
    values = []
    header_row = ['identifier', 'name', 'type', 'phone',
                  'address',
                  'public_desc', 'additional_desc', 'latitude', 'longitude',
                  'progress', 'root_site_identifier']
    if project.cluster_sites:
        header_row.append('region_identifier')
    meta_ques = project.site_meta_attributes
    for question in meta_ques:
        if not question['question_type'] == 'Link':
            header_row.append(question['question_name'])
    values.append(header_row)
    sites = Site.objects.filter(project=project_id)
    for site in sites.select_related('region').iterator():
        row = [site.identifier,
             site.name,
             site.type.identifier if site.type else "",
             site.phone,
             site.address,
             site.public_desc, site.additional_desc, site.latitude,
             site.longitude, site.current_progress,
             site.site.identifier if site.site else ""]
        if project.cluster_sites:
            row.append(site.region.identifier if site.region else "")
        meta_ans = site.all_ma_ans
        for question in meta_ques:
            if not question['question_type'] == 'Link':
                # question is not draw from another project
                question_name = question['question_name']
                row.append(meta_ans.get(question_name, ""))
        values.append(row)

    return values


def progress_information(project_id):
    project = Project.objects.get(pk=project_id)
    data = []
    ss_index = []
    form_ids = []
    stages_rows = []
    head_row = ["Site ID", "Name", "Region ID", "Address", "Latitude",
                "longitude", "Status", "Progress"]

    query = {}

    stages = project.stages.filter(stage__isnull=True)
    for stage in stages:
        sub_stages = stage.parent.filter(stage_forms__isnull=False)
        if len(sub_stages):
            head_row.append("Stage :" + stage.name)
            stages_rows.append("Stage :" + stage.name)
            ss_index.append(str(""))
            for ss in sub_stages:
                head_row.append("Sub Stage :" + ss.name)
                ss_index.append(str(ss.stage_forms.id))
                form_ids.append(str(ss.stage_forms.id))
                query[str(ss.stage_forms.id)] = Sum(
                    Case(
                        When(
                            site_instances__project_fxf_id=ss.stage_forms.id,
                            then=1),
                        default=0, output_field=IntegerField()
                    ))

    query['flagged'] = Sum(
        Case(
            When(site_instances__form_status=2,
                 site_instances__project_fxf_id__in=form_ids, then=1),
            default=0, output_field=IntegerField()
        ))

    query['rejected'] = Sum(
        Case(
            When(site_instances__form_status=1,
                 site_instances__project_fxf_id__in=form_ids, then=1),
            default=0, output_field=IntegerField()
        ))

    query['submission'] = Sum(
        Case(
            When(site_instances__project_fxf_id__in=form_ids, then=1),
            default=0, output_field=IntegerField()
        ))

    head_row.extend(
        ["Site Visits", "Submission Count", "Flagged Submission",
         "Rejected Submission"])
    data.append(head_row)

    sites = Site.objects.filter(is_active=True)

    sites_filter = {'project_id': project.id}
    finstance_filter = {'project_fxf__in': form_ids}
    site_dict = {}

    # Redoing query because annotate and lat long did not go well in single query.
    # Probable only an issue because of old django version.

    for site_obj in sites.filter(**sites_filter).iterator():
        site_dict[str(site_obj.id)] = {'visits': 0,
                                       'site_status': 'No Submission',
                                       'latitude': site_obj.latitude,
                                       'longitude': site_obj.longitude}

    sites_status = FInstance.objects.filter(
        **finstance_filter).order_by('site_id', '-id').distinct(
        'site_id').values_list('site_id', 'form_status')

    for site_status in sites_status:
        try:
            site_dict[str(site_status[0])]['site_status'] = \
            form_status_map[site_status[1]]
        except:
            pass
    sites_status = None

    site_visits = settings.MONGO_DB.instances.aggregate([{"$match": {
        "fs_project": project.id,
        "fs_project_uuid": {"$in": form_ids}}}, {"$group": {
        "_id": {
            "fs_site": "$fs_site",
            "date": {"$substr": ["$start", 0, 10]}
        },
    }
                                                         }, {"$group": {
        "_id": "$_id.fs_site", "visits": {
            "$push": {
                "date": "$_id.date"
            }
        }
        }}], cursor={})
    site_visits = list(site_visits)

    for site_visit in site_visits:
        try:
            site_dict[str(site_visit['_id'])]['visits'] = len(
                site_visit['visits'])
        except:
            pass

    site_visits = None

    sites = sites.filter(**sites_filter).values('id', 'identifier',
                                                'name',
                                                'region__identifier',
                                                'address',
                                                "current_progress").annotate(
        **query)

    for site in sites:
        try:
            site_row = [site['identifier'], site['name'],
                        site['region__identifier'], site['address'],
                        site_dict[str(site.get('id'))]['latitude'],
                        site_dict[str(site.get('id'))]['longitude'],
                        site_dict[str(site.get('id'))]['site_status'],
                        site['current_progress']]

            for stage in ss_index:
                site_row.append(site.get(stage, 0))

            site_row.extend([site_dict[str(site.get('id'))]['visits'],
                             site['submission'], site['flagged'],
                             site['rejected']])

            data.append(site_row)
        except Exception as e:
            pass
    return data


def form_submission(form_id):
    from onadata.libs.utils.export_tools import ExportBuilder, query_mongo
    fieldsight_xf = FieldSightXF.objects.get(pk=form_id)
    xform = fieldsight_xf.xf
    export_builder = ExportBuilder()
    export_builder.GROUP_DELIMITER = group_delimiter
    export_builder.SPLIT_SELECT_MULTIPLES = True
    export_builder.BINARY_SELECT_MULTIPLES = False
    export_builder.set_survey(xform.data_dictionary().survey)

    prefix = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + "__" + \
            xform.id_string
    temp_file = NamedTemporaryFile(prefix=prefix, suffix=(".xls"))
    filter_query = {'$and': [{'fs_project_uuid': str(form_id)}, {'$or': [{
        '_deleted_at':{'$exists': False}}, {'_deleted_at': None}]}],
                    '_deleted_at': {'$exists': False}}
    # filter_query = {"fs_project_uuid": str(form_id)}
    records = query_mongo(xform.user.username, xform.id_string, filter_query)
    export_builder.to_xls_export(temp_file.name, records, xform.user.username,
                                 xform.id_string, filter_query)

    df = pd.read_excel(temp_file)
    df = df.applymap(unicode)

    # select multiples as Bool
    childrens = json.loads(xform.json)['children']
    select_multiples = [c['name'] for c in childrens if c['type'] == 'select all that apply']
    select_multiples_slash = [s+"/" for s in select_multiples]
    dict_keys = {"1.0": True, "0.0": False}
    for col in df.columns:
        for select_m_slash in select_multiples_slash:
            if select_m_slash in col:
                df = df.replace({col: dict_keys})

    df = df.replace('nan', '')

    try:
        print("df shape", df.shape)
        x, y = df.shape
        print(" total cell in sheets ==", x*y)
        values = df.values.tolist()
        values.insert(0, list(df.columns.values))
        return values
    except Exception as e:
        return [[]]
    return [[]]


def custom_report_values(report_obj):
    if report_obj.type == 0:
        df = site_report(report_obj)
    elif report_obj.type == 4:
        df = user_report(report_obj)
    elif report_obj.type == 5:
        df = time_report(report_obj)
    try:
        print("df shape", df.shape)
        x, y = df.shape
        print(" total cell in sheets ==", x * y)
        values = df.values.tolist()
        values.insert(0, list(df.columns.values))
        return values
    except Exception as e:
        print(str(e))
        return [[]]

