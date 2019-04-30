from datetime import datetime

from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from django.db import transaction

from onadata.apps.userrole.models import UserRole
from onadata.apps.users.models import UserProfile
from django.contrib.auth import get_user_model
from django.conf import settings


class Command(BaseCommand):
    help = 'Creates region supervisor from many site supervisors'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str)

    def handle(self, *args, **options):
        username = options['username']
        self.stdout.write(username)
        user = User.objects.get(username__icontains=username)
        group = Group.objects.get(name="Region Supervisor")
        regions = UserRole.objects.filter(user=user, group__name="Site Supervisor", ended_at__isnull=False, site__region__isnull=False)\
            .order_by('site__region').distinct().values_list('site__region', flat=True)
        for r in regions:
            site_roles = UserRole.objects.filter(user=user, group__name="Site Supervisor", site__region=r, ended_at__isnull=False)
            if len(site_roles) > 50:
                with transaction.atomic():
                    UserRole.objects.filter(user=user, group__name="Site Supervisor", site__region=r, ended_at__isnull=False).update(ended_at=datetime.now())
                    _, created = UserRole.objects.get_or_create(user=user, group=group, region_id=r)
                    print ("cleaned in region ", r, created)











