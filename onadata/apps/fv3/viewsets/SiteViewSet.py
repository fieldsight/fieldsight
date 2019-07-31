import json

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
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


class SiteSubmissionsPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'


class SiteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Site.objects.select_related('project', 'region')
    serializer_class = SiteSerializer
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        return self.queryset


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def site_map(request, pk):
    obj = get_object_or_404(Site, pk=pk, is_active=True)
    data = serialize('custom_geojson', [obj], geometry_field='location',
                     fields=('name', 'public_desc', 'additional_desc', 'address', 'location', 'phone', 'id'))

    return Response(json.loads(data))


class SiteSubmissionsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FInstance.objects.select_related('instance', 'site_fxf__xf', 'submitted_by')
    serializer_class = FInstanceSerializer
    permission_classes = [AllowAny, ]
    pagination_class = SiteSubmissionsPagination

    def get_queryset(self):
        site_id = self.request.query_params.get('site', None)
        site = get_object_or_404(Site, id=int(site_id))
        return self.queryset.filter(site=site, is_deleted=False)


class SiteForms(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args,  **kwargs):

        site_id = self.kwargs.get('site_id', None)
        query_params = self.request.query_params.get('type')

        if site_id and query_params:
            try:
                project_id = get_object_or_404(Site, pk=site_id).project.id

                if query_params == 'general':
                    generals = FieldSightXF.objects.select_related('xf').filter(is_staged=False, is_deleted=False, is_scheduled=False,
                                                           is_survey=False). \
                        filter(Q(site__id=site_id, from_project=False) | Q(project__id=project_id))

                    data = [{'form_name': obj.xf.title, 'new_submission_url':
                             settings.SITE_URL + '/forms/new-submission/' + str(obj.id) + '/' + str(site_id) + '/'} for obj in generals]

                    return Response({'general_forms': data})

                elif query_params == 'scheduled':

                    schedules = Schedule.objects.prefetch_related('schedule_forms__xf').filter(schedule_forms__is_deleted=False,
                                                        schedule_forms__isnull=False).filter(
                        Q(site__id=site_id, schedule_forms__from_project=False)
                        | Q(project__id=project_id))

                    data = [{'form_name': obj.schedule_forms.xf.title, 'new_submission_url':
                             settings.SITE_URL + '/forms/new-submission/' + str(obj.id) + '/' + str(site_id) + '/'} for obj in schedules]

                    return Response({'scheduled_forms': data})

                elif query_params == 'stage':

                    stages_queryset = Stage.objects.filter(
                        stage__isnull=True
                    ).filter(Q(site__id=site_id,
                               project_stage_id=0
                               ) | Q(
                        project__id=project_id
                    )).order_by('order', 'date_created')
                    stages = StageFormSerializer(stages_queryset, many=True, context={'site_id': site_id})

                    return Response({'stage_forms': stages.data})

                else:
                    return Response(data="Form of type " + str(query_params) + " not found.", status=status.HTTP_204_NO_CONTENT)

            except Exception as e:
                return Response(data=str(e), status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(data="Site Id and form type required.", status=status.HTTP_400_BAD_REQUEST)


class SiteCropImage(APIView):
    """
    Retrieve and update site logo.
    """
    authentication_classes = (CsrfExemptSessionAuthentication, SessionAuthentication, BasicAuthentication)

    def get_object(self, pk):
        try:
            return Site.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, format=None):
        site = self.get_object(pk)
        serializer = SiteCropImageSerializer(site)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
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
    site_featured_images = Site.objects.get(pk=site_id).site_featured_images
    recent_pictures = get_recent_images(site_id)
    recent_pictures = list(recent_pictures["result"])
    return Response({'site_featured_images': site_featured_images,
                     'recent_pictures': recent_pictures})


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
    blueprints_obj = Site.objects.get(pk=site_id).blueprints.all()
    data = [{'name': blueprint.get_name(), 'file': blueprint.image.url, 'type': check_file_extension((blueprint.image.url.lower()))}
            for blueprint in blueprints_obj]
    return Response(data)
