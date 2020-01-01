from __future__ import absolute_import

import os
import time
from uuid import uuid4

from celery import shared_task
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from onadata.apps.eventlog.models import CeleryTaskProgress
from onadata.apps.reporting.models import ReportSettings
from onadata.apps.reporting.utils.site_report import site_report
from onadata.apps.reporting.utils.user_report import user_report


def save_file(df, directory, filename):
    if not os.path.exists(settings.MEDIA_ROOT + directory):
        os.makedirs(settings.MEDIA_ROOT + directory)
    xls = df.to_excel(settings.MEDIA_ROOT + directory + filename + ".xls")
    # return xls
    # xls_url = default_storage.save(, ContentFile(xls))
    return directory + filename + ".xls"


@shared_task()
def new_export(report_id, task_id):
    time.sleep(5)
    task = CeleryTaskProgress.objects.get(pk=task_id)
    task.status = 1
    task.save()
    try:
        report_obj = ReportSettings.objects.get(pk=report_id)
        if report_obj.type == 1:
            df = site_report(report_obj)
            xls_url = save_file(df,  "custom_report/", "site_report" + uuid4().hex)
        elif report_obj.type == 4:
            df = user_report(report_obj)
            xls_url = save_file(df, "custom_report/", "user_report" + uuid4().hex)
        task.file.name = xls_url
        task.status = 2
        task.save()
        task.logs.create(source=task.user, type=32, title="Report generation",
                                recipient=task.user, content_object=task, extra_object=task.content_object,
                                extra_message=" <a href='" + task.file.url + "'> Custom Report  </a> generation with title ")
    except Exception as e:
        task.description = "ERROR: " + str(e.message)
        task.status = 3
        task.save()
        task.logs.create(source=task.user, type=432, title="Report generation",
                                content_object=task.content_object, recipient=task.user,
                                extra_message="@error " + u'{}'.format(e.message))


