import datetime
import json

from collections import OrderedDict

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.serializers import serialize

from rest_framework import serializers

from onadata.apps.fieldsight.bar_data_project import ProgressBarGenerator
from onadata.apps.fieldsight.models import Project, ProjectLevelTermsAndLabels, Site, Organization
from onadata.apps.fsforms.models import Stage, FieldSightXF, FInstance, Schedule, OrganizationFormLibrary
from onadata.apps.fv3.role_api_permissions import check_del_site_perm
from onadata.apps.fv3.serializer import Base64ImageField
from onadata.apps.logger.models import Instance
from onadata.apps.eventlog.models import FieldSightLog
from onadata.apps.eventlog.serializers.LogSerializer import NotificationSerializer
from onadata.apps.fsforms.line_data_project import date_range
from onadata.apps.users.models import UserProfile


class LineChartGeneratorProject(object):

    def __init__(self, project):
        self.project = project
        self.date_list = list(date_range(project.date_created.strftime("%Y%m%d"),
                                         datetime.datetime.today().strftime("%Y%m%d"), 6))

    def get_count(self, date):
        import datetime as dt
        date = date + dt.timedelta(days=1)
        obj = self.project.project_instances.filter(date__lte=date.date())
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


class ProjectDashboardSerializer(serializers.ModelSerializer):
    contacts = serializers.SerializerMethodField()
    project_activity = serializers.SerializerMethodField()
    total_sites = serializers.SerializerMethodField()
    total_users = serializers.SerializerMethodField()
    project_managers = serializers.SerializerMethodField()
    logs = serializers.SerializerMethodField()
    terms_and_labels = serializers.SerializerMethodField()
    form_submissions_chart_data = serializers.SerializerMethodField()
    has_region = serializers.SerializerMethodField()
    site_progress_chart_data = serializers.SerializerMethodField()
    breadcrumbs = serializers.SerializerMethodField()
    map = serializers.SerializerMethodField()
    is_project_manager = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ('id', 'identifier', 'name', 'address', 'public_desc', 'logo', 'contacts', 'project_activity',
                  'total_sites', 'total_users', 'project_managers', 'has_region', 'logs', 'form_submissions_chart_data',
                  'site_progress_chart_data', 'map', 'terms_and_labels', 'breadcrumbs', 'is_project_manager')

    def get_contacts(self, obj):
        contacts = {
            'phone': obj.phone,
            'fax': obj.fax,
            'email': obj.email,
            'website': obj.website,

        }

        return contacts

    def get_is_project_manager(self, obj):
        request = self.context['request']

        is_project_manager = False
        organization_id = obj.organization.id
        org = Organization.objects.get(id=organization_id)
        user_role_as_manager = request.roles.filter(project_id=obj.id, group__name="Project Manager")
        user_role_as_team_admin = request.roles.filter(organization_id=organization_id, group__name="Organization Admin")

        if user_role_as_manager or request.is_super_admin or user_role_as_team_admin:
            is_project_manager = True

        elif org.parent_id in request.roles.filter(super_organization_id=org.parent_id,
                                                   group__name="Super Organization Admin").\
                values_list('super_organization_id', flat=True):
            is_project_manager = True

        return is_project_manager

    def get_project_activity(self, obj):
        one_week_ago = datetime.datetime.today() - datetime.timedelta(days=7)
        instances = Instance.objects.filter(fieldsight_instance__project_id=obj.id, date_created__gte=one_week_ago)

        try:
            site_visits_query = settings.MONGO_DB.instances.aggregate(
                [{"$match": {"fs_project": obj.id, "start": {'$gte': one_week_ago.isoformat()}}}, {"$group": {
                    "_id": {
                        "fs_site": "$fs_site",
                        "date": {"$substr": ["$start", 0, 10]}
                    },
                }
                }, {"$group": {"_id": "$_id.fs_site", "visits": {'$sum': 1}
                               }},
                 {"$group": {"_id": None, "total_sum": {'$sum': '$visits'}}}
                 ])['result']

            if not site_visits_query:
                site_visits_in_last_7_days = 0
            else:
                site_visits_in_last_7_days = site_visits_query[0]['total_sum']
        except:
            site_visits_in_last_7_days = "Error occured."

        outstanding, flagged, approved, rejected = obj.get_submissions_count()

        return {
            'site_visits_in_last_7_days': site_visits_in_last_7_days,
            'submissions_in_last_7_days': instances.count(),
            'active_supervisors_in_last_7_days': instances.distinct('user').count(),
            'total_submissions': outstanding + flagged + approved + rejected,
            'pending_submissions': outstanding,
            'approved_submissions': approved,
            'rejected_submissions': rejected,
            'flagged_submissions': flagged

        }

    def get_total_users(self, obj):

        total_users = obj.project_roles.select_related('user').filter(ended_at__isnull=True).distinct('user').count()
        return total_users

    def get_total_sites(self, obj):
        total_sites = obj.sites.filter(is_active=True, is_survey=False,
                                       site__isnull=True,
                                       ).count()
        return total_sites

    def get_project_managers(self, obj):
        project_managers_qs = obj.project_user_roles

        project_managers = [{'id': role.user.id, 'full_name': role.user.get_full_name(), 'email': role.user.email,
                             'profile_picture': role.user.user_profile.profile_picture.url} for role in
                            project_managers_qs]

        return project_managers

    def get_logs(self, obj):
        qs = FieldSightLog.objects.select_related('source', 'source__user_profile', 'project__terms_and_labels',
                                                  'extra_content_type', 'content_type') \
                 .prefetch_related('content_object', 'extra_object', 'seen_by').filter(Q(project=obj) | (
                Q(content_type=ContentType.objects.get(app_label="fieldsight", model="project")) & Q(
            object_id=obj.id)))[:20]
        serializers_qs = NotificationSerializer(qs, many=True)
        return serializers_qs.data

    def get_has_region(self, obj):
        return obj.cluster_sites

    def get_form_submissions_chart_data(self, obj):
        line_chart = LineChartGeneratorProject(obj)
        line_chart_data = line_chart.data()
        data = {'total_submissions':
                    {'data': [d['total_submissions'] for d in line_chart_data.values()],
                     'labels': line_chart_data.keys()},
                'pending_submissions':
                    {'data': [d['pending_submissions'] for d in line_chart_data.values()],
                     'labels': line_chart_data.keys()},
                'approved_submissions':
                    {'data': [d['approved_submissions'] for d in line_chart_data.values()],
                     'labels': line_chart_data.keys()},
                'rejected_submissions':
                    {'data': [d['rejected_submissions'] for d in line_chart_data.values()],
                     'labels': line_chart_data.keys()},
                'flagged_submissions':
                    {'data': [d['flagged_submissions'] for d in line_chart_data.values()],
                     'labels': line_chart_data.keys()}
                }

        return data

    def get_site_progress_chart_data(self, obj):
        bar_graph = ProgressBarGenerator(obj)
        progress_labels = bar_graph.data.keys()
        progress_data = bar_graph.data.values()

        return {
            'labels': progress_labels,
            'data': progress_data
        }

    def get_terms_and_labels(self, obj):

        try:
            return {'site': obj.terms_and_labels.site,
                        'donor': obj.terms_and_labels.donor,
                        'site_supervisor': obj.terms_and_labels.site_supervisor,
                        'site_reviewer': obj.terms_and_labels.site_reviewer,
                        'region': obj.terms_and_labels.region,
                        'region_supervisor': obj.terms_and_labels.region_supervisor,
                        'region_reviewer': obj.terms_and_labels.region_reviewer,
                        }
        except:
            return {'site': 'Site',
                        'donor': 'Donor',
                        'site_supervisor': 'Site Supervisor',
                        'site_reviewer': 'Site Reviewer',
                        'region': 'Region',
                        'region_supervisor': 'Region Supervisor',
                        'region_reviewer': 'Region Reviewer',
                        }

    def get_map(self, obj):
        organization_location = obj.organization.location
        sites_with_no_location = Site.objects.filter(project=obj, location=None).update(location=organization_location)
        if not obj.location:
            obj.location = organization_location
            obj.save()

        sites = Site.objects.filter(project=obj).exclude(location=None)[:100]
        data = serialize('custom_geojson', sites, geometry_field='location', fields=('location', 'id', 'name'))
        return json.loads(data)

    def get_breadcrumbs(self, obj):
        project = obj.name
        organization = obj.organization
        organization_url = obj.get_absolute_url()
        request = self.context['request']
        if request.roles.filter(group__name="Organization Admin", organization=organization) or request.is_super_admin:
            organization_url = organization.get_absolute_url()

        elif organization.parent:
                if organization.parent.id in request.roles.filter(super_organization=organization.parent,
                                                         group__name="Super Organization Admin"). \
                        values_list('super_organization_id', flat=True):
                    organization_url = organization.get_absolute_url()

        return {'name': project, 'organization': organization.name, 'organization_url': organization_url}


class ProgressStageFormSerializer(serializers.ModelSerializer):
    sub_stages = serializers.SerializerMethodField()

    class Meta:
        model = Stage

        fields = ('name', 'sub_stages')

    def get_sub_stages(self, obj):
        project = obj.project
        total_sites = project.sites.filter(is_active=True, is_survey=False, enable_subsites=False).count()

        try:

            data = [{'form_name': form.stage_forms.xf.title, 'form_url':  '/fieldsight/application/#/submission-data/{}/{}'\
                .format(project.id, form.stage_forms.id),
                     'pending': form.stage_forms.project_form_instances.filter(form_status=0).count(),
                     'rejected': form.stage_forms.project_form_instances.filter(form_status=1).count(), 'flagged': form.stage_forms.project_form_instances.\
                filter(form_status=2).count(), 'approved': form.stage_forms.project_form_instances.\
                filter(form_status=3).count(), 'progress': round((float(form.stage_forms.project_form_instances.all().
                                                            distinct('site').count())/total_sites)*100)}
                    for form in obj.active_substages().prefetch_related('stage_forms', 'stage_forms__xf')

                    ]
        except ZeroDivisionError:
            data = [{'form_name': form.stage_forms.xf.title, 'form_url':  '/fieldsight/application/#/submission-data/{}/{}'
                .format(project.id, form.stage_forms.id), 'pending': form.stage_forms.project_form_instances. \
                filter(form_status=0).count(), 'rejected': form.stage_forms.project_form_instances. \
                filter(form_status=1).count(), 'flagged': form.stage_forms.project_form_instances. \
                filter(form_status=2).count(), 'approved': form.stage_forms.project_form_instances. \
                filter(form_status=3).count(), 'progress': 0}
                    for form in obj.active_substages().prefetch_related('stage_forms', 'stage_forms__xf')

                    ]
        return data


class ProgressGeneralFormSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    progress_data = serializers.SerializerMethodField()
    form_url = serializers.SerializerMethodField()
    from_organization = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = FieldSightXF

        fields = ('name', 'form_url', 'progress_data', 'from_organization')

    def get_name(self, obj):
        return obj.xf.title

    def get_from_organization(self, obj):
        if obj.organization_form_lib:
            return True
        else:
            return False

    def get_form_url(self, obj):
        return '/fieldsight/application/#/submission-data/{}/{}' .format(obj.project_id, obj.id)

    def get_progress_data(self, obj):
        total_sites = []
        [total_sites.append(i) for i in obj.project.total_sites]
        submission_in_site = obj.project_form_instances.all().distinct('site').count()

        try:
            progress = round((float(submission_in_site)/len(total_sites))*100, 2)
        except ZeroDivisionError:
            progress = 0
        data = [{'pending': len(obj.pending), 'rejected': len(obj.rejected), 'flagged': len(obj.flagged),
                 'approved': len(obj.approved), 'progress': progress}
                ]
        return data


class ProgressScheduledFormSerializer(serializers.ModelSerializer):
    progress_data = serializers.SerializerMethodField()
    form_url = serializers.SerializerMethodField()
    from_organization = serializers.SerializerMethodField(read_only=True)
    name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Schedule

        fields = ('name', 'form_url', 'progress_data', 'from_organization')

    def get_name(self, obj):
        return obj.schedule_forms.xf.title

    def get_form_url(self, obj):
        project_id =self.context.get('project_id', None)
        return '/fieldsight/application/#/submission-data/{}/{}' .format(project_id, obj.schedule_forms.id)

    def get_from_organization(self, obj):
        if obj.schedule_forms.organization_form_lib:
            return True
        else:
            return False

    def get_progress_data(self, obj):
        project = obj.project
        total_sites = project.sites.filter(is_active=True, is_survey=False).count()
        submission_in_site = obj.schedule_forms.project_form_instances.distinct('site').count()
        try:
            progress = round((float(submission_in_site)/total_sites)*100, 2)
        except ZeroDivisionError:
            progress = 0
        data = [{'pending': obj.schedule_forms.project_form_instances.filter(form_status=0).count(), 'rejected':
            obj.schedule_forms.project_form_instances.filter(form_status=1).count(), 'flagged': obj.schedule_forms.\
            project_form_instances.filter(form_status=2).count(),
                 'approved': obj.schedule_forms.project_form_instances.filter(form_status=3).count(), 'progress': progress}
                ]
        return data


class SiteFormSerializer(serializers.ModelSerializer):
    logo = Base64ImageField(
        max_length=None, use_url=True, allow_empty_file=True, allow_null=True, required=False
    )
    site_meta_attributes_answers = serializers.SerializerMethodField()
    delete_perm = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Site
        fields = ('id', 'name', 'location', 'identifier', 'site_meta_attributes_ans', 'weight', 'logo', 'type',
                  'phone', 'address', 'public_desc', 'project', 'region', 'enable_subsites', 'site',
                  'site_meta_attributes_answers', 'delete_perm')

    def get_site_meta_attributes_answers(self, obj):
        metas = obj.site_meta_attributes_ans

        return metas

    def get_delete_perm(self, obj):
        request = self.context.get('request')
        if check_del_site_perm(request, obj.id):
            return True
        else:
            return False


class SitelistForMetasLinkSerializer(serializers.ModelSerializer):
    label = serializers.ReadOnlyField(source='name', read_only=True)
    id = serializers.SerializerMethodField()

    class Meta:
        model = Site
        fields = ('id', 'label', 'identifier',)

    def get_id(self, obj):
        return obj.identifier


class SubStageFormSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    response_count = serializers.SerializerMethodField()
    form_id = serializers.SerializerMethodField()

    class Meta:
        model = Stage
        fields = ('id', 'name', 'order', 'title', 'response_count',
                  'form_id')

    def get_form_id(self, obj):
        return obj.stage_forms.xf.id

    def get_title(self, obj):
        return obj.stage_forms.xf.title

    def get_response_count(self, obj):

        try:
            fsxf = FieldSightXF.objects.get(stage=obj)
            count = fsxf.project_form_instances.count()
            return count

        except ObjectDoesNotExist:
            return 0


class StageFormSerializer(serializers.ModelSerializer):
    sub_stages = serializers.SerializerMethodField()

    class Meta:
        model = Stage
        fields = ('id', 'name', 'sub_stages')

    def get_sub_stages(self, obj):
        queryset = Stage.objects.filter(stage__isnull=False)

        stage_id = obj.id
        queryset = queryset.filter(stage__id=stage_id)

        queryset = queryset.order_by('order', 'date_created').select_related('stage_forms', 'stage_forms__xf'). \
            prefetch_related('stage_forms__site_form_instances').exclude(stage_forms__isnull=True)

        data = SubStageFormSerializer(queryset, many=True).data
        return data


class ProjectUserProfileSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField(read_only=True)
    full_name = serializers.SerializerMethodField(read_only=True)
    role = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = UserProfile
        exclude = ('notification_seen_date', 'task_last_view_date', 'organization', 'timezone', 'user')

    def get_id(self, obj):
        return obj.user_id

    def get_full_name(self, obj):
        return obj.user.get_full_name()

    def get_role(self, obj):
        project_id = self.context.get('project_id', None)
        return obj.user.user_roles.filter(project_id=project_id).values('group__name')[0]['group__name']


class OrganizationFormLibrarySerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = OrganizationFormLibrary
        fields = ('id', 'xf', 'title')

    def get_title(self, obj):
        return obj.xf.title