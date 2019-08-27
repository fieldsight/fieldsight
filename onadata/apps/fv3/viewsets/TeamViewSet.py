from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny

from onadata.apps.fv3.serializers.TeamSerializer import TeamSerializer
from onadata.apps.fieldsight.models import Organization
from onadata.apps.fv3.role_api_permissions import TeamDashboardPermissions


class TeamDashboardViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated, TeamDashboardPermissions]

    def get_queryset(self):
        return self.queryset

    def get_serializer_context(self):
        context = {'request': self.request}

        return context
