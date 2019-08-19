from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from onadata.apps.fieldsight.models import Project
from onadata.apps.fv3.serializers.ProjectDashboardSerializer import ProjectDashboardSerializer
from onadata.apps.fv3.role_api_permissions import ProjectDashboardPermissions


class ProjectDashboardViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Project.objects.select_related('type', 'sector', 'sub_sector', 'organization')
    serializer_class = ProjectDashboardSerializer
    permission_classes = [IsAuthenticated, ProjectDashboardPermissions]

    def get_queryset(self):
        return self.queryset

    def get_serializer_context(self):
        return {'request': self.request}