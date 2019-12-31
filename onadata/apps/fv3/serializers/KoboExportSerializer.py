from rest_framework import serializers
from onadata.apps.viewer.models import Export


class ExportSerializer(serializers.Serializer):

    class Meta:
        model = Export
        exclude = ()

