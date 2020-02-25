import time

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from onadata.apps.userrole.models import UserRole


class Command(BaseCommand):
    help = 'Delete Site Supervisor role if user in Region.'

    def add_arguments(self, parser):
        parser.add_argument('project_id', type=int)

    def handle(self, *args, **options):
        batchsize = 25
        project_id = options.get("project_id")
        users = User.objects.filter(user_roles__project_id=project_id).distinct('id').values_list('id', flat=True)
        stop = False
        offset = 0
        while stop is not True:
            time.sleep(5)

            limit = offset + batchsize
            users_list = users[offset:limit]
            if users_list:
                for user in users_list:

                    region_supervisor_ids = UserRole.objects.filter(user=user, group__name="Region Supervisor",
                                                                    ended_at=None).values_list('region', flat=True)
                    site_supervisor_roles = UserRole.objects.filter(user=user, group__name="Site Supervisor",
                                                                    site__region_id__in=region_supervisor_ids).delete()

                self.stdout.write('Deleted Site supervisors successfully for batch {}-{}'.format(offset, limit))

                offset += batchsize

            else:
                stop = True
