from rest_framework import serializers

from onadata.apps.logger.models import XForm

from onadata.apps.fsforms.models import Asset

from onadata.apps.fsforms.models import FieldSightXF


from django.conf import settings


class XFormSerializer(serializers.ModelSerializer):
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

    class Meta:
        model = XForm
        fields = ('id_string','title', 'edit_url', 'preview_url', 'replace_url',
                  'download_url', 'media_url', 'date_created', 'date_modified', 'share_users_url',
                  'share_project_url', 'share_team_url', 'share_global_url', 'add_language_url', 'clone_form_url')

    def get_edit_url(self, obj):
        return "{}#forms/{}/edit/".format(settings.KPI_URL, obj.id_string)

    def get_preview_url(self, obj):
        return "{}/forms/preview/{}/".format(settings.KOBOCAT_URL, obj.id_string)

    def get_replace_url(self, obj):
        return "{}{}/".format(settings.KPI_URL,"import")

    def get_download_url(self, obj):
        return "{}{}.{}".format(settings.KPI_ASSET_URL, obj.id_string, "xls")

    def get_media_url(self, obj):
        return "{}/{}/forms/{}/form_settings".format(settings.KOBOCAT_URL, obj.user.username, obj.id_string)

    def get_share_users_url(self, obj):
        return "{}/fv3/api/share/".format(settings.KOBOCAT_URL)

    def get_share_project_url(self, obj):
        return "{}/fv3/api/share/project/".format(settings.KOBOCAT_URL)

    def get_share_team_url(self, obj):
        return "{}/fv3/api/share/team/".format(settings.KOBOCAT_URL)

    def get_share_global_url(self, obj):
        return "{}/fv3/api/share/global/".format(settings.KOBOCAT_URL)

    def get_add_language_url(self, obj):
        return "{}/fv3/api/add-language/".format(settings.KOBOCAT_URL)

    def get_clone_form_url(self, obj):
        return "{}/fv3/api/clone/".format(settings.KOBOCAT_URL)


class ShareFormSerializer(serializers.Serializer):
    id_string = serializers.CharField()
    users = serializers.ListField(child=serializers.IntegerField())


class ShareProjectFormSerializer(serializers.Serializer):
    id_string = serializers.CharField()
    project = serializers.IntegerField()


class ShareTeamFormSerializer(serializers.Serializer):
    id_string = serializers.CharField()
    team = serializers.IntegerField()


class ShareGlobalFormSerializer(serializers.Serializer):
    id_string = serializers.CharField()


class AddLanguageSerializer(serializers.Serializer):
    id_string = serializers.CharField()
    language = serializers.CharField()
    code = serializers.CharField()


class CloneFormSerializer(serializers.Serializer):
    id_string = serializers.CharField()
    project = serializers.IntegerField()

