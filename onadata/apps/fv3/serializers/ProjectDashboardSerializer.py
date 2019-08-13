import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, F
from django.conf import settings

from rest_framework import serializers


from onadata.apps.fieldsight.models import Project, ProjectLevelTermsAndLabels
from onadata.apps.main.models import UserProfile
from onadata.apps.userrole.models import UserRole
from onadata.apps.logger.models import Instance


class ProjectDashboardSerializer(serializers.ModelSerializer):
    contacts = serializers.SerializerMethodField()
    project_activity = serializers.SerializerMethodField()
    total_sites = serializers.SerializerMethodField()
    total_users = serializers.SerializerMethodField()
    project_managers = serializers.SerializerMethodField()
    terms_and_labels = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ('id', 'name', 'address', 'public_desc', 'logo', 'contacts', 'project_activity', 'total_sites',
                  'total_users', 'project_managers', 'terms_and_labels')

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

    def get_breadcrumbs(self, obj):
        name = obj.name
        project = obj.project
        project_url = '#'
        organization = obj.project.organization
        organization_url = ''
        request = self.context['request']
        if request.roles.filter(Q(group__name="Project Manager", project=project) | Q(group__name="Organization Admin",
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
