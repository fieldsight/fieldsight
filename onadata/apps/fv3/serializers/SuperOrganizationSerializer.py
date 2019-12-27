from rest_framework import serializers
from onadata.apps.fieldsight.models import SuperOrganization, Site


class OrganizationSerializer(serializers.ModelSerializer):
    total_teams = serializers.SerializerMethodField()
    total_projects = serializers.SerializerMethodField()
    total_users = serializers.SerializerMethodField()
    total_organizations = serializers.SerializerMethodField()

    class Meta:
        model = SuperOrganization
        fields = ('id', 'name', 'type', 'phone', 'country', 'additional_desc',
                  'logo',  'logs', 'total_teams', 'total_projects',
                  'total_users', 'total_organizations')
        read_only_fields = ('total_projects', 'total_teams', 'total_users',
                            'total_organizations', 'date_created')

    def get_total_organizations(self, obj):
        pass
        # return SuperOrganization.objects.all().count()

    def get_total_teams(self, obj):
        pass
        # return obj.Organization.objects.filter(parent=obj).count()

    def get_teams(self, obj):
        pass
        # team_data = obj.organization.filter(is_active=True, parent=obj)
        # teams = []
        # for obj in team_data:
        #     teams.append({'id': obj.id, 'name': obj.name,
        #                   "country": obj.country, 'logo': obj.logo.url,
        #                   'address': obj.address})
        # return teams

    def get_total_sites(self, obj):
        pass
        # total_sites = Site.objects.filter(project__organization=obj,
        #                                   is_survey=False, is_active=True)\
        #     .count()
        #
        # return total_sites

    def get_total_projects(self, obj):
        pass
        # return obj.projects.filter(is_active=True).count()

    def get_total_users(self, obj):
        pass
        # return obj.organization_roles.filter(ended_at__isnull=True).distinct(
        #     'user_id').count()
