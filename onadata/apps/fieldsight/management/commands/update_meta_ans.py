from django.core.management.base import BaseCommand

from onadata.apps.fieldsight.models import Site
from onadata.apps.fieldsight.tasks import update_metas_in_sites


def update_site_meta_attribs_ans(pk):
    total_sites = Site.objects.filter(is_active=True, project=pk).count()
    page_size = 1000
    page = 0
    while total_sites > 0:
        update_metas_in_sites.delay(pk, page * page_size, (page + 1) * page_size)
        total_sites -= page_size
        page += 1


class Command(BaseCommand):
    help = 'Create default groups'

    def add_arguments(self, parser):
        parser.add_argument('project_id', type=int)

    def handle(self, *args, **options):
        project_id = options['project_id']
        update_site_meta_attribs_ans(project_id)
        self.stdout.write('Updating meta ans for "%d"' % project_id)
