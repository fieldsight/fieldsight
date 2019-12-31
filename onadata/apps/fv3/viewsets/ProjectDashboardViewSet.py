import datetime
import json

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.conf import settings
from django.contrib.gis.geos import Point

from rest_framework import viewsets, status
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from onadata.apps.eventlog.models import CeleryTaskProgress
from onadata.apps.fieldsight.models import Project, Site, Region, SiteType
from onadata.apps.fieldsight.utils.siteMetaAttribs import get_site_meta_ans
from onadata.apps.fieldsight.viewsets.SiteViewSet import SiteUnderProjectPermission
from onadata.apps.fsforms.models import Stage, FieldSightXF, Schedule, FInstance
from onadata.apps.fv3.serializers.ProjectDashboardSerializer import ProjectDashboardSerializer, \
    ProgressGeneralFormSerializer, ProgressScheduledFormSerializer, ProgressStageFormSerializer, SiteFormSerializer, \
    SitelistForMetasLinkSerializer
from onadata.apps.fv3.role_api_permissions import ProjectDashboardPermissions, SiteFormPermissions, \
    SupervisorPermission
from onadata.apps.fsforms.enketo_utils import CsrfExemptSessionAuthentication
from onadata.apps.logger.models import Instance
from onadata.apps.fieldsight.tasks import UnassignAllSiteRoles


class ProjectDashboardViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Project.objects.select_related('type', 'sector', 'sub_sector', 'organization')
    serializer_class = ProjectDashboardSerializer
    permission_classes = [IsAuthenticated, ProjectDashboardPermissions]

    def get_queryset(self):
        return self.queryset

    def get_serializer_context(self):
        return {'request': self.request}


class ProjectProgressTableViewSet(APIView):
    permission_classes = [IsAuthenticated, ProjectDashboardPermissions]

    def get(self, request, *args,  **kwargs):

        project_id = self.kwargs.get('pk', None)
        project_id = get_object_or_404(Project, pk=project_id).id

        generals_queryset = FieldSightXF.objects.select_related('xf', 'project')\
            .filter(is_staged=False, is_scheduled=False, is_deleted=False,
                                                        project_id=project_id, is_survey=False)
        generals = ProgressGeneralFormSerializer(generals_queryset, many=True)

        schedules_queryset = Schedule.objects.select_related('project').prefetch_related('schedule_forms')\
            .filter(project_id=project_id, schedule_forms__is_deleted=False, site__isnull=True,
                    schedule_forms__isnull=False, schedule_forms__xf__isnull=False)
        schedules = ProgressScheduledFormSerializer(schedules_queryset, many=True, context={'project_id': project_id})

        stages_queryset = Stage.objects.select_related('project').filter(stage__isnull=True, project_id=project_id, stage_forms__isnull=True).\
            order_by('order')

        stages = ProgressStageFormSerializer(stages_queryset, many=True)

        return Response({'generals': generals.data, 'schedules': schedules.data, 'stages': stages.data})


class ProjectSurveyFormsViewSet(APIView):
    permission_classes = [IsAuthenticated, ProjectDashboardPermissions]

    def get(self, request, *args,  **kwargs):

        project_id = self.kwargs.get('pk', None)
        try:
            project_id = get_object_or_404(Project, pk=project_id).id
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data={"detail": "Not found."})

        surveys = FieldSightXF.objects.filter(is_staged=False, is_scheduled=False, is_deleted=False,
                                              project_id=project_id, is_survey=True)

        data = [{'form_name': obj.xf.title, 'new_submission_url': '/forms/new/0/' + str(obj.id)} for obj in surveys]

        return Response(status=status.HTTP_200_OK, data=data)


@permission_classes([IsAuthenticated, ProjectDashboardPermissions])
@api_view(['GET'])
def project_regions_types(request, pk):
    try:
        project = Project.objects.get(id=pk, is_active=True)

    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, data="Not found")

    regions = Region.objects.filter(project_id=project.id, is_active=True)
    regions_data = [{'id': reg.id, 'identifier': reg.identifier, 'name': reg.name} for reg in regions]
    site_types = SiteType.objects.filter(project_id=project.id, deleted=False)
    site_types_data = [{'id': si_type.id, 'identifier': si_type.identifier, 'name': si_type.name} for si_type in site_types]
    data = {'regions': regions_data, 'site_types': site_types_data}

    return Response(status=status.HTTP_200_OK, data=data)


class SiteFormViewSet(viewsets.ModelViewSet):
    queryset = Site.objects.all()
    serializer_class = SiteFormSerializer
    permission_classes = [IsAuthenticated, SiteFormPermissions]
    authentication_classes = [CsrfExemptSessionAuthentication, ]

    def get_queryset(self):
        return self.queryset

    def get_serializer_context(self):
        return {'request': self.request}

    def list(self, request, *args, **kwargs):
        try:
            project = Project.objects.get(id=request.query_params.get('project'))
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data={'detail': 'Not Found'})
        json_questions = project.site_meta_attributes
        location = project.location

        site_types = SiteType.objects.filter(project=project, deleted=False).values('id', 'name')
        regions = Region.objects.filter(is_active=True, project=project).values('id', 'name')
        if project.cluster_sites:
            return Response(status=status.HTTP_200_OK, data={'json_questions': json_questions, 'site_types': site_types,
                                                         'regions': regions, 'location': str(location),
                                                             'project_id': project.id})
        else:
            return Response(status=status.HTTP_200_OK, data={'json_questions': json_questions, 'site_types': site_types,
                                                             'location': str(location), 'project_id': project.id})

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        if instance.site is None:
            data.pop('weight')

        if instance.project.cluster_sites is False:
            data.pop('region')
        return Response(data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        existing_identifier = Site.objects.filter(identifier=request.data.get('identifier'),
                                                  project_id=request.query_params.get('project'))
        if existing_identifier:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'detail': 'Your identifier "' +
                                                                                request.data.get('identifier')
                                                                                + '" conflict with existing site '
                                                                                  'please use different identifier '
                                                                                  'to create site.'})

        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        longitude = request.data.get('longitude', None)
        latitude = request.data.get('latitude', None)
        site = request.data.get('site', None)
        instance.save()

        if latitude and longitude is not None:
            p = Point(round(float(longitude), 6), round(float(latitude), 6), srid=4326)
            instance.location = p
            instance.save()

        if instance.site_meta_attributes_ans:
            metas = get_site_meta_ans(instance.id)
            instance.all_ma_ans = metas
            instance.save()
        if site is not None:
            instance.logs.create(source=self.request.user, type=110, title="new sub Site", site=instance.site,
                                 organization=instance.project.organization, project=instance.project,
                                 content_object=instance, extra_object=instance.site,
                                 description=u'{0} created a new Sub ' u'site named {1} in {2}'.\
                                 format(self.request.user.get_full_name(), instance.name, instance.project.name))

        else:
            instance.logs.create(source=self.request.user, type=11, title="new Site",
                                 organization=instance.project.organization, project=instance.project,
                                 content_object=instance, extra_object=instance.project,
                                 description=u'{0} created a new site ' u'named {1} in {2}'.\
                                 format(self.request.user.get_full_name(), instance.name, instance.project.name))

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        previous_identifier = instance.identifier

        existing_identifier = Site.objects.filter(identifier=request.data.get('identifier'),
                                                  project_id=instance.project_id)
        check_identifier = previous_identifier == request.data.get('identifier')

        if not check_identifier and existing_identifier:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'detail': 'Your identifier "' + request.data.get(
                'identifier') + '" conflict with existing site please use different identifier to update site'})

        old_meta = instance.site_meta_attributes_ans

        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)
        longitude = request.data.get('longitude', None)
        latitude = request.data.get('latitude', None)

        if latitude and longitude is not None:
            p = Point(round(float(longitude), 6), round(float(latitude), 6), srid=4326)
            instance.location = p
            instance.save()
        instance.save()

        new_meta = json.loads(instance.site_meta_attributes_ans)

        if instance.site_meta_attributes_ans:
            metas = get_site_meta_ans(instance.id)
            instance.all_ma_ans = metas
            instance.save()

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

        description = u'{0} changed the details of site named {1}'.format(
            self.request.user.get_full_name(), instance.name
        )
        instance.logs.create(
            source=self.request.user, type=15, title="edit Site",
            organization=instance.project.organization,
            project=instance.project, content_object=instance,
            description=description,
            extra_json=extra_json,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        return serializer.save()

    def perform_update(self, serializer):
        instance = serializer.save()
        return instance

    def destroy(self, request, *args, **kwargs):
        try:
            site = self.get_object()
            site.is_active = False
            site.identifier = site.identifier + str('_' + self.kwargs.get('pk'))
            site.save()

            instances = site.site_instances.all().values_list('instance', flat=True)

            Instance.objects.filter(id__in=instances).update(deleted_at=datetime.datetime.now())

            # update in mongo
            settings.MONGO_DB.instances.update({"_id": {"$in": list(instances)}},
                                                        {"$set": {'_deleted_at': datetime.datetime.now()}}, multi=True)

            FInstance.objects.filter(instance_id__in=instances).update(is_deleted=True)

            task_obj = CeleryTaskProgress.objects.create(user=self.request.user,
                                                         description="Removal of UserRoles After Site delete",
                                                         task_type=7, content_object=site)

            if task_obj:
                task = UnassignAllSiteRoles.delay(task_obj.id, site.id)
                task_obj.task_id = task.id
                task_obj.save()

            task_obj.logs.create(source=self.request.user, type=36, title="Delete Site",
                                 organization=site.project.organization, extra_object=site.project,
                                 project=site.project, extra_message="site", site=site, content_object=site,
                                 description=u'{0} deleted of site named {'u'1}'.\
                                 format(self.request.user.get_full_name(), site.name))
            return Response(status=status.HTTP_200_OK)
        except Http404:
            return Response(status=status.HTTP_204_NO_CONTENT)


class SitelistForMetasLink(viewsets.ModelViewSet):
    queryset = Site.objects.all()
    serializer_class = SitelistForMetasLinkSerializer
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    permission_classes = (SiteUnderProjectPermission,)

    def filter_queryset(self, queryset):
        return queryset.filter(project__id=self.kwargs.get('pk', None))


class SupervisorProjectDashboardView(APIView):
    permission_classes = [IsAuthenticated, SupervisorPermission]

    def get(self, request, *args,  **kwargs):

        project_id = self.kwargs.get('pk', None)
        obj = get_object_or_404(Project, pk=project_id)
        total_users = obj.project_roles.select_related('user').filter(ended_at__isnull=True).distinct('user').count()
        outstanding, flagged, approved, rejected = obj.get_submissions_count()
        total_submissions = outstanding + flagged + approved + rejected,
        total_sites = obj.sites.filter(is_active=True, is_survey=False, site__isnull=True).count()
        total_regions = obj.project_region.filter(is_active=True, parent__isnull=True).count()
        project_managers_qs = obj.project_roles.select_related("user", "user__user_profile").filter(
            ended_at__isnull=True,
            group__name="Project Manager")

        users = [{'id': role.user.id, 'full_name': role.user.get_full_name(),
                  'profile_picture': role.user.user_profile.profile_picture.url, 'role': 'Project Manager'} for role in
                 project_managers_qs]

        return Response({'total_users': total_users,
                         'total_submissions': total_submissions[0],
                         'total_sites': total_sites,
                         'total_regions': total_regions,
                         'users': users})