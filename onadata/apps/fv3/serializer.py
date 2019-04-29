from rest_framework import serializers

from onadata.apps.fieldsight.models import Project, Organization, Region


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ('name', 'id')


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ('id', 'name')


class ProjectSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer()
    project_region = RegionSerializer(many=True)
    meta_attributes = serializers.SerializerMethodField()
    has_unassigned_sites = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ('name', 'id', 'latitude', 'longitude', 'address', 'public_desc', 'type', 'phone',
                  'organization', 'project_region', 'meta_attributes', 'has_unassigned_sites')

    def get_meta_attributes(self, obj):
        filtered_ma = []
        for ma in obj.site_meta_attributes:
            if ma['question_type'] in ['Text', 'Number', 'MCQ', 'Date']:
                filtered_ma.append(ma)
        return filtered_ma

    def get_has_unassigned_sites(self, obj):
        return obj.has_unassigned_sites
