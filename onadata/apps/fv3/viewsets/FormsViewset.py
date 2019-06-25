import json

from rest_framework import viewsets, status
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db import models, IntegrityError, transaction
from django.conf import settings

from onadata.apps.fieldsight.models import Project, Organization
from onadata.apps.fsforms.models import FieldSightXF, ObjectPermission, Asset, DeletedXForm
from onadata.apps.fv3.serializers.FormSerializer import XFormSerializer, ShareFormSerializer, \
    ShareProjectFormSerializer, ShareTeamFormSerializer, ShareGlobalFormSerializer, \
    AddLanguageSerializer, CloneFormSerializer, ProjectFormSerializer, MyFormDeleteSerializer, \
    ShareUserListSerializer, ShareTeamListSerializer
from onadata.apps.logger.models import XForm
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from onadata.apps.userrole.models import UserRole
from onadata.apps.eventlog.models import CeleryTaskProgress
from onadata.apps.fv3.permissions.xform import XFormSharePermission, XFormDeletePermission, XFormEditPermission
from onadata.apps.fsforms.enketo_utils import CsrfExemptSessionAuthentication


class MyFormsViewSet(viewsets.ReadOnlyModelViewSet):
    """
        A simple ViewSet for viewing myforms.
        """
    authentication_classes = ([SessionAuthentication,BasicAuthentication])
    queryset = XForm.objects.all()
    serializer_class = XFormSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user, deleted_xform=None)


class ShareUserListViewSet(viewsets.ReadOnlyModelViewSet):
    """
        A ViewSet for getting the list of shareable users for sharing form
        """
    authentication_classes = ([SessionAuthentication, BasicAuthentication])
    queryset = User.objects.all()
    serializer_class = ShareUserListSerializer

    def get_queryset(self):
        projects = self.request.roles.filter(
            ended_at__isnull=True).values_list("project", flat=True).order_by('project').distinct()
        return self.queryset.filter(user_roles__project_id__in=projects).distinct()


class ShareTeamListViewSet(viewsets.ReadOnlyModelViewSet):
    """
            A ViewSet for getting the list of shareable team for sharing form
            """
    authentication_classes = ([SessionAuthentication, BasicAuthentication])
    queryset = Organization.objects.all()
    serializer_class = ShareTeamListSerializer

    def get_queryset(self):
        teams = self.request.roles.filter(
            ended_at__isnull=True, group__name="Organization Admin").values_list(
            "organization", flat=True)
        return self.queryset.filter(id__in=teams).distinct()


class MyProjectFormsViewSet(viewsets.ReadOnlyModelViewSet):
    """
        A simple ViewSet for viewing my  project forms.
        forms assigned in my project is project forms
        """
    authentication_classes = ([SessionAuthentication,BasicAuthentication])
    queryset = Project.objects.all()
    serializer_class = ProjectFormSerializer

    def get_queryset(self):
        projects = self.request.roles.filter(
            ended_at__isnull=True).values_list("project", flat=True).order_by('project').distinct()
        organizations = self.request.roles.filter(
            ended_at__isnull=True, group__name="Organization Admin").values_list(
            "organization", flat=True)
        admin_projects = Project.objects.filter(organization__pk__in=organizations).values_list("pk", flat=True)
        projects = [p for p in projects] + [p for p in admin_projects]
        projects = Project.objects.filter(id__in=projects).order_by('id')
        return projects


class ShareFormViewSet(APIView):
    """
        A ViewSet for sharing the form to users
        """
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, XFormSharePermission)

    def post(self, request, **kwargs):
        serializer = ShareFormSerializer(data=request.data)
        if serializer.is_valid(raise_exception=False):

            xf = XForm.objects.get(id_string=request.data['id_string'])
            self.check_object_permissions(request, xf)

            task_obj = CeleryTaskProgress.objects.create(user=request.user,
                                                         description="Share Forms Individual",
                                                         task_type=19, content_object=xf)
            if task_obj:
                from onadata.apps.fsforms.tasks import api_share_form
                try:
                    with transaction.atomic():

                        api_share_form.delay(xf.id, request.data['users'], task_obj.id)
                except IntegrityError:
                    pass
            return Response({"message": "Form shared successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ShareProjectFormViewSet(APIView):
    """
        A ViewSet for sharing a form to the project managers of a project and the organization admin
        """

    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, XFormSharePermission)

    def post(self, request, **kwargs):
        serializer = ShareProjectFormSerializer(data=request.data)
        if serializer.is_valid(raise_exception=False):
            xf = XForm.objects.get(id_string=request.data['id_string'])
            self.check_object_permissions(request, xf)

            task_obj = CeleryTaskProgress.objects.create(user=request.user,
                                                         description="Share Forms Project Manager and Admin",
                                                         task_type=20, content_object=xf)
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
                        api_share_form.delay(xf.id, user_ids, task_obj.id)
                except IntegrityError:
                    pass
            return Response({"message": "Form shared successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ShareTeamFormViewSet(APIView):
    """
        A ViewSet for sharing a form to all the team members(project managers and organization admin)
        """

    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, XFormSharePermission)

    def post(self, request, **kwargs):
        serializer = ShareTeamFormSerializer(data=request.data)
        if serializer.is_valid(raise_exception=False):

            xf = XForm.objects.get(id_string=request.data['id_string'])
            self.check_object_permissions(request, xf)
            task_obj = CeleryTaskProgress.objects.create(user=request.user, description="Share XForm to Team",
                                                         task_type=21, content_object=xf)
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
                        api_share_form.delay(xf.id, user_ids, task_obj.id)
                except IntegrityError:
                    pass
            return Response({"message": "Form shared successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ShareGlobalFormViewSet(APIView):
    """
        A ViewSet for sharing a form globally
        """

    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, XFormSharePermission)

    def post(self, request, **kwargs):
        serializer = ShareGlobalFormSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        xf = XForm.objects.get(id_string=request.data['id_string'])
        self.check_object_permissions(request, xf)

        from onadata.apps.fsforms.share_xform import share_form_global
        shared = share_form_global(xf)
        if shared:
            return Response({"message": "Form shared successfully",
                             'share_link': settings.KPI_URL + '#/forms/' + xf.id_string},
                            status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CloneFormViewSet(APIView):
    """
        A ViewSet for cloning a form
        """
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, )

    def post(self, request, **kwargs):
        serializer = CloneFormSerializer(data=request.data)
        if serializer.is_valid():
            xf = XForm.objects.get(id_string=request.data['id_string'])
            project = Project.objects.get(id=request.data['project'])
            task_obj = CeleryTaskProgress.objects.create(user=request.user, description="Clone Form",
                                                         task_type=22, content_object=xf)
            if task_obj:
                from onadata.apps.fsforms.tasks import api_clone_form
                api_clone_form.delay(xf.id, project.id, request.user.id, task_obj.id)
                return Response({"message": "Form cloned successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
       

class FormAddLanguageViewSet(APIView):
    """
        A ViewSet for adding languages to a form
        """
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, XFormSharePermission)

    def post(self, request, *args,  **kwargs):
        serializer = AddLanguageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        xf = XForm.objects.get(id_string=request.data['id_string'])
        self.check_object_permissions(request, xf)
        a = Asset.objects.get(uid=xf.id_string)
        translation = u'' + request.data['language'] + ' ' + '(' + request.data['code'] + ')'
        if 'translations' in a.content:
            a.content['translations'].append(translation)
            if 'survey' in a.content:
                sheet = a.content['survey']
                for row in sheet:
                    if 'label' in row:
                        row['label'].append(None)
            a.save()
            return Response({"message": "Language added successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "This form has no languages defined yet."}, status=status.HTTP_400_BAD_REQUEST)


class MyFormDeleteViewSet(APIView):
    """
        A ViewSet for deleting the xform from my forms
        """
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, XFormDeletePermission)

    def post(self, request, *args, **kwargs):
        serializer = MyFormDeleteSerializer(data=request.data)
        if serializer.is_valid(raise_exception=False):
            xf = XForm.objects.get(id_string=request.data['id_string'])
            self.check_object_permissions(request, xf)
            obj, created = DeletedXForm.objects.get_or_create(xf=xf)
            if obj or created:
                return Response({"message": "Form deleted successfully."}, status=status.HTTP_201_CREATED)
            else:
                return Response({"message": "Error occurred while deleting form"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


