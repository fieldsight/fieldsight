import json

from django.core.serializers import serialize

from rest_framework import serializers

from onadata.apps.fieldsight.models import Organization, Site, Project
from onadata.apps.userrole.models import UserRole


class OrganizationSerializer(serializers.ModelSerializer):

    total_sites = serializers.SerializerMethodField()
    submissions = serializers.SerializerMethodField()
    contact = serializers.SerializerMethodField()
    projects = serializers.SerializerMethodField()
    admin = serializers.SerializerMethodField()
    map_data = serializers.SerializerMethodField()

    class Meta:
        model = Organization
        fields = ('id', 'name', 'address', 'logo', 'public_desc', 'contact', 'total_sites',
                  'submissions', 'projects', 'admin', 'map_data')

    def get_total_sites(self, obj):

        total_sites = Site.objects.filter(project__organization=obj, is_survey=False, is_active=True).count()

        return total_sites

    def get_submissions(self, obj):
        outstanding, flagged, approved, rejected = obj.get_submissions_count()
        total_submissions = flagged + approved + rejected + outstanding
        submissions = {'total_submissions': total_submissions, 'pending': outstanding, 'flagged': flagged, 'approved':
                       approved, 'rejected': rejected}

        return submissions

    def get_contact(self, obj):

        contact = {'phone': obj.phone, 'email': obj.email, 'website': obj.website}

        return contact

    def get_projects(self, obj):
        projects = Project.objects.filter(organization_id=obj.pk, is_active=True).values('id', 'name', 'logo')

        return projects

    def get_admin(self, obj):
        admin = UserRole.objects.filter(organization=obj, ended_at__isnull=True, group__name="Organization Admin").\
            values('id', 'user__username', 'user__email', 'user__user_profile__profile_picture')

        return admin

    def get_map_data(self, obj):
        sites = Site.objects.filter(project__organization=obj, is_survey=False, is_active=True)[:100]
        data = serialize('custom_geojson', sites, geometry_field='location',
                         fields=('name', 'public_desc', 'additional_desc', 'address', 'location', 'phone', 'id'))

        return json.loads(data)





