from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny

from onadata.apps.fv3.serializers.SiteSerializer import SiteSerializer
from onadata.apps.fieldsight.models import Site


class SiteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Site.objects.all()
    serializer_class = SiteSerializer
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        return self.queryset
