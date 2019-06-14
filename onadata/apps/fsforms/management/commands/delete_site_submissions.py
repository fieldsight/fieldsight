import datetime

from django.core.management.base import BaseCommand
from django.conf import settings

from onadata.apps.fsforms.models import FInstance
from onadata.apps.logger.models import Instance
from onadata.apps.fieldsight.models import Site


class Command(BaseCommand):
    help = 'Delete all submissions from mongo and postgres of given deleted sites.'

    def add_arguments(self, parser):
        parser.add_argument('-l', '--site_identifier', nargs='+',
                            help=' python manage.py delete_site_submissions  -l '
                                 '<site_identifier1> <site_identifier2> <site_identifier3 '
                                 '<....site_identifiern>', required=True)

    def handle(self, *args, **options):

        deleted_site_identifier = options['site_identifier']

        for site_id in deleted_site_identifier:

            try:

                site = Site.all_objects.get(identifier=site_id, is_active=False)

                instances = site.site_instances.all().values_list('instance', flat=True)

                # soft delete in postgres
                Instance.objects.filter(id__in=instances).update(deleted_at=datetime.datetime.now())

                # soft delete in mongo

                result = settings.MONGO_DB.instances.update({"_id": {"$in": list(instances)}},
                                                            {"$set": {'_deleted_at': datetime.datetime.now()}}, multi=True)

                FInstance.objects.filter(instance_id__in=instances).update(is_deleted=True)

                self.stdout.write('Successfully deleted submissions for "%s"' % site_id)

            except Exception as e:
                print('Error for ' + site_id + ':', e)

