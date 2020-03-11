from django.db import connection
from django.core.management.base import BaseCommand
from onadata.apps.fieldsight.models import Site
from psycopg2.extras import Json


def bulk_update_sites(pk):
    sites = Site.objects.filter(is_active=True, project=pk)[:1000]
    list(sites)
    left_sql = u"""update fieldsight_site as t 
            set name = c.name,
            public_desc = c.public_desc, 
            additional_desc = c.additional_desc,
            address = c.address,
            phone = c.phone,
            region_id = CAST(c.region_id AS INTEGER),
            site_id = CAST(c.site_id AS INTEGER),
            type_id = CAST(c.type AS INTEGER),
            site_meta_attributes_ans = CAST(c.site_meta_attributes_ans AS json), 
            all_ma_ans = CAST(c.all_ma_ans AS json),
            current_progress = c.current_progress,
            location = CAST(ST_SetSRID(ST_Point( c.lat, c.longitude), 4326) as geography)
            from (values """

    right_sql = u""") as c(identifier, name, address, phone, site_id, project_id, type, public_desc, 
            additional_desc, region_id, 
            site_meta_attributes_ans, all_ma_ans, current_progress, lat, longitude) where
            CAST(c.identifier as VarChar)=CAST(t.identifier as VarChar) and CAST(
            c.project_id as int)=CAST(t.project_id as int); """

    values_sql = u""""""

    for site in sites:
        lat = site.latitude
        longitude = site.longitude
        site_meta_attributes_ans = Json(site.site_meta_attributes_ans)
        all_ma_ans = Json(site.all_ma_ans)
        values_sql += u"""('{}', '{}', '{}', '{}', {}, {}, {}, '{}', '{}', {},{}, {}, {}, {}, {}),""".format(
            site.identifier, site.name, site.address, site.phone, site.site_id, site.project_id,
            site.type_id, site.public_desc, site.additional_desc,
            site.region_id,
            site_meta_attributes_ans, all_ma_ans,
            site.current_progress, lat, longitude)

    values_sql = values_sql[:-1]
    values_sql = values_sql.replace("None", "null")
    sql = left_sql + values_sql + right_sql
    print(sql)
    with connection.cursor() as cursor:
        cursor.execute(sql)


class Command(BaseCommand):
    help = 'bulk update sites'

    def add_arguments(self, parser):
        parser.add_argument('project_id', type=int)

    def handle(self, *args, **options):
        project_id = options['project_id']
        bulk_update_sites(project_id)
        self.stdout.write('Updating site for project "%d"' % project_id)
