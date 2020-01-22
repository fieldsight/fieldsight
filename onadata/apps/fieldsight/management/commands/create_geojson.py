from django.core.management.base import BaseCommand
from onadata.apps.fieldsight.models import Project, ProjectGeoJSON


class Command(BaseCommand):
	help = 'Create site data Geojson file backup for all projects'

	def add_arguments(self, parser):
		parser.add_argument('project_id', type=int)

	def handle(self, *args, **options):
		project_id = options['project_id']

		if project_id != 0:
			project = Project.objects.get(id=project_id)
			try:
				project_geojson = project.project_geojson
			except:
				project_geojson = ProjectGeoJSON.objects.create(project_id=project.id)
				project_geojson.save()
			project_geojson.generate_new()
			self.stdout.write('Created new project geo data with success for "%s "' % project.name)
		else:
			projects = Project.objects.filter(is_active=True)
			new_projects = 0
			for project in projects:
				try:
					project_geojson = project.project_geojson
				except:
					project_geojson = ProjectGeoJSON.objects.create(project_id=project.id)
				project_geojson.save()
				new_projects += 1
				project_geojson.generate_new()
			self.stdout.write('Created "%s " new projects geo data with success!' % new_projects)