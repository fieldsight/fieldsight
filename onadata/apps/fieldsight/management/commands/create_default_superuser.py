import os

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group, Permission
from onadata.apps.userrole.models import UserRole
from onadata.apps.users.models import UserProfile


class Command(BaseCommand):
    help = 'Create default superuser'

    def handle(self, *args, **options):
        username = os.environ.get('username', 'admin')
        email = os.environ.get('email', 'admin@gmail.com')
        password = os.environ.get('password', '123456')
        user, _ = User.objects.get_or_create(username=username, email=email)
        user.set_password(password)
        user.save()
        codenames = ['add_asset', 'change_asset', 'delete_asset', 'view_asset', 'share_asset', 'add_finstance',
                     'change_finstance', 'add_instance', 'change_instance']
        permissions = Permission.objects.filter(codename__in=codenames)
        for permission in permissions:
            user.user_permissions.add(permission)
        super_admin = Group.objects.get(name="Super Admin")

        UserProfile.objects.get_or_create(user=user)
        new_group, created = UserRole.objects.get_or_create(user=user, group=super_admin)
        self.stdout.write('Superuser created successfully.')