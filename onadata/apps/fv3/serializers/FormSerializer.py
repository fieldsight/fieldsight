from rest_framework import serializers

from onadata.apps.logger.models import XForm

from django.conf import settings


class XFormSerializer(serializers.ModelSerializer):
    edit_url = serializers.SerializerMethodField()
    preview_url = serializers.SerializerMethodField()
    replace_url = serializers.SerializerMethodField()
    download_url = serializers.SerializerMethodField()

    class Meta:
        model = XForm
        fields = ('id_string','title', 'edit_url', 'preview_url', 'replace_url', 'download_url', 'date_created')

    def get_edit_url(self, obj):
        return "{}#forms/{}/edit/".format(settings.KPI_URL, obj.id_string)

    def get_preview_url(self, obj):
        return "{}/forms/preview/{}/".format(settings.KOBOCAT_URL, obj.id_string)

    def get_replace_url(self, obj):
        return obj.id_string

    def get_download_url(self, obj):
        return "{}{}.{}".format(settings.KPI_ASSET_URL, obj.id_string, "xls")