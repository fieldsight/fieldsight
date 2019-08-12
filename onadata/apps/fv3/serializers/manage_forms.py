from rest_framework import serializers

from onadata.apps.fsforms.models import FieldSightXF, Schedule, Stage
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
        fields = ('id', 'xf', 'date_created', 'default_submission_status',
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


class GeneralProjectFormSerializer(serializers.ModelSerializer):
    em = EMSerializer(read_only=True)
    xf = XFormSerializer()
    responses_count = serializers.SerializerMethodField()

    class Meta:
        model = FieldSightXF
        fields = ('id', 'xf', 'date_created', 'default_submission_status',
                  'responses_count', 'em')

    def get_responses_count(self, obj):
        is_project = self.context.get('project_id', False)
        if is_project:
            # return obj.project_form_instances.count()
            return obj.responses_count\
                if hasattr(obj, "responses_count") else 0
        return 0


class ScheduleSerializer(serializers.ModelSerializer):
    em = serializers.SerializerMethodField('get_education_material',
                                           read_only=True)
    xf = serializers.SerializerMethodField('get_assigned_form',
                                             read_only=True)
    is_deployed = serializers.SerializerMethodField(
        'get_is_deployed_status', read_only=True)
    default_submission_status = serializers.SerializerMethodField()
    schedule_level = serializers.SerializerMethodField(
        'get_schedule_level_type', read_only=True)
    responses_count = serializers.SerializerMethodField()

    def validate(self, data):
        """
        Check that form is unique for general form.
        """
        if data.has_key('site'):
            if FieldSightXF.objects.filter(
                    xf__id=data['xf'],
                    is_staged=False,
                    is_scheduled=True,
                    site=data['site']).exists():
                raise serializers.ValidationError(
                    "Form Already Exists, Duplicate Forms Not Allowed")
        elif data.has_key('project'):
            if FieldSightXF.objects.filter(
                    xf__id=data['xf'],
                    is_staged=False,
                    is_scheduled=True, project=data['project']).exists():
                raise serializers.ValidationError(
                    "Form Already Exists, Duplicate Forms Not Allowed")
        return data

    class Meta:
        model = Schedule
        fields = ('id', 'em', 'xf',
                  'is_deployed', 'default_submission_status', 'schedule_level',
                  'responses_count', 'date_created', 'schedule_level_id')

    def get_all_days(self, obj):
        return u"%s" % (", ".join(day.day for day in obj.selected_days.all()))

    def get_schedule_level_type(self, obj):
        if obj.schedule_level_id == 2:
            return "Monthly"
        elif obj.schedule_level_id == 1:
            return "Weekly"
        else:
            return "Daily"

    def get_assigned_form(self, obj):
        if not FieldSightXF.objects.filter(schedule=obj).exists():
            return None
        else:
            fsxf = FieldSightXF.objects.get(schedule=obj)
            if fsxf.xf:
                return XFormSerializer(fsxf.xf).data
        return None


    def get_is_deployed_status(self, obj):
        if not FieldSightXF.objects.filter(schedule=obj).exists():
            return False
        else:
            return FieldSightXF.objects.get(schedule=obj).is_deployed

    def get_default_submission_status(self, obj):
        try:
            return obj.schedule_forms.default_submission_status
        except:
            return 0

    def get_education_material(self, obj):
        try:
            em =  obj.schedule_forms.em
            return EMSerializer(em).data
        except Exception:
            return {}

    def get_responses_count(self, obj):
        is_project = self.context.get('is_project', False)
        if is_project:
            return obj.response_count if hasattr(obj, "response_count") else 0
        elif obj.project:
            return obj.response_count if hasattr(obj, "response_count") else 0
        elif obj.site:
            return obj.site_response_count if hasattr(obj, "site_response_count") else 0


class StageSerializer(serializers.ModelSerializer):
    sub_stage_weight = serializers.SerializerMethodField()

    class Meta:
        model = Stage
        fields = ('id', 'name', 'sub_stage_weight')

    def get_sub_stage_weight(self, obj):
        if hasattr(obj, "sub_stage_weight"):
            return obj.sub_stage_weight
        return 0