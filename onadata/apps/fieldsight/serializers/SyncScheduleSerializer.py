from onadata.apps.fieldsight.models import Project
from onadata.apps.fsform.models import SyncSchedule
from rest_framework import serializers

class SyncScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SyncSchedule
        fields = ('id', 'fxf', 'schedule', 'date', 'end_of_month')
        extra_kwargs = {
        	'schedule': {'required': True}
        	'date': {'required': True}
        }

class ProjectSyncScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'gsuit_sync_schedule', 'date', 'end_of_month')
        extra_kwargs = {
        	'gsuit_sync_schedule': {'required': True}
        	'date': {'required': True}
        }