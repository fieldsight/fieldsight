from datetime import datetime
from django.contrib.auth.models import User

from rest_framework import serializers
from onadata.apps.userrole.models import UserRole
from onadata.apps.fieldsight.models import UserInvite
from onadata.apps.fsforms.models import FInstance


class MyRolesSerializer(serializers.ModelSerializer):

    name = serializers.SerializerMethodField()
    post = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()

    class Meta:
        model = UserRole
        fields = ('post', 'name', 'address')

    def get_post(self, obj):

        return obj.group.name

    def get_name(self, obj):

        if obj.group.name == 'Region Supervisor' or obj.group.name == 'Region Reviewer':
            return obj.region.name

        elif obj.group.name == 'Project Manager' or obj.group.name == 'Project Donor' or obj.group.name == 'Staff Project Manager':
            return obj.project.name

        elif obj.group.name == 'Site Supervisor' or obj.group.name == 'Site Reviewer':
            return obj.site.name

        elif obj.group.name == 'Organization Admin':
            return obj.organization.name

    def get_address(self, obj):

        if obj.group.name == 'Region Supervisor' or obj.group.name == 'Region Reviewer':
            return None

        elif obj.group.name == 'Project Manager' or obj.group.name == 'Project Donor' or obj.group.name == 'Staff Project Manager':
            return obj.project.address

        elif obj.group.name == 'Site Supervisor' or obj.group.name == 'Site Reviewer':
            return obj.site.address

        elif obj.group.name == 'Organization Admin':
            return obj.organization.address


class UserInvitationSerializer(serializers.ModelSerializer):
    group = serializers.CharField(source='group.name')
    by_user = serializers.CharField(source='by_user.username')
    current_user = serializers.SerializerMethodField()

    class Meta:
        model = UserInvite
        fields = ('id', 'by_user', 'group', 'current_user')

    def get_current_user(self, obj):

        user = User.objects.get(email=obj.email)
        return user.username


class LatestSubmissionSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()
    form = serializers.SerializerMethodField()
    date =serializers.SerializerMethodField()

    class Meta:
        model = FInstance
        fields = ('id', 'date', 'form', 'detail_url')

    def get_detail_url(self, obj):
        return '/#/submission-details/{}'.format(obj.id)

    def get_form(self, obj):
        if obj.project_fxf:
            return obj.project_fxf.xf.title
        elif obj.site_fxf:
            return obj.site_fxf.xf.title

    def get_date(self, obj):
        return datetime.strftime(obj.date, '%Y-%m-%d %H:%M:%S')

