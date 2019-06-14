from rest_framework import serializers
from onadata.apps.fieldsight.models import ProjectLevelTermsAndLabels


class ProjectLevelTermsSerializers(serializers.ModelSerializer):

    class Meta:
        model = ProjectLevelTermsAndLabels
        exclude = ('id',)
