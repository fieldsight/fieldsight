from rest_framework import serializers

from onadata.apps.fsforms.models import FieldSightXF, FInstance


class ProjectSiteResponseSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    title = serializers.SerializerMethodField(read_only=True)
    created_date = serializers.SerializerMethodField(read_only=True)
    last_response = serializers.SerializerMethodField(read_only=True)
    response_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = FieldSightXF
        fields = ('id', 'name', 'title', 'created_date', 'response_count', 'last_response')

    def get_name(self, obj):
        return u"%s" % obj.xf.title

    def get_title(self, obj):
        return u"%s" % obj.xf.id_string

    def get_created_date(self, obj):
        return obj.date_created

    def get_last_response(self, obj):
        is_project = self.context.get('is_project', False)
        if is_project:
            return obj.project_form_instances.order_by('-pk').values(
                    'date')[:1]

    def get_response_count(self, obj):
        is_project = self.context.get('is_project', False)
        if is_project:
            count = obj.response_count if hasattr(obj, 'response_count') else 0
            return count