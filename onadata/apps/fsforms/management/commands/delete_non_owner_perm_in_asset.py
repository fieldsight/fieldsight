from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from django.db.models import Q

from onadata.apps.fsforms.models import Asset, ObjectPermission


class Command(BaseCommand):
    help = 'Delete non owner object permission of kpi object.'

    def add_arguments(self, parser):
        parser.add_argument('uid', type=str)

    def handle(self, *args, **options):
        uid = options['uid']
        try:
            asset = Asset.objects.get(uid=uid)
            user = asset.owner
            ObjectPermission.objects.filter(~(Q(user=user)), object_id=asset.id).delete()
            self.stdout.write('Deleted successfully.')

        except ObjectDoesNotExist as e:
            self.stdout.write(str(e))
