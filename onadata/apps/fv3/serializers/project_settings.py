from rest_framework import serializers

from onadata.apps.fieldsight.models import ProgressSettings


class ProgressSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgressSettings
        exclude = ('active', 'project', 'user')