from django.db.models import Count
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.authentication import BasicAuthentication
from rest_framework.views import APIView

from onadata.apps.fieldsight.models import SuperOrganization, Organization, Project
from rest_framework.permissions import IsAuthenticated
from onadata.apps.fsforms.enketo_utils import CsrfExemptSessionAuthentication
from django.contrib.gis.geos import Point
from rest_framework.response import Response
from onadata.apps.fv3.permissions.super_admin import SuperAdminPermission

from onadata.apps.fsforms.models import OrganizationFormLibrary, FieldSightXF
from onadata.apps.fv3.serializers.SuperOrganizationSerializer import OrganizationSerializer, \
    OrganizationFormLibrarySerializer
from onadata.apps.fv3.serializer import TeamSerializer


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = SuperOrganization.objects.all()
    serializer_class = OrganizationSerializer
    authentication_classes = [CsrfExemptSessionAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=False)
            self.object = self.perform_create(serializer)
            self.object.owner = self.request.user
            self.object.date_created = timezone.now()
            self.object.save()
            longitude = request.data.get('longitude', None)
            latitude = request.data.get('latitude', None)
            if latitude and longitude is not None:
                p = Point(round(float(longitude), 6), round(float(latitude), 6),
                          srid=4326)
                self.object.location = p
                self.object.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"test", str(e)})

    def perform_create(self, serializer):
        return serializer.save()


class SuperOrganizationListView(APIView):
    """
    A simple view for list of super organizations.
    """
    permission_classes = [IsAuthenticated, SuperAdminPermission]

    def get(self, request, *args, **kwargs):

        super_organizations = SuperOrganization.objects.all().annotate(teams=Count('organizations')).\
            values('id', 'name', 'teams')

        return Response(status=status.HTTP_200_OK, data=super_organizations)


class ManageTeamsView(APIView):

    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    permission_classes = [IsAuthenticated, SuperAdminPermission]

    def get(self, request, pk, *args,  **kwargs):
        queryset = Organization.objects.all()
        selected_teams_qs = queryset.filter(parent_id=pk)
        selected_teams = TeamSerializer(selected_teams_qs, many=True).data
        selected_team_ids = [team['id'] for team in selected_teams if 'id' in team]
        teams = queryset.exclude(id__in=selected_team_ids).values('id', 'name')
        is_superuser = True if request.user.is_superuser else False
        return Response(status=status.HTTP_200_OK, data={'teams': teams, 'selected_teams': selected_teams,
                                                         'is_superuser': is_superuser})

    def post(self, request, pk, format=None):
        team_ids = request.data.get('team_ids', None)
        team_id = request.data.get('team_id', None)

        if team_ids:
            Organization.objects.filter(id__in=team_ids).update(parent_id=pk)
            projects = Project.objects.filter(organization__id__in=team_ids)
            library_forms = OrganizationFormLibrary.objects.filter(organization=pk)
            fsxf_list = []
            for p in projects:
                for lf in library_forms:
                    fsxf = FieldSightXF(xf=lf.xf, project=p, is_deployed=True)
                    fsxf_list.append(fsxf)
            FieldSightXF.objects.bulk_create(fsxf_list)

            return Response(status=status.HTTP_200_OK, data={'detail': 'successfully updated.'})

        elif team_id:
            Organization.objects.get(id=team_id).update(parent_id=None)

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'detail': 'team_ids or team_id '
                                                                                'field is required.'})


class OrganizationFormLibraryVS(viewsets.ModelViewSet):
    queryset = OrganizationFormLibrary.objects.all()
    serializer_class = OrganizationFormLibrarySerializer
    authentication_classes = [CsrfExemptSessionAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        params = self.request.query_params
        org = params.get('org')
        if not org:
            return []
        return self.queryset.filter(organization=org)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.deleted = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
