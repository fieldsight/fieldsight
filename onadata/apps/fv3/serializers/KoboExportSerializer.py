from rest_framework import serializers
from onadata.apps.viewer.models import Export


class ExportSerializer(serializers.ModelSerializer):

    class Meta:
        model = Export
        fields = ('id', 'filename', 'internal_status', 'created_on',)
        read_only_fields = ('id', 'filename', 'internal_status', 'created_on',)

