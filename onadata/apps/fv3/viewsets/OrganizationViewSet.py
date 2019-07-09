from django.db.models import Prefetch
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny

from onadata.apps.fv3.serializers.OrganizationSerializer import OrganizationSerializer
from onadata.apps.fieldsight.models import Organization


class OrganizationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        return self.queryset
