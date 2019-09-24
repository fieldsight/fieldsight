from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from onadata.apps.fieldsight.models import Project
from onadata.apps.fsforms.models import FieldSightXF
from onadata.apps.fv3.serializers.ViewFormSerializer import ProjectSiteResponseSerializer


class ProjectSiteResponsesView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, format=None):
        project = request.query_params.get('project', None)
        site = request.query_params.get('site')
        type = request.query_params.get('type', None)

        from django.core.exceptions import ObjectDoesNotExist
        try:
            project = Project.objects.get(id=project, is_active=True)

        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data={"detail": "Not found."})

        if type == 'general':
            generals_queryset = FieldSightXF.objects.select_related('xf').filter(is_staged=False, is_scheduled=False,
                                                                                 is_deleted=False, project=project,
                                                                                 is_survey=False)
            data = ProjectSiteResponseSerializer(generals_queryset, many=True).data

            return Response(status=status.HTTP_200_OK, data=data)
