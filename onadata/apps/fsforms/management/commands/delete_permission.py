from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.auth.models import Permission


class Command(BaseCommand):
    help = 'Delete unwanted permission object that is created after migration'

    def handle(self, *args, **kwargs):
        try:
            Permission.objects.get(codename='change_asset', content_type__app_label='fsforms').delete()
            self.stdout.write('Deleted permission object for fsform change_asset.')
        except Permission.DoesNotExist:
            self.stdout.write('Permission object is already deleted.')

