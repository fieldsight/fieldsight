from rest_framework import viewsets, status
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db import models, IntegrityError, transaction

from onadata.apps.fieldsight.models import Project
from onadata.apps.fsforms.models import FieldSightXF, ObjectPermission, Asset
from onadata.apps.fv3.serializers.FormSerializer import XFormSerializer, ShareFormSerializer, \
    ShareProjectFormSerializer, ShareTeamFormSerializer
from onadata.apps.logger.models import XForm
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from onadata.apps.userrole.models import UserRole
from onadata.apps.eventlog.models import CeleryTaskProgress
from onadata.apps.fv3.permissions.xform import XFormSharePermission


class MyFormsViewSet(viewsets.ReadOnlyModelViewSet):
    """
        A simple ViewSet for viewing myforms.
        """
    authentication_classes = ([SessionAuthentication,BasicAuthentication])
    queryset = XForm.objects.all()
    serializer_class = XFormSerializer

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


class MyProjectFormsViewSet(viewsets.ReadOnlyModelViewSet):
    """
        A simple ViewSet for viewing my  project forms.
        forms assigned in my project is project forms
        """
    authentication_classes = ([SessionAuthentication,BasicAuthentication])
    queryset = XForm.objects.all()
    serializer_class = XFormSerializer

    def get_queryset(self):
        projects = self.request.roles.filter(
            ended_at__isnull=True).values_list("project", flat=True).order_by('project').distinct()
        organizations = self.request.roles.filter(
            ended_at__isnull=True, group__name="Organization Admin").values_list(
            "organization", flat=True)
        admin_projects = Project.objects.filter(organization__pk__in=organizations).values_list("pk", flat=True)
        projects = [p for p in projects] + [p for p in admin_projects]
        fieldsight_forms = FieldSightXF.objects.filter(
            project__in=projects).exclude(xf__user=self.request.user).order_by("xf").distinct()
        results = [f.xf for f in fieldsight_forms]
        return results


class ShareFormViewSet(APIView):
    """
        A ViewSet for sharing the form to users
        """
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = [IsAuthenticated, XFormSharePermission]

    def get_queryset(self):
        return ObjectPermission.objects.filter()

    def post(self, request, **kwargs):
        serializer = ShareFormSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        fxf = FieldSightXF.objects.get(pk=kwargs.get('pk'))
        task_obj = CeleryTaskProgress.objects.create(user=request.user,
                                                     description="Share Forms Individual",
                                                     task_type=19, content_object=fxf)
        if task_obj:
            from onadata.apps.fsforms.tasks import api_share_form
            try:
                with transaction.atomic():
                    api_share_form.delay(fxf.id, request.data['user_ids'], task_obj.id)
            except IntegrityError:
                pass
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ShareProjectFormViewSet(APIView):
    """
        A ViewSet for sharing a form to the project managers of a project and the organization admin
        """

    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, XFormSharePermission)

    def post(self, request, **kwargs):
        serializer = ShareProjectFormSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        fxf = FieldSightXF.objects.get(pk=kwargs.get('pk'))
        task_obj = CeleryTaskProgress.objects.create(user=request.user,
                                                     description="Share Forms Project Manager and Admin",
                                                     task_type=20, content_object=fxf)
        if task_obj:
            from onadata.apps.fsforms.tasks import api_share_form
            try:
                with transaction.atomic():
                    project = Project.objects.get(id=request.data['project'])
                    userrole = UserRole.objects.filter(project=project,
                                                       group__name__in=["Project Manager", "Organization Admin"],
                                                       organization=project.organization,
                                                       ended_at__isnull=True)
                    users = User.objects.filter(user_roles__in=userrole)
                    user_ids = []
                    for item in users:
                        user_ids.append(item.id)
                    api_share_form.delay(fxf.id, user_ids, task_obj.id)
            except IntegrityError:
                pass
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ShareTeamFormViewSet(APIView):
    """
        A ViewSet for sharing a form to all the team members(project managers and organization admin)
        """

    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, XFormSharePermission)

    def post(self, request, **kwargs):
        serializer = ShareTeamFormSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        fxf = FieldSightXF.objects.get(pk=kwargs.get('pk'))
        task_obj = CeleryTaskProgress.objects.create(user=request.user, description="Share XForm to Team",
                                                     task_type=21, content_object=fxf)
        if task_obj:
            from onadata.apps.fsforms.tasks import api_share_form
            try:
                with transaction.atomic():
                    userrole = UserRole.objects.filter(organization_id=request.data['team'],
                                                       group__name__in=["Project Manager", "Organization Admin"],
                                                       ended_at__isnull=True)
                    users = User.objects.filter(user_roles__in=userrole)
                    user_ids = []
                    for item in users:
                        user_ids.append(item.id)
                    api_share_form.delay(fxf.id, user_ids, task_obj.id)
            except IntegrityError:
                pass
        return Response(serializer.data, status=status.HTTP_201_CREATED)



