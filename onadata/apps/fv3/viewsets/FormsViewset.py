from rest_framework import viewsets

from onadata.apps.fv3.serializers.FormSerializer import XFormSerializer
from onadata.apps.logger.models import XForm


class MyFormsViewSet(viewsets.ReadOnlyModelViewSet):
    """
        A simple ViewSet for viewing myforms.
        """
    queryset = XForm.objects.all()
    serializer_class = XFormSerializer
