from django.core.files.storage import default_storage
from rest_framework import serializers
from onadata.apps.viewer.models import Export


class ExportSerializer(serializers.ModelSerializer):
    status_title = serializers.SerializerMethodField()
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = Export
        fields = ('id', 'filename', 'internal_status', 'created_on', 'status_title', 'file_url')
        read_only_fields = ('filename', 'internal_status', 'created_on', 'status_title', 'file_url')

    def get_status_title(self, obj):
        if obj.internal_status == 0:
            return "Pending"
        elif obj.internal_status == 1:
            return "Successfull"
        elif obj.internal_status == 2:
            return "Failed"

    def get_file_url(self, obj):
        if obj.status == 1:
            return default_storage.url(obj.filepath)
        return ""


