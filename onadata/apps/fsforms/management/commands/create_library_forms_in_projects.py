from django.core.management.base import BaseCommand
from onadata.apps.fieldsight.models import ProjectType, Project
from onadata.apps.fsforms.models import FieldSightXF, OrganizationFormLibrary


class Command(BaseCommand):
    help = 'Create default groups'

    def handle(self, *args, **options):
        org_id = 0
        projects = Project.objects.filter(organization__parent=org_id)
        library_forms = OrganizationFormLibrary.objects.filter(organization=org_id)
        fsxf_list = []
        for p in projects:
            for lf in library_forms:
                fsxf = FieldSightXF(xf=lf.xf, project=p, is_deployed=True)
                fsxf_list.append(fsxf)
        FieldSightXF.objects.bulk_create(fsxf_list)
