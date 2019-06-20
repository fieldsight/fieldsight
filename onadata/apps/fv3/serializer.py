from rest_framework import serializers

from onadata.apps.fieldsight.models import Project, Organization, Region, Site, Sector, SiteType, \
    ProjectLevelTermsAndLabels


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
                  'current_progress', 'identifier', 'type', 'region', 'project', 'date_modified', 'is_active', 'site_meta_attributes_ans')


class ProjectSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer()
    project_region = RegionSerializer(many=True)
    meta_attributes = serializers.SerializerMethodField()
    has_site_role = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    terms_and_labels = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ('name', 'id', 'address', 'organization', 'project_region', 'meta_attributes', 'has_site_role', 'url',
                  'terms_and_labels')

    def get_meta_attributes(self, obj):
        filtered_ma = []
        for ma in obj.site_meta_attributes:
            if ma['question_type'] in ['Text', 'Number', 'MCQ', 'Date']:
                filtered_ma.append(ma)
        return filtered_ma

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
        exclude = ()


class ProjectSiteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Site
        fields = ('id', 'project', 'identifier', 'name', 'type', 'phone', 'address', 'public_desc', 'logo', 'longitude',
                  'latitude')


class ProjectRegionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Region
        fields = ('id', 'project', 'identifier', 'name', 'date_created', 'parent')


class ProjectSitesSerializer(serializers.ModelSerializer):
    region = serializers.CharField(source='region.name')
    submissions = serializers.SerializerMethodField()
    progress = serializers.SerializerMethodField()

    class Meta:
        model = Site
        fields = ('id', 'project', 'name', 'identifier', 'address', 'region', 'submissions', 'progress', 'phone', 'public_desc',
                  'type', 'logo')

        extra_kwargs = {
            'project': {'write_only': True},
            'phone': {'write_only': True},
            'public_desc': {'write_only': True},
            'type': {'write_only': True},
            'logo': {'write_only': True}

        }

    def get_submissions(self, obj):
        response = obj.get_site_submission_count()

        return response['flagged'] + response['approved'] + response['rejected'] + response['outstanding']

    def get_progress(self, obj):
        site_progress = obj.progress()

        return site_progress


