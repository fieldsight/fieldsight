import json

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from django.core.serializers import serialize
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView

from onadata.apps.fsforms.enketo_utils import CsrfExemptSessionAuthentication
from onadata.apps.fv3.serializers.SiteSerializer import SiteSerializer, FInstanceSerializer, StageFormSerializer, \
    SiteCropImageSerializer
from onadata.apps.fieldsight.models import Site
from onadata.apps.fsforms.models import FInstance, Schedule, Stage, FieldSightXF

from onadata.apps.fsforms.reports_util import get_recent_images
from onadata.apps.fv3.role_api_permissions import SiteDashboardPermissions, SiteSubmissionPermission, check_site_permission


class SiteSubmissionsPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'


class SiteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Site.objects.select_related('project', 'region')
    serializer_class = SiteSerializer
    permission_classes = [IsAuthenticated, SiteDashboardPermissions]

    def get_queryset(self):
        return self.queryset

    def get_serializer_context(self):
        return {'request': self.request}


@permission_classes([SiteSubmissionPermission,])
@api_view(['GET'])
def site_map(request, pk):
    if check_site_permission(request, int(pk)):
        pk = int(pk)
        obj = get_object_or_404(Site, pk=pk, is_active=True)
        data = serialize('custom_geojson', [obj], geometry_field='location',
                         fields=('name', 'public_desc', 'additional_desc', 'address', 'location', 'phone', 'id'))

        return Response(json.loads(data))
    else:
        return Response(status=status.HTTP_403_FORBIDDEN, data={"detail": "You do not have permission to perform this action."})


class SiteSubmissionsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FInstance.objects.select_related('instance', 'site_fxf__xf', 'submitted_by')
    serializer_class = FInstanceSerializer
    permission_classes = [IsAuthenticated, SiteSubmissionPermission]
    pagination_class = SiteSubmissionsPagination

    def get_queryset(self):
        site_id = self.request.query_params.get('site', None)
        site = get_object_or_404(Site, id=int(site_id))
        return self.queryset.filter(site=site, is_deleted=False).order_by('-date')


class SiteForms(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args,  **kwargs):

        site_id = self.kwargs.get('site_id', None)
        query_params = self.request.query_params.get('type')

        if check_site_permission(request, int(site_id)):

            if site_id and query_params:
                site_id = int(site_id)
                try:
                    project_id = get_object_or_404(Site, pk=int(site_id)).project.id

                    if query_params == 'general':
                        generals = FieldSightXF.objects.select_related('xf').filter(is_staged=False, is_deleted=False, is_scheduled=False,
                                                               is_survey=False). \
                            filter(Q(site__id=site_id, from_project=False) | Q(project__id=project_id))

                        data = [{'form_name': obj.xf.title, 'new_submission_url':
                                 settings.SITE_URL + '/forms/new/' + str(site_id) + '/' + str(obj.id)} for obj in generals]

                        return Response({'general_forms': data})

                    elif query_params == 'scheduled':

                        schedules = Schedule.objects.prefetch_related('schedule_forms__xf').filter(schedule_forms__is_deleted=False,
                                                            schedule_forms__isnull=False).filter(
                            Q(site__id=site_id, schedule_forms__from_project=False)
                            | Q(project__id=project_id))

                        data = [{'form_name': obj.schedule_forms.xf.title, 'new_submission_url':
                                 settings.SITE_URL + '/forms/new/' + str(site_id) + '/' + str(obj.schedule_forms.id)} for obj in schedules]

                        return Response({'scheduled_forms': data})

                    elif query_params == 'stage':
                        site = Site.objects.get(pk=site_id)

                        if site.type:
                            project_id = site.project.id
                            stages_queryset = Stage.objects.filter(stage__isnull=True).filter(Q(site__id=site_id,
                                                         project_stage_id=0)
                                                       | Q
                                                       (Q(project__id=project_id) &
                                                        Q(tags__contains=[site.type_id])) |
                                                       Q(Q(project__id=project_id)
                                                         & Q(tags=[]))
                                                       )
                        else:
                            project_id = site.project.id
                            stages_queryset = Stage.objects.filter(stage__isnull=True).filter(
                                Q(site__id=site_id, project_stage_id=0)
                                | Q(project__id=project_id))
                        stages = StageFormSerializer(stages_queryset, many=True, context={'site_id': site_id})

                        return Response({'stage_forms': stages.data})

                    else:
                        return Response(data="Form of type " + str(query_params) + " not found.", status=status.HTTP_204_NO_CONTENT)

                except Exception as e:
                    return Response(data=str(e), status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(data="Site Id and form type required.", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN,
                            data={"detail": "You do not have permission to perform this action."})


class SiteCropImage(APIView):
    """
    Retrieve and update site logo.
    """
    authentication_classes = (CsrfExemptSessionAuthentication, SessionAuthentication, IsAuthenticated)

    def get_object(self, pk):
        try:
            return Site.objects.get(pk=int(pk))
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    #
    # def get(self, request, pk, format=None):
    #     site = self.get_object(pk)
    #     serializer = SiteCropImageSerializer(site)
    #     return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(int(pk))
        serializer = SiteCropImageSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def site_recent_pictures(request):
    query_params = request.query_params
    site_id = query_params.get('site')
    if check_site_permission(request, int(site_id)):
        try:
            site_featured_images = Site.objects.get(pk=int(site_id)).site_featured_images
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        recent_pictures = get_recent_images(int(site_id))
        recent_pictures = list(recent_pictures["result"])
        return Response({'site_featured_images': site_featured_images,
                         'recent_pictures': recent_pictures})
    else:
        return Response(status=status.HTTP_403_FORBIDDEN,
                        data={"detail": "You do not have permission to perform this action."})


def check_file_extension(file_url):
    type = 'others'

    if file_url.endswith(('.jpg', '.png', '.jpeg')):
        type = 'image'

    elif file_url.endswith(('.xls', '.xlsx')):
        type = 'excel'

    elif file_url.endswith('.pdf'):
        type = 'pdf'

    elif file_url.endswith(('.doc', '.docm', 'docx', '.dot', '.dotm', '.dot', '.txt', '.odt')):
        type = 'word'

    return type


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def site_documents(request):
    query_params = request.query_params
    site_id = query_params.get('site_id')
    site_id = int(site_id)
    if check_site_permission(request, site_id):
        try:
            blueprints_obj = Site.objects.get(pk=site_id).blueprints.all()
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        data = [{'name': blueprint.get_name(), 'file': blueprint.image.url, 'type': check_file_extension((blueprint.image.url.lower()))}
                for blueprint in blueprints_obj]
        return Response(data)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN,
                        data={"detail": "You do not have permission to perform this action."})

