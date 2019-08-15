import datetime
import json

from collections import OrderedDict
from django.db.models import Q
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.serializers import serialize

from rest_framework import serializers

from onadata.apps.fieldsight.bar_data_project import ProgressBarGenerator
from onadata.apps.fieldsight.models import Project, ProjectLevelTermsAndLabels, Site
from onadata.apps.logger.models import Instance
from onadata.apps.eventlog.models import FieldSightLog
from onadata.apps.eventlog.serializers.LogSerializer import NotificationSerializer
from onadata.apps.fsforms.line_data_project import date_range


class LineChartGeneratorProject(object):

    def __init__(self, project):
        self.project = project
        self.date_list = list(date_range(project.date_created.strftime("%Y%m%d"), datetime.datetime.today().strftime("%Y%m%d"), 6))

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

    class Meta:
        model = Project
        fields = ('id', 'name', 'address', 'public_desc', 'logo', 'contacts', 'project_activity', 'total_sites',
                  'total_users', 'project_managers', 'has_region', 'logs', 'form_submissions_chart_data',
                  'site_progress_chart_data', 'map', 'terms_and_labels', 'breadcrumbs')

    def get_contacts(self, obj):
        contacts = {
            'phone': obj.phone,
            'fax': obj.fax,
            'email': obj.email,
            'website': obj.website,

        }

        return contacts

    def get_project_activity(self, obj):
        one_week_ago = datetime.datetime.today() - datetime.timedelta(days=7)

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

        submissions_in_last_7_days = Instance.objects.filter(fieldsight_instance__project=obj, date_created=one_week_ago)
        active_supervisors_in_last_7_days = submissions_in_last_7_days.distinct('user').count()
        outstanding, flagged, approved, rejected = obj.get_submissions_count()

        return {
            'site_visits_in_last_7_days': site_visits_in_last_7_days,
            'submissions_in_last_7_days': submissions_in_last_7_days.count(),
            'active_supervisors_in_last_7_days': active_supervisors_in_last_7_days,
            'total_submissions': outstanding + flagged + approved + rejected,
            'pending_submissions': outstanding,
            'approved_submissions': approved,
            'rejected_submissions': rejected,
            'flagged_submissions': flagged

        }

    def get_total_users(self, obj):

        total_users = obj.project_roles.filter(ended_at__isnull=True).distinct('user').count()
        return total_users

    def get_total_sites(self, obj):
        total_sites = obj.sites.filter(is_active=True, is_survey=False,
                                       site__isnull=True,
                                       ).count()
        return total_sites

    def get_project_managers(self, obj):
        project_managers_qs = obj.project_roles.filter(ended_at__isnull=True, group__name="Project Manager").\
            select_related("user", "user__user_profile")
        project_managers = [{'id': role.user.id, 'full_name': role.user.get_full_name(), 'email': role.user.email,
                             'profile_picture': role.user.user_profile.profile_picture.url} for role in
                            project_managers_qs]

        return project_managers

    def get_logs(self, obj):
        qs = FieldSightLog.objects.filter(Q(project=obj) | (
                Q(content_type=ContentType.objects.get(app_label="fieldsight", model="project")) & Q(
            object_id=obj.id)))[:20]
        serializers_qs = NotificationSerializer(qs, many=True)
        return serializers_qs.data

    def get_has_region(self, obj):
        has_region = False
        if obj.project_region.all():
            has_region = True
        return has_region

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

        if ProjectLevelTermsAndLabels.objects.select_related('project').filter(project=obj).exists():

                return {'site': obj.terms_and_labels.site,
                        'donor': obj.terms_and_labels.donor,
                        'site_supervisor': obj.terms_and_labels.site_supervisor,
                        'site_reviewer': obj.terms_and_labels.site_reviewer,
                        'region': obj.terms_and_labels.region,
                        'region_supervisor': obj.terms_and_labels.region_supervisor,
                        'region_reviewer': obj.terms_and_labels.region_reviewer,
                        }
        else:
                return {'site': 'Site',
                        'donor': 'Donor',
                        'site_supervisor': 'Site Supervisor',
                        'site_reviewer': 'Site Reviewer',
                        'region': 'Region',
                        'region_supervisor': 'Region Supervisor',
                        'region_reviewer': 'Region Reviewer',
                        }

    def get_map(self, obj):
        sites = Site.objects.filter(project=obj)[:100]
        data = serialize('custom_geojson', sites, geometry_field='location', fields=('location', 'id', 'name'))
        return json.loads(data)

    def get_breadcrumbs(self, obj):
        project = obj.name
        organization = obj.organization
        organization_url = obj.get_absolute_url()
        request = self.context['request']
        if request.roles.filter(group__name="Organization Admin", organization=organization) or request.is_super_admin:
            organization_url = organization.get_absolute_url()

        return {'name': project, 'organization': organization.name, 'organization_url': organization_url}