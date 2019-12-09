from rest_framework import serializers

from onadata.apps.fieldsight.models import ReportData
from onadata.apps.fsforms.models import ReportSyncSettings


class ReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReportData
        exclude = ('location', 'user')


class ReportSyncSettingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReportSyncSettings
        exclude = ()
