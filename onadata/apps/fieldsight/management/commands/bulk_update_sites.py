from django.db import connection
from django.core.management.base import BaseCommand
from onadata.apps.fieldsight.models import Site
from psycopg2.extras import Json


def bulk_update_sites(pk):
    sites = Site.objects.filter(is_active=True, project=pk)[:10]
    list(sites)
    a = []
    cursor = connection.cursor()
    for site in sites:
        lat = site.latitude
        longitude = site.longitude
        site_meta_attributes_ans = Json(site.site_meta_attributes_ans)
        all_ma_ans = Json(site.all_ma_ans)
        a.append((site.identifier, site.name, site.project_id,
                  site.type_id, site.public_desc, site.additional_desc,
                  site.region_id,
                  site_meta_attributes_ans, all_ma_ans,
                  site.current_progress, lat, longitude))
    final = tuple(a)
    cursor.execute("""update fieldsight_site as t 
    set name = c.name, type_id = CAST(c.type AS INTEGER), public_desc = c.public_desc, 
    additional_desc = c.additional_desc,
    region_id = CAST(c.region AS INTEGER), site_meta_attributes_ans = 
    CAST(c.site_meta_attributes_ans AS json), 
    all_ma_ans = CAST(c.all_ma_ans AS json),current_progress = c.current_progress,
    location = CAST(ST_SetSRID(ST_Point( c.lat, c.longitude), 4326) as geography)
    from (values %s
    ) as c(identifier, name, project_id, type, public_desc, 
    additional_desc, region, 
    site_meta_attributes_ans, all_ma_ans, current_progress, lat, longitude) where
    CAST(c.identifier as VarChar)=CAST(t.identifier as VarChar) and CAST(
    c.project_id as int)=CAST(t.project_id as int); """, [final[0]])


class Command(BaseCommand):
    help = 'bulk update sites'

    def add_arguments(self, parser):
        parser.add_argument('project_id', type=int)

    def handle(self, *args, **options):
        project_id = options['project_id']
        bulk_update_sites(project_id)
        self.stdout.write('Updating site for project "%d"' % project_id)
