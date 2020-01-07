import ast

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
from onadata.apps.fv3.permissions.super_organization import SuperOrganizationAdminPermission

from onadata.apps.fsforms.models import OrganizationFormLibrary, FieldSightXF
from onadata.apps.fv3.serializers.SuperOrganizationSerializer import OrganizationSerializer, \
    OrganizationFormLibrarySerializer
from onadata.apps.fv3.serializer import TeamSerializer
from onadata.apps.logger.models import XForm


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
            """
                Add teams in super organization
            """
            Organization.objects.filter(id__in=team_ids).update(parent_id=pk)
            projects = Project.objects.filter(organization__id__in=team_ids)
            library_forms = OrganizationFormLibrary.objects.filter(organization=pk)
            fsxf_list = []
            for p in projects:
                for lf in library_forms:
                    fsxf = FieldSightXF(xf=lf.xf, project=p, is_deployed=True)
                    fsxf_list.append(fsxf)
            FieldSightXF.objects.bulk_create(fsxf_list)
            selected_teams_qs = Organization.objects.filter(parent_id=pk)
            selected_teams = TeamSerializer(selected_teams_qs, many=True).data
            return Response(status=status.HTTP_200_OK, data=selected_teams)

        elif team_id:
            """
                Remove team from super organization
            """
            Organization.objects.filter(id=team_id).update(parent_id=None)
            projects = Project.objects.filter(organization__id=team_id).values_list('id', flat=True)
            library_forms = OrganizationFormLibrary.objects.filter(organization=pk).values_list('xf', flat=True)

            FieldSightXF.objects.filter(project_id__in=projects, id__in=library_forms).update(is_deleted=True,
                                                                                              is_deployed=False)

            return Response(status=status.HTTP_200_OK, data={'detail': 'successfully removed.'})

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'detail': 'team_ids or team_id '
                                                                                'field is required.'})


class ManageSuperOrganizationLibraryView(APIView):

    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    permission_classes = [IsAuthenticated, SuperOrganizationAdminPermission]

    def get(self, request, pk, *args,  **kwargs):
        my_forms = XForm.objects.filter(user=request.user, deleted_xform=None)
        selected_org_forms = OrganizationFormLibrary.objects.filter(organization_id=pk).values('xf_id', 'xf__title')
        selected_form_ids = [form['xf_id'] for form in selected_org_forms if 'xf_id' in form]
        forms = my_forms.exclude(id__in=selected_form_ids).values('id', 'title')
        selected_forms = [{'id': form['xf_id'], 'title': form['xf__title']} for form in selected_org_forms]
        return Response(status=status.HTTP_200_OK, data={'forms': forms, 'selected_forms': selected_forms})

    def post(self, request, pk, format=None):
        xf_ids = request.data.get('xf_ids', None)
        xf_id = request.data.get('xf_id', None)
        form_type = request.data.get('form_type', None)
        schedule_level_id = request.data.get('schedule_level_id', None)
        date_range_start = request.data.get('date_range_start', None)
        date_range_end = request.data.get('date_range_end', None)
        selected_days = ast.literal_eval(request.data.get('selected_days', None))
        default_submission_status = request.data.get('default_submission_status', None)
        frequency = request.data.get('frequency', None)
        month_day = request.data.get('month_day', None)

        selected_days_objs = []

        for days in selected_days:
            selected_days_objs.append(days)

        if xf_ids:
            """
                Add forms in super organization form library
            """
            for org_form in xf_ids:
                org_form_lib = OrganizationFormLibrary.objects.create(xf_id=org_form,
                                                                      organization_id=pk,
                                                                      form_type=form_type,
                                                                      schedule_level_id=schedule_level_id,
                                                                      date_range_start=date_range_start,
                                                                      date_range_end=date_range_end,
                                                                      default_submission_status=default_submission_status,
                                                                      frequency=frequency,
                                                                      month_day=month_day
                                                                      )
                org_form_lib.selected_days.add(*selected_days_objs)

            selected_org_forms = OrganizationFormLibrary.objects.filter(organization_id=pk).values('xf_id', 'xf__title')
            selected_forms = [{'id': form['xf_id'], 'title': form['xf__title']} for form in selected_org_forms]
            return Response(status=status.HTTP_201_CREATED, data=selected_forms)

        elif xf_id:
            """
                Remove form from super organization library
            """
            OrganizationFormLibrary.objects.filter(xf_id=xf_id, organization_id=pk).update(deleted=True)
            return Response(status=status.HTTP_200_OK, data={'detail': 'successfully removed.'})

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'detail': 'xf_ids or xf_id '
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

    def perform_create(self, serializer):
        return serializer.save(organization_id=self.request.query_params.get('org'))

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.deleted = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
