import json

from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework.response import Response
from rest_framework import status

from onadata.apps.fieldsight.fs_exports.utils import project_map_data
from onadata.apps.fieldsight.models import Organization, Site, Project
from onadata.apps.fieldsight.static_lists import COUNTRIES
from onadata.apps.fsforms.models import FieldSightXF
from onadata.apps.fv3.role_api_permissions import ProjectDashboardPermissions


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


class ProjectsInCountries(APIView):

    def get(self, request, format=None):
        """
        Return a list projects in countries.
        """
        all_countries = [c[0] for c in COUNTRIES]
        countries = Project.objects.all().values_list('organization__country', flat=True)

        data = []
        for c in all_countries:
            data.append({'country': c, 'projects': len([k for k in countries if k == c])})
        return Response(status=status.HTTP_200_OK, data=data)


class OrganizationSerializer(ModelSerializer):
    class Meta:
        model = Organization
        fields = ('pk', 'name')


class SiteSerializer(ModelSerializer):
    latlng = SerializerMethodField()

    class Meta:
        model = Site
        fields = ('pk', 'name', 'latlng', 'region', 'type', 'current_progress')

    def get_latlng(self, obj):
        if obj.location:
            return [obj.location.y, obj.location.x]
        return None


class OrganizationViewset(ReadOnlyModelViewSet):
    queryset = Organization.objects.all().values('pk', 'name')
    serializer_class = OrganizationSerializer


class ExtremeLargeJsonResultsSetPagination(PageNumberPagination):
    page_size = 3000
    page_size_query_param = 'page_size'
    max_page_size = 200


class SiteViewset(ReadOnlyModelViewSet):
    queryset = Site.objects.all()
    serializer_class = SiteSerializer
    pagination_class = ExtremeLargeJsonResultsSetPagination

    def get_queryset(self):
        project_ids = self.request.GET.getlist('project_id')
        return self.queryset.filter(project__in=project_ids)


class ProjectSiteMetaAttributesView(APIView):
    permission_classes = [IsAuthenticated, ProjectDashboardPermissions]

    def get(self, request, *args, **kwargs):
        project_id = self.kwargs.get('pk', None)
        obj = get_object_or_404(Project, pk=project_id)

        json_questions = obj.site_meta_attributes
        filter_questions = []
        filter_types = ['Number', 'Form', 'Link', 'FormSubStat']
        [filter_questions.append(quest) for quest in json_questions if quest['question_type'] in filter_types]
        return Response(status=status.HTTP_200_OK, data={'site_meta_attributes_questions': filter_questions})


class FormQuestionsView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        fxf_id = self.kwargs.get('pk', None)
        obj = get_object_or_404(FieldSightXF, pk=fxf_id)

        json_questions = json.loads(obj.xf.json)
        filter_questions = []
        filter_types = ['group', 'integer', 'decimal']
        [filter_questions.append(quest) for quest in json_questions['children'] if quest['type'] in filter_types]

        return Response(status=status.HTTP_200_OK, data={'questions': filter_questions})