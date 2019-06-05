from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication, SessionAuthentication

from onadata.apps.fieldsight.models import Project
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
            ended_at__isnull=True).values_list("project", flat=True).order_by('project').distinct()
        organizations = self.request.roles.filter(
            ended_at__isnull=True, group__name="Organization Admin").values_list(
            "organization", flat=True)
        admin_projects = Project.objects.filter(organization__pk__in=organizations).values_list("pk", flat=True)
        projects = [p for p in projects] + [p for p in admin_projects]
        fieldsight_forms = FieldSightXF.objects.filter(
            project__in=projects).exclude(xf__user=self.request.user).order_by("xf").distinct()
        results = [f.xf for f in fieldsight_forms]
        return results
