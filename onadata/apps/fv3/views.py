import json
from datetime import datetime

from django.db.models import Prefetch
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework import generics, status
from rest_framework.permissions import BasePermission
from rest_framework.views import APIView
from django.http import JsonResponse
from onadata.apps.fieldsight.models import Project, Region, Site, Sector, SiteType, ProjectLevelTermsAndLabels
from onadata.apps.fieldsight.rolemixins import ProjectRoleMixin
from onadata.apps.fsforms.notifications import get_notifications_queryset
from onadata.apps.fv3.serializer import ProjectSerializer, SiteSerializer, ProjectUpdateSerializer, SectorSerializer, \
    SiteTypeSerializer, ProjectLevelTermsAndLabelsSerializer, ProjectRegionSerializer
from onadata.apps.userrole.models import UserRole
from onadata.apps.users.viewsets import ExtremeLargeJsonResultsSetPagination
from onadata.apps.fsforms.enketo_utils import CsrfExemptSessionAuthentication
from onadata.apps.fieldsight.tasks import UnassignAllProjectRolesAndSites
from onadata.apps.eventlog.models import CeleryTaskProgress
from onadata.apps.geo.models import GeoLayer
from .role_api_permissions import ProjectRoleApiPermissions


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def supervisor_projects(request):
    regions = UserRole.objects.filter(user=request.user,
                                     ended_at=None,
                                     group__name="Region Supervisor"
                                     ).values_list('region', flat=True)
    "Distinct Regions when a user is assigned."

    project_ids = UserRole.objects.filter(user=request.user,
                                      ended_at=None,
                                      group__name__in=["Region Supervisor", "Site Supervisor"]
                                      ).values_list('project', flat=True)
    "Projects where a user is assigned as Region Supervisor or Site Supervisor"

    projects = Project.objects.filter(pk__in=project_ids).select_related('organization').prefetch_related(
        Prefetch("project_region", queryset=Region.objects.filter(pk__in=regions)))
    "Distinct Projects Where a user can be site supervisor or region reviewer"

    site_supervisor_role = UserRole.objects.filter(user=request.user,
                                     ended_at=None,
                                     group__name="Site Supervisor"
                                     ).values_list('project', flat=True).order_by('project').distinct()

    "If a user is assigned as site supervisor in a given project."
    for p in projects:
        if p.id in site_supervisor_role:
            p.has_site_role = True
        else:
            p.has_site_role = False
    data = ProjectSerializer(projects, many=True).data
    return Response(data)


class MySuperviseSitesViewset(viewsets.ModelViewSet):
    serializer_class = SiteSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = ExtremeLargeJsonResultsSetPagination
    renderer_classes = [JSONRenderer]

    def get_queryset(self):
        query_params = self.request.query_params
        region_id = query_params.get('region_id')
        project_id = query_params.get('project_id')
        last_updated = query_params.get('last_updated')

        if region_id:  # Region Reviewer Roles
            sites = Site.all_objects.filter(region=region_id)
        elif project_id:  # Site Supervisor Roles
            sites = Site.all_objects.filter(project=project_id, site_roles__region__isnull=True,
                                        site_roles__group__name="Site Supervisor")
        else:
            sites = []
        if last_updated:
            try:
                last_updated_date = datetime.fromtimestamp(int(last_updated))#  Deleted and last updated sites.
                sites = sites.filter(date_modified__gte=last_updated_date)

            except:
                return []

        return sites


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def site_blueprints(request):
    query_params = request.query_params
    site_id = query_params.get('site_id')
    data = Site.objects.get(pk=site_id).blueprints.all()
    urls = [m.image.url for m in data]
    return Response({'blueprints': urls})


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def supervisor_logs(request):
    email = request.user.email
    date = None
    last_updated = request.query_params.get('last_updated')
    if last_updated:
        try:
            date = datetime.fromtimestamp(int(last_updated))  # notifications newer than this date.
        except:
            return Response({'notifications': []})
    notifications = get_notifications_queryset(email, date)
    return Response({'notifications': notifications})


class ProjectUpdateViewset(generics.RetrieveUpdateDestroyAPIView):
    """
    A simple ViewSet for viewing and editing project. Allowed methods 'get', 'put', 'delete'.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectUpdateSerializer
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    permission_classes = [IsAuthenticated, ProjectRoleApiPermissions, ]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        noti = instance.logs.create(source=self.request.user, type=14, title="Edit Project",
                                       organization=instance.organization,
                                       project=instance, content_object=instance,
                                       description='{0} changed the details of project named {1}'.format(
                                           self.request.user.get_full_name(), instance.name))
        return Response(serializer.data)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
        task_obj = CeleryTaskProgress.objects.create(user=self.request.user,
                                                     description="Removal of UserRoles After project delete",
                                                     task_type=7, content_object=instance)
        if task_obj:
            task = UnassignAllProjectRolesAndSites.delay(task_obj.id, instance.id)
            task_obj.task_id = task.id
            task_obj.save()

        noti = task_obj.logs.create(source=self.request.user, type=36, title="Delete Project",
                                    organization=instance.organization, extra_message="project",
                                    project=instance, content_object=instance, extra_object=instance.organization,
                                    description='{0} deleted of project named {1}'.format(
                                        self.request.user.get_full_name(), instance.name))


class sectors_subsectors(viewsets.ModelViewSet):
    """
    A simple ViewSet viewing setors and subsectors. Allowed methods 'get'.
    """
    queryset = Sector.objects.filter(sector=None)
    serializer_class = SectorSerializer
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def filter_queryset(self, queryset):
        sector_id = self.request.query_params.get('sector', None)
        if sector_id:
            return Sector.objects.filter(sector_id=sector_id)

        else:
            return queryset


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
            return self.queryset.filter(project=project)
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

    def get_queryset(self):

        project_id = self.request.query_params.get('project', None)
        region_id = self.request.query_params.get('region', None)

        if project_id and region_id:

            region = get_object_or_404(Region, id=region_id)
            project = get_object_or_404(Project, id=project_id)
            return self.queryset.filter(project=project, parent_id=region.id)

        elif project_id:
            project = get_object_or_404(Project, id=project_id)
            return self.queryset.filter(project=project)

        else:
            return self.queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=False)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        parent_exists = serializer.validated_data.get('parent', None)

        if parent_exists is not None:
            if serializer.validated_data['parent']:

                parent_identifier = serializer.validated_data['parent'].get_concat_identifier()
                new_identifier = parent_identifier + serializer.validated_data['identifier']
                serializer.save(identifier=new_identifier)
        else:

            serializer.save()


class RegionViewset(generics.RetrieveUpdateDestroyAPIView):
    """
    A simple ViewSet for viewing, editing and deleting region. Allowed methods 'get', 'put', 'delete'.
    """
    queryset = Region.objects.all()
    serializer_class = ProjectRegionSerializer
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)


class GeoLayerView(APIView):
    """
    A simple view for viewing organization geo layers and add geo-layers from project. Allowed methods 'get', 'post'.
    """
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    permission_classes = [IsAuthenticated, ProjectRoleApiPermissions, ]

    def get(self, request, format=None):

        project_id = request.query_params.get('project', None)
        project = get_object_or_404(Project, id=project_id)

        organization = project.organization
        data = GeoLayer.objects.filter(organization=organization).values('title')

        return Response(data)

    def post(self, request, format=None):
        project_id = request.query_params.get('project', None)
        project = get_object_or_404(Project, id=project_id)
        try:
            geo_layers = eval(request.data.get('geo_layers'))
            if geo_layers:
                try:
                    project.geo_layers.add(*geo_layers)

                    return Response(status=status.HTTP_201_CREATED)
                except Exception as e:
                    return Response(data='Error: ' + str(e), status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(data='Error: POST requires only geo_layers field.', status=status.HTTP_400_BAD_REQUEST)


class ProjectDefineSiteMeta(APIView):
    """
    A simple view for viewing and adding project site meta. Allowed methods 'get', 'post'.
    """
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    permission_classes = [IsAuthenticated, ]

    def get(self, request, pk, format=None):
        project_obj = Project.objects.get(pk=pk)
        level = "1"
        project_data = Project.objects.filter(pk=pk).values('id', 'name', 'organization_id', 'organization__name', )
        terms_and_labels = ProjectLevelTermsAndLabels.objects.filter(project=project_obj).exists()

        return Response({'json_questions': project_obj.site_meta_attributes, 'site_basic_info': project_obj.site_basic_info,
                         'site_featured_images': project_obj.site_featured_images, 'level': level,
                         'terms_and_labels': terms_and_labels, 'obj': project_data})

    def post(self, request, pk, format=None):

        # try:
        project = Project.objects.get(pk=pk)
        old_meta = project.site_meta_attributes
        # print old_meta===================================
        # print "----"
        project.site_meta_attributes = request.POST.get('json_questions');
        project.site_basic_info = request.POST.get('site_basic_info');
        project.site_featured_images = request.POST.get('site_featured_images');
        new_meta = json.loads(project.site_meta_attributes)
        try:
            if old_meta != new_meta:
                deleted = []

                for meta in old_meta:
                    if meta not in new_meta:
                        deleted.append(meta)

                for other_project in Project.objects.filter(organization_id=project.organization_id):

                    for meta in other_project.site_meta_attributes:

                        if meta['question_type'] == "Link":
                            if str(project.id) in meta['metas']:
                                for del_meta in deleted:
                                    if del_meta in meta['metas'][str(project.id)]:
                                        del meta['metas'][str(project.id)][meta['metas'][str(project.id)].index(del_meta)]

                    other_project.save()
            project.save()
            return Response({'message': "Successfully created", 'status': status.HTTP_201_CREATED})

        except Exception as e:
            return Response(data='Error: ' + str(e), status=status.HTTP_400_BAD_REQUEST)


