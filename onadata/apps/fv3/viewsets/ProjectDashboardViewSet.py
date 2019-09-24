import json

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from onadata.apps.fieldsight.models import Project, Site, Region, SiteType
from onadata.apps.fsforms.models import Stage, FieldSightXF, Schedule
from onadata.apps.fv3.serializers.ProjectDashboardSerializer import ProjectDashboardSerializer, ProgressGeneralFormSerializer, \
    ProgressScheduledFormSerializer, ProgressStageFormSerializer, SiteFormSerializer
from onadata.apps.fv3.role_api_permissions import ProjectDashboardPermissions
from onadata.apps.fsforms.enketo_utils import CsrfExemptSessionAuthentication


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

        generals_queryset = FieldSightXF.objects.select_related('xf').filter(is_staged=False, is_scheduled=False, is_deleted=False,
                                                        project_id=project_id, is_survey=False)
        generals = ProgressGeneralFormSerializer(generals_queryset, many=True)

        schedules_queryset = Schedule.objects.filter(project_id=project_id, schedule_forms__is_deleted=False,
                                                     site__isnull=True, schedule_forms__isnull=False,
                                                     schedule_forms__xf__isnull=False)
        schedules = ProgressScheduledFormSerializer(schedules_queryset, many=True)

        stages_queryset = Stage.objects.filter(stage__isnull=True, project_id=project_id, stage_forms__isnull=True).\
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


@permission_classes([IsAuthenticated, ])
@api_view(['GET'])
def project_regions_types(request, project_id):
    try:
        project = Project.objects.get(id=project_id, is_active=True)

    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, data="Not found")

    regions = Region.objects.filter(project_id=project.id, is_active=True)
    regions_data = [{'id': reg.id, 'identifier': reg.identifier, 'name': reg.name} for reg in regions]
    site_types = SiteType.objects.filter(project_id=project.id, deleted=False)
    site_types_data = [{'id': si_type.id, 'identifier': si_type.identifier, 'name': si_type.name} for si_type in site_types]
    data = {'regions': regions_data, 'site_types': site_types_data}

    return Response(status=status.HTTP_200_OK, data=data)


class SiteFormViewSet(viewsets.ModelViewSet):
    serializer_class = SiteFormSerializer
    permission_classes = [IsAuthenticated, ProjectDashboardPermissions]
    authentication_classes = [CsrfExemptSessionAuthentication, ]

    def get_queryset(self):
        return self.queryset

    def get_serializer_context(self):
        return {'request': self.request}

    def list(self, request, *args, **kwargs):
        try:
            project = Project.objects.get(id=self.kwargs.get('pk'))
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data={'detail': 'Not Found'})
        json_questions = project.site_meta_attributes
        site_types = SiteType.objects.filter(project=project, deleted=False).values('id', 'name')
        regions = Region.objects.filter(is_active=True, project=project).values('id', 'name')

        return Response(status=status.HTTP_200_OK, data={'json_questions': json_questions, 'site_types': site_types,
                                                         'regions': regions})

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=False)
        self.object = self.perform_create(serializer)
        noti = self.object.logs.create(source=self.request.user, type=11, title="new Site",
                                       organization=self.object.project.organization,
                                       project=self.object.project, content_object=self.object,
                                       extra_object=self.object.project,
                                       description=u'{0} created a new site '
                                                   u'named {1} in {2}'.format(self.request.user.get_full_name(),
                                                                              self.object.name,
                                                                              self.object.project.name))

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        return serializer.save()




