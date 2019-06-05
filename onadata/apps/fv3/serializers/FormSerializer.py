from rest_framework import serializers

from onadata.apps.logger.models import XForm


class XFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = XForm
        fields=('id_string','title')