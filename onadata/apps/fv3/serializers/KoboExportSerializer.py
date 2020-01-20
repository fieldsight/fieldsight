from rest_framework import serializers
from onadata.apps.viewer.models import Export


class ExportSerializer(serializers.ModelSerializer):
    status_title = serializers.SerializerMethodField()

    class Meta:
        model = Export
        fields = ('id', 'filename', 'internal_status', 'created_on', 'status_title')
        read_only_fields = ('filename', 'internal_status', 'created_on', 'status_title')

    def get_status_title(self, obj):
        if obj.internal_status == 0:
            return "Pending"
        elif obj.internal_status == 1:
            return "Successfull"
        elif obj.internal_status == 2:
            return "Failed"

