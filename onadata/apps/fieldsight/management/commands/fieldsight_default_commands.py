from django.core import management
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Run all default fieldsight commands.'

    def handle(self, *args, **options):
        management.call_command("create_groups",)
        management.call_command("create_default_superuser",)
        management.call_command("create_days", )
        management.call_command("create_timezones", )
        management.call_command("create_organization_type",)
        management.call_command("create_project_type",)
        management.call_command("create_sectors",)
        management.call_command("create_banks",)
        management.call_command("create_packages",)