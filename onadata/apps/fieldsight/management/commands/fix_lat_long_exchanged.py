from django.core.management.base import BaseCommand
from django.db import connection

from onadata.apps.fieldsight.models import Site


def bulk_update_sites_location(sites):
    if not sites:
        return
    pk_list = [str(s[0]) for s in sites]
    pk_list_string = ','.join(pk_list)
    whens = ""
    for id, location in sites:
        when_statement = "WHEN id={0} THEN ST_SetSRID(ST_MakePoint({1},{2})," \
                         "4326) ".format(id, location.y, location.x)
        whens += when_statement
    statement = "UPDATE fieldsight_site set location = CASE "
    where = " END WHERE id IN (" + pk_list_string + ")"
    query = statement + whens + where
    with connection.cursor() as cursor:
        cursor.execute(query)


def exchange_lat_long(pk):
    total_sites = Site.objects.filter(is_active=True, project=pk).count()
    page_size = 1000
    page = 0
    while total_sites > 0:
        sites = Site.objects.filter(
            is_active=True,
            project=pk)[page * page_size: (page + 1) * page_size].values_list(
            "pk", "location")
        bulk_update_sites_location(sites)
        print("updated for batch ", page * page_size, "<-->",  (page + 1) *
              page_size)
        total_sites -= page_size
        page += 1


class Command(BaseCommand):
    help = 'Create default groups'

    def add_arguments(self, parser):
        parser.add_argument('project_id', type=int)

    def handle(self, *args, **options):
        project_id = options['project_id']
        exchange_lat_long(project_id)
        self.stdout.write("fixing lat long for "%d"' % project_id)
