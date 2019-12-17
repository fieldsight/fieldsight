from rest_framework import serializers

from onadata.apps.fsforms.models import Stage
from .models import ReportSettings


class StageFormSerializer(serializers.ModelSerializer):
    sub_stages = serializers.SerializerMethodField()

    class Meta:
        model = Stage

        fields = ('name', 'sub_stages')

    def get_sub_stages(self, obj):

        data = [{'id': form.stage_forms.xf.id, 'form_name': form.stage_forms.xf.title}
                for form in obj.active_substages().prefetch_related('stage_forms', 'stage_forms__xf')
                ]

        return data


class ReportSettingsSerializer(serializers.ModelSerializer):
    owner_full_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ReportSettings

        exclude = ('owner',)

    def get_owner_full_name(self, obj):
        return obj.owner.get_full_name()

