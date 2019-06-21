from rest_framework import serializers

from onadata.apps.logger.models import XForm

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

    class Meta:
        model = XForm
        fields = ('id_string','title', 'edit_url', 'preview_url', 'replace_url', 'download_url', 'media_url', 'date_created')

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

    def get_share_users_url(self):
        return "{}/fv3/api/share/".format(settings.KOBOCAT_URL)

    def get_share_project_url(self):
        return "{}/fv3/api/share/project/".format(settings.KOBOCAT_URL)

    def get_share_team_url(self):
        return "{}/fv3/api/share/team/".format(settings.KOBOCAT_URL)

    def get_share_global_url(self):
        return "{}/fv3/api/share/global/".format(settings.KOBOCAT_URL)


class ShareFormSerializer(serializers.Serializer):
    form = serializers.IntegerField()
    users = serializers.ListField(child=serializers.IntegerField())


class ShareProjectFormSerializer(serializers.Serializer):
    form = serializers.IntegerField()
    project = serializers.IntegerField()


class ShareTeamFormSerializer(serializers.Serializer):
    form = serializers.IntegerField()
    team = serializers.IntegerField()


class ShareGlobalFormSerializer(serializers.Serializer):
    form = serializers.IntegerField()
