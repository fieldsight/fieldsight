from pprint import pprint
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient import discovery
from django.core.management.base import BaseCommand, CommandError

from onadata.apps.fieldsight.utils.google_sheet_sync import site_information

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive',
         'https://www.googleapis.com/auth/spreadsheets']

class Command(BaseCommand):
    ''' This command replace string in xml '''

    help = 'update sheet data in google'

    def add_arguments(self, parser):
        parser.add_argument(
            '--spreadsheet_id',
            type=str,
            dest='spreadsheet_id',
            help='spreadsheet_id google'
        )
        parser.add_argument(
            '--project',
            type=int,
            dest='project',
            help='project id'
        )

        parser.add_argument(
            '--range',
            type=str,
            dest='range',
            help='range of columns e.g. A1:B3 '
        )
        parser.add_argument(
            '--form_id',
            type=int,
            dest='form_id',
            help='fieldsight Form id'
        )
        parser.add_argument(
            '--report_type',
            type=str,
            dest='report_type',
            help='type of report'
        )

    def handle(self, *args, **options):
        spreadsheet_id = options["spreadsheet_id"]
        project = options["project"]
        range = options["range"]
        form_id = options["form_id"]
        report_type = options["report_type"]
        form_id = None

        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            'service_account.json', scope)

        service = discovery.build('sheets', 'v4', credentials=credentials)

        values = []
        if form_id:
            return

        if report_type == "site_info":
            values = site_information(project)

        body = {'data': [{'majorDimension': 'ROWS',
                          'range': range,
                          'values': values
                          }],
                'valueInputOption': 'RAW'}

        request = service.spreadsheets().values().batchUpdate(
            spreadsheetId=spreadsheet_id, body=body)

        response = request.execute()
        pprint(response)


        self.stderr.write(
            '\nFinished {} '.format(
                spreadsheet_id,)
        )

