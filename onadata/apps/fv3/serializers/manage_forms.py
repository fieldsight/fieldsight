from rest_framework import serializers

from onadata.apps.fsforms.models import FieldSightXF
from onadata.apps.fsforms.serializers.FieldSightXFormSerializer import \
    EMSerializer
from onadata.apps.logger.models import XForm


class XFormSerializer(serializers.ModelSerializer):

    class Meta:
        model = XForm
        fields = ("id_string", "title")


class GeneralFormSerializer(serializers.ModelSerializer):
    em = EMSerializer(read_only=True)
    xf = XFormSerializer()
    responses_count = serializers.SerializerMethodField()

    class Meta:
        model = FieldSightXF
        fields = ('xf', 'date_created', 'default_submission_status',
                  'responses_count', 'em')

    def get_responses_count(self, obj):
        is_project = self.context.get('project_id', False)
        if is_project:
            # return obj.project_form_instances.count()
            return obj.response_count\
                if hasattr(obj, "response_count") else 0
        elif obj.project:
            # return obj.project_form_instances.filter(self.context.get(
            # 'site_id').count()
            return obj.response_count\
                if hasattr(obj, "response_count") else 0
        elif obj.site:
            return obj.site_response_count\
                if hasattr(obj, "site_response_count") else 0

