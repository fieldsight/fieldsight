from datetime import datetime
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import Q

from rest_framework import serializers
from onadata.apps.userrole.models import UserRole
from onadata.apps.fieldsight.models import UserInvite, Project, Region, Site
from onadata.apps.fsforms.models import FInstance

FORM_STATUS = {0: 'Pending', 1: "Rejected", 2: 'Flagged', 3: 'Approved'}


class MyProjectSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='project_id')
    name = serializers.CharField(source='project.name')
    has_project_access = serializers.SerializerMethodField()
    project_url = serializers.SerializerMethodField()

    class Meta:
        model = UserRole
        fields = ('id', 'name', 'has_project_access', 'project_url')

    def get_has_project_access(self, obj):
        user = self.context['user']
        # if obj.group.name == "Project Manager" or obj.group.name == "Project Donor":
        if obj.project_id in user.user_roles.filter(group__name__in=["Project Manager", "Project Donor"],
                                                         ended_at=None).values_list('project_id', flat=True):

            has_access = True

        else:
            has_access = False

        return has_access

    def get_project_url(self, obj):
        user = self.context['user']
        has_project_access = self.get_has_project_access(obj)

        if has_project_access:
            if user.user_roles.filter(project=obj.project, group__name="Project Manager", ended_at=None):

                project_url = obj.project.get_absolute_url()
            else:
                project_url = obj.project.get_absolute_url()

            return project_url


class MyRegionSerializer(serializers.ModelSerializer):
    total_sites = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()
    region_url = serializers.SerializerMethodField()

    class Meta:
        model = Region
        fields = ('id', 'identifier', 'name', 'total_sites', 'role', 'region_url')

    def get_total_sites(self, obj):
        return obj.get_sites_count()

    def get_role(self, obj):
        user = self.context['request'].user
        is_project_manager_or_team_admin = user.user_roles.all().filter(Q(group__name__in=["Project Manager", "Project Donor"], project=obj.project)|
                                                                         Q(group__name="Organization Admin",
                                                                           organization=obj.project.organization, ended_at=None))\
            .exists()

        if is_project_manager_or_team_admin:
            group = None

        else:

            obj = obj.region_roles.select_related('group').filter(user=user)

            if len(obj) > 1:
                group = "Region Supervisor"
            else:
                group = obj.get().group.name

        return group

    def get_region_url(self, obj):
        return settings.SITE_URL + obj.get_absolute_url()


class MySiteSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    submissions = serializers.SerializerMethodField()
    progress = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    site_url = serializers.SerializerMethodField()
    region = serializers.CharField(source='region.name')
    type = serializers.CharField(source='type.name')

    class Meta:
        model = Site
        fields = ('id', 'identifier', 'name', 'address', 'site_url', 'region', 'role', 'submissions', 'progress',
                  'status', 'type')

    def get_role(self, obj):
        user = self.context['request'].user
        is_project_manager_or_team_admin = user.user_roles.all().filter(Q(group__name="Project Manager", project=obj.project)|
                                                          Q(group__name="Organization Admin", organization=obj.project.organization),
                                                                        ended_at=None).exists()
        is_project_donor = user.user_roles.all().filter(group__name="Project Donor", project=obj.project,
                                                        ended_at=None).exists()
        if is_project_manager_or_team_admin:
            group = None

        elif is_project_donor:
            group = 'Donor'

        else:
            site_group = obj.site_roles.select_related('group').filter(user=user)

            if len(site_group) > 1:
                group = "Site Supervisor"

            elif len(site_group) == 0:
                region_group = user.user_roles.filter(group__name__in=["Region Supervisor", "Region Reviewer"],
                                                      region__is_active=True, ended_at=None)
                if len(region_group) > 1:
                    group = 'Region Supervisor'
                else:
                    group = region_group[0].group.name

            else:
                group = obj.site_roles.all().filter(user=user)[0].group.name

        return group

    def get_submissions(self, obj):
        queryset = FInstance.objects.order_by('-date')
        total_sites = list(obj.sub_sites.values_list('id', flat=True))
        total_sites.append(obj.id)
        submissions = queryset.filter(site__in=total_sites).count()

        return submissions

    def get_status(self, obj):

        total_sites = list(obj.sub_sites.values_list('id', flat=True))
        total_sites.append(obj.id)
        sites_subsite_instances = FInstance.objects.filter(site__in=total_sites)
        try:
            if sites_subsite_instances:
                return FORM_STATUS[sites_subsite_instances.order_by('-date')[0].form_status]
        except:
            return None

    def get_progress(self, obj):

        if obj.current_progress:
            return obj.current_progress
        else:
            return 0

    def get_site_url(self, obj):
        return settings.SITE_URL + obj.get_absolute_url()

    def get_region_url(self, obj):
        if obj.region:
            return settings.SITE_URL + obj.region.get_absolute_url()


class MyRolesSerializer(serializers.ModelSerializer):

    name = serializers.SerializerMethodField()
    # post = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    logo = serializers.SerializerMethodField()
    has_organization_access = serializers.SerializerMethodField()
    team_url = serializers.SerializerMethodField()
    projects = serializers.SerializerMethodField()
    id = serializers.IntegerField(source='organization.id')

    class Meta:
        model = UserRole
        fields = ('id', 'name', 'address', 'logo', 'has_organization_access', 'team_url', 'projects')

    def get_name(self, obj):
        return obj.organization.name

    def get_address(self, obj):
        return obj.organization.address

    def get_logo(self, obj):
        return obj.organization.logo.url

    def get_has_organization_access(self, obj):
        user = self.context['user']
        if obj.organization_id in user.user_roles.filter(group__name="Organization Admin", ended_at=None).values_list('organization_id', flat=True):
            has_access = True

        else:
            has_access = False

        return has_access

    def get_projects(self, obj):
        user = self.context['user']
        org_admin = self.get_has_organization_access(obj)

        if org_admin:
            data = Project.objects.filter(organization=obj.organization, is_active=True)
            roles = [{'id': r.id, 'name': r.name, 'has_project_access': True, 'project_url': r.get_absolute_url()} for r in data]
            # roles = [{'id': proj.id, 'name': proj.name, 'project_url': settings.SITE_URL + proj.get_absolute_url()} for proj in data]

        else:
            data = UserRole.objects.filter(user=obj.user, organization=obj.organization).select_related('user', 'group', 'site', 'organization',
                                                                      'staff_project', 'region').filter(Q(group__name="Project Manager", project__is_active=True)|
                                                                    Q(group__name="Site Supervisor", site__is_active=True)|
                                                                    Q(group__name="Reviewer", site__is_active=True)|
                                                                    Q(group__name="Region Reviewer", region__is_active=True)|
                                                                    Q(group__name="Region Supervisor", region__is_active=True)|
                                                                    Q(group__name="Project Donor", project__is_active=True)
                                                                                                        ).distinct('project')
            roles = MyProjectSerializer(data, many=True, context={'user': user}).data
        return roles

    def get_team_url(self, obj):
        return settings.SITE_URL + obj.organization.get_absolute_url()

    def to_representation(self, obj):
        data = super(MyRolesSerializer, self).to_representation(obj)
        user = self.context['user']

        if obj.organization_id not in user.user_roles.filter(group__name="Organization Admin", ended_at=None).values_list('organization_id', flat=True):

            data.pop('team_url')

        return data
    #
    # def get_post(self, obj):
    #
    #     return obj.group.name

    # def get_name(self, obj):
    #
    #     if obj.group.name == 'Region Supervisor' or obj.group.name == 'Region Reviewer':
    #         return obj.region.name
    #
    #     elif obj.group.name == 'Project Manager' or obj.group.name == 'Project Donor' or obj.group.name == 'Staff Project Manager':
    #         return obj.project.name
    #
    #     elif obj.group.name == 'Site Supervisor' or obj.group.name == 'Site Reviewer':
    #         return obj.site.name
    #
    #     elif obj.group.name == 'Organization Admin':
    #         return obj.organization.name

    # def get_address(self, obj):
    #
    #     if obj.group.name == 'Region Supervisor' or obj.group.name == 'Region Reviewer':
    #         return None
    #
    #     elif obj.group.name == 'Project Manager' or obj.group.name == 'Project Donor' or obj.group.name == 'Staff Project Manager':
    #         return obj.project.address
    #
    #     elif obj.group.name == 'Site Supervisor' or obj.group.name == 'Site Reviewer':
    #         return obj.site.address
    #
    #     elif obj.group.name == 'Organization Admin':
    #         return obj.organization.address


class UserInvitationSerializer(serializers.ModelSerializer):
    group = serializers.SerializerMethodField(read_only=True)
    by_user = serializers.CharField(source='by_user.username', read_only=True)
    current_user = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = UserInvite
        fields = ('id', 'by_user', 'group', 'current_user')

    def get_current_user(self, obj):
        request = self.context.get('request')
        return request.user.username

    def get_group(self, obj):
        if obj.group.name == 'Organization Admin':
            group = 'Team Admin'

        elif obj.group.name == 'Super Organization Admin':
            group = 'Organization Admin'

        else:
            group = obj.group.name

        return group


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


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)