from rest_framework import serializers
from onadata.apps.viewer.models import Export


class ExportSerializer(serializers.ModelSerializer):

    class Meta:
        model = Export
        fields = ('id', 'filename', 'internal_status', 'created_on', 'status')
        read_only_fields = ('filename', 'internal_status', 'created_on', 'status')

    def get_status(self, obj):
        if obj.internam_status == 0:
            return "Pending"
        elif obj.internam_status == 1:
            return "Successfull"
        elif obj.internam_status == 2:
            return "Failed"

