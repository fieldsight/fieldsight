from rest_framework import serializers
from onadata.apps.fieldsight.models import ProjectMapFiltersMetrics


class ProjectFilterMetricsSerializer(serializers.ModelSerializer):
    site_information_filters = serializers.JSONField(required=False)
    form_data_filters = serializers.JSONField(required=False)

    class Meta:
        model = ProjectMapFiltersMetrics
        exclude = ('project',)