from rest_framework import serializers

from onadata.apps.fieldsight.models import Project, Organization, Region, Site


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ('name', 'id')


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ('id', 'name')


class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = ('id', 'name', 'latitude', 'longitude', 'address', 'phone',
                  'current_progress', 'identifier', 'type', 'region', 'project', 'date_modified', 'is_active', 'site_meta_attributes_ans'
                                                                                                               ''
                                                                                                               '')


class ProjectSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer()
    project_region = RegionSerializer(many=True)
    meta_attributes = serializers.SerializerMethodField()
    has_site_role = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ('name', 'id', 'address', 'organization', 'project_region', 'meta_attributes', 'has_site_role', 'url')

    def get_meta_attributes(self, obj):
        filtered_ma = []
        for ma in obj.site_meta_attributes:
            if ma['question_type'] in ['Text', 'Number', 'MCQ', 'Date']:
                filtered_ma.append(ma)
        return filtered_ma

    def get_has_site_role(self, obj):
        return obj.has_site_role

    def get_url(self, obj):
        return obj.logo.url
