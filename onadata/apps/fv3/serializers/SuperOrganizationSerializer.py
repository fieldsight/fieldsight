import collections

from rest_framework import serializers
from onadata.apps.fieldsight.models import SuperOrganization, Site, Project
from onadata.apps.fsforms.models import OrganizationFormLibrary, FInstance


class OrganizationSerializer(serializers.ModelSerializer):
    total_teams = serializers.SerializerMethodField()
    total_projects = serializers.SerializerMethodField()
    total_users = serializers.SerializerMethodField()
    total_organizations = serializers.SerializerMethodField()

    class Meta:
        model = SuperOrganization
        fields = ('id', 'identifier', 'name', 'type', 'phone', 'country', 'additional_desc',
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


class OrganizationFormLibrarySerializer(serializers.ModelSerializer):
    xf_title = serializers.SerializerMethodField()

    class Meta:
        model = OrganizationFormLibrary
        fields = ('id', 'xf', 'date_created', 'xf_title')
        read_only_fields = ('date_created',)

    def get_xf_title(self, obj):
        return obj.xf.title


class OrganizationGeneralScheduledFormSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField(read_only=True)
    form_type = serializers.SerializerMethodField(read_only=True)
    default_submission_status = serializers.SerializerMethodField(read_only=True)
    scheduled_type = serializers.SerializerMethodField(read_only=True)
    start_date = serializers.SerializerMethodField(read_only=True)
    end_date = serializers.SerializerMethodField(read_only=True)
    total_submissions = serializers.SerializerMethodField(read_only=True)
    last_response_on = serializers.SerializerMethodField(read_only=True)
    submissions = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = OrganizationFormLibrary
        fields = ('id', 'title', 'form_type', 'default_submission_status', 'scheduled_type', 'start_date', 'end_date',
                  'total_submissions', 'last_response_on', 'submissions')

    def get_title(self, obj):
        return obj.xf.title

    def get_form_type(self, obj):
        return obj.get_form_type_display()

    def get_default_submission_status(self, obj):
        return obj.get_default_submission_status_display()

    def get_scheduled_type(self, obj):
        return obj.get_schedule_level_id_display()

    def get_start_date(self, obj):
        return obj.date_range_start

    def get_end_date(self, obj):
        return obj.date_range_end

    def get_total_submissions(self, obj):
        fxf_ids = obj.organization_forms.values_list('id', flat=True)
        instances = FInstance.objects.filter(organization_fxf_id__in=fxf_ids).count()
        return instances

    def get_submissions(self, obj):
        data = [{'pending': len(o.pending),
                 'rejected': len(o.rejected),
                 'flagged': len(o.flagged),
                 'approved': len(o.approved)
                 }
                for o in obj.organization_forms.all()]
        if not data:
            data = [{'pending': 0,
                     'rejected': 0,
                     'flagged': 0,
                     'approved': 0
                     }]
        counter = collections.Counter()
        for d in data:
            counter.update(d)
        return counter

    def get_last_response_on(self, obj):
        try:
            last_response = obj.last_response[:1][0].date
        except:
            last_response = ''

        return last_response


class OrganizationFormSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField(read_only=True)
    form_type = serializers.SerializerMethodField(read_only=True)
    submissions = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = OrganizationFormLibrary
        fields = ('id', 'title', 'form_type', 'submissions')

    def get_title(self, obj):
        return obj.xf.title

    def get_form_type(self, obj):
        return obj.get_form_type_display()

    def get_submissions(self, obj):

        data = [{'pending': len(o.pending),
                 'rejected': len(o.rejected),
                 'flagged': len(o.flagged),
                 'approved': len(o.approved)
                 }
                for o in obj.organization_forms.all()]
        if not data:
            data = [{'pending': 0,
                     'rejected': 0,
                     'flagged': 0,
                     'approved': 0
                     }]
        counter = collections.Counter()
        for d in data:
            counter.update(d)
        return counter


class OrganizationProjectsFormSerializer(serializers.ModelSerializer):
    submissions = serializers.SerializerMethodField(read_only=True)
    total_submissions = serializers.SerializerMethodField(read_only=True)
    team = serializers.SerializerMethodField(read_only=True)
    last_response_on = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Project
        fields = ('id', 'name', 'submissions', 'team', 'last_response_on', 'total_submissions')

    def get_total_submissions(self, obj):

        return len(obj.project_instances_count)

    def get_team(self, obj):
        return obj.organization.name

    def get_last_response_on(self, obj):
        try:
            last_response = obj.last_response[:1][0].date
        except:
            last_response = ''

        return last_response

    def get_submissions(self, obj):

        data = [{'pending': len(o.pending),
                 'rejected': len(o.rejected),
                 'flagged': len(o.flagged),
                 'approved': len(o.approved)
                 }
                for o in obj.project_forms.all()]
        if not data:
            data = [{'pending': 0,
                     'rejected': 0,
                     'flagged': 0,
                     'approved': 0
                     }]
        counter = collections.Counter()
        for d in data:
            counter.update(d)
        return counter
