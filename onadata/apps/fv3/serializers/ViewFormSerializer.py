from django.core.urlresolvers import reverse_lazy
from django.db.models import Q, Count

from rest_framework import serializers

from onadata.apps.fsforms.models import FieldSightXF, Schedule, Stage, FInstance


class ViewGeneralsAndSurveyFormSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    title = serializers.SerializerMethodField(read_only=True)
    created_date = serializers.SerializerMethodField(read_only=True)
    last_response = serializers.SerializerMethodField(read_only=True)
    response_count = serializers.SerializerMethodField(read_only=True)
    view_submission_url = serializers.SerializerMethodField(read_only=True)
    download_url = serializers.SerializerMethodField(read_only=True)
    versions_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = FieldSightXF
        fields = ('id', 'name', 'title', 'created_date', 'response_count', 'last_response', 'view_submission_url',
                  'download_url', 'versions_url')

    def get_name(self, obj):
        return u"%s" % obj.xf.title

    def get_title(self, obj):
        return u"%s" % obj.xf.id_string

    def get_created_date(self, obj):
        return obj.date_created

    def get_last_response(self, obj):
        is_project = self.context.get('is_project', False)
        if is_project or obj.project:
            return obj.project_form_instances.order_by('-pk').values_list(
                    'date', flat=True)[:1]

        elif obj.site:
            return obj.site_form_instances.order_by('-pk').values_list(
                    'date', flat=True)[:1]

    def get_response_count(self, obj):
        is_project = self.context.get('is_project', False)
        if is_project or obj.project:
            count = obj.response_count if hasattr(obj, 'response_count') else 0
            return count
        elif obj.site:
            count = obj.site_response_count if hasattr(obj, 'site_response_count') else 0
            return count

    def get_view_submission_url(self, obj):
        is_project = self.context.get('is_project', False)
        if is_project:
            return '/forms/project-submissions/{}'.format(obj.id)
        else:
            return '/forms/site-submissions/{}/{}'.format(obj.id, obj.site.id)

    def get_download_url(self, obj):
        if self.get_response_count(obj) > 0:
            is_project = self.context.get('is_project', False)
            if is_project:
                return '/{}/exports/{}/xls/1/{}/0/0/'.format(obj.xf.user.username, obj.xf.id_string, obj.id)
            else:
                return ''

    def get_versions_url(self, obj):
        if obj.has_versions:
            return '/forms/submissions/versions/1/{}'.format(obj.id)


class ViewScheduledFormSerializer(serializers.ModelSerializer):
    form_name = serializers.SerializerMethodField(read_only=True)
    name = serializers.SerializerMethodField(read_only=True)
    title = serializers.SerializerMethodField(read_only=True)
    created_date = serializers.SerializerMethodField(read_only=True)
    last_response = serializers.SerializerMethodField(read_only=True)
    response_count = serializers.SerializerMethodField(read_only=True)
    view_submission_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Schedule
        fields = ('id', 'name', 'form_name', 'title', 'created_date', 'response_count', 'last_response',
                  'view_submission_url')

    def get_name(self, obj):
        return u"%s" % obj.name

    def get_form_name(self, obj):
        return u"%s" % obj.schedule_forms.xf.title

    def get_title(self, obj):
        return u"%s" % obj.schedule_forms.xf.id_string

    def get_created_date(self, obj):
        return obj.schedule_forms.date_created

    def get_last_response(self, obj):
        is_project = self.context.get('is_project', False)
        if is_project or obj.project:
            return obj.schedule_forms.project_form_instances.order_by('-pk').values_list(
                    'date', flat=True)[:1]

        elif obj.site:
            return obj.schedule_forms.site_form_instances.order_by('-pk').values_list(
                    'date', flat=True)[:1]

    def get_response_count(self, obj):
        is_project = self.context.get('is_project', False)
        if is_project or obj.project:
            count = obj.response_count if hasattr(obj, 'response_count') else 0
            return count
        elif obj.site:
            count = obj.site_response_count if hasattr(obj, 'site_response_count') else 0
            return count

    def get_view_submission_url(self, obj):
        is_project = self.context.get('is_project', False)
        if is_project:
            return '/forms/project-submissions/{}'.format(obj.schedule_forms.id)
        else:
            return '/forms/site-submissions/{}/{}'.format(obj.schedule_forms.id, obj.site.id)

    def get_download_url(self, obj):
        if self.get_response_count(obj) > 0:
            return '/{}/exports/{}/xls/1/{}/0/0/'.format(obj.schedule_forms.xf.user.username, obj.schedule_forms.xf.id_string,
                                                         obj.schedule_forms.id)

    def get_versions_url(self, obj):
        if obj.has_versions:
            return '/forms/submissions/versions/1/{}'.format(obj.schedule_forms.id)


class ViewSubStageFormSerializer(serializers.ModelSerializer):
    form_name = serializers.SerializerMethodField()
    response_count = serializers.SerializerMethodField()
    last_response = serializers.SerializerMethodField()

    class Meta:
        model = Stage
        fields = ('id', 'name', 'order', 'form_name', 'response_count', 'last_response')

    def get_form_name(self, obj):
        return obj.stage_forms.xf.title

    def get_response_count(self, obj):
        is_project = self.context.get('is_project', False)
        if is_project or obj.project:
            count = obj.response_count if hasattr(obj, 'response_count') else 0
            return count
        elif obj.site:
            count = obj.site_response_count if hasattr(obj, 'site_response_count') else 0
            return count

    def get_last_response(self, obj):
        is_project = self.context.get('is_project', False)
        if is_project or obj.project:
            return obj.stage_forms.project_form_instances.order_by('-pk').values_list(
                    'date', flat=True)[:1]

        elif obj.site:
            return obj.stage_forms.site_form_instances.order_by('-pk').values_list(
                    'date', flat=True)[:1]


class ViewStageFormSerializer(serializers.ModelSerializer):
    sub_stages = serializers.SerializerMethodField()

    class Meta:
        model = Stage
        fields = ('id', 'name', 'sub_stages')

    def get_sub_stages(self, obj):
        if obj.site:
            is_project = False
            queryset = Stage.objects.filter(stage__isnull=False, stage=obj)
            site = obj.site
            if site.type and site.region:
                queryset = queryset.filter(Q(tags__contains=[site.type_id])
                                           | Q(regions__contains=[site.region_id])
                                           )
            elif site.type:
                queryset = queryset.filter(tags__contains=[site.type_id])
            elif site.region:
                queryset = queryset.filter(regions__contains=[site.region_id])

            queryset = queryset.select_related('stage_forms', 'em').order_by('order', 'date_created').\
                annotate(site_response_count=Count('stage_forms__site_form_instances'))
            data = ViewSubStageFormSerializer(queryset, many=True,  context={'is_project': is_project}).data

            return data

        elif obj.project:
            is_project = True
            queryset = Stage.objects.filter(stage__isnull=False, stage=obj, project=obj.project)
            queryset = queryset.select_related('stage_forms', 'em').order_by('order', 'date_created').\
                annotate(response_count=Count('stage_forms__project_form_instances'))
            data = ViewSubStageFormSerializer(queryset, many=True, context={'is_project': is_project}).data

            return data


class ViewSubmissionStatusSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    submitted_by = serializers.CharField(source='submitted_by.username')
    submission_url = serializers.SerializerMethodField()
    profile_url = serializers.SerializerMethodField()

    class Meta:
        model = FInstance

        fields = ('id', 'name', 'date', 'submitted_by', 'submission_url', 'profile_url')

    def get_name(self, obj):
        if obj.project_fxf:
            name = obj.project_fxf.xf.title
            return name
        elif obj.site_fxf:
            name = obj.site_fxf.xf.title
            return name

    def get_submission_url(self, obj):
        return '/fieldsight/application/?submission={}#/submission-details'.format(obj.id)

    def get_profile_url(self, obj):
        return '/users/profile/{}/'.format(obj.submitted_by.id)


class FormSubmissionSerializer(serializers.ModelSerializer):
    submitted_by = serializers.CharField(source='submitted_by.username')
    profile_url = serializers.SerializerMethodField()

    class Meta:
        model = FInstance
        fields = ('id', 'name', 'date', 'submitted_by', 'profile_url')

    def get_profile_url(self, obj):
        return '/users/profile/{}/'.format(obj.submitted_by.id)


