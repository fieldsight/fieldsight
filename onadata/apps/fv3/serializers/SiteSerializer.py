from django.db.models import Q

from rest_framework import serializers

from onadata.apps.eventlog.models import FieldSightLog
from onadata.apps.fieldsight.models import Site
from onadata.apps.userrole.models import UserRole
from onadata.apps.users.models import UserProfile
from django.core.exceptions import ObjectDoesNotExist
from onadata.apps.fsforms.line_data_project import ProgressGeneratorSite, LineChartGeneratorSite
from onadata.apps.fsforms.models import FInstance


class SiteSerializer(serializers.ModelSerializer):

    region = serializers.CharField(source='region.name')
    submissions = serializers.SerializerMethodField()
    total_users = serializers.SerializerMethodField()
    users = serializers.SerializerMethodField()
    # progress_chart_data = serializers.SerializerMethodField()
    line_chart_data = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()

    class Meta:
        model = Site
        fields = ('id', 'name', 'address', 'logo', 'public_desc', 'location', 'region', 'enable_subsites', 'site',
                  'total_users', 'users', 'submissions', 'line_chart_data')

    def get_submissions(self, obj):
        response = obj.get_site_submission_count()

        outstanding, flagged, approved, rejected = obj.get_site_submission_count()
        total_submissions = response['flagged'] + response['approved'] + response['rejected'] + response['outstanding']
        submissions = {
                        'total_submissions': total_submissions, 'pending': response['outstanding'], flagged:
                        response['flagged'], 'approved': response['approved'], 'rejected': response['rejected']
                       }

        return submissions

    def get_location(self, obj):

        data = {'coordinates': [obj.location.x, obj.location.y]}

        return data

    def get_total_users(self, obj):

        peoples_involved = UserRole.objects.filter(ended_at__isnull=True).filter(
            Q(site=obj) | Q(region__project=obj.project)).select_related('user').distinct('user_id').count()
        return peoples_involved

    def get_users(self, obj):

        project = Site.objects.get(pk=obj.pk).project

        users_role = UserRole.objects.filter(ended_at__isnull=True).filter(Q(site_id=obj.pk) | Q(region__project=project)).\
            select_related('user', 'user__user_profile').distinct('user_id')
        users_list = []
        for role in users_role:
            try:
                users_list.append({'user': role.user.id, 'username': role.user.username, 'email': role.user.email,
                               'profile_picture': role.user.user_profile.profile_picture.url})
            except ObjectDoesNotExist:
                UserProfile.objects.get_or_create(user=role.user)

        return users_list

    def get_progress_chart_data(self, obj):

        progress_chart = ProgressGeneratorSite(obj)
        progress_chart_data = progress_chart.data()

        data = {'progress_data':  progress_chart_data.keys(), 'progress_labels':  progress_chart_data.values()}

        return data

    def get_line_chart_data(self, obj):

        line_chart = LineChartGeneratorSite(obj)
        line_chart_data = line_chart.data()

        data = {'line_data': line_chart_data.values(), 'line_labels': line_chart_data.keys()}

        return data


class FInstanceSerializer(serializers.ModelSerializer):
    form = serializers.SerializerMethodField()
    status = serializers.CharField(source='get_form_status_display')
    submitted_by = serializers.CharField(source='submitted_by.username')
    reviewed_by = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()

    class Meta:
        model = FInstance
        fields = ('id', 'date', 'form', 'status', 'submitted_by', 'reviewed_by')

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
