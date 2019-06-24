from rest_framework import serializers

from onadata.apps.fieldsight.models import ReportData


class ReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReportData
        exclude = ('location', 'user')
