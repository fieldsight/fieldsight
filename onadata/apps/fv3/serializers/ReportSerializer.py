from rest_framework import serializers

from onadata.apps.fieldsight.models import ReportData
from onadata.apps.fsforms.models import ReportSyncSettings, FieldSightXF


class ReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReportData
        exclude = ('location', 'user')


class ReportSyncSettingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReportSyncSettings
        exclude = ()


class ProjectFormSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = FieldSightXF
        fields = ('id', 'title')

    def get_title(self, obj):
        return u"%s" % obj.xf.title