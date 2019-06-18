import json

from django.core.serializers import serialize

from rest_framework import serializers

from onadata.apps.fieldsight.models import Organization, Site, Project
from onadata.apps.userrole.models import UserRole


class SiteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Site
        fields = ('id', 'name', 'address', 'logo', 'public_desc')
