import base64
import imghdr
import uuid

from django.contrib.auth.models import User
from django.core.serializers import serialize
import six, json
from django.core.files.base import ContentFile
from rest_framework import serializers


from onadata.apps.fieldsight.models import Project, Organization, Region, Site, Sector, SiteType,  ProjectLevelTermsAndLabels, SuperOrganization
from onadata.apps.fieldsight.serializers.SiteSerializer import SiteTypeSerializer


class Base64ImageField(serializers.ImageField):

    def to_internal_value(self, data):

        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                header, data = data.split(';base64,')

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            # Generate file name:
            file_name = str(uuid.uuid4())[:12] # 12 characters are more than enough.
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (file_name, file_extension, )

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ('name', 'id')


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ('id', 'name')


class SiteSerializer(serializers.ModelSerializer):
    type_label = serializers.CharField(source='type.name')
    region = serializers.SerializerMethodField()

    class Meta:
        model = Site
        fields = ('id', 'name', 'latitude', 'longitude', 'address', 'phone',
                  'current_progress', 'identifier', 'type', 'type_label', 'region', 'project',
                  'date_modified', 'is_active', 'site_meta_attributes_ans',
                  'enable_subsites', 'site')

    def get_region(self, obj):
        parent_region = self.context['parent_region']

        return parent_region


class ProjectSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer()
    project_region = RegionSerializer(many=True)
    types = SiteTypeSerializer(many=True)
    meta_attributes = serializers.SerializerMethodField()
    has_site_role = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    terms_and_labels = serializers.SerializerMethodField()
    total_regions = serializers.SerializerMethodField(read_only=True)
    total_sites = serializers.SerializerMethodField(read_only=True)
    total_users = serializers.SerializerMethodField(read_only=True)
    total_submissions = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Project

        fields = ('name', 'id', 'address', 'organization', 'project_region', 'meta_attributes', 'has_site_role', 'url',
                  'terms_and_labels', 'types', 'total_regions', 'total_sites', 'total_users', 'total_submissions')

    def get_meta_attributes(self, obj):
        filtered_ma = []
        for ma in obj.site_meta_attributes:
            if ma['question_type'] in ['Text', 'Number', 'MCQ', 'Date']:
                filtered_ma.append(ma)
        return filtered_ma

    def get_total_regions(self, obj):
        return len(obj.regions)

    def get_total_sites(self, obj):
        return obj.sites.count()

    def get_total_users(self, obj):
        return obj.project_roles.count()

    def get_total_submissions(self, obj):
        outstanding, flagged, approved, rejected = obj.get_submissions_count()
        total_submissions = outstanding + flagged + approved + rejected,
        return total_submissions[0]

    def get_has_site_role(self, obj):
        return obj.has_site_role

    def get_url(self, obj):
        if obj.logo:
            return obj.logo.url
        return None

    def get_terms_and_labels(self, obj):

        terms = ProjectLevelTermsAndLabels.objects.filter(project=obj).exists()

        if terms:
            return {'site': obj.terms_and_labels.site,
                    'donor': obj.terms_and_labels.donor,
                    'site_supervisor': obj.terms_and_labels.site_supervisor,
                    'site_reviewer': obj.terms_and_labels.site_reviewer,
                    'region': obj.terms_and_labels.region,
                    'region_supervisor': obj.terms_and_labels.region_supervisor,
                    'region_reviewer': obj.terms_and_labels.region_reviewer,
                    }


class ProjectUpdateSerializer(serializers.ModelSerializer):
    logo = Base64ImageField(
        max_length=None, use_url=True, allow_empty_file=True, allow_null=True, required=False
    )
   
    class Meta:
        model = Project
        fields = ('id', 'name', 'phone', 'email', 'address', 'website', 'donor', 'public_desc', 'logo',
                  'location', 'cluster_sites', 'sector', 'sub_sector', 'organization')


class SectorSerializer(serializers.ModelSerializer):
    subSectors = serializers.SerializerMethodField()

    class Meta:
        model = Sector
        fields = ('id', 'name', 'subSectors')

    def get_subSectors(self, obj):
        if obj.sectors:
            return obj.sectors.all().values('id', 'name')


class SiteTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = SiteType
        exclude = ()


class ProjectLevelTermsAndLabelsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectLevelTermsAndLabels
        exclude = ('sub_site',)


class ProjectSiteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Site
        fields = ('id', 'project', 'identifier', 'name', 'type', 'phone', 'address', 'public_desc', 'logo', 'longitude',
                  'latitude')


class ProjectRegionSerializer(serializers.ModelSerializer):
    number_of_sites = serializers.SerializerMethodField()

    class Meta:
        model = Region
        fields = ('id', 'project', 'identifier', 'name', 'date_created', 'parent', 'number_of_sites')

    def get_number_of_sites(self, obj):
        return obj.get_sites_count()


class ProjectSitesSerializer(serializers.ModelSerializer):
    logo = Base64ImageField(
        max_length=None, use_url=True, allow_empty_file=True, allow_null=True, required=False
    )

    class Meta:
        model = Site
        fields = ('id', 'project', 'name', 'identifier', 'address', 'region', 'phone', 'public_desc',
                  'type', 'logo', 'location')

        extra_kwargs = {'location': {'read_only': True}}


class TeamSerializer(serializers.ModelSerializer):
    team_owner = serializers.SerializerMethodField()
    team_owner_id = serializers.SerializerMethodField()
    projects = serializers.SerializerMethodField()
    users = serializers.SerializerMethodField()
    sites = serializers.SerializerMethodField()

    class Meta:
        model = Organization
        fields = ('id', 'name', 'logo', 'address', 'team_owner', 'team_owner_id', 'projects', 'users', 'sites')

    def get_team_owner(self, obj):
        return obj.owner.get_full_name() if obj.owner else None

    def get_team_owner_id(self, obj):
        return obj.owner.id if obj.owner else None

    def get_projects(self, obj):
        org_projects = obj.projects.count()

        return org_projects

    def get_sites(self, obj):
        total_sites = Site.objects.filter(project__organization=obj, is_survey=False, is_active=True).count()

        return total_sites

    def get_users(self, obj):
        users = obj.organization_roles.filter(ended_at__isnull=True).distinct('user').count()

        return users


class SuperOrganizationSerializer(serializers.ModelSerializer):
    total_sites = serializers.SerializerMethodField()
    submissions = serializers.SerializerMethodField()
    contact = serializers.SerializerMethodField()
    projects = serializers.SerializerMethodField()
    total_projects = serializers.SerializerMethodField()
    total_users = serializers.SerializerMethodField()
    breadcrumbs = serializers.SerializerMethodField()
    map = serializers.SerializerMethodField()
    total_teams = serializers.SerializerMethodField()
    teams = serializers.SerializerMethodField()

    class Meta:
        model = SuperOrganization
        fields = ('id', 'name', 'phone', 'country', 'additional_desc', 'logo',
                  'total_teams', 'email', 'total_sites', 'total_projects',
                  'total_users', 'submissions', 'contact', 'projects',
                  'breadcrumbs', 'teams', 'map')
        read_only_fields = ('total_teams', 'total_sites', 'contact',
                            'projects', 'total_projects', 'total_users', 'map',
                            'breadcrumbs', 'submissions')

    def get_submissions(self, obj):
        outstanding, flagged, approved, rejected = obj.get_submissions_count()
        total_submissions = flagged + approved + rejected + outstanding
        submissions = {'total_submissions': total_submissions,
                       'pending': outstanding, 'flagged': flagged,
                       'approved': approved, 'rejected': rejected}
        return submissions

    def get_teams(self, obj):
        qs = Project.objects.filter(is_active=True, organization__parent=obj)
        teams = []
        for i in qs:
            teams.append({'id': i.id, 'name': i.name, 'logo': i.logo.url,
                          'address': i.address})

        return teams

    def get_total_teams(self, obj):
        return Organization.objects.filter(parent=obj).count()

    def get_total_sites(self, obj):
        total_sites = Site.objects.filter(is_survey=False, is_active=True).\
            count()
        # total_sites = Site.objects.filter(project__organization__parent=obj,
        #                                   is_survey=False, is_active=True). \
        #     count()
        return total_sites

    def get_contact(self, obj):

        contact = {'phone': obj.phone, 'email': obj.email,
                   'website': obj.website}

        return contact

    def get_projects(self, obj):
        qs = Project.objects.filter(is_active=True)
        # qs = Project.objects.filter(is_active=True, organization__parent=obj)
        projects = []
        for i in qs:
            projects.append({'id': i.id, 'name': i.name, 'logo': i.logo.url,
                             'address': i.address})

        return projects

    def get_total_projects(self, obj):
        total_projects = Project.objects.filter(is_active=True).count()
        # total_projects = Project.objects.filter(is_active=True,
        #                                         organization__parent=obj). \
        #     count()
        return total_projects

    def get_total_users(self, obj):
        return User.objects.filter(is_superuser=False).count()
        # return obj.organization_roles.filter(ended_at__isnull=True).\
        #     distinct('user_id').count()

    def get_breadcrumbs(self, obj):
        request = self.context['request']
        if request.is_super_admin:
            return {'name': obj.name,
                    'super_organizations': 'SuperOrganization',
                    'super_organization_url':
                        '/fieldsight/application/#/SuperOrganizations'}

        else:
            return {'name': obj.name}

    def get_map(self, obj):
        org_obj = Organization.objects.filter(parent=obj).count()
        sites = Site.objects.filter(project=org_obj,
                                    is_survey=False,
                                    is_active=True).exclude(
            location=None)[:100]
        data = serialize('custom_geojson', sites, geometry_field='location',
                         fields=('name', 'public_desc', 'additional_desc',
                                 'address', 'location', 'phone', 'id'))

        return json.loads(data)
