from django.core.management.base import BaseCommand, CommandError

from onadata.apps.fieldsight.models import Project
from onadata.apps.fsforms.models import FieldSightXF, ReportSyncSettings


class Command(BaseCommand):
    help = 'Create default groups'

    def handle(self, *args, **options):
        projects = Project.objects.all()
        forms = FieldSightXF.objects.filter(is_deleted=False, project__isnull=False)
        list(forms)
        settings = []
        for f in forms:
            s = ReportSyncSettings(project=f.project, report_type="form", schedule_type=0, form=f)
            settings.append(s)

        for p in projects:
            s = ReportSyncSettings(project=p, report_type="site_info", schedule_type=0)
            so = ReportSyncSettings(project=p, report_type="site_progress", schedule_type=0)
            settings.append(s)
            settings.append(so)
        ReportSyncSettings.objects.bulk_create(settings)

