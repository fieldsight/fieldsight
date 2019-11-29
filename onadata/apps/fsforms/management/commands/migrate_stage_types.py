from django.core.management.base import BaseCommand
from django.conf import settings
from django.db.models import Count

from onadata.apps.fieldsight.models import SiteType, Region, Project
from onadata.apps.fsforms.models import Stage


class Command(BaseCommand):
    help = 'Migrate Stage types old [] to [all tags]'

    def handle(self, *args, **options):
        project_ids = Stage.objects.filter(stage__isnull=True, project__isnull=False).order_by('project').distinct().values_list('project', flat=True)
        for project in project_ids:
            site_types = SiteType.objects.filter(project=project, deleted=False).values_list('pk', flat=True)
            regions = Region.objects.filter(project=project, is_active=True).values_list('pk', flat=True)
            regions = list(regions)
            if regions:
                regions.append(0)
                Stage.objects.filter(project=project).update(regions=regions)
                Stage.objects.filter(stage__project=project).update(regions=regions)
            if site_types:
                stages_id = Stage.objects.filter(project=project, tags=[], is_deleted=False, stage__isnull=True
                                                 ).values_list('pk', flat=True)
                list(stages_id)
                stages = Stage.objects.filter(project=project, stage__isnull=True).exclude(pk__in=stages_id) \
                    .prefetch_related("parent")
                list(stages)
                stages_with_no_types = Stage.objects.filter(pk__in=stages_id).prefetch_related("parent")
                # print(stages_with_no_types, "no types")
                list(stages_with_no_types)
                site_types = list(site_types)
                if site_types:
                    if 0 not in site_types:
                        site_types.append(0)

                # print(Stage.objects.filter(stage__tags=[], stage__project=project, tags=[]))
                Stage.objects.filter(stage__tags=[], stage__project=project, tags=[]).update(tags=site_types)
                Stage.objects.filter(pk__in=stages_id).update(tags=site_types)

                for stage in stages: # stages with some tags
                    if 0 not in stage.tags:
                        parent_tags = list(stage.tags)
                        parent_tags.append(0)
                        stage.tags = list(set(parent_tags))
                        stage.save()
                    substages = stage.parent.all()
                    for substage in substages:
                        substage_tags = substage.tags
                        if substage_tags:
                            tags_with_parent = substage_tags
                            if 0 not in tags_with_parent:
                                tags_with_parent.append(0)
                            substage.tags = list(set(tags_with_parent))
                        else:
                            tags_with_parent = substage_tags + stage.tags # add parent tag and 0 to substage
                            if 0 not in tags_with_parent:
                                tags_with_parent.append(0)
                            substage.tags = list(set(tags_with_parent))
                        substage.save()

                for stage in stages_with_no_types:
                    substages = stage.parent.all().exclude(tags=[])
                    for substage in substages:
                        substage_tags = substage.tags
                        substage_tags = list(substage_tags)
                        if 0 not in substage_tags:
                            substage_tags.append(0)
                        substage.tags = list(set(substage_tags))
                        substage.save()

        self.stdout.write('Migrating  stage types in project ')
