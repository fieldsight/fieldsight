from __future__ import unicode_literals

import os
import sys
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from onadata.apps.fsforms.models import FieldSightXF
from onadata.apps.userrole.models import UserRole
from onadata.apps.fsforms.tasks import share_forms
from onadata.apps.fieldsight.models import Project

class Command(BaseCommand):
    help = 'Share XForm to the project managers and organization admin of each project'

    def add_arguments(self, parser):
        parser.add_argument('project', type=int)

    def handle(self, *args, **options):
        project = Project.objects.get(id=options['project'])
        userrole = UserRole.objects.filter(
            project=project,
            organization=project.organization,
            group__name__in=["Project Manager", "Organization Admin"],
            ended_at__isnull=False)
        users = User.objects.filter(user_roles__in=userrole)
        for user in users:
            fxf = FieldSightXF.objects.filter(project=project)
            shared = share_forms(user, fxf)
            if shared:
                sys.stdout.write('Forms of project {} shared to user {}\n'.format(project.name, user.username))

