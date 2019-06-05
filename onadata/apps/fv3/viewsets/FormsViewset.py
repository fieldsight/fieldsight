from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication, SessionAuthentication

from onadata.apps.fsforms.models import FieldSightXF
from onadata.apps.fv3.serializers.FormSerializer import XFormSerializer
from onadata.apps.logger.models import XForm


class MyFormsViewSet(viewsets.ReadOnlyModelViewSet):
    """
        A simple ViewSet for viewing myforms.
        """
    authentication_classes = ([SessionAuthentication,BasicAuthentication])
    queryset = XForm.objects.all()
    serializer_class = XFormSerializer

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


class MyProjectFormsViewSet(viewsets.ReadOnlyModelViewSet):
    """
        A simple ViewSet for viewing my  project forms.
        forms assigned in my project is project forms
        """
    authentication_classes = ([SessionAuthentication,BasicAuthentication])
    queryset = XForm.objects.all()
    serializer_class = XFormSerializer

    def get_queryset(self):
        projects = self.request.roles.filter(
            ended_at__isnull=False).values_list("project", flat=True).order_by('project').distinct('project')
        forms = FieldSightXF.objects.filter(
            project__in=projects).exclude().order_by("xf").values('xf').distinct()
        return forms
