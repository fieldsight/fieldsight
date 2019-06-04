from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group

from onadata.apps.fsforms.models import InstanceStatusChanged, FInstance


class Command(BaseCommand):
    help = 'Create default groups'

    def handle(self, *args, **options):
        batchsize = 100
        stop = False
        offset = 0
        self.stdout.write('Starting copying message .. "%s"' % "")
        data = InstanceStatusChanged.objects.all().order_by("-finstance", "-date").values_list(
            "finstance", "message").distinct('finstance')
        while stop is not True:
            limit = offset + batchsize
            slice = data[offset:limit]
            self.stdout.write('copying from .. "%s" to "%s"' % (str(offset), str(limit)))
            if slice:
                for i, comment in slice:
                    FInstance.objects.filter(pk=i).update(comment=comment)
                offset += batchsize
            else:
                stop = True
