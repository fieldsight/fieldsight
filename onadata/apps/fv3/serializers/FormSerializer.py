from rest_framework import serializers
from rest_framework.reverse import reverse

from onadata.apps.fv3.serializers.manage_forms import FormSettingsReadOnlySerializer, \
    FormSettingsReadOnlySerializerSchedule
from onadata.libs.utils.decorators import check_obj
from onadata.apps.logger.models import XForm

from onadata.apps.fsforms.models import Asset, FieldSightXF, ObjectPermission, \
    Schedule, Stage

from onadata.apps.fieldsight.models import Project, Organization
from onadata.apps.fsforms.utils import get_version
from onadata.apps.fsforms.serializers.FieldSightXFormSerializer import \
    EMSerializer

from django.conf import settings
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from datetime import datetime


class XFormSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()
    date_created = serializers.SerializerMethodField()
    date_modified = serializers.SerializerMethodField()
    edit_url = serializers.SerializerMethodField()
    preview_url = serializers.SerializerMethodField()
    replace_url = serializers.SerializerMethodField()
    download_url = serializers.SerializerMethodField()
    media_url = serializers.SerializerMethodField()
    share_users_url = serializers.SerializerMethodField()
    share_project_url = serializers.SerializerMethodField()
    share_team_url = serializers.SerializerMethodField()
    share_global_url = serializers.SerializerMethodField()
    add_language_url = serializers.SerializerMethodField()
    clone_form_url = serializers.SerializerMethodField()
    delete_url = serializers.SerializerMethodField()
    shareable_users_url = serializers.SerializerMethodField()
    shareable_teams_url = serializers.SerializerMethodField()
    shareable_projects_url = serializers.SerializerMethodField()
    can_view = serializers.SerializerMethodField()
    can_edit = serializers.SerializerMethodField()

    class Meta:
        model = XForm
        fields = ('id','id_string', 'title', 'owner', 'edit_url', 'preview_url', 'replace_url',
                  'download_url', 'media_url', 'date_created', 'date_modified', 'share_users_url',
                  'share_project_url', 'share_team_url', 'share_global_url', 'add_language_url',
                  'clone_form_url', 'delete_url', 'shareable_users_url', 'shareable_teams_url', 'shareable_projects_url',
                  'can_view', 'can_edit')

    def get_owner(self, obj):
        return obj.user.username

    def get_date_created(self, obj):
        date_created = obj.date_created
        date_created = datetime.strftime(date_created, "%Y-%m-%d")
        return date_created

    def get_date_modified(self, obj):
        date_modified = obj.date_modified
        date_modified = datetime.strftime(date_modified, "%Y-%m-%d")
        return date_modified

    def get_edit_url(self, obj):
        return "{}#forms/{}/edit/".format(settings.KPI_URL, obj.id_string)

    def get_preview_url(self, obj):
        return "{}/forms/preview/{}/".format(settings.KOBOCAT_URL, obj.id_string)

    def get_replace_url(self, obj):
        return "{}{}/".format(settings.KPI_URL,"imports")

    def get_download_url(self, obj):
        return "{}{}.{}".format(settings.KPI_ASSET_URL, obj.id_string, "xls")

    def get_media_url(self, obj):
        return "{}/{}/forms/{}/form_settings".format(settings.KOBOCAT_URL, obj.user.username, obj.id_string)

    def get_share_users_url(self, obj):
        return "/fv3/api/share/"

    def get_share_project_url(self, obj):
        return "/fv3/api/share/project/"

    def get_share_team_url(self, obj):
        return "/fv3/api/share/team/"

    def get_share_global_url(self, obj):
        return "/fv3/api/share/global/"

    def get_add_language_url(self, obj):
        return "/fv3/api/add-language/"

    def get_clone_form_url(self, obj):
        return "/fv3/api/clone/"

    def get_delete_url(self, obj):
        return "/fv3/api/form/delete/"

    def get_shareable_users_url(self, obj):
        return "/fv3/api/form/users/"

    def get_shareable_teams_url(self, obj):
        return "/fv3/api/form/teams/"

    def get_shareable_projects_url(self, obj):
        return "/fv3/api/form/projects/"

    def get_can_view(self, obj):
        return True
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        permission = Permission.objects.get(content_type__app_label='kpi', codename='view_asset')
        object_id = Asset.objects.get(uid=obj.id_string).id
        content_type = ContentType.objects.get(id=settings.ASSET_CONTENT_TYPE_ID)
        if ObjectPermission.objects.filter(object_id=object_id,
                                           content_type=content_type,
                                           user=user,
                                           permission_id=permission.pk).exists():
            return True
        else:
            return False

    def get_can_edit(self, obj):
        return True
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        permission = Permission.objects.get(content_type__app_label='kpi', codename='change_asset')
        object_id = Asset.objects.get(uid=obj.id_string).id
        content_type = ContentType.objects.get(id=settings.ASSET_CONTENT_TYPE_ID)
        if ObjectPermission.objects.filter(object_id=object_id,
                                           content_type=content_type,
                                           user=user,
                                           permission_id=permission.pk).exists():
            return True
        else:
            return False


class ShareUserListSerializer(serializers.ModelSerializer):
    profile_picture = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'profile_picture')

    def get_profile_picture(self, obj):
        try:
            image_url = obj.user_profile.profile_picture.url
            return image_url
        except:
            return ''


class ShareTeamListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organization
        fields = ('id', 'name', 'logo')


class ShareProjectListSerializer(serializers.ModelSerializer):
    organization = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ('id', 'name', 'logo', 'organization')

    def get_organization(self, obj):
        return obj.organization.name


class ProjectFormSerializer(serializers.ModelSerializer):
    forms = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ('id', 'name', 'forms')

    def get_forms(self, obj):
        xf = XForm.objects.filter(field_sight_form__project=obj,
                                  field_sight_form__is_deployed=True,
                                  field_sight_form__is_deleted=False).distinct()
        serializer = XFormSerializer(xf, many=True, context={'request': self.context['request']})
        return serializer.data


class ShareFormSerializer(serializers.Serializer):
    id_string = serializers.CharField()
    share_id = serializers.ListField(child=serializers.IntegerField())


class ShareProjectFormSerializer(serializers.Serializer):
    id_string = serializers.CharField()
    share_id = serializers.ListField(child=serializers.IntegerField())


class ShareTeamFormSerializer(serializers.Serializer):
    id_string = serializers.CharField()
    share_id = serializers.ListField(child=serializers.IntegerField())


class ShareGlobalFormSerializer(serializers.Serializer):
    id_string = serializers.CharField()


class AddLanguageSerializer(serializers.Serializer):
    id_string = serializers.CharField()
    language = serializers.CharField()
    code = serializers.CharField()


class CloneFormSerializer(serializers.Serializer):
    id_string = serializers.CharField()


class MyFormDeleteSerializer(serializers.Serializer):
    id_string = serializers.CharField()


class FSXFormSerializer(serializers.ModelSerializer):
    em = EMSerializer(read_only=True)
    settings = FormSettingsReadOnlySerializer(read_only=True)
    name = serializers.SerializerMethodField('get_title', read_only=True)
    descriptionText = serializers.SerializerMethodField('get_description', read_only=True)
    version = serializers.SerializerMethodField()
    hash = serializers.SerializerMethodField()
    downloadUrl = serializers.SerializerMethodField('get_url', read_only=True)
    formID = serializers.SerializerMethodField('get_form_id', read_only=True)
    manifestUrl = serializers.SerializerMethodField('get_manifest_url')
    site_project_id = serializers.SerializerMethodField()
    last_submission = serializers.SerializerMethodField()


    class Meta:
        model = FieldSightXF
        fields = ('id', 'site', 'project', 'site_project_id', 'downloadUrl', 'manifestUrl',
                  'name', 'descriptionText', 'formID',
                  'version', 'hash', 'em', 'settings', 'last_submission')

    def get_version(self, obj):
        return get_version(obj.xf.xml)

    @check_obj
    def get_hash(self, obj):
        return u"md5:%s" % obj.xf.hash

    @check_obj
    def get_title(self, obj):
        return u"%s" % obj.xf.title

    @check_obj
    def get_form_id(self, obj):
        return u"%s" % obj.xf.id_string

    @check_obj
    def get_description(self, obj):
        return u"%s" % obj.xf.description

    @check_obj
    def get_url(self, obj):
        kwargs = {'pk': obj.pk}
        request = self.context.get('request')

        return reverse('forms:download_xform', kwargs=kwargs, request=request)

    @check_obj
    def get_manifest_url(self, obj):
        kwargs = {'pk': obj.xf.pk, 'username': obj.xf.user.username}
        request = self.context.get('request')

        return reverse('manifest-url', kwargs=kwargs, request=request)

    def get_site_project_id(self, obj):
        if obj.site:
            return obj.site.project_id
        return None

    def get_last_submission(self, obj):
        if obj.project:
            last_sub = obj.project_form_instances.order_by('-date').first()
            if last_sub:
                return last_sub.date
        if obj.site:
            last_sub = obj.site_form_instances.order_by('-date').first()
            if last_sub:
                return last_sub.date


class SurveyFSXFormSerializer(FSXFormSerializer):
    settings = serializers.SerializerMethodField()
    last_submission = serializers.SerializerMethodField()

    class Meta:
        model = FieldSightXF
        fields = ('id', 'site', 'project', 'site_project_id', 'downloadUrl', 'manifestUrl',
                  'name', 'descriptionText', 'formID',
                  'version', 'hash', 'em', 'settings', 'last_submission')

    def get_settings(self, obj):
        return None

    def get_last_submission(self, obj):
        if obj.project:
            last_sub = obj.project_form_instances.order_by('-date').first()
            if last_sub:
                return last_sub.date
        if obj.site:
            last_sub = obj.site_form_instances.order_by('-date').first()
            if last_sub:
                return last_sub.date


class ScheduleSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='get_schedule_level_id_display')

    class Meta:
        model = Schedule
        fields = ('id', 'name', 'date_range_start', 'date_range_end',
                  'selected_days', 'frequency', 'month_day',
                  'type')


class SchedueFSXFormSerializer(FSXFormSerializer):
    settings = FormSettingsReadOnlySerializerSchedule(read_only=True)

    class Meta:
        model = FieldSightXF
        fields = ('id', 'site', 'project', 'site_project_id', 'downloadUrl', 'manifestUrl',
                  'name', 'descriptionText', 'formID',
                  'version', 'hash', 'em', 'schedule', 'settings', 'last_submission')

    def get_last_submission(self, obj):
        try:
            if obj.project:
                last_sub = obj.schedule_forms.project_form_instances.order_by('-date').first()
                if last_sub:
                    return last_sub.date
            if obj.site:
                last_sub = obj.schedule_forms.site_form_instances.order_by('-date').first()
                if last_sub:
                    return last_sub.date
        except:
            return ""


class SubStageSerializer(serializers.ModelSerializer):
    stage_forms = FSXFormSerializer()
    # em = EMSerializer(read_only=True)
    # tags = serializers.SerializerMethodField()

    class Meta:
        model = Stage
        exclude = ('shared_level', 'site', 'group', 'ready', 'project', 'stage', 'date_modified', 'date_created')

    # def get_tags(self, obj):
    #     parent_tags = self.context.get(str(obj.stage_id), [])
    #     obj.tags.extend(parent_tags)
    #     return list(set(obj.tags))


class StageSerializer(serializers.ModelSerializer):
    sub_stages = SubStageSerializer(many=True, source="parent")
    site_project_id = serializers.SerializerMethodField()
    types = serializers.SerializerMethodField()

    class Meta:
        model = Stage
        exclude = ('shared_level', 'group', 'ready', 'stage', 'date_modified', 'date_created',
                   'tags',)

    # def get_substages(self, stage):
    #     stages = Stage.objects.filter(stage=stage, is_deleted=False,
    #                                   stage_forms__is_deleted=False,
    #                                   stage_forms__is_deployed=True
    #                                   ).select_related('stage_forms',
    #                                                     'stage_forms__xf',
    #                                                     'em').order_by(
    #         'order', 'date_created')
    #     serializer = SubStageSerializer(instance=stages, many=True)
    #     return serializer.data

    def get_site_project_id(self, obj):
        if obj.site:
            return obj.site.project_id
        return None

    def get_types(self, obj):
        return obj.tags
