from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from onadata.apps.fieldsight.models import Project
from onadata.apps.fv3.serializers.ProjectDashboardSerializer import ProjectDashboardSerializer


class ProjectDashboardViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Project.objects.select_related('type', 'sector', 'sub_sector', 'organization')
    serializer_class = ProjectDashboardSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return self.queryset
