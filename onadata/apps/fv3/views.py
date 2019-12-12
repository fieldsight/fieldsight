import json
from datetime import datetime
import pandas as pd
from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers import serialize
from django.db.models import Prefetch, Q, Count
from django.http import Http404, JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.db import connection
from django.contrib.auth.models import User, Group

from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework import generics, status
from rest_framework.views import APIView
from django.contrib.gis.geos import Point
from onadata.apps.fieldsight.models import Project, Region, Site, Sector, SiteType, ProjectLevelTermsAndLabels, \
    ProjectMetaAttrHistory, Organization
from onadata.apps.fsforms.models import FInstance, ProgressSettings, Stage
from onadata.apps.fsforms.tasks import clone_form

from onadata.apps.fsforms.notifications import get_notifications_queryset
from onadata.apps.fv3.serializer import ProjectSerializer, SiteSerializer, ProjectUpdateSerializer, SectorSerializer, \
    ProjectRegionSerializer, ProjectSitesSerializer
from onadata.apps.fv3.util import get_user_roles
from onadata.apps.fv3.viewsets.ProjectSitesListViewset import ProjectsitesPagination
from onadata.apps.logger.models import Instance
from onadata.apps.subscriptions.models import Package, Customer, Subscription
from onadata.apps.userrole.models import UserRole
from onadata.apps.users.viewsets import ExtremeLargeJsonResultsSetPagination, MySitesOnlyResultsSetPagination

from onadata.apps.fieldsight.tasks import UnassignAllProjectRolesAndSites, UnassignAllSiteRoles, \
    create_site_meta_attribs_ans_history, email_after_subscribed_plan
from onadata.apps.fsforms.enketo_utils import CsrfExemptSessionAuthentication
from onadata.apps.fieldsight.tasks import UnassignAllProjectRolesAndSites, UnassignAllSiteRoles, \
    create_site_meta_attribs_ans_history, update_sites_info
from onadata.apps.eventlog.models import CeleryTaskProgress
from onadata.apps.geo.models import GeoLayer
from onadata.apps.fv3.serializers.ProjectSitesListSerializer import ProjectSitesListSerializer
from .role_api_permissions import ProjectRoleApiPermissions, RegionalPermission, check_regional_perm, \
    check_site_permission, SuperUserPermissions, TeamCreationPermission
from .serializer import TeamSerializer
from onadata.apps.fsforms.enketo_utils import CsrfExemptSessionAuthentication


class ProjectSitesPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'


class TeamsPagination(PageNumberPagination):
    page_size = 200
    page_size_query_param = 'page_size'
    max_page_size = 1000


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
                                      ).values_list('project',
                                                    flat=True).distinct()
    "Projects where a user is assigned as Region Supervisor or Site Supervisor"

    projects = Project.objects.filter(pk__in=project_ids).select_related('organization').prefetch_related(
        Prefetch("project_region", queryset=Region.objects.filter(pk__in=regions)),
        Prefetch("types", queryset=SiteType.objects.filter(deleted=False)),

    )
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
            sites = Site.objects.filter(Q(region=region_id) | Q(
                region_id__parent=region_id) | Q(region_id__parent__parent=region_id))
        elif project_id:  # Site Supervisor Roles
            sites = Site.objects.filter(project=project_id).filter(Q(
                site_roles__group__name="Site Supervisor",
                site_roles__ended_at__isnull=True,
                site_roles__user=self.request.user) | Q(
                site__site_roles__group__name="Site Supervisor",
                site__site_roles__ended_at__isnull=True,
                site__site_roles__user=self.request.user)).order_by(
                'id').distinct('id')

        else:
            sites = []
        if last_updated:
            try:
                last_updated_date = datetime.fromtimestamp(int(last_updated))#  Deleted and last updated sites.
                sites = sites.filter(date_modified__gte=last_updated_date)

            except:
                return []

        return sites

    def get_serializer_context(self):
        return {'parent_region': self.request.query_params.get('region_id')}


class MySuperviseSitesViewsetV4(viewsets.ModelViewSet):
    serializer_class = SiteSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = MySitesOnlyResultsSetPagination
    renderer_classes = [JSONRenderer]

    def get_queryset(self):
        query_params = self.request.query_params
        region_id = query_params.get('region_id')
        project_id = query_params.get('project_id')
        last_updated = query_params.get('last_updated')

        if region_id:  # Region Reviewer Roles
            sites = Site.objects.filter(Q(region=region_id) | Q(
                region_id__parent=region_id) | Q(region_id__parent__parent=region_id))
        elif project_id:  # Site Supervisor Roles
            sites = Site.objects.filter(project=project_id).filter(Q(
                site_roles__group__name="Site Supervisor",
                site_roles__ended_at__isnull=True,
                site_roles__user=self.request.user) | Q(
                site__site_roles__group__name="Site Supervisor",
                site__site_roles__ended_at__isnull=True,
                site__site_roles__user=self.request.user)).order_by(
                'id').distinct('id')

        else:
            sites = []
        if last_updated:
            try:
                last_updated_date = datetime.fromtimestamp(int(last_updated))#  Deleted and last updated sites.
                sites = sites.filter(date_modified__gte=last_updated_date)

            except:
                return []
        return sites

    def list(self, request, *args, **kwargs):
        sites = self.filter_queryset(self.get_queryset())
        if not sites:
            return Response({})
        page = self.paginate_queryset(sites)
        pks = [o.pk for o in page]
        sites = Site.objects.filter(pk__in=pks)
        query_sites = sites.values('id', 'name', 'location', 'address', 'phone',
                                   'current_progress', 'identifier', 'type', 'type__name', 'region', 'project',
                                   'date_modified', 'is_active', 'site_meta_attributes_ans',
                                   'enable_subsites', 'site')
        df_sites = pd.DataFrame(list(query_sites), columns=['id', 'name', 'location', 'address', 'phone',
                                                            'current_progress', 'identifier', 'type', 'type__name',
                                                            'region', 'project',
                                                            'date_modified', 'is_active', 'site_meta_attributes_ans',
                                                            'enable_subsites', 'site'])

        annos = sites.values('id').annotate(
            submissions=Count('site_instances')).annotate(
            users=Count('site_roles')).values('id', 'submissions', 'users')
        df = pd.DataFrame(list(annos), columns=["id", "submissions", "users"])
        ddf = df_sites.merge(df, on='id', how="left", sort=False)
        ddf['region_id'] = self.request.query_params.get('region_id')
        ddf['latitude'] = ddf.location.apply(
            lambda x: x.y if x else "")
        ddf['longitude'] = ddf.location.apply(
            lambda x: x.x if x else "")
        del ddf['location']
        ddf = ddf.replace('nan', '')
        data = ddf.to_dict(orient='records')
        if page is not None:
            return self.get_paginated_response(data)
        return Response(data)

    def get_serializer_context(self):
        return {'parent_region': self.request.query_params.get('region_id')}


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
    previous_next_type = request.query_params.get('type')
    if last_updated:
        try:
            date = datetime.fromtimestamp(int(last_updated))  # notifications newer than this date.
            print(date)
        except:
            return Response({'notifications': []})
    notifications = get_notifications_queryset(email, date, previous_next_type)
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
        logo_url = serializer.initial_data['logo']
        if logo_url.endswith('.jpg') or logo_url.endswith('.png'):
            serializer.initial_data.pop('logo')

        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        long = request.data.get('longitude', None)
        lat = request.data.get('latitude', None)
        if lat and long is not None:
            p = Point(round(float(long), 6), round(float(lat), 6), srid=4326)
            instance.location = p
            instance.save()
        instance.logs.create(source=self.request.user, type=14, title="Edit Project",
                                       organization=instance.organization,
                                       project=instance, content_object=instance,
                                       description=u"{0} changed the details of project named {1}".format(
                                           self.request.user.get_full_name(),
                                           instance.name))
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
    # authentication_classes = (SessionAuthentication,)

    def filter_queryset(self, queryset):
        sector_id = self.request.query_params.get('sector', None)
        if sector_id:
            return Sector.objects.filter(sector_id=sector_id)

        else:
            return queryset


class ProjectSitesViewset(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing, creating, updating and deleting sites. Allowed methods 'get', 'post', 'put', 'delete'.
    """
    queryset = Site.objects.select_related('region', 'project', 'type')
    serializer_class = ProjectSitesSerializer
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = [IsAuthenticated, ProjectRoleApiPermissions, ]
    pagination_class = ProjectSitesPagination

    def get_queryset(self):

        project_id = self.request.query_params.get('project', None)

        if project_id:
            project = get_object_or_404(Project, id=project_id)
            return self.queryset.filter(project=project)

        else:
            return self.queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=False)
        self.object = self.perform_create(serializer)

        if isinstance(self.object, Site):

            long = request.POST.get('longitude', None)
            lat = request.POST.get('latitude', None)

            if lat and long is not None:
                p = Point(round(float(long), 6), round(float(lat), 6), srid=4326)
                self.object.location = p
                self.object.save()

            noti = self.object.logs.create(source=self.request.user, type=11, title="new Site",
                                           organization=self.object.project.organization,
                                           project=self.object.project, content_object=self.object,
                                           extra_object=self.object.project,
                                           description='{0} created a new site named {1} in {2}'.format(
                                               self.request.user.get_full_name(),
                                               self.object.name, self.object.project.name))
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(status=self.object.data['status'], data=self.object.data['message'])

    def perform_create(self, serializer):

        existing_identifier = Site.objects.filter(identifier=serializer.validated_data['identifier'],
                                                  project_id=self.request.query_params.get('project'))

        if existing_identifier:
            return Response({'status': status.HTTP_400_BAD_REQUEST,
                             'message': 'Your identifier conflict with existing site please use different identifier to create site.'})
        else:

            obj = serializer.save()
            return obj

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        long = request.POST.get('longitude', None)
        lat = request.POST.get('latitude', None)
        if lat and long is not None:
            p = Point(round(float(long), 6), round(float(lat), 6), srid=4326)
            instance.location = p
            instance.save()
        previous_identifier = instance.identifier
        old_meta = instance.site_meta_attributes_ans
        existing_identifier = Site.objects.filter(identifier=serializer.validated_data.get('identifier'),
                                                  project_id=instance.project_id)

        check_identifier = previous_identifier == serializer.validated_data.get('identifier')

        if not check_identifier and existing_identifier:
            return Response({'message': 'Your identifier ' + serializer.data['identifier'] +
                                        ' conflict with existing site please use different identifier to update site'})

        self.perform_update(serializer)
        self.object = instance
        new_meta = json.loads(self.object.site_meta_attributes_ans)

        extra_json = None
        if old_meta != new_meta:
            updated = {}
            meta_questions = instance.project.site_meta_attributes
            for question in meta_questions:
                key = question['question_name']
                label = question['question_text']
                if old_meta.get(key) != new_meta.get(key):
                    updated[key] = {'label': label, 'data': [old_meta.get(key, 'null'), new_meta.get(key, 'null')]}
            extra_json = updated

        description = '{0} changed the details of site named {1}'.format(
            self.request.user.get_full_name(), self.object.name
        )

        noti = self.object.logs.create(
            source=self.request.user, type=15, title="edit Site",
            organization=instance.project.organization,
            project=instance.project, content_object=instance,
            description=description,
            extra_json=extra_json,
        )

        return Response(status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.identifier = instance.identifier + str('_' + self.kwargs.get('pk'))
        instance.save()

        instances = instance.site_instances.all().values_list('instance', flat=True)

        Instance.objects.filter(id__in=instances).update(deleted_at=datetime.now())

        # update in mongo

        result = settings.MONGO_DB.instances.update({"_id": {"$in": list(instances)}},
                                                    {"$set": {'_deleted_at': datetime.now()}}, multi=True)

        FInstance.objects.filter(instance_id__in=instances).update(is_deleted=True)

        task_obj = CeleryTaskProgress.objects.create(user=self.request.user,
                                                     description="Removal of UserRoles After Site delete", task_type=7,
                                                     content_object=instance)

        if task_obj:
            task = UnassignAllSiteRoles.delay(task_obj.id, instance.id)
            task_obj.task_id = task.id
            task_obj.save()

        noti = task_obj.logs.create(source=self.request.user, type=36, title="Delete Site",
                                    organization=instance.project.organization, extra_object=instance.project,
                                    project=instance.project, extra_message="site", site=instance, content_object=instance,
                                    description='{0} deleted of site named {1}'.format(
                                        self.request.user.get_full_name(), instance.name))
    #


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
        print('userrr', self.request.user)

        project_id = request.query_params.get('project', None)

        if project_id:
            project = get_object_or_404(Project, id=project_id)

            data = project.geo_layers.all().values('id', 'title')

            return Response(data)
        else:
            return Response({'message': 'Project Id is required'}, status=status.HTTP_204_NO_CONTENT)

    def post(self, request, format=None):
        project_id = request.query_params.get('project', None)
        project = get_object_or_404(Project, id=project_id)
        try:
            geo_layers = eval(str(request.data.get('geo_layers')))
            previous_geo_layers = project.geo_layers.all().values_list('id', flat=True)

            if geo_layers:
                try:
                    project.geo_layers.remove(*previous_geo_layers)

                    project.geo_layers.add(*geo_layers)

                    return Response(status=status.HTTP_200_OK)
                except Exception as e:
                    return Response(data='Error: ' + str(e), status=status.HTTP_400_BAD_REQUEST)
            else:
                project.geo_layers.remove(*previous_geo_layers)
                return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data=str(e), status=status.HTTP_204_NO_CONTENT)


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def organization_geolayer(request):
    print('userrr', request.user)
    query_params = request.query_params
    project_id = query_params.get('project')
    if project_id:
        project = get_object_or_404(Project, id=project_id)
        organization = project.organization
        data = GeoLayer.objects.filter(organization=organization).values('title', 'id')
        return Response(data)
    else:
        return Response({'message': 'Project Id is required'}, status=status.HTTP_204_NO_CONTENT)


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def check_region(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if Project.objects.filter(id=project.id, cluster_sites=True).exists():

        return Response({'has_region': True})
    else:
        return Response({'has_region': False})


def check_site_info_changed(pk, old_site_basic_info, site_basic_info):
    location_changed = False
    picture_changed = False
    if site_basic_info:
        site_location = site_basic_info.get('site_location', {})
        site_picture = site_basic_info.get('site_picture', {})
        if old_site_basic_info:
            old_site_location = old_site_basic_info.get('site_location', {})
            old_site_picture = old_site_basic_info.get('site_picture', {})
            if old_site_location:
                form_id = old_site_location.get("form_id", None)
                question_name = old_site_location.get("question", {}).get("name")
                if form_id != site_location.get("form_id", None) or (
                        question_name != site_location.get("question", {}).get("name")):
                    location_changed = True
            else:
                location_changed = True

            if old_site_picture:
                form_id = old_site_picture.get("form_id", None)
                question_name = old_site_picture.get("question", {}).get("name")
                if form_id != site_picture.get("form_id", None) or (
                        question_name != site_picture.get("question", {}).get("name")):
                    picture_changed = True
            else:
                picture_changed = True
        else:
            location_changed = True
            picture_changed = True
    if location_changed or picture_changed:
        location_form = site_basic_info.get('site_location', {}).get('form_id', 0)
        location_question = site_basic_info.get('site_location', {}).get("question", {}).get("name")
        picture_form = site_basic_info.get('site_picture', {}).get('form_id', 0)
        picture_question = site_basic_info.get('site_picture', {}).get("question", {}).get("name")
        if not location_form or not location_question:
            location_changed = False
        if not picture_form or not picture_question:
            picture_changed = False
        update_sites_info.delay(
            pk, location_changed, picture_changed, location_form, location_question, picture_form, picture_question)


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
        project_settings = ProgressSettings.objects.filter(project_id=self.kwargs['pk'], active=True).values('id',
                                                                                                             'source',
                                                                                                             'pull_integer_form',
                                                                                                             'pull_integer_form_question',
                                                                                                             'no_submissions_form',
                                                                                                             'no_submissions_total_count',
                                                                                                             'deployed')

        return Response({'json_questions': project_obj.site_meta_attributes, 'site_basic_info': project_obj.site_basic_info,
                         'site_featured_images': project_obj.site_featured_images, 'level': level,
                         'terms_and_labels': terms_and_labels, 'obj': project_data, 'project_settings': project_settings})

    def post(self, request, pk, format=None):

        project = Project.objects.get(pk=pk)
        old_meta = project.site_meta_attributes
        new_meta_attributes_raw = request.data.get('json_questions')
        for i, nm in enumerate(new_meta_attributes_raw):
            for om in old_meta:
                if nm['id'] == om['id']:
                    new_meta_attributes_raw[i]['question_name'] = om['question_name']

        project.site_meta_attributes = new_meta_attributes_raw
        old_site_basic_info = project.site_basic_info
        site_basic_info = request.data.get('site_basic_info')
        check_site_info_changed(project.pk, old_site_basic_info, site_basic_info)
        project.site_basic_info = site_basic_info
        project.site_featured_images = request.data.get('site_featured_images')

        new_meta = project.site_meta_attributes
        if old_meta != new_meta:
            ProjectMetaAttrHistory.objects.create(old_meta_attributes=old_meta,
                                                  new_meta_atrributes=new_meta, user=request.user, project=project)
            deleted = []

            for meta in old_meta:
                if meta not in new_meta:
                    deleted.append(meta)

            for other_project in Project.objects.filter(organization_id=project.organization_id):
                for meta in other_project.site_meta_attributes:

                    if meta['question_type'] == "Link":
                        try:
                            if str(project.id) in meta['metas']:
                                for del_meta in deleted:
                                    if del_meta in meta['metas'][str(project.id)]:
                                        del meta['metas'][str(project.id)][meta['metas'][str(project.id)].index(del_meta)]
                        except Exception as e:
                            pass

                other_project.save()
        project.save()

        return Response({'message': "Successfully created", 'status': status.HTTP_201_CREATED})

        # except Exception as e:
        #     return Response(data='Error: ' + str(e), status=status.HTTP_400_BAD_REQUEST)


class RegionalSites(viewsets.ReadOnlyModelViewSet):
    queryset = Site.objects.select_related('project', 'region', 'type')
    serializer_class = ProjectSitesListSerializer
    permission_classes = [IsAuthenticated, RegionalPermission]
    pagination_class = ProjectsitesPagination

    def get_queryset(self):

        region_id = self.request.query_params.get('region', None)
        search_param = self.request.query_params.get('q', None)

        if search_param and region_id:
            return self.queryset.filter(Q(name__icontains=search_param) | Q(identifier__icontains=search_param),
                                        region_id=region_id, is_survey=False, is_active=True, site__isnull=True)

        if region_id:
            return self.queryset.filter(region_id=region_id, is_survey=False, is_active=True, site__isnull=True)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        try:
            page = self.paginate_queryset(queryset)
        except:
            return Response({"message": "Region Id is required."}, status=status.HTTP_204_NO_CONTENT)

        try:
            region = Region.objects.get(id=int(self.request.query_params.get('region')))

        except ObjectDoesNotExist:
            return Response({"message": "Region Id is required."}, status=status.HTTP_204_NO_CONTENT)

        search_param = request.query_params.get('q', None)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({'data': serializer.data, 'query': search_param,
                                                })

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_serializer_context(self):
        return {'is_region': True}


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def sub_regions(request):
    query_params = request.query_params
    region_id = query_params.get('region')

    try:
        region = Region.objects.get(id=region_id)
        if check_regional_perm(request, region.id):
            project = region.project
            if ProjectLevelTermsAndLabels.objects.select_related('project').filter(project=project).exists():

                terms_and_labels = {'site': project.terms_and_labels.site,
                                    'donor': project.terms_and_labels.donor,
                                    'site_supervisor': project.terms_and_labels.site_supervisor,
                                    'site_reviewer': project.terms_and_labels.site_reviewer,
                                    'region': project.terms_and_labels.region,
                                    'region_supervisor': project.terms_and_labels.region_supervisor,
                                    'region_reviewer': project.terms_and_labels.region_reviewer,
                                    }

            else:
                terms_and_labels = {'site': 'Site',
                                    'donor': 'Donor',
                                    'site_supervisor': 'Site Supervisor',
                                    'site_reviewer': 'Site Reviewer',
                                    'region': 'Region',
                                    'region_supervisor': 'Region Supervisor',
                                    'region_reviewer': 'Region Reviewer',
                                    }
        else:
            return Response(status=status.HTTP_403_FORBIDDEN,
                            data={"detail": "You do not have permission to perform this action."})

    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, data="Region Id does not exist.")

    region_queryset = Region.objects.select_related('parent', 'project').filter(parent=region_id, is_active=True)
    region_data = [{'id': r.id, 'identifier': r.identifier, 'name': r.name, 'total_sites': r.get_sites_count()} for r in
                   region_queryset]
    project_name = ''
    project_url = ''
    if request.roles.filter(Q(group__name="Project Manager", project_id=region.project.id)|
                            Q(group__name="Organization Admin", organization_id=region.project.organization.id)) or request.is_super_admin:
        project_name = region.project.name
        project_url = region.project.get_absolute_url()
    breadcrumbs = {'region': region.name, 'project_name': project_name, 'project_url': project_url}
    return Response({'data': region_data, 'project': region.project.id, 'breadcrumbs': breadcrumbs, 'terms_and_labels': terms_and_labels})


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def users(request):
    site = request.query_params.get('site', None)
    project = request.query_params.get('project', None)
    team = request.query_params.get('team', None)

    if site is not None:
            try:
                site = Site.objects.select_related('project').get(id=site)
            except ObjectDoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND, data={'detail': 'Not found.'})
            region = site.region
            if check_site_permission(request, site.id):

                project = get_object_or_404(Project, id=site.project.id)
                region = site.region
                if region is not None:
                    queryset = UserRole.objects.filter(ended_at__isnull=True).filter(
                        Q(site_id=site.id) | Q(region=region)). \
                        select_related('user', 'user__user_profile').distinct('user_id')
                else:
                    queryset = UserRole.objects.filter(ended_at__isnull=True).filter(site=site).\
                        select_related('user', 'user__user_profile').distinct('user_id')

                data = [{'id': user_obj.user.id, 'full_name': user_obj.user.get_full_name(), 'username': user_obj.user.username,
                         'email': user_obj.user.email,
                         'profile_picture': user_obj.user.user_profile.profile_picture.url, 'role': get_user_roles(user_obj, site)}
                        for user_obj in queryset]

                return Response({'users': data, 'breadcrumbs': {'name': 'Users', 'site': site.name, 'site_url':
                    site.get_absolute_url()}})
            else:
                return Response(status=status.HTTP_403_FORBIDDEN,
                                data={"detail": "You do not have permission to perform this action."})
    elif project is not None:
        try:
            project = Project.objects.get(id=project)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data={'detail': 'Not found.'})

        queryset = UserRole.objects.select_related('user', 'user__profile').filter(project=project,
                                                                   ended_at__isnull=True).distinct('user_id')

        data = [{'id': user_obj.user.id, 'full_name': user_obj.user.get_full_name(), 'username': user_obj.user.username,
                 'email': user_obj.user.email,
                 'profile_picture': user_obj.user.user_profile.profile_picture.url, 'role': get_user_roles(user_obj, project)}
                for user_obj in queryset]

        return Response({'users': data, 'breadcrumbs': {'name': 'Users', 'project': project.name, 'project_url':
            project.get_absolute_url()}})

    elif team is not None:
        try:
            team = Organization.objects.get(id=team)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data={'detail': 'Not found.'})

        queryset = UserRole.objects.select_related('user').filter(organization=team, ended_at__isnull=True).distinct('user_id')

        data = [{'id': user_obj.user.id, 'full_name': user_obj.user.get_full_name(), 'username': user_obj.user.username,
                 'email': user_obj.user.email,
                 'profile_picture': user_obj.user.user_profile.profile_picture.url, 'role': get_user_roles(user_obj, team)}
                for user_obj in queryset]

        return Response({'users': data, 'breadcrumbs': {'name': 'Users', 'team': team.name, 'team_url':
            team.get_absolute_url()}})

    else:
        return Response(status=status.HTTP_404_NOT_FOUND, data={'detail': 'site id or project id or team id is required.'})


# def mvt_tiles(request, zoom, x, y):
#
#     """
#     Custom view to serve Mapbox Vector Tiles for the custom polygon model.
#     """
#     with connection.cursor() as cursor:
#         cursor.execute("SELECT ST_AsMVT(tile) FROM (SELECT id,name, ST_AsMVTGeom(location::geometry, TileBBox(%s, %s, %s, 4326)) FROM  fieldsight_site) AS tile", [zoom, x, y])
#         tile = bytes(cursor.fetchone()[0])
#         # return HttpResponse(len(tile))
#         # if not len(tile):
#         #     raise Http404()
#     return HttpResponse(tile, content_type="application/x-protobuf")

@permission_classes([IsAuthenticated])
@api_view(['GET'])
def project_sites_vt(request, pk, zoom, x, y):

    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT ST_AsMVT(tile) FROM (SELECT id,name, ST_AsMVTGeom(location::geometry, TileBBox(%s, %s, %s, 4326)) FROM  fieldsight_site where project_id=%s) AS tile",
            [zoom, x, y, pk])
        tile = bytes(cursor.fetchone()[0])

    return HttpResponse(tile, content_type="application/x-protobuf")


class TeamsViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Organization.objects.select_related('owner').prefetch_related('projects')
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated, SuperUserPermissions]
    pagination_class = TeamsPagination


class TeamFormViewset(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = TeamSerializer
    authentication_classes = [CsrfExemptSessionAuthentication, ]
    permission_classes = [IsAuthenticated, TeamCreationPermission]
    pagination_class = TeamsPagination

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=False)
        self.object = self.perform_create(serializer)
        self.object.owner = self.request.user
        self.object.save()

        longitude = request.data.get('longitude', None)
        latitude = request.data.get('latitude', None)

        if latitude and longitude is not None:
            p = Point(round(float(longitude), 6), round(float(latitude), 6), srid=4326)
            self.object.location = p
            self.object.save()

        noti = self.object.logs.create(source=self.request.user, type=9, title="new Organization",
                                       organization=self.object, content_object=self.object,
                                       description=u"{0} created a new Team "
                                                   u"named {1}".
                                       format(self.request.user, self.object.name))

        user = self.request.user
        user_id = User.objects.get(username=user).id
        profile = user.user_profile
        if not profile.organization:
            profile.organization = self.object
            profile.save()

        # subscribed to free plan
        if not user.is_superuser:
            free_package = Package.objects.get(plan=0)
            customer = Customer.objects.create(user=self.request.user, stripe_cust_id="free_cust_id")
            Subscription.objects.create(stripe_sub_id="free_plan", stripe_customer=customer,
                                        initiated_on=datetime.now(),
                                        package=free_package, organization=self.object)
            user_id = user_id
            email_after_subscribed_plan.delay(user_id)

        project = Project.objects.get(name="Example Project", organization_id=self.object.id)
        sites = Site.objects.filter(project=project)

        task_obj = CeleryTaskProgress.objects.create(user=user,
                                                     description="Auto Clone and Deployment of Forms",
                                                     task_type=15, content_object=self.object)
        if task_obj:
            project_id = Project.objects.get(name="Example Project", organization_id=self.object.id).id

            clone_form.delay(user_id, project_id, task_obj.id)

        if self.request.roles.filter(group__name="Unassigned").exists() or self.request.user.organizations.all():
            previous_group = UserRole.objects.filter(user=self.request.user, group__name="Unassigned").exists()
            if previous_group:
                unassigned_group = UserRole.objects.filter(user=self.request.user, group__name="Unassigned")
                unassigned_group.delete()

            new_group = Group.objects.get(name="Organization Admin")
            UserRole.objects.create(user=self.request.user, group=new_group, organization=self.object)

            group = Group.objects.get(name='Site Supervisor')
            for site in sites:
                UserRole.objects.get_or_create(user=user, group=group, organization=self.object, project_id=project.id,
                                               site_id=site.id)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        return serializer.save()


class EnableClusterSitesView(APIView):
    """
    A simple view for updating cluster sites from project level.
    """
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    permission_classes = [IsAuthenticated, ]

    def get(self, request, pk, *args, **kwargs):

        try:
            project = Project.objects.get(id=pk)
            cluster_sites = project.cluster_sites

            return Response(status=status.HTTP_200_OK, data={'cluster_sites': cluster_sites})

        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data={'detail': 'Project not found.'})

    def post(self, request, pk, format=None):
        try:
            project = Project.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data={'detail': 'Project not found.'})
        cluster_sites = request.data.get('cluster_sites')
        project.cluster_sites = cluster_sites
        project.save()
        return Response(status=status.HTTP_200_OK, data={'detail': 'successfully updated.', 'cluster_sites':
            project.cluster_sites})


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def project_full_map(request, pk):
    project = Project.objects.get(id=pk)
    organization_location = project.organization.location
    sites_with_no_location = Site.objects.filter(project=project, location=None).update(location=organization_location)
    if not project.location:
        project.location = organization_location
        project.save()

    sites = Site.objects.filter(project=project).exclude(location=None)
    data = serialize('custom_geojson', sites, geometry_field='location', fields=('location', 'id', 'name'))
    return Response(status=status.HTTP_200_OK, data=json.loads(data))


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def forms_breadcrumbs(request):
    project = request.GET.get('project')
    site = request.GET.get('site')
    type = request.GET.get('type')

    if project and type == 'create':
        project = Project.objects.get(id=project)

        breadcrumbs = {'current_page': 'Create Site', 'name': project.name, 'name_url': project.get_absolute_url()}

    elif site and type == 'edit':
        site = Site.objects.get(id=site)
        breadcrumbs = {'current_page': 'Edit', 'name': site.name, 'name_url': site.get_absolute_url()}

    else:
        breadcrumbs = {}
    return Response(status=status.HTTP_200_OK, data=breadcrumbs)
