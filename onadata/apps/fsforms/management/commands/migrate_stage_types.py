from django.core.management.base import BaseCommand
from django.conf import settings

from onadata.apps.fieldsight.models import SiteType
from onadata.apps.fsforms.models import Stage


class Command(BaseCommand):
    help = 'Migrate Stage types where types is [] or substage types is []'

    def add_arguments(self, parser):
        parser.add_argument('project', type=int)

    def handle(self, *args, **options):
        project = options['project']
        site_types = SiteType.objects.filter(project=project, deleted=False).values_list('pk', flat=True)
        stages_id = Stage.objects.filter(project=project, tags=[], is_deleted=False, stage__isnull=True
                                         ).values_list('pk', flat=True)
        Stage.objects.filter(pk__in=stages_id).update(tags=list(site_types))
        Stage.objects.filter(stage__id__in=stages_id, tags=[], is_deleted=False).update(tags=list(site_types))
        stages = Stage.objects.filter(project=project, stage__isnull=True).exclude(pk__in=stages_id)\
            .prefetch_related("parent")
        for stage in stages:
            print(stage.id)
            substages = stage.parent.all()
            for substage in substages:
                substage_tags = substage.tags
                sub_stage_pure_tags = [t for t in substage_tags if t in stage.tags]
                tags_with_parent = sub_stage_pure_tags + stage.tags
                substage.tags = list(set(tags_with_parent))
                substage.save()

        self.stdout.write('Migrating  stage types in project "%s"' % str(project))
