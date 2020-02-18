from django.db import connection
from django.core.management.base import BaseCommand
from psycopg2._psycopg import cursor
from onadata.apps.fieldsight.models import Site
from psycopg2.extras import Json
from onadata.apps.fieldsight.tasks import update_metas_in_sites


def bulk_update_sites(pk):
    sites = Site.objects.filter(is_active=True, project=pk)[:10]
    list(sites)
    a = []
    cursor = connection.cursor()
    for site in sites:
        a_dictionary = Json(site.site_featured_images)
        site_meta_attributes_ans_modified = Json(site.site_meta_attributes_ans)
        all_ma_ans_modified = Json(site.all_ma_ans)
        a.append((site.identifier, site.name, site.project_id,
                  a_dictionary, site.type_id, site.phone, site.additional_desc,
                  str(site.logo), site.is_active, site.is_survey,
                  site.region_id,
                  site_meta_attributes_ans_modified, all_ma_ans_modified,
                  site.weight))
    final = tuple(a)
    cursor.execute("""update fieldsight_site as t 
    set name = c.name, site_featured_images = CAST(c.site_featured_images AS json),
    type_id = CAST(c.type AS INTEGER), phone = c.phone, 
    additional_desc = c.additional_desc, logo = CAST(c.logo AS VarChar),
    is_active = c.is_active, is_survey = c.is_survey, 
    region_id = CAST(c.region AS INTEGER), site_meta_attributes_ans = 
    CAST(c.site_meta_attributes_ans AS json), 
    all_ma_ans = CAST(c.all_ma_ans AS json),weight = c.weight
    from (values %s
    ) as c(identifier, name, project_id, site_featured_images, type, phone, 
    additional_desc, logo, is_active, is_survey, region, 
    site_meta_attributes_ans, all_ma_ans, weight) where
    CAST(c.identifier as VarChar)=CAST(t.identifier as VarChar) and CAST(
    c.project_id as int)=CAST(t.project_id as int); """, [final[0]])
# location = CAST(ST_SetSRID( ST_Point( -71.104, 42.315), 4326) AS geography),


class Command(BaseCommand):
    help = 'Create default groups'

    def add_arguments(self, parser):
        parser.add_argument('project_id', type=int)

    def handle(self, *args, **options):
        project_id = options['project_id']
        bulk_update_sites(project_id)
        self.stdout.write('Updating meta ans for "%d"' % project_id)
