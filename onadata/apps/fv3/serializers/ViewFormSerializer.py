from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, Count

from rest_framework import serializers

from onadata.apps.fieldsight.models import Site
from onadata.apps.fsforms.models import FieldSightXF, Schedule, Stage, FInstance, XformHistory
from django.contrib.humanize.templatetags.humanize import naturaltime

from onadata.apps.fsforms.templatetags.fs_filters import get_xform_version
from onadata.apps.logger.models import XForm


class ViewGeneralsAndSurveyFormSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    title = serializers.SerializerMethodField(read_only=True)
    created_date = serializers.SerializerMethodField(read_only=True)
    last_response = serializers.SerializerMethodField(read_only=True)
    response_count = serializers.SerializerMethodField(read_only=True)
    download_url = serializers.SerializerMethodField(read_only=True)
    versions_url = serializers.SerializerMethodField(read_only=True)
    from_organization = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = FieldSightXF
        fields = ('id', 'name', 'title', 'created_date', 'response_count', 'last_response', 'download_url',
                  'versions_url', 'from_organization')

    def get_name(self, obj):
        return u"%s" % obj.xf.title

    def get_from_organization(self, obj):
        if obj.organization_form_lib:
            return True
        else:
            return False

    def get_title(self, obj):
        return u"%s" % obj.xf.id_string

    def get_created_date(self, obj):
        return obj.date_created.strftime("%b %d, %Y at %I:%M %p")

    def get_last_response(self, obj):
        is_project = self.context.get('is_project', False)

        if is_project or obj.project:
            return obj.project_form_instances.order_by('-pk').values_list(
                    'date', flat=True)[:1]

        elif obj.site:
            return obj.site_form_instances.order_by('-pk').values_list(
                    'date', flat=True)[:1]
        return []

    def get_response_count(self, obj):
        is_project = self.context.get('is_project', False)
        site = self.context.get('site', None)

        if is_project:
            count = obj.project_form_instances.count()
            return count

        elif obj.site:
            count = obj.site_form_instances.count()

            return count

        elif obj.project and site:
            count = obj.project_form_instances.filter(site__id=site).count()
            return count

    def get_download_url(self, obj):
        if self.get_response_count(obj) > 0:
            is_project = self.context.get('is_project', False)
            site = self.context.get('site', None)

            if is_project:
                return '/{}/exports/{}/xls/1/{}/0/0/'.format(obj.xf.user.username, obj.xf.id_string, obj.id)
            elif site is not None:
                return '/{}/exports/{}/xls/0/{}/{}/0/'.format(obj.xf.user.username, obj.xf.id_string, obj.id, site)

            else:
                return ''

    def get_versions_url(self, obj):
        is_project = self.context.get('is_project', False)
        site = self.context.get('site', None)
        if obj.has_versions:
            if is_project:
                return '/forms/submissions/versions/1/{}'.format(obj.id)
            elif site:
                return '/forms/submissions/versions/0/{}/{}'.format(obj.id, site)


class ViewScheduledFormSerializer(serializers.ModelSerializer):
    form_name = serializers.SerializerMethodField(read_only=True)
    name = serializers.SerializerMethodField(read_only=True)
    title = serializers.SerializerMethodField(read_only=True)
    created_date = serializers.SerializerMethodField(read_only=True)
    last_response = serializers.SerializerMethodField(read_only=True)
    response_count = serializers.SerializerMethodField(read_only=True)
    download_url = serializers.SerializerMethodField(read_only=True)
    versions_url = serializers.SerializerMethodField(read_only=True)
    fsxf_id = serializers.IntegerField(source='schedule_forms.id')
    from_organization = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Schedule
        fields = ('id', 'name', 'fsxf_id', 'form_name', 'title', 'created_date', 'response_count', 'last_response',
                  'download_url', 'versions_url', 'from_organization')

    def get_name(self, obj):
        return u"%s" % obj.name

    def get_from_organization(self, obj):
        if obj.schedule_forms.organization_form_lib:
            return True
        else:
            return False

    def get_form_name(self, obj):
        return u"%s" % obj.schedule_forms.xf.title

    def get_title(self, obj):
        return u"%s" % obj.schedule_forms.xf.id_string

    def get_created_date(self, obj):
        return obj.schedule_forms.date_created.strftime("%b %d, %Y at %I:%M %p")

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
        site = self.context.get('site', None)

        if is_project:
            count = obj.schedule_forms.project_form_instances.count()
            return count

        elif obj.site:
            count = obj.schedule_forms.site_form_instances.count()
            return count

        elif obj.project and site:
            count = obj.schedule_forms.project_form_instances.filter(site__id=site).count()
            return count

    def get_download_url(self, obj):

        if self.get_response_count(obj) > 0:
            is_project = self.context.get('is_project', False)
            site = self.context.get('site', None)

            if is_project:
                return '/{}/exports/{}/xls/1/{}/0/0/'.format(obj.schedule_forms.xf.user.username,
                                                             obj.schedule_forms.xf.id_string,  obj.schedule_forms.id)
            elif site is not None:
                return '/{}/exports/{}/xls/0/{}/{}/0/'.format(obj.schedule_forms.xf.user.username,
                                                              obj.schedule_forms.xf.id_string, obj.schedule_forms.id,
                                                              site)
            else:
                return ''

    def get_versions_url(self, obj):
        is_project = self.context.get('is_project', False)
        site = self.context.get('site', False)

        if obj.schedule_forms.has_versions:
            if is_project:
                return '/forms/submissions/versions/1/{}'.format(obj.schedule_forms.id)
            elif site:
                return '/forms/submissions/versions/0/{}/{}'.format(obj.schedule_forms.id, site)


class ViewSubStageFormSerializer(serializers.ModelSerializer):
    form_name = serializers.SerializerMethodField()
    response_count = serializers.SerializerMethodField()
    last_response = serializers.SerializerMethodField()
    download_url = serializers.SerializerMethodField(read_only=True)
    versions_url = serializers.SerializerMethodField(read_only=True)
    fsxf_id = serializers.IntegerField(source='stage_forms.id')

    class Meta:
        model = Stage
        fields = ('id', 'name', 'order', 'form_name', 'response_count', 'last_response', 'download_url', 'versions_url',
                  'fsxf_id')

    def get_form_name(self, obj):
        return obj.stage_forms.xf.title

    def get_response_count(self, obj):

        try:
            fsxf = FieldSightXF.objects.get(stage=obj)

            is_project = self.context.get('is_project', False)

            if is_project:

                count = fsxf.project_form_instances.count()
                return count

            else:
                site_id = self.context.get('site', False)
                if fsxf.project:
                    return fsxf.project_form_instances.filter(site=site_id).count()
                else:
                    return fsxf.site_form_instances.count()
        except ObjectDoesNotExist:
            return 0

    def get_last_response(self, obj):
        is_project = self.context.get('is_project', False)
        if is_project or obj.project:
            return obj.stage_forms.project_form_instances.order_by('-pk').values_list(
                    'date', flat=True)[:1]

        elif obj.site:

            return obj.stage_forms.site_form_instances.order_by('-pk').values_list(
                    'date', flat=True)[:1]

    def get_download_url(self, obj):
       
        if self.get_response_count(obj) > 0:
            is_project = self.context.get('is_project', False)
            site = self.context.get('site', None)

            if is_project:
                return '/{}/exports/{}/xls/1/{}/0/0/'.format(obj.stage_forms.xf.user.username,
                                                             obj.stage_forms.xf.id_string,  obj.stage_forms.id)
            elif site is not None:
                return '/{}/exports/{}/xls/0/{}/{}/0/'.format(obj.stage_forms.xf.user.username,
                                                              obj.stage_forms.xf.id_string, obj.stage_forms.id,
                                                              site)
            else:
                return ''

    def get_versions_url(self, obj):
        is_project = self.context.get('is_project', False)
        site = self.context.get('site', False)

        if obj.stage_forms.has_versions:
            if is_project:
                return '/forms/submissions/versions/1/{}'.format(obj.stage_forms.id)
            elif site:
                return '/forms/submissions/versions/0/{}/{}'.format(obj.stage_forms.id, site)


class ViewStageFormSerializer(serializers.ModelSerializer):
    sub_stages = serializers.SerializerMethodField()

    class Meta:
        model = Stage
        fields = ('id', 'name', 'sub_stages')

    def get_sub_stages(self, obj):
        site_id = self.context.get('site', False)
        is_project = self.context.get('is_project', False)
        queryset = Stage.objects.filter(stage__isnull=False).exclude(stage_forms__isnull=True)

        stage_id = obj.id
        queryset = queryset.filter(stage__id=stage_id)
        stage = Stage.objects.get(pk=stage_id)
        project = stage.project
        site_id = site_id

        if project and site_id:
            site = Site.objects.get(pk=site_id)
            types_count = project.types.count()
            if project.cluster_sites and types_count:
                if not site.type:
                    site.type_id = 0
                if not site.region:
                    site.region_id = 0
                queryset = queryset.filter(tags__contains=[site.type_id], regions__contains=[site.region_id])
            elif types_count:
                if not site.type:
                    site.type_id = 0
                queryset = queryset.filter(tags__contains=[site.type_id])
            elif project.cluster_sites:
                if not site.region:
                    site.region_id = 0
                queryset = queryset.filter(regions__contains=[site.region_id])

            queryset = queryset.order_by('order', 'date_created').select_related('stage_forms', 'stage_forms__xf',
                                                                                 'stage_forms__xf__user', 'site',
                                                                                 'project'). \
                prefetch_related('stage_forms__site_form_instances', 'stage_forms__xf__fshistory')

            data = ViewSubStageFormSerializer(queryset, many=True, context={'site': site_id}).data

            return data

        elif is_project:
            queryset = queryset.order_by('order', 'date_created').select_related('stage_forms', 'stage_forms__xf',
                                                                                 'stage_forms__xf__user', 'site',
                                                                                 'project'). \
                prefetch_related('stage_forms__site_form_instances', 'stage_forms__xf__fshistory')

            data = ViewSubStageFormSerializer(queryset, many=True, context={'is_project': is_project}).data
            return data
        else:
            queryset = queryset.order_by('order', 'date_created').select_related('stage_forms', 'stage_forms__xf',
                                                                                 'stage_forms__xf__user', 'site',
                                                                                 'project'). \
                prefetch_related('stage_forms__site_form_instances', 'stage_forms__xf__fshistory')

            data = ViewSubStageFormSerializer(queryset, many=True, context={'site': site_id}).data
            return data

            # if obj.project or is_project:
        #     is_project = True
        #     queryset = Stage.objects.filter(stage__isnull=False, stage=obj, project=obj.project)
        #     queryset = queryset.order_by('order', 'date_created').select_related('stage_forms', 'stage_forms__xf',
        #                                                                'stage_forms__xf__user').\
        #             prefetch_related('stage_forms__project_form_instances', 'stage_forms__xf__fshistory')
        #     data = ViewSubStageFormSerializer(queryset, many=True, context={'is_project': is_project}).data
        #
        #     return data
        #
        # elif site_id:
        #     queryset = Stage.objects.filter(stage__isnull=False, stage=obj)
        #     site = Site.objects.select_related('region', 'type').get(id=site_id)
        #     project_id = site.project_id
        #     if site.type and site.region:
        #         queryset = queryset.filter(Q(site__id=site.id, project_stage_id=0)
        #                                     | Q(project__id=project_id, tags__contains=[site.type_id])
        #                                     | Q(project__id=project_id, regions__contains=[site.region_id])
        #                                     )
        #     elif site.type:
        #         queryset.filter(Q(site__id=site.id,
        #                           project_stage_id=0)
        #                         | Q(project__id=project_id, tags__contains=[site.type_id])
        #
        #                         )
        #     elif site.region:
        #         queryset = queryset.filter(Q(site__id=site.id,
        #                                      project_stage_id=0)
        #                                    | Q(project__id=project_id, regions__contains=[site.region_id])
        #                                    )
        #     else:
        #         queryset = queryset.filter(
        #             Q(site__id=site.id, project_stage_id=0)
        #             | Q(project__id=project_id))


class ViewSubmissionStatusSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    submitted_by = serializers.CharField(source='submitted_by.username')
    submission_url = serializers.SerializerMethodField()
    profile_url = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()

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
        return '/fieldsight/application/?submission={}#/submission-details'.format(obj.instance.id)

    def get_profile_url(self, obj):
        return '/users/profile/{}/'.format(obj.submitted_by.id)

    def get_date(self, obj):
        return naturaltime(obj.date)


class FormSubmissionSerializer(serializers.ModelSerializer):
    submitted_by = serializers.CharField(source='submitted_by.get_full_name')
    profile_url = serializers.SerializerMethodField()
    site_name = serializers.CharField(source='site.name')
    site_identifier = serializers.CharField(source='site.identifier')
    submission_id = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()

    class Meta:
        model = FInstance
        fields = ('id', 'submission_id', 'date', 'submitted_by', 'profile_url', 'site_name', 'site_identifier')

    def get_profile_url(self, obj):
        return '/users/profile/{}/'.format(obj.submitted_by.id)

    def get_submission_id(self, obj):
        return obj.instance.id

    def to_representation(self, obj):
        data = super(FormSubmissionSerializer, self).to_representation(obj)
        is_project = self.context.get('is_project', False)
        is_organization = self.context.get('is_organization', False)

        if not(is_project or is_organization):
            data.pop('site_identifier')
            data.pop('site_name')
        return data

    def get_date(self, obj):
        return obj.instance.date_created.strftime("%b %d, %Y at %I:%M %p")


def get_version_submission_data(fsf, is_project, site, xform_or_history):
    date = ""
    count = 0
    if isinstance(xform_or_history,  XForm):
        form_version = get_xform_version(xform_or_history)
    else:
        form_version = xform_or_history.version
    if is_project == 1:
        latest = FInstance.objects.filter(project_fxf=fsf, version=form_version).last()
        if latest:
            date = latest.date
        count = FInstance.objects.filter(project_fxf=fsf, version=form_version).count()
    elif is_project == 0:
        if fsf.project:
            latest = FInstance.objects.filter(project_fxf=fsf, version=form_version, site=site).last()
            if latest:
                date = latest.date
            count = FInstance.objects.filter(project_fxf=fsf, version=form_version, site=site).count()

        elif fsf.site:
            latest = FInstance.objects.filter(site_fxf=fsf, version=form_version, site=site).last()
            if latest:
                date = latest.date
            count = FInstance.objects.filter(site_fxf=fsf, version=form_version, site=site).count()

    has_submissions = True if count > 0 else False
    return dict(date=date, count=count, has_submissions=has_submissions, version=form_version)


class SubmissionsVersionSerializer(serializers.ModelSerializer):
    last_response = serializers.SerializerMethodField()
    total_submissions = serializers.SerializerMethodField()
    overidden_date = serializers.SerializerMethodField()
    download_url = serializers.SerializerMethodField()
    version_id = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = XformHistory
        fields = ('id', 'title', 'version', 'overidden_date', 'total_submissions', 'last_response', 'download_url',
                  'version_id')

    def get_overidden_date(self, obj):
        return obj.date.strftime("%b %d, %Y at %I:%M %p")

    def get_total_submissions(self, obj):
        is_project = self.context.get('is_project', False)
        fsf = self.context.get('fsf', False)
        site = self.context.get('site', False)

        if is_project == 1:
            data = get_version_submission_data(fsf, 1, None, obj)
            count = data['count']

        elif is_project == 0:
            data = get_version_submission_data(fsf, 0, site, obj)
            count = data['count']

        else:
            count = 0

        return count

    def get_last_response(self, obj):
        is_project = self.context.get('is_project', False)
        fsf = self.context.get('fsf', False)
        site = self.context.get('site', False)

        if is_project == 1:
            data = get_version_submission_data(fsf, 1, None, obj)
            date = data['date']

        elif is_project == 0:
            data = get_version_submission_data(fsf, 0, site, obj)
            date = data['date']

        else:
            date = ''

        return date

    def get_download_url(self, obj):
            is_project = self.context.get('is_project', False)
            fsf = self.context.get('fsf', None)
            site = self.context.get('site', None)

            form_version = obj.version

            if is_project:
                url = '/{}/exports/{}/xls/1/{}/0/{}/'.format(fsf.xf.user.username, fsf.xf.id_string, fsf.id, form_version)

            else:
                url = '/{}/exports/{}/xls/0/{}/{}/{}/'.format(fsf.xf.user.username, fsf.xf.id_string, fsf.id, site,
                                                              form_version)

            return url

    def get_version_id(self, obj):
        form_version = obj.version

        return form_version


