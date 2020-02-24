import json
from django.core.management.base import BaseCommand



class Command(BaseCommand):
    help = 'Create default groups'

    def handle(self, *args, **options):
        pass