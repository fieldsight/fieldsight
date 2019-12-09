import datetime
import gc
import os
from io import BytesIO

from openpyxl import Workbook

from django.conf import settings
from django.db.models import Q
from django.core.files.storage import get_storage_class
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

from onadata.apps.api.models import Project
from onadata.apps.userrole.models import UserRole


class DriveException(Exception):
    pass


def upload_to_drive(file_path, title, folder_title, project, user, sheet=None):
    # pass
    """ TODO: folder names of 'Site Details' and 'Site Progress' must be in google drive."""
    try:
        gauth = GoogleAuth()
        drive = GoogleDrive(gauth)

        folders = drive.ListFile({'q': "title = '" + folder_title + "'"}).GetList()

        if folders:
            folder_id = folders[0]['id']
        else:
            folder_metadata = {'title': folder_title, 'mimeType': 'application/vnd.google-apps.folder'}
            new_folder = drive.CreateFile(folder_metadata)
            new_folder.Upload()
            folder_id = new_folder['id']

        file = drive.ListFile({'q': "title = '" + title + "' and trashed=false"}).GetList()

        if not file:
            new_file = drive.CreateFile({'title': title, "parents": [{"kind": "drive#fileLink", "id": folder_id}]})
            new_file.SetContentFile(file_path)
            new_file.Upload({'convert': True})
            file = drive.ListFile({'q': "title = '" + title + "' and trashed=false"}).GetList()[0]

        else:
            file = file[0]
            file.SetContentFile(file_path)
            file.Upload({'convert': True})

        sheet.spreadsheet_id = file['alternateLink']
        sheet.last_synced_date = datetime.datetime.now(),

        permissions = file.GetPermissions()

        user_emails = UserRole.objects.filter(
            Q(Q(group__name="Organization Admin", project__isnull=True) | Q(
                group__name__in=["Project Manager", "Project Donor"], project_id=_project.id)),
            organization_id=sheet.project.organization_id
        ).distinct().values_list('user__email', flat=True)

        user_emails.append(settings.SERVICE_ACCOUNT_EMAIL)
        all_users = set(user_emails)

        existing_perms = []

        for permission in permissions:
            existing_perms.append(permission['emailAddress'])

        perms = set(existing_perms)

        perm_to_rm = perms - all_users
        perm_to_add = all_users - perms

        for permission in permissions:
            if permission['emailAddress'] in perm_to_rm and (
                    permission['emailAddress'] != "exports.fieldsight@gmail.com"):
                file.DeletePermission(permission['id'])

        retry_emails = []
        index = 0
        for perm in perm_to_add:
            try:
                file.InsertPermission({
                    'type': 'user',
                    'value': perm,
                    'role': 'writer'
                })

            except Exception as e:
                if "Since there is no Google account associated with this email address" not in str(e):
                    retry_emails.append(perm)

            index += 1

        if retry_emails:
            print "retrying again for ", retry_emails
            from onadata.apps.fieldsight.task import gsuit_assign_perm
            gsuit_assign_perm.delay(title, retry_emails)

    except Exception as e:
        raise DriveException({"message": e})


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
            header_columns += [{'id': 'region_identifier', 'name': 'region_id'}, ]

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
        for site in sites.select_related('region').iterator():
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
                    "{} - Site Information".format(project.id), "Site Information", project, sheet.user)

    os.remove(temporarylocation)
