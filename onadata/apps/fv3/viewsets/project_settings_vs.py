from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from onadata.apps.fieldsight.models import ProgressSettings
from onadata.apps.fv3.permissions.project_settings import ProjectSettingsPermission
from onadata.apps.fv3.serializers.project_settings import ProgressSettingsSerializer


class ProjectSettingsOptions(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        # self.has_object_permission(request, project)
        return Response(dict(ProgressSettings.CHOICES))


class ProjectProgressSettings(viewsets.ModelViewSet):
    queryset = ProgressSettings.objects.all()
    permission_classes = [IsAuthenticated, ProjectSettingsPermission]
    serializer_class = ProgressSettingsSerializer

    def perform_create(self, serializer):
        ProgressSettings.objects.filter(project_id=self.kwargs['pk']).update(active=False)
        serializer.save(user=self.request.user, project_id=self.kwargs['pk'])


    def get_queryset(self):
        return self.queryset.filter(project_id=self.kwargs['pk'], active=True)

