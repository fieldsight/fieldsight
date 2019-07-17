import json

from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from django.core.serializers import serialize
from django.shortcuts import get_object_or_404

from onadata.apps.fv3.serializers.SiteSerializer import SiteSerializer, FInstanceSerializer
from onadata.apps.fieldsight.models import Site
from onadata.apps.fsforms.models import FInstance


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
        return self.queryset.filter(site=site)
