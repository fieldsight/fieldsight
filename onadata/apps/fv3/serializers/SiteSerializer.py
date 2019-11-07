from datetime import datetime
from collections import OrderedDict

from django.db.models import Q
from django.conf import settings
from rest_framework import serializers
from rest_framework.reverse import reverse_lazy

from onadata.apps.eventlog.models import FieldSightLog
from onadata.apps.fieldsight.models import Site, ProjectLevelTermsAndLabels
from onadata.apps.fv3.serializer import Base64ImageField
from onadata.apps.userrole.models import UserRole
from onadata.apps.users.models import UserProfile
from django.core.exceptions import ObjectDoesNotExist
from onadata.apps.fsforms.line_data_project import ProgressGeneratorSite
from onadata.apps.fsforms.models import FInstance, Stage
from onadata.apps.fv3.role_api_permissions import has_write_permission_in_site
from onadata.apps.fieldsight.models import BluePrints

from onadata.apps.fsforms.line_data_project import date_range


class FormSubmissionChartGenerator(object):

    def __init__(self, site):
        self.site = site
        self.date_list = list(date_range(site.date_created.strftime("%Y%m%d"), datetime.today().strftime("%Y%m%d"), 6))

    def get_count(self, date):
        import datetime as dt
        date = date + dt.timedelta(days=1)
        obj = self.site.site_instances.filter(date__lte=date.date())
        total_submissions = obj.count()
        pending_submissions = obj.filter(form_status=0).count()
        rejected_submissions = obj.filter(form_status=1).count()
        flagged_submissions = obj.filter(form_status=2).count()
        approved_submissions = obj.filter(form_status=3).count()

        return {'total_submissions': total_submissions, 'pending_submissions': pending_submissions, 'approved_submissions':
                approved_submissions, 'rejected_submissions': rejected_submissions, 'flagged_submissions': flagged_submissions}

    def data(self):
        d = OrderedDict()
        dt = self.date_list
        for date in dt:
            count = self.get_count(date)
            d[date.strftime('%Y-%m-%d')] = count
        return d


class SiteSerializer(serializers.ModelSerializer):

    region = serializers.CharField(source='region.name')
    submissions = serializers.SerializerMethodField()
    total_users = serializers.SerializerMethodField()
    total_subsites = serializers.SerializerMethodField()
    users = serializers.SerializerMethodField()
    site_progress_chart_data = serializers.SerializerMethodField()
    form_submissions_chart_data = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    terms_and_labels = serializers.SerializerMethodField()
    has_write_permission = serializers.SerializerMethodField()
    project_id = serializers.SerializerMethodField()
    breadcrumbs = serializers.SerializerMethodField()
    type = serializers.CharField(source='type.name')

    class Meta:
        model = Site
        fields = ('id', 'name', 'type', 'identifier', 'project_id', 'address', 'logo', 'public_desc', 'location',
                  'region', 'enable_subsites', 'site', 'total_users', 'users', 'submissions',
                  'form_submissions_chart_data', 'site_progress_chart_data', 'total_subsites', 'terms_and_labels',
                  'has_write_permission', 'breadcrumbs', 'current_progress')

    def get_submissions(self, obj):
        queryset = FInstance.objects.order_by('-date')
        total_sites = list(obj.sub_sites.values_list('id', flat=True))
        total_sites.append(obj.id)
        total_submissions = queryset.filter(site__in=total_sites).count()
        outstanding = queryset.filter(site__in=total_sites, form_status=0).count()
        flagged = queryset.filter(site__in=total_sites, form_status=2).count()
        rejected = queryset.filter(site__in=total_sites, form_status=1).count()
        approved = queryset.filter(site__in=total_sites, form_status=3).count()

        # response = obj.get_site_submission_count()
        #
        # outstanding, flagged, approved, rejected = obj.get_site_submission_count()
        # total_submissions = response['flagged'] + response['approved'] + response['rejected'] + response['outstanding']
        # submissions = {
        #                 'total_submissions': total_submissions, 'pending': response['outstanding'], flagged:
        #                 response['flagged'], 'approved': response['approved'], 'rejected': response['rejected']
        #                }
        submissions = {
            'total_submissions': total_submissions, 'pending': outstanding,  'flagged': flagged, 'rejected': rejected,
            'approved': approved
        }

        return submissions

    def get_location(self, obj):
        if obj.location:

            data = {'coordinates': [obj.location.x, obj.location.y]}
        else:
            data = {
                     "coordinates": [
                    85.324309,
                    27.714876
                    ]
                    }

        return data

    def get_total_users(self, obj):
        region = obj.region
        if region is not None:
            peoples_involved = UserRole.objects.filter(ended_at__isnull=True).filter(Q(site_id=obj.pk) | Q(region=region)).\
                select_related('user', 'user__user_profile').distinct('user_id').count()
        else:
            peoples_involved = obj.site_roles.filter(ended_at__isnull=True).select_related('user').distinct('user_id').count()

        return peoples_involved

    def get_total_subsites(self, obj):
        if obj.enable_subsites:
            return obj.sub_sites.filter(is_active=True).count()
        return 0

    def get_users(self, obj):

        project = obj.project
        region = obj.region
        if region is not None:
            users_role = UserRole.objects.filter(ended_at__isnull=True).filter(Q(site_id=obj.pk) | Q(region=region)).\
                select_related('user', 'user__user_profile').distinct('user_id')

        else:
            users_role = UserRole.objects.filter(ended_at__isnull=True).filter(site_id=obj.pk). \
                select_related('user', 'user__user_profile').distinct('user_id')
        users_list = []
        for role in users_role:
            try:
                users_list.append({'user': role.user.id, 'username': role.user.username, 'full_name': role.user.first_name + ' ' + role.user.last_name,
                                   'email': role.user.email, 'profile_picture': role.user.user_profile.profile_picture.url})
            except ObjectDoesNotExist:
                UserProfile.objects.get_or_create(user=role.user)

        return users_list

    def get_site_progress_chart_data(self, obj):

        progress_chart = ProgressGeneratorSite(obj)
        progress_chart_data = progress_chart.data()

        data = {'labels':  progress_chart_data.values(), 'data':  progress_chart_data.keys()}

        return data

    def get_form_submissions_chart_data(self, obj):

        line_chart = FormSubmissionChartGenerator(obj)
        line_chart_data = line_chart.data()

        data = {'total_submissions':
                    {'data': [d['total_submissions'] for d in line_chart_data.values()], 'labels': line_chart_data.keys()},
                'pending_submissions':
                    {'data': [d['pending_submissions'] for d in line_chart_data.values()], 'labels': line_chart_data.keys()},
                'approved_submissions':
                    {'data': [d['approved_submissions'] for d in line_chart_data.values()], 'labels': line_chart_data.keys()},
                'rejected_submissions':
                    {'data': [d['rejected_submissions'] for d in line_chart_data.values()], 'labels': line_chart_data.keys()},
                'flagged_submissions':
                    {'data': [d['flagged_submissions'] for d in line_chart_data.values()], 'labels': line_chart_data.keys()}
                }

        return data

    def get_terms_and_labels(self, obj):
        project = obj.project
        if ProjectLevelTermsAndLabels.objects.select_related('project').filter(project=project).exists():

            return {'site': project.terms_and_labels.site,
                    'donor': project.terms_and_labels.donor,
                    'site_supervisor': project.terms_and_labels.site_supervisor,
                    'sub_site': project.terms_and_labels.sub_site,
                    'site_reviewer': project.terms_and_labels.site_reviewer,
                    'region': project.terms_and_labels.region,
                    'region_supervisor': project.terms_and_labels.region_supervisor,
                    'region_reviewer': project.terms_and_labels.region_reviewer,
                    }

        else:
            return {'site': 'Site',
                    'donor': 'Donor',
                    'site_supervisor': 'Site Supervisor',
                    'sub_site': 'Subsite',
                    'site_reviewer': 'Site Reviewer',
                    'region': 'Region',
                    'region_supervisor': 'Region Supervisor',
                    'region_reviewer': 'Region Reviewer',
                    }

    def get_has_write_permission(self, obj):

        request = self.context['request']
        if has_write_permission_in_site(request, obj.id):
            return True
        else:
            return False

    def get_project_id(self, obj):
        return obj.project.id

    def get_breadcrumbs(self, obj):
        name = obj.name
        project = obj.project
        project_url = obj.get_absolute_url()
        organization = obj.project.organization
        organization_url = obj.get_absolute_url()
        request = self.context['request']
        if request.roles.filter(Q(group__name__in=["Project Manager", "Project Donor"], project=project) | Q(group__name="Organization Admin",
                                                                                      organization=organization)) or request.is_super_admin:
            project_url = project.get_absolute_url()
        if request.roles.filter(group__name="Organization Admin", organization=organization) or request.is_super_admin:
            organization_url = organization.get_absolute_url()

        if obj.site:
            return {
                'root_site': obj.site.name,
                'root_site_url': obj.site.get_absolute_url(),
                'site': name,
                'project': project.name,
                'project_url': project_url,
                'organization': organization.name,
                'organization_url': organization_url
            }

        return {
            'site': name,
            'project': project.name,
            'project_url': project_url,
            'organization': organization.name,
            'organization_url': organization_url
        }


class FInstanceSerializer(serializers.ModelSerializer):
    form = serializers.SerializerMethodField()
    status = serializers.CharField(source='get_form_status_display')
    submitted_by = serializers.CharField(source='submitted_by.username')
    reviewed_by = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()
    instance_id = serializers.IntegerField(source="instance.id")

    class Meta:
        model = FInstance
        fields = ('id', 'instance_id', 'date', 'form', 'status', 'submitted_by', 'reviewed_by')

    def get_form(self, obj):
        if obj.site_fxf:
            return obj.site_fxf.xf.title

        elif obj.project_fxf:
            return obj.project_fxf.xf.title

    def get_reviewed_by(self, obj):
        if FieldSightLog.objects.filter(type=17, object_id=obj.id).select_related('source').exists():
            log = FieldSightLog.objects.filter(type=17, object_id=obj.id).select_related('source').order_by('-pk')[0]
            return log.source.get_full_name()

        else:
            return None

    def get_date(self, obj):
        if FieldSightLog.objects.filter(type=17, object_id=obj.id).select_related('source').exists():
            log = FieldSightLog.objects.filter(type=17, object_id=obj.id).select_related('source').order_by('-pk')[0]
            return log.date

        else:
            return obj.date


class StageFormSerializer(serializers.ModelSerializer):
    sub_stages = serializers.SerializerMethodField()

    class Meta:
        model = Stage

        fields = ('name', 'sub_stages')

    def get_sub_stages(self, obj):
        data = [{'sub_stage_name': form.name,'form_name': form.stage_forms.xf.title, 'new_submission_url': settings.SITE_URL + '/forms/new/' +
                                                                               str(self.context['site_id']) + '/'+str(form.stage_forms.id)}
                for form in obj.active_substages().prefetch_related('stage_forms', 'stage_forms__xf')]
        return data


class SiteCropImageSerializer(serializers.ModelSerializer):
    logo = Base64ImageField(
        max_length=None, use_url=True, allow_empty_file=True, allow_null=True, required=False
    )

    class Meta:
        model = Site
        fields = ('id', 'logo',)
