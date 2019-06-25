from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from onadata.apps.fieldsight.models import ProgressSettings


class ProjectSettings(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        return Response(dict(ProgressSettings.CHOICES))