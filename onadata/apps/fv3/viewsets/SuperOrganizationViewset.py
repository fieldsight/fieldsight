from django.utils import timezone
from rest_framework import viewsets, status
from onadata.apps.fieldsight.models import SuperOrganization
from rest_framework.permissions import IsAuthenticated
from onadata.apps.fsforms.enketo_utils import CsrfExemptSessionAuthentication
from django.contrib.gis.geos import Point
from rest_framework.response import Response
from onadata.apps.fv3.serializers.SuperOrganizationSerializer import OrganizationSerializer


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = SuperOrganization.objects.all()
    serializer_class = OrganizationSerializer
    authentication_classes = [CsrfExemptSessionAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=False)
            self.object = self.perform_create(serializer)
            self.object.owner = self.request.user
            self.object.date_created = timezone.now()
            self.object.save()
            longitude = request.data.get('longitude', None)
            latitude = request.data.get('latitude', None)
            if latitude and longitude is not None:
                p = Point(round(float(longitude), 6), round(float(latitude), 6),
                          srid=4326)
                self.object.location = p
                self.object.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"test", str(e)})

    def perform_create(self, serializer):
        return serializer.save()