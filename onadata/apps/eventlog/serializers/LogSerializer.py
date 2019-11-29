import json
from urlparse import urlparse

from django.contrib.gis.geos import Point
from rest_framework import serializers
from onadata.apps.eventlog.models import FieldSightLog, CeleryTaskProgress
from onadata.apps.fieldsight.models import ProjectLevelTermsAndLabels, Project, Site

from django.shortcuts import get_object_or_404

from onadata.apps.fsforms.models import FieldSightXF


class LogSerializer(serializers.ModelSerializer):
    source_uid = serializers.ReadOnlyField(source='source_id', read_only=True)
    source_name = serializers.SerializerMethodField(read_only=True)
    source_img = serializers.ReadOnlyField(source='source.user_profile.profile_picture.url', read_only=True)
    get_source_url = serializers.ReadOnlyField()
    
    get_event_name = serializers.ReadOnlyField()
    get_event_url = serializers.ReadOnlyField()

    get_extraobj_name = serializers.ReadOnlyField()
    get_extraobj_url = serializers.ReadOnlyField()

    get_absolute_url = serializers.ReadOnlyField()

    extra_json = serializers.JSONField(binary=False)
    
    # org_name = serializers.ReadOnlyField(source='organization.name', read_only=True)
    # get_org_url = serializers.ReadOnlyField()

    # project_name = serializers.ReadOnlyField(source='project.name', read_only=True)
    # get_project_url = serializers.ReadOnlyField()

    # site_name = serializers.ReadOnlyField(source='site.name', read_only=True)
    # get_site_url = serializers.ReadOnlyField()

    class Meta:
        model = FieldSightLog
        exclude = ('description', 'is_seen', 'content_type', 'organization', 'project', 'site', 'object_id', 'extra_object_id', 'source', 'extra_content_type',)

    def get_source_name(self, obj):
        return obj.source.first_name + " " + obj.source.last_name


class NotificationSerializer(serializers.ModelSerializer):
    source_uid = serializers.ReadOnlyField(source='source_id', read_only=True)
    source_name = serializers.SerializerMethodField(read_only=True)
    source_img = serializers.ReadOnlyField(source='source.user_profile.profile_picture.url', read_only=True)
    get_source_url = serializers.ReadOnlyField()
    
    get_event_name = serializers.ReadOnlyField()
    get_event_url = serializers.SerializerMethodField()

    get_extraobj_name = serializers.ReadOnlyField()
    get_extraobj_url = serializers.ReadOnlyField()

    get_absolute_url = serializers.ReadOnlyField()
    extra_json = serializers.JSONField(binary=False)
    terms_and_labels = serializers.SerializerMethodField()
    # org_name = serializers.ReadOnlyField(source='organization.name', read_only=True)
    # get_org_url = serializers.ReadOnlyField()

    # project_name = serializers.ReadOnlyField(source='project.name', read_only=True)
    # get_project_url = serializers.ReadOnlyField()

    # site_name = serializers.ReadOnlyField(source='site.name', read_only=True)
    # get_site_url = serializers.ReadOnlyField()

    class Meta:
        model = FieldSightLog
        exclude = ('description', 'project', 'is_seen', 'content_type', 'organization', 'site', 'object_id',
                   'extra_object_id', 'source', 'extra_content_type',)

    def get_source_name(self, obj):
        return obj.source.first_name + " " + obj.source.last_name

    def get_get_event_url(self, obj):
        if obj.type in [16, 17, 18, 19, 31, 33] and obj.content_object.is_deleted if isinstance(obj.content_object,
                                                                                                FieldSightXF) else False:
            get_event_url = '#'

        else:
            get_event_url = obj.get_event_url()
        return get_event_url

    def get_terms_and_labels(self, obj):

        if obj.project:
            terms = ProjectLevelTermsAndLabels.objects.select_related('project').filter(project=obj.project)

            if terms:

                return {'site': obj.project.terms_and_labels.site,
                        'sub_site': obj.project.terms_and_labels.sub_site,
                        'donor': obj.project.terms_and_labels.donor,
                        'site_supervisor': obj.project.terms_and_labels.site_supervisor,
                        'site_reviewer': obj.project.terms_and_labels.site_reviewer,
                        'region': obj.project.terms_and_labels.region,
                        'region_supervisor': obj.project.terms_and_labels.region_supervisor,
                        'region_reviewer': obj.project.terms_and_labels.region_reviewer,
                        }


class TaskSerializer(serializers.ModelSerializer):
    source_name = serializers.SerializerMethodField(read_only=True)
    source_img = serializers.ReadOnlyField(source='user.user_profile.profile_picture.url', read_only=True)
    get_source_url = serializers.ReadOnlyField()
    get_task_type_display = serializers.ReadOnlyField()
    get_event_name = serializers.ReadOnlyField()
    get_event_url = serializers.ReadOnlyField()
    terms_and_labels = serializers.SerializerMethodField()

    class Meta:
        model = CeleryTaskProgress
        exclude = ('content_type', 'object_id', 'user',)

    def get_source_name(self, obj):
        return obj.user.first_name + " " + obj.user.last_name

    def get_terms_and_labels(self, obj):

        if obj.task_type in [0, 2, 3, 4, 8, 10, 13]:

            if obj.get_event_url():
                project_id = int(obj.get_event_url().split('/')[5])
                project = Project.objects.get(id=project_id)
                terms = ProjectLevelTermsAndLabels.objects.filter(project_id=project.id).exists()

                if terms:
                    return {'site': project.terms_and_labels.site,
                            'sub_site': project.terms_and_labels.sub_site,
                            'donor': project.terms_and_labels.donor,
                            'site_supervisor': project.terms_and_labels.site_supervisor,
                            'site_reviewer': project.terms_and_labels.site_reviewer,
                            'region': project.terms_and_labels.region,
                            'region_supervisor': project.terms_and_labels.region_supervisor,
                            'region_reviewer': project.terms_and_labels.region_reviewer,
                            }
                else:
                    return None

        elif obj.task_type == 6:
            site_id = int(obj.get_event_url().split('/')[5])
            site = Site.all_objects.get(id=site_id)
            project = Project.objects.get(id=site.project.id)

            terms = ProjectLevelTermsAndLabels.objects.filter(project_id=project.id).exists()

            if terms:

                return {'site': project.terms_and_labels.site,
                        'sub_site': project.terms_and_labels.sub_site,
                        'donor': project.terms_and_labels.donor,
                        'site_supervisor': project.terms_and_labels.site_supervisor,
                        'site_reviewer': project.terms_and_labels.site_reviewer,
                        'region': project.terms_and_labels.region,
                        'region_supervisor': project.terms_and_labels.region_supervisor,
                        'region_reviewer': project.terms_and_labels.region_reviewer,
                        }

