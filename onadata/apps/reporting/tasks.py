from __future__ import absolute_import

import calendar
import datetime
import os
import time
from io import BytesIO
from googleapiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials
from uuid import uuid4
from celery import shared_task
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db.models import Q

from onadata.apps.eventlog.models import CeleryTaskProgress
from onadata.apps.reporting.models import ReportSettings
from onadata.apps.reporting.utils.excel_utils import to_excel_auto_width
from onadata.apps.reporting.utils.site_report import site_report
from onadata.apps.reporting.utils.time_report import time_report
from onadata.apps.reporting.utils.user_report import user_report


def save_file(df, directory, filename):
    if not os.path.exists(settings.MEDIA_ROOT + directory):
        os.makedirs(settings.MEDIA_ROOT + directory)
    to_excel_auto_width(settings.MEDIA_ROOT + directory + filename, df)
    # df.to_excel(settings.MEDIA_ROOT + directory + filename)
    with open("media/" + directory + filename, 'rb') as fin:
        buffer_file = BytesIO(fin.read())
        buffer_file.seek(0)
        path = default_storage.save(
            "media/" + directory + filename,
            ContentFile(buffer_file.getvalue())
        )
        buffer_file.close()
    os.remove(settings.MEDIA_ROOT + directory + filename)
    return path


@shared_task(time_limit=600, max_retries=2, soft_time_limit=600)
def new_export(report_id, task_id):
    time.sleep(5)
    task = CeleryTaskProgress.objects.get(pk=task_id)
    task.status = 1
    task.save()
    try:
        report_obj = ReportSettings.objects.get(pk=report_id)
        if report_obj.type == 0:
            df = site_report(report_obj)
            xls_url = save_file(df,  "custom_report/", "site_report_" + uuid4().hex + ".xlsx")
        elif report_obj.type == 4:
            df = user_report(report_obj)
            xls_url = save_file(df, "custom_report/", "user_report_" + uuid4().hex + ".xlsx")
        elif report_obj.type == 5:
            df = time_report(report_obj)
            xls_url = save_file(df, "custom_report/", "time_report_" + uuid4().hex + ".xlsx")
        task.file.name = xls_url
        task.status = 2
        task.save()
        task.logs.create(source=task.user, type=32, title="Report generation",
                                recipient=task.user, content_object=task, extra_object=task.content_object,
                                extra_message="Custom " + report_obj.get_type_display() + " Report  <a href='" + task.file.url + "'> Download </a>  with title ")
    except Exception as e:
        task.description = "ERROR: " + str(e)
        task.status = 3
        task.save()
        task.logs.create(source=task.user, type=432, title="Report generation",
                                content_object=task.content_object, recipient=task.user,
                                extra_message="@error " + u'{}'.format(e.message))


@shared_task()
def sync_report():
    from onadata.apps.fsforms.models import ReportSyncSettings
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
                from onadata.apps.fsforms.management.commands.corn_sync_report import update_sheet
                update_sheet(service, sheet,
                             report_type, project, form_id, spreadsheet_id, grid_id, sheet_range)

            else:
                from onadata.apps.fsforms.management.commands.corn_sync_report import create_new_sheet
                create_new_sheet(sheet)
