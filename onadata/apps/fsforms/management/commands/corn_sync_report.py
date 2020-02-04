import datetime
import calendar
from pprint import pprint

from django.db.models import Q
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient import discovery
from django.core.management.base import BaseCommand
from django.conf import settings

from onadata.apps.fieldsight.utils.google_sheet_create import generate_site_info, generate_site_progress, \
    generate_form_report, generate_custom_report
from onadata.apps.fieldsight.utils.google_sheet_sync import site_information, \
    progress_information, form_submission, custom_report_values
from onadata.apps.fsforms.models import ReportSyncSettings

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive',
         'https://www.googleapis.com/auth/spreadsheets']


def update_sheet(service, sheet_obj, report_type, project, form_id, spreadsheet_id, grid_id, sheet_range):
    spreadsheet_id = spreadsheet_id.split("/")[-2]
    if not sheet_range:
        sheet_range = "A1:GZ50000"
    if report_type == "site_info":
        values = site_information(project.id)
    elif report_type == "site_progress":
        values = progress_information(project.id)
    elif report_type == "form":
        values = form_submission(form_id)
    elif report_type == "custom":
        values = custom_report_values(sheet_obj.report)

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
            if "error" in response:
                pprint(response)
                print("failed ", sheet_obj.id)
                if grid_id:
                    add_rows = {
                        "requests": [
                            {
                                "appendDimension": {
                                    "dimension": "ROWS",
                                    "length": 100,
                                    "sheetId": grid_id
                                }
                            }
                        ],
                        "includeSpreadsheetInResponse": False
                    }
                    request_add_row = service.spreadsheets().values().batchUpdate(
                        spreadsheetId=spreadsheet_id, body=add_rows)

                    response_add_row = request_add_row.execute()
                    pprint(response_add_row)
            else:
                print("finished ,", sheet_obj.id, page)
                total_sites -= page_size
                page += 1
        sheet_obj.last_synced_date = datetime.datetime.now()
        sheet_obj.save()
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
        if "error" in response:
            pprint(response)
            print("failed ", sheet_obj.id)
            if grid_id:
                add_rows = {
                    "requests": [
                        {
                            "appendDimension": {
                                "dimension": "ROWS",
                                "length": 100,
                                "sheetId": grid_id
                            }
                        }
                    ],
                    "includeSpreadsheetInResponse": False
                }
                request_add_row = service.spreadsheets().values().batchUpdate(
                    spreadsheetId=spreadsheet_id, body=add_rows)

                response_add_row = request_add_row.execute()
                pprint(response_add_row)
                request = service.spreadsheets().values().batchUpdate(
                    spreadsheetId=spreadsheet_id, body=body)

                response = request.execute()
                pprint(response)

        # pprint(response)
        sheet_obj.last_synced_date = datetime.datetime.now()
        sheet_obj.save()
        print("finished ,", sheet_obj.id)


def create_new_sheet(sheet):
    if sheet.report_type == "site_info":
        generate_site_info(sheet)
    elif sheet.report_type == "site_progress":
        generate_site_progress(sheet)
    elif sheet.report_type == "form":
        generate_form_report(sheet)
    elif sheet.report_type == "custom":
        generate_custom_report(sheet)


class Command(BaseCommand):
    ''' This command update sheets in drive'''

    help = 'update sheet data in google'

    def handle(self, *args, **options):
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive',
                 'https://www.googleapis.com/auth/spreadsheets']
        week_day = int(datetime.datetime.today().strftime('%w'))
        day = datetime.datetime.today().day
        _start, _end = calendar.monthrange(datetime.datetime.today().year, datetime.datetime.today().month)
        if day == _end:
            sheet_list = ReportSyncSettings.objects.exclude(schedule_type=0).filter(Q(schedule_type=1)
                            | Q(schedule_type=2, day=week_day)
                            | Q(schedule_type=3, day=0)
                            )

        else:
            sheet_list = ReportSyncSettings.objects.exclude(schedule_type=0).filter(Q(schedule_type=1)
                            | Q(schedule_type=2, day=week_day)
                            | Q(schedule_type=3, day=day)
                            )

        if sheet_list:
            credentials = ServiceAccountCredentials.from_json_keyfile_name(
                settings.SERVICE_ACCOUNT_JSON, scope)

            service = discovery.build('sheets', 'v4', credentials=credentials,
                                      cache_discovery=False)
            for sheet in sheet_list:
                print("syncing for ", sheet.id)
                report_type = sheet.report_type
                project = sheet.project
                form_id = sheet.form_id if sheet.form else 0
                spreadsheet_id = sheet.spreadsheet_id
                grid_id = sheet.grid_id
                sheet_range = sheet.range
                if spreadsheet_id:  # Already Have file in Drive
                    update_sheet(service, sheet,
                                 report_type, project, form_id, spreadsheet_id, grid_id, sheet_range)
                    
                else:
                    create_new_sheet(sheet)
                    

