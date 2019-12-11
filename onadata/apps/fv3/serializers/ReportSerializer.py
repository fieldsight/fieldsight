from rest_framework import serializers

from onadata.apps.fieldsight.models import ReportData
from onadata.apps.fsforms.models import ReportSyncSettings, FieldSightXF, SCHEDULED_TYPE


class ReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReportData
        exclude = ('location', 'user')


class ReportSyncSettingsSerializer(serializers.ModelSerializer):
    day_display = serializers.SerializerMethodField()

    class Meta:
        model = ReportSyncSettings
        exclude = ()

    def get_day_display(self, obj):
        if obj.day and obj.schedule_type == 2:
            return {'0': "Sunday", '1': "Monday", '2': "Tuesday",
                    '3': "Wednesday", '4': "Thursday",
                    '5': "Friday", '6': "Saturday"}.get(str(obj.day), "-")
        return ""


class ProjectFormSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = FieldSightXF
        fields = ('id', 'title')

    def get_title(self, obj):
        return u"%s" % obj.xf.title
