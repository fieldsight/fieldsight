import json
from django.contrib.auth.models import Group
from django.db import transaction
from fcm.utils import get_device_model
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, BasePermission

from channels import Group as ChannelGroup
from onadata.apps.fieldsight.mixins import USURPERS
from onadata.apps.fieldsight.models import Site, Project, Organization, SuperOrganization
from onadata.apps.userrole.serializers.UserRoleSerializer import UserRoleSerializer
from onadata.apps.fieldsight.serializers.ProjectSerializer import ProjectTypeSerializer
from onadata.apps.fieldsight.serializers.SiteSerializer import SiteSerializer, ProjectSiteListSerializer
from onadata.apps.fieldsight.serializers.OrganizationSerializer import OrganizationSerializer
from onadata.apps.userrole.models import UserRole
from django.db.models import Q
from django.views.generic import View
from django.http import HttpResponse
from rest_framework.pagination import PageNumberPagination

SAFE_METHODS = ('GET', 'POST')


class ManagePeoplePermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.role.group.name == "Super Admin":
            return True
        if not request.role.group.name in USURPERS['Reviewer']:
            return False
        return request.role.organization == obj.organization


class DonorRoleViewSet(viewsets.ModelViewSet):
    queryset = UserRole.objects.filter(organization__isnull=False, ended_at__isnull=True)
    serializer_class = UserRoleSerializer
    permission_classes = (IsAuthenticated, ManagePeoplePermission)

    def filter_queryset(self, queryset):
        try:
            pk = self.kwargs.get('pk', None)   
            queryset = queryset.filter(project__id=pk, group__name="Project Donor", ended_at__isnull=True)
        except:
            queryset = []
        return queryset


class UserRoleViewSet(viewsets.ModelViewSet):
    queryset = UserRole.objects.filter(organization__isnull=False, ended_at__isnull=True)
    serializer_class = UserRoleSerializer
    permission_classes = (IsAuthenticated, ManagePeoplePermission)

    def filter_queryset(self, queryset):
        try:
            level = self.kwargs.get('level', None)
            pk = self.kwargs.get('pk', None)
            if level == "0":
                queryset = queryset.filter(site__id=pk,  ended_at__isnull=True,
                                           group__name__in=['Site Supervisor', 'Reviewer'])
            elif level == "1":
                queryset = queryset.filter(project__id=pk, group__name='Project Manager',
                                           ended_at__isnull=True).distinct('user_id')
            elif level == "2":
                queryset = queryset.filter(organization__id=pk, group__name='Organization Admin',
                                           ended_at__isnull=True).distinct('user_id')

            elif level == "3":
                queryset = UserRole.objects.filter(super_organization__id=pk, group__name='Super Organization Admin',
                                                   ended_at__isnull=True).distinct('user_id')
        except:
            queryset = []
        return queryset

    def custom_create(self, *args, **kwargs):
        data = self.request.data
       
        level = self.kwargs.get('level')

        with transaction.atomic():
            group = Group.objects.get(name=data.get('group'))

            for user in data.get('users'):
                if level == "0":

                    site = Site.objects.get(pk=self.kwargs.get('pk'))

                    role, created = UserRole.objects.get_or_create(user_id=user, site_id=site.id,
                                                                   project__id=site.project.id,
                                                                   organization__id=site.project.organization_id,
                                                                   group=group, ended_at=None)

                    if created:
                        description = "{0} was assigned  as {1} in {2}".format(
                            role.user.get_full_name(), role.group.name, role.project)
                        noti_type = 8

                        if data.get('group') == "Reviewer":
                            noti_type =7
                        
                        noti = role.logs.create(source=role.user, type=noti_type, title=description,
                                                description=description, content_object=site, site=site,
                                                project=site.project, organization=site.project.organization,
                                                extra_object=self.request.user)

                elif level == "1":

                    project = Project.objects.get(pk=self.kwargs.get('pk'))
                    role, created = UserRole.objects.get_or_create(user_id=user,
                                                                   organization_id=project.organization_id,
                                                                   project_id=self.kwargs.get('pk'), site_id=None,
                                                                   group=group, ended_at=None)

                    if created:
                        
                        description = "{0} was assigned  as {2} in {1}".format(
                            role.user.get_full_name(), role.project, role.group.name)
                        
                        noti_type = 6
                        if data.get('group') == "Project Donor":
                            noti_type =25

                        noti = role.logs.create(source=role.user, type=noti_type, title=description,
                                                organization=project.organization, project=project,
                                                description=description, content_object=project,
                                                extra_object=self.request.user)

                        result = {}
                        result['description'] = description
                        result['url'] = noti.get_absolute_url()
                        ChannelGroup("notify-{}".format(role.organization.id)).send({"text": json.dumps(result)})
                        ChannelGroup("project-{}".format(role.project.id)).send({"text": json.dumps(result)})
                        ChannelGroup("notify-0").send({"text": json.dumps(result)})

                elif level == "2":
                    organization = Organization.objects.get(pk=self.kwargs.get('pk'))
                    role, created = UserRole.objects.get_or_create(user_id=user,
                                                                   organization_id=self.kwargs.get('pk'),
                                                                   project_id=None, site_id=None, group=group)
                    if created:
                        description = "{0} was assigned  as Team Admin in {1}".format(
                            role.user.get_full_name(), role.organization)
                        noti = role.logs.create(source=role.user, type=5, title=description,
                                                organization=organization, description=description,
                                                content_object=organization, extra_object=self.request.user)
                        result = {}
                        result['description'] = description
                        result['url'] = noti.get_absolute_url()
                        ChannelGroup("notify-{}".format(role.organization.id)).send({"text": json.dumps(result)})
                        ChannelGroup("notify-0").send({"text": json.dumps(result)})
                    else:
                        role.ended_at = None
                        role.save()

                elif level == "3":
                    super_organization = SuperOrganization.objects.get(pk=self.kwargs.get('pk'))
                    role, created = UserRole.objects.get_or_create(user_id=user,
                                                                   super_organization_id=self.kwargs.get('pk'),
                                                                   organization_id=None,
                                                                   project_id=None, site_id=None, group=group)
                    if created:
                        description = "{0} was assigned  as Super Organization Admin in {1}".format(
                            role.user.get_full_name(), role.super_organization)
                        noti = role.logs.create(source=role.user, type=5, title=description,
                                                super_organization=super_organization, description=description,
                                                content_object=super_organization, extra_object=self.request.user)
                        result = {}
                        result['description'] = description
                        result['url'] = noti.get_absolute_url()
                        ChannelGroup("notify-{}".format(role.super_organization.id)).send({"text": json.dumps(result)})
                        ChannelGroup("notify-0").send({"text": json.dumps(result)})
                    else:
                        role.ended_at = None
                        role.save()

        return Response({'msg': data}, status=status.HTTP_200_OK)

    def all_notification(user, message):
        ChannelGroup("%s" % user).send({
            "text": json.dumps({
                "msg": message
            })
        })


class MultiUserAssignRoleViewSet(View):
    def get(self, * args, **kwargs):
        return HttpResponse('Get Request Not Allowed.')

    def post(self, * args, **kwargs):
        queryset = UserRole.objects.filter(organization__isnull=False, ended_at__isnull=True)
        data = self.request.data
        level = self.kwargs.get('level')
        try:
            with transaction.atomic():
                group = Group.objects.get(name=data.get('group'))
                if level == "0":
                    for site_id in data.get('sites'):
                        site = Site.objects.get(pk=site_id)
                        for user in data.get('users'):
                            role, created = UserRole.objects.get_or_create(user_id=user, site_id=site.id,
                                                                           project__id=site.project.id, organization_id=site.project.organization.id, group=group)
                            if created:
                                description = "{0} was assigned  as {1} in {2}".format(
                                    role.user.get_full_name(), role.lgroup.name, role.project)
                                noti_type = 8

                                if data.get('group') == "Reviewer":
                                    noti_type =7
                                
                                noti = role.logs.create(source=role.user, type=noti_type, title=description,
                                                        description=description, content_type=site, extra_object=self.request.user,
                                                        site=role.site)
                                # result = {}
                                # result['description'] = description
                                # result['url'] = noti.get_absolute_url()
                                # ChannelGroup("notify-{}".format(role.organization.id)).send({"text": json.dumps(result)})
                                # ChannelGroup("project-{}".format(role.project.id)).send({"text": json.dumps(result)})
                                # ChannelGroup("site-{}".format(role.site.id)).send({"text": json.dumps(result)})
                                # ChannelGroup("notify-0").send({"text": json.dumps(result)})

                            # Device = get_device_model()
                            # if Device.objects.filter(name=role.user.email).exists():
                            #     message = {'notify_type':'Assign Site', 'site':{'name': site.name, 'id': site.id}}
                            #     Device.objects.filter(name=role.user.email).send_message(message)

                elif level == "1":
                    for project_id in data.get('projects'):
                        project = Project.objects.get(pk=project_id)
                        for user in data.get('users'):
                            role, created = UserRole.objects.get_or_create(user_id=user, project_id=project_id,
                                                                           organization__id=project.organization.id,
                                                                           group=group)
                            if created:
                                description = "{0} was assigned  as Project Manager in {1}".format(
                                    role.user.get_full_name(), role.project)
                                noti = role.logs.create(source=role.user, type=6, title=description, description=description,
                                 content_type=project, extra_object=self.request.user)
                                result = {}
                                result['description'] = description
                                result['url'] = noti.get_absolute_url()
                                ChannelGroup("notify-{}".format(role.organization.id)).send({"text": json.dumps(result)})
                                ChannelGroup("project-{}".format(role.project.id)).send({"text": json.dumps(result)})
                                ChannelGroup("notify-0").send({"text": json.dumps(result)})

                elif level == "2":
                    for organization_id in data.get('organizations'):
                        organization = Organization.objects.get(pk=organization_id)
                        for user in data.get('users'):
                            role, created = UserRole.objects.get_or_create(user_id=user, organization_id=project_id,
                                                                           group=group)
                            if created:
                                description = "{0} was assigned  as Team Admin in {1}".format(
                                    role.user.get_full_name(), role.project)
                                noti = role.logs.create(source=role.user, type=7, title=description, description=description,
                                 content_type=organization, extra_object=self.request.user)
                                result = {}
                                result['description'] = description
                                result['url'] = noti.get_absolute_url()
                                ChannelGroup("notify-{}".format(role.organization.id)).send({"text": json.dumps(result)})
                                ChannelGroup("project-{}".format(role.project.id)).send({"text": json.dumps(result)})
                                ChannelGroup("notify-0").send({"text": json.dumps(result)})

        except Exception as e:
            raise ValidationError({
                "User Creation Failed ".format(str(e)),
            })
        return Response({'msg': 'ok'}, status=status.HTTP_200_OK)

class LargeResultsSetPagination(PageNumberPagination):
    page_size = 2


class MultiUserlistViewSet(viewsets.ModelViewSet):
    serializer_class = UserRoleSerializer
    permission_classes = (IsAuthenticated, ManagePeoplePermission)
    # pagination_class = LargeResultsSetPagination
    def get_queryset(self):
        queryset = UserRole.objects.filter(organization__isnull=False)
        level = self.kwargs.get('level', None)
        pk = self.kwargs.get('pk', None)
        if level == "0":
            try:
                site = Site.objects.get(pk=pk)
            except Exception as e:
                raise ValidationError({
                    "No such site exists ".format(str(e)),
                })
            queryset = queryset.filter(organization__id=site.project.organization_id, ended_at__isnull=True).distinct('user_id')
        elif level == "1":
            try:
                project = Project.objects.get(pk=pk)
            except Exception as e:
                raise ValidationError({
                    "No such project exists ".format(str(e)),
                })
            queryset = queryset.filter(organization__id=project.organization_id, ended_at__isnull=True).distinct('user_id')
        elif level == "2":
            try:
                organization = Organization.objects.get(pk=pk)
            except Exception as e:
                raise ValidationError({
                    "No such Team exists ".format(str(e)),
                })
            queryset = queryset.filter(organization__id=organization.id, ended_at__isnull=True).distinct('user_id')

        elif level == "3":
            try:
                super_organization = SuperOrganization.objects.get(pk=pk)
            except Exception as e:
                raise ValidationError({
                    "No such Super Organization exists ".format(str(e)),
                })
            team_ids = Organization.objects.filter(parent=super_organization).values_list('id', flat=True)
            queryset = UserRole.objects.filter(organization_id__in=team_ids, ended_at__isnull=True).distinct('user_id')

        return queryset


class MultiOPSlistViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, ManagePeoplePermission)
    # pagination_class = LargeResultsSetPagination

    def get_serializer_class(self):
        if self.kwargs.get('level') == "0":
            # return SiteSerializer

            return ProjectSiteListSerializer

        elif self.kwargs.get('level') == "1":
            return ProjectTypeSerializer

        elif self.kwargs.get('level') == "2":
            return OrganizationSerializer
        else:
            return ProjectTypeSerializer

    def get_queryset(self):
    
        level = self.kwargs.get('level', None)
        pk = self.kwargs.get('pk', None)
        if level == "0":

            queryset = Site.objects.filter(project__id=pk).select_related('project', 'region', 'type')

        elif level == "1":
            queryset = Project.objects.filter(organization__id=pk)

        elif level == "2":
            queryset = Organization.objects.filter(parent_id=pk)

        return queryset
    