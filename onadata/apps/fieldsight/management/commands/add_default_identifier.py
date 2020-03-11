import string, random
from django.core.management.base import BaseCommand

from onadata.apps.fieldsight.models import SuperOrganization, Organization, Project


def randomString(stringLength):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


class Command(BaseCommand):
    help = 'Add default identifier in Organizations, Teams and Projects'

    def handle(self, *args, **options):
        organizations = SuperOrganization.objects.filter(is_active=True).values_list('id', flat=True)
        for org in organizations:
            SuperOrganization.objects.filter(id=org).update(identifier=randomString(8))
        teams = Organization.objects.filter(is_active=True).values_list('id', flat=True)
        for team in teams:
            Organization.objects.filter(id=team).update(identifier=randomString(10))
        projects = Project.objects.filter(is_active=True).values_list('id', flat=True)
        for project in projects:
            Project.objects.filter(id=project).update(identifier=randomString(12))

        self.stdout.write('Successfully added identifier')
