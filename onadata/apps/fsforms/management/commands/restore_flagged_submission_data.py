import datetime

from django.core.management.base import BaseCommand
from django.conf import settings

from onadata.apps.fsforms.models import FInstance, InstanceStatusChanged
from onadata.apps.logger.models import Instance
from onadata.apps.fieldsight.templatetags.filters import FORM_STATUS
from onadata.apps.fsforms.notifications import save_notification


class Command(BaseCommand):
    help = 'Store flagged submission status in log'

    def add_arguments(self, parser):
        parser.add_argument('project', type=int)

    def handle(self, *args, **options):
        last_date = datetime.datetime(2019, 5, 26, 10, 56, 5, 310000)
        changed = InstanceStatusChanged.objects.filter(finstance__project_id=options['project'], date__lt=last_date)
        for fi in changed:
            if fi.finstance.submitted_by:
                comment_url = "{}/forms/api/instance/change_status-detail/{}".format(settings.KOBOCAT_URL, fi.id)
                emails = [fi.finstance.submitted_by.email]
                is_deleted = False
                message = {
                    'notify_type': 'Form_Flagged',
                    'is_delete': is_deleted,
                    'form_id': fi.finstance.fsxf.id,
                    'project_form_id': fi.finstance.fsxf.id,
                    'comment': fi.message,
                    'form_name': fi.finstance.fsxf.xf.title,
                    'xfid': fi.finstance.fsxf.xf.id_string,
                    'form_type': fi.finstance.fsxf.form_type(), 'form_type_id': fi.finstance.fsxf.form_type_id(),
                    'status': FORM_STATUS.get(fi.finstance.form_status, "New Form"),
                    'comment_url': comment_url,
                    'submission_date_time': str(fi.finstance.date),
                    'submission_id': fi.finstance.id,
                    'version': fi.finstance.version
                }
                if fi.finstance.site:
                    message['site'] = {'name': fi.finstance.site.name, 'id': fi.finstance.site.id, 'identifier': fi.finstance.site.identifier}
                if fi.finstance.project:
                    message['project'] = {'name': fi.finstance.project.name, 'id': fi.finstance.project.id}
                if fi.finstance.fsxf.site:
                    message['site_level_form'] = True
                else:
                    message['site_level_form'] = False
                save_notification(message, emails, date=fi.date)
