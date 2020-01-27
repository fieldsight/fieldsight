from optparse import make_option

from django.core.management.base import BaseCommand
from onadata.apps.logger.models import Instance
from onadata.apps.viewer.models.parsed_instance import update_mongo_instance


class Command(BaseCommand):
    help = 'Create mongo submission data from postgres'


    def add_arguments(self, parser):
        parser.add_argument('batchsize', type=int)

    def handle(self, *args, **kwargs):
        batchsize = kwargs.get("batchsize", 100)
        stop = False
        offset = 0
        while stop is not True:
            limit = offset + batchsize
            instances = Instance.objects.filter(
                deleted_at__isnull=True, fieldsight_instance__isnull=False,
                fieldsight_instance__is_deleted=False).order_by('-date_created')[offset:limit]
            if instances:
                for i in instances:
                    d = i.parsed_instance.to_dict_for_mongo()
                    try:
                        x = i.fieldsight_instance
                        d.update({'fs_project_uuid': str(x.project_fxf_id), 'fs_project': x.project_id,
                                  'fs_status': 0, 'fs_site': x.site_id, 'fs_uuid': x.site_fxf_id})
                        try:
                            synced = update_mongo_instance(d, i.id)
                            print(synced, "updated in mongo success")
                        except Exception as e:
                            print(str(e))
                    except Exception as e:
                        print(str(e))
                offset += batchsize
            else:
                stop = True
