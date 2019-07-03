from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from onadata.apps.fieldsight.models import Site
from onadata.apps.fv3.serializers.ProjectSitesListSerializer import ProjectSitesListSerializer


class ProjectsitesPagination(PageNumberPagination):
    page_size = 200


class ProjectSitesListViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Site.objects.select_related('project', 'region', 'type')
    serializer_class = ProjectSitesListSerializer
    permission_classes = [IsAuthenticated, ]
    pagination_class = ProjectsitesPagination

    def get_queryset(self):

        project_id = self.request.query_params.get('project', None)

        if project_id is not None:

            return self.queryset.filter(project_id=project_id, is_survey=False, is_active=True)
