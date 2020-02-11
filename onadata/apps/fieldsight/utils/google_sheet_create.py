import datetime
import gc
import os
from io import BytesIO
from tempfile import NamedTemporaryFile

from openpyxl import Workbook

from django.conf import settings
from django.db.models import Sum, Case, When, IntegerField, Q
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import pyexcel as p

from onadata.apps.fieldsight.models import Site
from onadata.apps.fsforms.models import FInstance, FieldSightXF
from onadata.apps.userrole.models import UserRole


form_status_map = ["Pending", "Rejected", "Flagged", "Approved"]


class DriveException(Exception):
    pass


def upload_to_drive(file_path, title, folder_title, project, user, sheet=None):
    """
    Uploads a google sheet to a drive.

    """
    from pydrive.auth import ServiceAccountCredentials, GoogleAuth
    gauth = GoogleAuth()
    team_drive_id = parent_folder_id = settings.PARENT_FOLDER_ID
    scope = ['https://www.googleapis.com/auth/drive']
    gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name('service_account.json', scope)
    drive = GoogleDrive(gauth)
    new_file = drive.CreateFile({'title': title,
                                     'parents': [{'kind': 'drive#fileLink',
                                                  'teamDriveId': team_drive_id,
                                                  'id': parent_folder_id}]
                                    })
    # md = new_file.FetchMetadata()
    # print(md)
    new_file.SetContentFile(file_path)
    new_file.Upload({'convert': True, 'supportsTeamDrives': True})
    print(new_file.__dict__)

    # drive_file = drive.ListFile({'q': "title = '{}' and trashed=false".format(title)}).GetList()[0]
    # drive_file = drive.ListFile({'q': "title = '{}' and trashed=false".format(title)}).GetList()[0]
    drive_file = new_file

    sheet.spreadsheet_id = drive_file['alternateLink']
    sheet.last_synced_date = datetime.datetime.now()
    sheet.save()

    permissions = drive_file.GetPermissions()

    user_emails = UserRole.objects.filter(ended_at__isnull=True).filter(
        Q(Q(group__name="Organization Admin", project__isnull=True) | Q(
            group__name__in=["Project Manager", "Project Donor"], project_id=sheet.project.id)),
        organization_id=sheet.project.organization_id
    ).distinct().values_list('user__email', flat=True)
    user_emails = list(user_emails)
    user_emails.append(settings.SERVICE_ACCOUNT_EMAIL)
    all_users = set(user_emails)

    existing_perms = []

    for permission in permissions:
        if "emailAddress" in permission:
            existing_perms.append(permission['emailAddress'])

    perms = set(existing_perms)

    perm_to_rm = perms - all_users
    perm_to_add = all_users - perms

    for permission in permissions:
        if "emailAddress" in permission:
            if permission['emailAddress'] in perm_to_rm and (
                    permission['emailAddress'] != settings.REPORT_ACCOUNT_EMAIL):
                drive_file.DeletePermission(permission['id'])

    retry_emails = []
    index = 0
    for perm in perm_to_add:
        try:
            drive_file.InsertPermission({
                'type': 'user',
                'value': perm,
                'role': 'writer'
            })

        except Exception as e:
            print(str(e), "Failed to share file {0} to {1} email".format(drive_file['alternateLink'], perm))
            if "Since there is no Google account associated with this email address" not in str(e):
                retry_emails.append(perm)

        index += 1

    if retry_emails:
        print "retrying again for ", retry_emails
        file = drive.ListFile({'q': "title = '" + title + "' and trashed=false"}).GetList()[0]
        import time
        for perm in retry_emails:
            time.sleep(1)
            try:
                file.InsertPermission({
                    'type': 'user',
                    'value': perm,
                    'role': 'writer'
                })
            except:
                pass


def site_details_generator(project, sites, ws):
    try:
        header_columns = [{'id': 'identifier', 'name': 'identifier'},
                          {'id': 'name', 'name': 'name'},
                          {'id': 'site_type_identifier', 'name': 'type'},
                          {'id': 'phone', 'name': 'phone'},
                          {'id': 'address', 'name': 'address'},
                          {'id': 'public_desc', 'name': 'public_desc'},
                          {'id': 'additional_desc', 'name': 'additional_desc'},
                          {'id': 'latitude', 'name': 'latitude'},
                          {'id': 'longitude', 'name': 'longitude'},
                          {'id': 'progress', 'name': 'progress'},
                          {'id': 'root_site_identifier', 'name': 'root_site_identifier'}, ]

        if project.cluster_sites:
            header_columns += [{'id': 'region_identifier', 'name': 'region_identifier'}, ]

        meta_ques = project.site_meta_attributes
        for question in meta_ques:
            if not question['question_type'] == 'Link':
                header_columns += [{'id': question['question_name'], 'name': question['question_name']}]
            else:
                question_name = question['question_name']
                try:
                    link_metas = question['metas'].values()[0]
                except:
                    link_metas = []
                for link_question in link_metas:
                    if not link_question['question_type'] == 'Link':  # ignore links of links
                        header_columns += [{
                            'id': question_name + "/" + link_question['question_name'],
                            'name': question_name + "/" + link_question['question_name']
                        }]

        site_list = {}
        for site in sites.select_related('region', 'type', 'site').iterator():
            root_site_identifier = None
            if site.site:
                root_site_identifier = site.site.identifier
            columns = {
                'identifier': site.identifier, 'name': site.name,
                'site_type_identifier': site.type.identifier if site.type else "", 'phone': site.phone,
                'address': site.address, 'public_desc': site.public_desc, 'additional_desc': site.additional_desc,
                'latitude': site.latitude,
                'longitude': site.longitude, 'progress': site.current_progress,
                'root_site_identifier': root_site_identifier
            }

            if project.cluster_sites:
                columns['region_identifier'] = site.region.identifier if site.region else ""

            meta_ans = site.all_ma_ans
            for question in meta_ques:
                if not question['question_type'] == 'Link':
                    # question is not draw from another project
                    question_name = question['question_name']
                    columns[question_name] = meta_ans.get(question_name, "")
                else:
                    question_name = question['question_name']
                    # question is draw from another project
                    # check answer is dict with children key
                    linked_answer = meta_ans.get(question_name, "")
                    if isinstance(linked_answer, dict):
                        children = linked_answer['children']
                        for k, v in children.items():
                            columns[question_name + "/" + k] = v
                    # else:
                    #     # no site referenced
                    #     # default empty answer
                    #     try:
                    #         link_metas = question['metas'].values()[0]
                    #     except:
                    #         link_metas = []
                    #     for link_question_of_link_metas in link_metas:
                    #         if not link_question_of_link_metas['question_type'] == 'Link':
                    #             columns[question_name + "/" + link_question_of_link_metas['question_name']] = ""

            site_list[site.id] = columns

        del sites
        gc.collect()

        header_row = []
        for col_num in range(len(header_columns)):
            # header_cell=WriteOnlyCell(ws, value=header_columns[col_num]['name'])
            # header_cell=Font(name='Courier', size=16)
            header_row.append(header_columns[col_num]['name'])

        ws.append(header_row)

        for key, site in site_list.iteritems():
            #    ws.append([site.get(header_columns[col_num]['id']) for col_num in range(len(header_columns))])
            row = []
            for col_num in range(len(header_columns)):
                row.append(site.get(header_columns[col_num]['id'], ""))
            ws.append(row)

        gc.collect()
        return True, 'success'

    except Exception as e:
        gc.collect()
        return False, e.message


def generate_site_info(sheet):
    buffer = BytesIO()
    wb = Workbook()
    ws = wb.active
    ws.title = 'Sites Detail'
    project = sheet.project
    sites = project.sites.filter(is_active=True).order_by('identifier')
    status, message = site_details_generator(project, sites, ws)

    if not status:
        raise ValueError(message)

    wb.save(buffer)
    buffer.seek(0)
    xls = buffer.getvalue()
    buffer.close()

    if not os.path.exists("media/site-details-report/"):
        os.makedirs("media/site-details-report/")

    temporarylocation = "media/site-details-report/site_details_{}.xls".format(project.id)
    with open(temporarylocation, 'wb') as out:  ## Open temporary file as bytes
        out.write(xls)  ## Read bytes into file

    upload_to_drive(temporarylocation,
                    "{} - Site Information".format(project.id), "Site Information", project, sheet.user, sheet)
    os.remove(temporarylocation)


def generate_site_progress(sheet):
    try:
        project = sheet.project
        data = []
        ss_index = []
        form_ids = []
        stages_rows = []
        head_row = ["Site ID", "Name", "Region ID", "Address", "Latitude", "longitude", "Status", "Progress"]

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
                            When(site_instances__project_fxf_id=ss.stage_forms.id, then=1),
                            default=0, output_field=IntegerField()
                        ))

        query['flagged'] = Sum(
            Case(
                When(site_instances__form_status=2, site_instances__project_fxf_id__in=form_ids, then=1),
                default=0, output_field=IntegerField()
            ))

        query['rejected'] = Sum(
            Case(
                When(site_instances__form_status=1, site_instances__project_fxf_id__in=form_ids, then=1),
                default=0, output_field=IntegerField()
            ))

        query['submission'] = Sum(
            Case(
                When(site_instances__project_fxf_id__in=form_ids, then=1),
                default=0, output_field=IntegerField()
            ))

        head_row.extend(["Site Visits", "Submission Count", "Flagged Submission", "Rejected Submission"])
        data.append(head_row)

        sites = Site.objects.filter(is_active=True)

        finstance_filter = {'project_fxf__in': form_ids}

        site_dict = {}

        # Redoing query because annotate and lat long did not go well in single query.
        # Probable only an issue because of old django version.

        for site_obj in sites.filter(project=project).iterator():
            site_dict[str(site_obj.id)] = {
                'visits': 0, 'site_status': 'No Submission', 'latitude': site_obj.latitude,
                'longitude': site_obj.longitude
            }

        sites_status = FInstance.objects.filter(**finstance_filter).order_by('site_id', '-id').distinct(
            'site_id').values_list('site_id', 'form_status')

        for site_status in sites_status:
            try:
                site_dict[str(site_status[0])]['site_status'] = form_status_map[site_status[1]]
            except:
                pass
        sites_status = None
        gc.collect()

        site_visits = settings.MONGO_DB.instances.aggregate(
            [{"$match": {"fs_project": project.id, "fs_project_uuid": {"$in": form_ids}}}, {
                "$group": {
                    "_id": {
                        "fs_site": "$fs_site",
                        "date": {"$substr": ["$start", 0, 10]}
                    },
                }
            }, {
                 "$group": {
                     "_id": "$_id.fs_site", "visits": {
                         "$push": {
                             "date": "$_id.date"
                         }
                     }
                 }
             }])['result']

        for site_visit in site_visits:
            try:
                site_dict[str(site_visit['_id'])]['visits'] = len(site_visit['visits'])
            except:
                pass

        site_visits = None
        gc.collect()

        sites = sites.filter(project=project).values('id', 'identifier', 'name', 'region__identifier', 'address',
                                                    "current_progress").annotate(**query)

        for site in sites.iterator():
            try:
                site_row = [site['identifier'], site['name'], site['region__identifier'], site['address'],
                            site_dict[str(site.get('id'))]['latitude'], site_dict[str(site.get('id'))]['longitude'],
                            site_dict[str(site.get('id'))]['site_status'], site['current_progress']]

                for stage in ss_index:
                    site_row.append(site.get(stage, ""))

                site_row.extend(
                    [site_dict[str(site.get('id'))]['visits'], site['submission'], site['flagged'], site['rejected']])

                data.append(site_row)
            except Exception as e:
                print e

        sites = None
        site_dict = None
        gc.collect()

        p.save_as(array=data, dest_file_name="media/stage-report/{}_stage_data.xls".format(project.id))

        with open("media/stage-report/{}_stage_data.xls".format(project.id), 'rb') as fin:
            buffer = BytesIO(fin.read())
            buffer.seek(0)
            path = default_storage.save(
                "media/stage-report/{}_stage_data.xls".format(project.id),
                ContentFile(buffer.getvalue())
            )
            buffer.close()

        upload_to_drive("media/stage-report/{}_stage_data.xls".format(project.id),
                        "{} - Progress Report".format(project.id), "Site Progress", project, sheet.user, sheet)
    except AttributeError as e:
        print("stage report failed to generate", str(e))
    except Exception as e:
        print("stage report failed to generate", str(e))



def generate_form_report(sheet):
    group_delimiter = '/'
    form_id = sheet.form.id
    from onadata.libs.utils.export_tools import ExportBuilder, query_mongo
    fieldsight_xf = FieldSightXF.objects.get(pk=form_id)
    xform = fieldsight_xf.xf
    id_string = xform.id_string
    export_builder = ExportBuilder()
    export_builder.GROUP_DELIMITER = group_delimiter
    export_builder.SPLIT_SELECT_MULTIPLES = True
    export_builder.BINARY_SELECT_MULTIPLES = False
    export_builder.set_survey(xform.data_dictionary().survey)

    prefix = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + "__" + \
             xform.id_string
    temp_file = NamedTemporaryFile(prefix=prefix, suffix=(".xls"))
    filter_query = {
        '$and': [{'fs_project_uuid': str(form_id)}, {
            '$or': [{
                '_deleted_at': {'$exists': False}
            }, {'_deleted_at': None}]
        }],
        '_deleted_at': {'$exists': False}
    }
    # filter_query = {"fs_project_uuid": str(form_id)}
    records = query_mongo(xform.user.username, xform.id_string, filter_query)
    export_builder.to_xls_export(temp_file.name, records, xform.user.username,
                                 xform.id_string, filter_query)

    if not os.path.exists("media/forms/"):
        os.makedirs("media/forms/")

    temporarylocation = "media/forms/submissions_{}.xls".format(xform.id_string)
    import shutil
    shutil.copy(temp_file.name, temporarylocation)
    if fieldsight_xf.schedule:
        name = fieldsight_xf.schedule.name
    elif fieldsight_xf.stage:
        name = fieldsight_xf.stage.name
    else:
        name = fieldsight_xf.xf.title
    upload_to_drive(temporarylocation, name + '_' + id_string, str(fieldsight_xf.id) + '_' + name + '_' + id_string,
                    fieldsight_xf.project, sheet.user, sheet)

    os.remove(temporarylocation)
