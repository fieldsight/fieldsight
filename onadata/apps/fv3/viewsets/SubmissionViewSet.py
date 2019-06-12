from django.db.models import Prefetch
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from onadata.apps.fsforms.models import FInstance
from onadata.apps.fv3.permissions.submission import SubmissionDetailPermission
from onadata.apps.fv3.serializers.SubmissionSerializer import SubmissionSerializer
from onadata.apps.logger.models import Instance


class SubmissionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Instance.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = [IsAuthenticated, SubmissionDetailPermission]

    def get_queryset(self):
        return self.queryset.select_related("xform","xform__user", "user").prefetch_related(
            Prefetch('fieldsight_instance',
                     queryset=FInstance.objects.all().select_related(
                         'site', 'site_fxf', 'project_fxf').prefetch_related("comments", "new_edits")
                     ))


    def get_serializer_context(self):
        return {'request': self.request, 'kwargs': self.kwargs,}

