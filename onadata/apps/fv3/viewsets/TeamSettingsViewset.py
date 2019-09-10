from django.contrib.gis.geos import Point
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework import viewsets, status

from onadata.apps.fieldsight.models import Organization, OrganizationType, COUNTRIES
from onadata.apps.fv3.serializers.TeamSerializer import TeamUpdateSerializer, TeamGeoLayer
from onadata.apps.fsforms.enketo_utils import CsrfExemptSessionAuthentication
from onadata.apps.geo.models import GeoLayer


class TeamViewset(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing team.
    """
    queryset = Organization.objects.all()
    serializer_class = TeamUpdateSerializer
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    permission_classes = [IsAuthenticated, ]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        long = request.data.get('longitude', None)
        lat = request.data.get('latitude', None)
        if lat and long is not None:
            p = Point(round(float(long), 6), round(float(lat), 6), srid=4326)
            instance.location = p
            instance.save()
        instance.logs.create(source=self.request.user, type=13, title="Edit Team",
                                       organization=instance, content_object=instance,
                                       description=u"{0} changed the details of Team named {1}".format(
                                           self.request.user.get_full_name(),
                                           instance.name))

        return Response(status=status.HTTP_200_OK, data=serializer.data)


class TeamGeoLayerViewset(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing geolayer.
    """
    queryset = GeoLayer.objects.all()
    serializer_class = TeamGeoLayer
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    permission_classes = [IsAuthenticated, ]

    def filter_queryset(self, queryset):
        team = self.request.query_params.get('team', None)
        if team:
            try:
                team = Organization.objects.get(id=team)
                return queryset.filter(organization=team)

            except ObjectDoesNotExist:
                return GeoLayer.objects.none()

        return queryset

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data
        if 'geo_shape_file' not in data:
            data.update({'geo_shape_file': instance.geo_shape_file})

        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(status=status.HTTP_200_OK, data=serializer.data)


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def team_types_countries(request):
    team_types = OrganizationType.objects.values('id', 'name')
    countries = [{'key': c[0], 'value': c[1]} for c in COUNTRIES]

    return Response(data={'team_types': team_types, 'countries': countries}, status=status.HTTP_200_OK)
