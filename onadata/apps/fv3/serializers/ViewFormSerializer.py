from rest_framework import serializers

from onadata.apps.fsforms.models import FieldSightXF, Schedule, Stage


class ViewGeneralsFormSerializer(serializers.ModelSerializer):
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
        if is_project or obj.project:
            return obj.project_form_instances.order_by('-pk').values_list(
                    'date', flat=True)[:1]

        elif obj.site:
            return obj.site_form_instances.order_by('-pk').values_list(
                    'date', flat=True)[:1]

    def get_response_count(self, obj):
        is_project = self.context.get('is_project', False)
        if is_project or obj.project:
            count = obj.response_count if hasattr(obj, 'response_count') else 0
            return count
        elif obj.site:
            count = obj.site_response_count if hasattr(obj, 'site_response_count') else 0
            return count


class ViewScheduledFormSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    title = serializers.SerializerMethodField(read_only=True)
    created_date = serializers.SerializerMethodField(read_only=True)
    last_response = serializers.SerializerMethodField(read_only=True)
    response_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Schedule
        fields = ('id', 'name', 'title', 'created_date', 'response_count', 'last_response')

    def get_name(self, obj):
        return u"%s" % obj.schedule_forms.xf.title

    def get_title(self, obj):
        return u"%s" % obj.schedule_forms.xf.id_string

    def get_created_date(self, obj):
        return obj.schedule_forms.date_created

    def get_last_response(self, obj):
        is_project = self.context.get('is_project', False)
        if is_project or obj.project:
            return obj.schedule_forms.project_form_instances.order_by('-pk').values_list(
                    'date', flat=True)[:1]

        elif obj.site:
            return obj.schedule_forms.site_form_instances.order_by('-pk').values_list(
                    'date', flat=True)[:1]

    def get_response_count(self, obj):
        is_project = self.context.get('is_project', False)
        if is_project or obj.project:
            count = obj.response_count if hasattr(obj, 'response_count') else 0
            return count
        elif obj.site:
            count = obj.site_response_count if hasattr(obj, 'site_response_count') else 0
            return count


class ViewStageFormSerializer(serializers.ModelSerializer):

    class Meta:
        model = Stage
        fields = ('id', 'name', 'order',)

    # def get_name(self, obj):
    #     return u"%s" % obj.stage_forms.xf.title
    #
    # def get_title(self, obj):
    #     return u"%s" % obj.stage_forms.xf.id_string
    #
    # def get_created_date(self, obj):
    #     return obj.stage_forms.date_created
    #
    # def get_last_response(self, obj):
    #     is_project = self.context.get('is_project', False)
    #     if is_project or obj.project:
    #         return obj.stage_forms.project_form_instances.order_by('-pk').values_list(
    #                 'date', flat=True)[:1]
    #
    #     elif obj.site:
    #         return obj.stage_forms.site_form_instances.order_by('-pk').values_list(
    #                 'date', flat=True)[:1]
    #
    # def get_response_count(self, obj):
    #     is_project = self.context.get('is_project', False)
    #     if is_project or obj.project:
    #         count = obj.response_count if hasattr(obj, 'response_count') else 0
    #         return count
    #     elif obj.site:
    #         count = obj.site_response_count if hasattr(obj, 'site_response_count') else 0
    #         return count