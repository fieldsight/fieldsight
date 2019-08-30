from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny

from onadata.apps.fv3.serializers.TeamSerializer import TeamSerializer, TeamProjectSerializer
from onadata.apps.fieldsight.models import Organization, Project
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


class TeamProjectsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Project.objects.all()
    serializer_class = TeamProjectSerializer
    permission_classes = [IsAuthenticated, TeamDashboardPermissions]

    def get_queryset(self):
        return self.queryset.filter(organization=self.kwargs.get('pk'), is_active=True)
