from django.db.models import Prefetch
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated

from onadata.apps.fsforms.enketo_utils import CsrfExemptSessionAuthentication
from onadata.apps.fsforms.models import FInstance, InstanceStatusChanged
from onadata.apps.fv3.permissions.submission import SubmissionDetailPermission, SubmissionChangePermission
from onadata.apps.fv3.serializers.SubmissionSerializer import SubmissionSerializer, AlterInstanceStatusSerializer, \
    SubmissionAnswerSerializer
from onadata.apps.logger.models import Instance


class SubmissionAnswerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Instance.objects.all()
    serializer_class = SubmissionAnswerSerializer
    permission_classes = [IsAuthenticated, SubmissionDetailPermission]

    def get_queryset(self):
        return self.queryset.select_related("xform","xform__user", "user").prefetch_related(
            Prefetch('fieldsight_instance',
                     queryset=FInstance.objects.all().select_related(
                         'site', 'site_fxf', 'project_fxf')
                     ))

    def get_serializer_context(self):
        return {'request': self.request, 'kwargs': self.kwargs,}


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


class AlterSubmissionStatusViewSet(viewsets.ModelViewSet):
    queryset = [InstanceStatusChanged.objects.first()]
    serializer_class = AlterInstanceStatusSerializer
    authentication_classes = [CsrfExemptSessionAuthentication, BasicAuthentication,]
    permission_classes = [IsAuthenticated, SubmissionChangePermission]
    parser_classes = [MultiPartParser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_context(self):
        images = []
        for k, v in self.request.data.items():
            if "image_" in k:
                images.append(v)
        return {'request': self.request, 'kwargs': self.kwargs, 'images': images}




