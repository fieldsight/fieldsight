from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication

from onadata.apps.fieldsight.models import ProgressSettings, Project, Region, SiteType, Site, ProjectLevelTermsAndLabels
from onadata.apps.fv3.permissions.project_settings import ProjectSettingsPermission
from onadata.apps.fsforms.enketo_utils import CsrfExemptSessionAuthentication
from onadata.apps.fv3.role_api_permissions import ProjectRoleApiPermissions
from onadata.apps.fv3.serializer import ProjectRegionSerializer, ProjectLevelTermsAndLabelsSerializer, \
    SiteTypeSerializer
from onadata.apps.fv3.serializers.project_settings import ProgressSettingsSerializer


class ProjectSettingsOptions(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        # self.has_object_permission(request, project)
        return Response(dict(ProgressSettings.CHOICES))


class ProjectProgressSettings(viewsets.ModelViewSet):
    queryset = ProgressSettings.objects.all()
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    permission_classes = [IsAuthenticated, ProjectSettingsPermission]
    serializer_class = ProgressSettingsSerializer

    def perform_create(self, serializer):
        ProgressSettings.objects.filter(project_id=self.kwargs['pk']).update(active=False)
        serializer.save(user=self.request.user, project_id=self.kwargs['pk'])

    def get_queryset(self):
        return self.queryset.filter(project_id=self.kwargs['pk'], active=True)


class ProjectTermsLabelsViewset(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing, creating, updating and deleting terms and labels. Allowed methods 'get', 'post', 'put',
    'delete'.
    """
    queryset = ProjectLevelTermsAndLabels.objects.filter(project__is_active=True)
    serializer_class = ProjectLevelTermsAndLabelsSerializer
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    permission_classes = [IsAuthenticated, ProjectRoleApiPermissions, ]

    def get_queryset(self):

        project_id = self.request.query_params.get('project', None)

        if project_id:
            project = get_object_or_404(Project, id=project_id)

            queryset = self.queryset.filter(project=project)

            if not ProjectLevelTermsAndLabels.objects.filter(project=project).exists():

               ProjectLevelTermsAndLabels.objects.create(project=project)

            return queryset
        else:
            return self.queryset


class ProjectRegionsViewset(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing, creating, updating and deleting regions. Allowed methods 'get', 'post', 'put', 'delete'.
    """
    queryset = Region.objects.all()
    serializer_class = ProjectRegionSerializer
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    permission_classes = [IsAuthenticated, ProjectRoleApiPermissions, ]

    def get_object(self):

        pk = self.kwargs.get('pk', None)
        obj = get_object_or_404(Region, pk=pk)
        self.check_object_permissions(self.request, obj)
        return obj

    def get_queryset(self):

        project_id = self.request.query_params.get('project', None)
        region_id = self.request.query_params.get('region', None)

        try:
            project = Project.objects.get(id=project_id)
        except :
            return Region.objects.all().none

        if project_id and region_id:

            region = get_object_or_404(Region, id=region_id)
            project = project
            return self.queryset.filter(project=project, parent_id=region.id)

        elif project_id:
            project = project
            return self.queryset.filter(project=project, parent=None)

        else:
            return self.queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        valid = serializer.is_valid(raise_exception=False)
        if valid:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:

            project_id = serializer.data.get('project')
            # parent_identifier = Region.objects.get(pk=self.kwargs.get('parent_pk')).get_concat_identifier()
            # form.cleaned_data['identifier'] = parent_identifier + form.cleaned_data.get('identifier')

            existing_identifier = Region.objects.filter(identifier=serializer.data.get('identifier'),
                                                        project_id=project_id)

            if existing_identifier:
                return Response({'status': status.HTTP_400_BAD_REQUEST,
                                 'message': 'Your identifier conflict with existing region please use different '
                                            'identifier to create region'})

    def perform_create(self, serializer):
        parent_exists = serializer.validated_data.get('parent', None)

        if parent_exists is not None:
            if serializer.validated_data['parent']:

                parent_identifier = serializer.validated_data['parent'].get_concat_identifier()
                new_identifier = parent_identifier + serializer.validated_data['identifier']
                serializer.save(identifier=new_identifier)
        else:

            serializer.save()

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            site = Site.objects.filter(region=instance)
            site.update(region_id=None)
            self.perform_destroy(instance)
            return Response(status=status.HTTP_200_OK)
        except Http404:
            return Response(status=status.HTTP_204_NO_CONTENT)


class ProjectSiteTypesViewset(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and creating site types of project. Allowed methods 'get', 'post', 'put', 'delete'.
    """
    queryset = SiteType.objects.all()
    serializer_class = SiteTypeSerializer
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    permission_classes = [IsAuthenticated, ProjectRoleApiPermissions, ]

    def get_queryset(self):

        project_id = self.request.query_params.get('project', None)
        if project_id:
            project = get_object_or_404(Project, id=project_id)
            return self.queryset.filter(project=project)
        else:
            return self.queryset
