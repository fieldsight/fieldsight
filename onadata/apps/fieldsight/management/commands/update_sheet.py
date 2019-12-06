import time

from pprint import pprint
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient import discovery
from django.core.management.base import BaseCommand, CommandError

from onadata.apps.fieldsight.utils.google_sheet_sync import site_information, \
    progress_information, form_submission

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive',
         'https://www.googleapis.com/auth/spreadsheets']



class Command(BaseCommand):
    ''' This command update sheets in drive'''

    help = 'update sheet data in google'

    def add_arguments(self, parser):
        parser.add_argument('schedule_type', type=str)

    def handle(self, *args, **options):
        schedule_type = options.get('schedule_type', 'd')
        print("schedule_type")
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive',
                 'https://www.googleapis.com/auth/spreadsheets']
        from onadata.apps.fieldsight.sheet_list import SHEET_LIST
        if SHEET_LIST:
            credentials = ServiceAccountCredentials.from_json_keyfile_name(
                'service_account.json', scope)

            service = discovery.build('sheets', 'v4', credentials=credentials,
                                      cache_discovery=False)
            for sheet in SHEET_LIST:
                time.sleep(3)
                values = []
                report_type = sheet.get('report_type')
                project = sheet.get('project')
                form_id = sheet.get('form_id')
                spreadsheet_id = sheet.get('spreadsheet_id')
                grid_id = sheet.get('grid_id')
                sheet_range = sheet.get('range')
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
                        print(range, "   ==========   range")
                        body = {'data': [{'majorDimension': 'ROWS',
                                          'range': range,
                                          'values': chunk
                                          }],
                                'valueInputOption': 'USER_ENTERED'}

                        request = service.spreadsheets().values().batchUpdate(
                            spreadsheetId=spreadsheet_id, body=body)

                        response = request.execute()
                        pprint(response)
                        print("finished ,", sheet, page)
                        total_sites -= page_size
                        page += 1
                else:
                    body = {'data': [{'majorDimension': 'ROWS',
                                      'range': sheet_range,
                                      'values': values
                                      }],
                            'valueInputOption': 'USER_ENTERED'}

                    request = service.spreadsheets().values().batchUpdate(
                        spreadsheetId=spreadsheet_id, body=body)

                    response = request.execute()
                    pprint(response)

                    print("finished ,", sheet)

