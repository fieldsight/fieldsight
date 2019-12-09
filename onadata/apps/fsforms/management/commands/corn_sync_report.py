import time

from pprint import pprint
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient import discovery
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from onadata.apps.fieldsight.utils.google_sheet_sync import site_information, \
    progress_information, form_submission
from onadata.apps.fsforms.models import ReportSyncSettings

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive',
         'https://www.googleapis.com/auth/spreadsheets']


def update_sheet(service, id, report_type, project, form_id, spreadsheet_id, grid_id, sheet_range):
    if not sheet_range:
        sheet_range = "A1:GZ50000"
    if report_type == "site_info":
        values = site_information(project)
    elif report_type == "site_progress":
        values = progress_information(project)
    elif report_type == "form":
        values = form_submission(form_id)
    if len(values) >= 10000:
        total_sites = len(values)
        page_size = 10000
        page = 0
        while total_sites > 0:
            chunk = values[page * page_size:(page + 1) * page_size]
            range = 'A{0}:GZ50000'.format((page * page_size) + 1)
            body = {
                'data': [{
                             'majorDimension': 'ROWS',
                             'range': range,
                             'values': chunk
                         }],
                'valueInputOption': 'USER_ENTERED'
            }

            request = service.spreadsheets().values().batchUpdate(
                spreadsheetId=spreadsheet_id, body=body)

            response = request.execute()
            pprint(response)
            print("finished ,", id, page)
            total_sites -= page_size
            page += 1
    else:
        body = {
            'data': [{
                         'majorDimension': 'ROWS',
                         'range': sheet_range,
                         'values': values
                     }],
            'valueInputOption': 'USER_ENTERED'
        }

        request = service.spreadsheets().values().batchUpdate(
            spreadsheetId=spreadsheet_id, body=body)

        response = request.execute()
        pprint(response)

        print("finished ,", id)


def generate_site_info(sheet):
    pass


def generate_site_progress(sheet):
    pass


def generate_form_report(sheet):
    pass


def create_new_sheet(sheet):
    if sheet.report_type == "site_info":
        generate_site_info(sheet)
    elif sheet.report_type == "site_progress":
        generate_site_progress(sheet)
    elif sheet.report_type == "form":
        generate_form_report(sheet)


class Command(BaseCommand):
    ''' This command update sheets in drive'''

    help = 'update sheet data in google'

    def add_arguments(self, parser):
        parser.add_argument('schedule_type', type=str)

    def handle(self, *args, **options):
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive',
                 'https://www.googleapis.com/auth/spreadsheets']
        sheet_list = ReportSyncSettings.objects.exclude(schedule_type=0)

        if sheet_list:
            credentials = ServiceAccountCredentials.from_json_keyfile_name(
                settings.SERVICE_ACCOUNT_JSON, scope)

            service = discovery.build('sheets', 'v4', credentials=credentials,
                                      cache_discovery=False)
            for sheet in sheet_list:
                report_type = sheet.report_type
                project = sheet.project
                form_id = sheet.form_id if sheet.form else 0
                spreadsheet_id = sheet.spreadsheet_id
                grid_id = sheet.grid_id
                sheet_range = sheet.range
                if spreadsheet_id:  # Already Have file in Drive
                    update_sheet(service, sheet.id,
                                 report_type, project, form_id, spreadsheet_id, grid_id, sheet_range)
                    
                else:
                    create_new_sheet(sheet)
                    

