from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.serializers import ModelSerializer
from rest_framework.response import Response

from onadata.apps.fieldsight.fs_exports.utils import project_map_data
from onadata.apps.fieldsight.models import Organization
from onadata.apps.fieldsight.static_lists import COUNTRIES


class ProjectsApi(APIView):
    def get(self, request, format=None):
        """
        Return a list projects.
        """
        df = project_map_data()
        data = df.to_dict(orient='records')
        return Response({'data': data})


class CountriesApi(APIView):
    def get(self, request, format=None):
        """
        Return a list countries.
        """
        data = [{'pk': c[0], 'name': c[1]} for c in COUNTRIES]
        return Response({'data': data})


class OrganizationSerializer(ModelSerializer):
    class Meta:
        model = Organization
        fields = ('pk', 'name')


class OrganizationViewset(ReadOnlyModelViewSet):
    queryset = Organization.objects.all().values('pk', 'name')
    serializer_class = OrganizationSerializer
