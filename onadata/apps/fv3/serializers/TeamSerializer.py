import json

from django.core.serializers import serialize

from rest_framework import serializers

from onadata.apps.fieldsight.models import Organization, Site, Project


class TeamSerializer(serializers.ModelSerializer):

    total_sites = serializers.SerializerMethodField()
    submissions = serializers.SerializerMethodField()
    contact = serializers.SerializerMethodField()
    projects = serializers.SerializerMethodField()
    admin = serializers.SerializerMethodField()
    total_projects = serializers.SerializerMethodField()
    total_users = serializers.SerializerMethodField()
    breadcrumbs = serializers.SerializerMethodField()

    class Meta:
        model = Organization
        fields = ('id', 'name', 'address', 'logo', 'public_desc', 'contact', 'total_sites', 'total_projects',
                  'total_users', 'submissions', 'projects', 'admin', 'breadcrumbs')

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
        projects = obj.projects.filter(is_active=True).values('id', 'name', 'logo', 'address')

        return projects

    def get_admin(self, obj):
        admin_queryset = obj.organization_roles.filter(ended_at__isnull=True, group__name="Organization Admin")

        data = [{'id': admin.id, 'full_name': admin.user.get_full_name(), 'email': admin.user.email, 'profile':
            admin.user.user_profile.profile_picture.url} for admin in admin_queryset]

        return data

    def get_total_projects(self, obj):
        return obj.projects.filter(is_active=True).count()

    def get_total_users(self, obj):
        return obj.organization_roles.filter(ended_at__isnull=True).distinct('user_id').count()

    def get_breadcrumbs(self, obj):
        request = self.context['request']
        if request.is_super_admin:
            return {'name': obj.name, 'teams': 'Teams', 'teams_url': '/fieldsight/organization'}

        else:
            return {'name': obj.name}

    def get_map_data(self, obj):
        sites = Site.objects.filter(project__organization=obj, is_survey=False, is_active=True)[:100]
        data = serialize('custom_geojson', sites, geometry_field='location',
                         fields=('name', 'public_desc', 'additional_desc', 'address', 'location', 'phone', 'id'))

        return json.loads(data)






