from rest_framework import serializers

from onadata.apps.fsforms.models import Stage, SCHEDULED_TYPE
from onadata.apps.fieldsight.models import Site

from .models import ReportSettings



class StageFormSerializer(serializers.ModelSerializer):
    sub_stages = serializers.SerializerMethodField()

    class Meta:
        model = Stage

        fields = ('name', 'sub_stages')

    def get_sub_stages(self, obj):

        data = [{'id': form.stage_forms.id, 'form_name': form.stage_forms.xf.title}
                for form in obj.active_substages().prefetch_related('stage_forms', 'stage_forms__xf')
                ]

        return data


class ReportSettingsSerializer(serializers.ModelSerializer):
    owner_full_name = serializers.SerializerMethodField(read_only=True)
    shared_with = serializers.SerializerMethodField()
    attributes = serializers.JSONField()
    filter = serializers.JSONField(default=dict)
    report_sync_settings = serializers.SerializerMethodField(read_only=True)
    datapoints = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ReportSettings

        exclude = ('owner', 'project')

    def get_owner_full_name(self, obj):
        return obj.owner.get_full_name()

    def get_shared_with(self, obj):
        users = []
        [users.append(user.get_full_name()) for user in obj.shared_with.all()]
        return users

    def get_report_sync_settings(self, obj):
        if obj.report_sync_settings.all():
            sync = obj.report_sync_settings.all()[0]
            sync_settings = {'id': sync.id,
                             'schedule_type': SCHEDULED_TYPE[int(sync.schedule_type)][1],
                             'last_synced_date': sync.last_synced_date,
                             'spreadsheet_id': sync.spreadsheet_id,
                             'range': sync.range,
                             'grid_id': sync.grid_id,
                             'day': sync.day
                             }

        else:
            sync_settings = {}

        return sync_settings

    def get_datapoints(self, obj):
        return len(obj.attributes)


class ReportSettingsListSerializer(serializers.ModelSerializer):
    owner_full_name = serializers.SerializerMethodField(read_only=True)
    shared_with = serializers.SerializerMethodField()
    datapoints = serializers.SerializerMethodField(read_only=True)
    report_sync_settings = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ReportSettings

        exclude = ('owner', 'project', 'filter', 'attributes')

    def get_owner_full_name(self, obj):
        return obj.owner.get_full_name()

    def get_shared_with(self, obj):
        users = []
        [users.append(user.get_full_name()) for user in obj.shared_with.all()]
        return users

    def get_datapoints(self, obj):
        return len(obj.attributes)

    def get_report_sync_settings(self, obj):
        if obj.report_sync_settings.all():
            sync = obj.report_sync_settings.all()[0]
            sync_settings = {'id': sync.id,
                             'schedule_type': SCHEDULED_TYPE[int(sync.schedule_type)][1],
                             'last_synced_date': sync.last_synced_date,
                             'spreadsheet_id': sync.spreadsheet_id,
                             'range': sync.range,
                             'grid_id': sync.grid_id,
                             'day': sync.day
                             }

        else:
            sync_settings = {}

        return sync_settings


class PreviewSiteInformationSerializer(serializers.ModelSerializer):
    region = serializers.CharField(source='region.identifier')
    latitude = serializers.SerializerMethodField()
    longitude = serializers.SerializerMethodField()

    class Meta:
        model = Site

        exclude = ('id', 'project', 'logo', 'location', 'current_status', 'enable_subsites', 'weight', 'date_created',
                   'date_modified', 'site_meta_attributes_ans', 'site_featured_images')

    def get_latitude(self, obj):
        if obj.location:
            return obj.location.y

    def get_longitude(self, obj):
        if obj.location:
            return obj.location.x

    def to_representation(self, instance):
        data = super(PreviewSiteInformationSerializer, self).to_representation(instance)
        project = instance.project

        if not project.cluster_sites:
            data.pop('region')
        return data


