from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count

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

        try:
            project = Project.objects.get(id=project, is_active=True)

        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data={"detail": "Not found."})

        if type == 'general':
            base_queryset = FieldSightXF.objects.select_related('xf').filter(is_staged=False, is_scheduled=False,
                                                                             is_deleted=False, is_survey=False)
            if project is not None:
                is_project = True
                generals_queryset = base_queryset.filter(project=project).annotate(response_count=
                                                                                   Count('project_form_instances'))
                generals = ProjectSiteResponseSerializer(generals_queryset, context={'is_project': is_project},
                                                     many=True).data

                general_deleted_qs = FieldSightXF.objects.filter(is_staged=False, is_scheduled=False,
                                                                    is_survey=False, is_deleted=True, project=project)
                general_deleted_forms = ProjectSiteResponseSerializer(general_deleted_qs, context={'is_project':
                                                                                                          is_project},
                                                                      many=True).data
                return Response(status=status.HTTP_200_OK, data={'generals_forms': generals,
                                                                 'deleted_forms': general_deleted_forms})

            elif site is not None:
                pass
