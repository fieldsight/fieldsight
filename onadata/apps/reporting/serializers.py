from rest_framework import serializers

from onadata.apps.fsforms.models import Stage


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