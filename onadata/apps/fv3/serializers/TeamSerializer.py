import json,os,requests

from django.core.serializers import serialize
from django.conf import settings

from rest_framework import serializers

from onadata.apps.fieldsight.models import Organization, Site, Project
from onadata.apps.fv3.serializer import Base64ImageField
from onadata.apps.subscriptions.models import Package, Subscription
from onadata.apps.geo.models import GeoLayer
from onadata.apps.userrole.models import UserRole


class TeamSerializer(serializers.ModelSerializer):

    total_sites = serializers.SerializerMethodField()
    submissions = serializers.SerializerMethodField()
    contact = serializers.SerializerMethodField()
    projects = serializers.SerializerMethodField()
    admin = serializers.SerializerMethodField()
    total_projects = serializers.SerializerMethodField()
    total_users = serializers.SerializerMethodField()
    breadcrumbs = serializers.SerializerMethodField()
    package_details = serializers.SerializerMethodField()
    stripe_token = serializers.SerializerMethodField()
    map = serializers.SerializerMethodField()

    class Meta:
        model = Organization
        fields = ('id', 'name', 'address', 'logo', 'public_desc', 'contact', 'total_sites', 'total_projects',
                  'total_users', 'submissions', 'projects', 'admin', 'breadcrumbs', 'package_details', 'stripe_token',
                  'map')

    def get_total_sites(self, obj):

        total_sites = Site.objects.filter(project__organization=obj,
                                          is_survey=False,
                                          is_active=True).count()

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
        qs = obj.projects.filter(is_active=True)
        projects = []
        for obj in qs:
            projects.append({'id': obj.id, 'name': obj.name, 'logo': obj.logo.url, 'address': obj.address})

        return projects

    def get_admin(self, obj):
        admin_queryset = obj.organization_roles.select_related('user', 'user__user_profile').\
            filter(ended_at__isnull=True, group__name="Organization Admin")

        data = [{'id': admin.user.id, 'full_name': admin.user.get_full_name(), 'email': admin.user.email, 'profile':
            admin.user.user_profile.profile_picture.url} for admin in admin_queryset]

        return data

    def get_total_projects(self, obj):
        return obj.projects.filter(is_active=True).count()

    def get_total_users(self, obj):
        return obj.organization_roles.filter(ended_at__isnull=True).distinct('user_id').count()

    def get_breadcrumbs(self, obj):
        request = self.context['request']
        if request.is_super_admin:
            return {'name': obj.name, 'teams': 'Teams', 'teams_url': '/fieldsight/application/#/teams'}

        else:
            return {'name': obj.name}

    def get_map(self, obj):

        sites = Site.objects.filter(project__organization=obj, is_survey=False, is_active=True).exclude(location=None)[:100]
        data = serialize('custom_geojson', sites, geometry_field='location',
                         fields=('name', 'public_desc', 'additional_desc', 'address', 'location', 'phone', 'id'))

        return json.loads(data)

    def get_package_details(self, obj):
        packages = []

        return packages
        # request = self.context['request']
        # has_user_free_package = Subscription.objects.filter(stripe_sub_id="free_plan", stripe_customer__user=request.user,
        #                             organization=obj).exists()
        # if not request.user.is_superuser and obj.owner == request.user and has_user_free_package:
        #     packages_qs = Package.objects.all()
        #     packages = [{'plan': package.get_plan_display(), 'submissions': package.submissions, 'total_charge':
        #         package.total_charge, 'extra_submissions_charge': package.extra_submissions_charge, 'period_type':
        #         package.get_period_type_display()} for package in packages_qs]
        #     return packages

    def get_stripe_token(self, obj):
        # return settings.STRIPE_PUBLISHABLE_KEY
        return ''


class TeamProjectSerializer(serializers.ModelSerializer):

    total_users = serializers.SerializerMethodField()
    total_submissions = serializers.SerializerMethodField()
    total_regions = serializers.SerializerMethodField()
    total_sites = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ('id', 'name', 'address', 'logo', 'total_users', 'total_submissions', 'total_regions', 'total_sites')

    def get_total_users(self, obj):
        users = obj.project_roles.count()

        return users

    def get_total_submissions(self, obj):
        instances = obj.project_instances.count()
        return instances

    def get_total_regions(self, obj):
        regions = obj.project_region.count()

        return regions

    def get_total_sites(self, obj):
        sites = obj.sites.count()

        return sites


class TeamUpdateSerializer(serializers.ModelSerializer):
    logo = Base64ImageField(
        max_length=None, use_url=True, allow_empty_file=True, allow_null=True, required=False
    )

    class Meta:
        model = Organization
        fields = ('id', 'name', 'identifier', 'type', 'phone', 'email', 'address', 'website', 'public_desc', 'logo',
                  'location', 'country')


class TeamGeoLayer(serializers.ModelSerializer):
    properties = serializers.SerializerMethodField()

    class Meta:
        model = GeoLayer
        fields = ('id', 'organization', 'level', 'title', 'title_prop', 'code_prop', 'geo_shape_file', 'tolerance',
                  'properties')

    def get_properties(self, obj):
        if obj.geo_shape_file:
            path = obj.geo_shape_file.url
            response = requests.get(path)
            read_data = json.loads(response.content)
            properties = read_data['features'][0]['properties'].keys()
            # update_properties = properties.pop('id', None)

            return properties