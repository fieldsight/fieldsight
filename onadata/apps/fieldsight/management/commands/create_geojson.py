from django.core.management.base import BaseCommand
from onadata.apps.fieldsight.models import Project, ProjectGeoJSON


class Command(BaseCommand):
	help = 'Create site data Geojson file backup for all projects'


	def handle(self, *args, **options):
		projects = Project.objects.filter(is_active=True)
		new_projects = 0
		for project in projects:
			try:
				project_jeojson = project.project_geojson
			except:
				project_jeojson = ProjectGeoJSON.objects.create(project_id=project.id)
			project_jeojson.save()
			new_projects += 1
			project_jeojson.generate_new()
		self.stdout.write('Created "%s " new projects geo data with success!' % new_projects)
