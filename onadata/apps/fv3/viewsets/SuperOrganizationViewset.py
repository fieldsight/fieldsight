import ast

from datetime import datetime
from django.db.models import Count, Prefetch, F
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.authentication import BasicAuthentication
from rest_framework.views import APIView

from onadata.apps.eventlog.models import CeleryTaskProgress
from onadata.apps.fieldsight.models import SuperOrganization, Organization, Project, Site, Region
from rest_framework.permissions import IsAuthenticated
from onadata.apps.fsforms.enketo_utils import CsrfExemptSessionAuthentication
from django.contrib.gis.geos import Point
from rest_framework.response import Response
from onadata.apps.fv3.permissions.super_admin import SuperAdminPermission
from onadata.apps.fv3.permissions.super_organization import SuperOrganizationAdminPermission

from onadata.apps.fsforms.models import OrganizationFormLibrary, FieldSightXF, FInstance, Schedule
from onadata.apps.fv3.serializers.SuperOrganizationSerializer import OrganizationSerializer, \
    OrganizationFormLibrarySerializer, OrganizationGeneralScheduledFormSerializer
from onadata.apps.fv3.serializer import TeamSerializer
from onadata.apps.fv3.serializers.TeamSerializer import TeamProjectSerializer
from onadata.apps.logger.models import XForm
from onadata.apps.userrole.models import UserRole
from onadata.apps.fieldsight.tasks import add_forms_in_projects


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
    permission_classes = [IsAuthenticated, SuperOrganizationAdminPermission]

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
            for project in projects:
                for obj in library_forms:
                    if obj.form_type == 0:
                        fsxf = FieldSightXF(xf=obj.xf, project=project, is_deployed=True,
                                            default_submission_status=obj.default_submission_status)
                        fsxf_list.append(fsxf)
                    else:
                        scheduled_obj = Schedule.objects. \
                            create(project=project, date_range_start=obj.date_range_start,
                                   date_range_end=obj.date_range_end,
                                   schedule_level_id=obj.schedule_level_id, frequency=obj.frequency,
                                   month_day=obj.month_day)
                        scheduled_obj.selected_days.add(*obj.selected_days.values_list('id', flat=True))
                        scheduled_obj.save()
                        scheduled_fxf = FieldSightXF(xf=obj.xf, project=project, is_deployed=True,
                                                     is_scheduled=True,
                                                     default_submission_status=obj.default_submission_status,
                                                     schedule=scheduled_obj)
                        fsxf_list.append(scheduled_fxf)

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
        queryset = OrganizationFormLibrary.objects.select_related('xf').filter(organization_id=pk, deleted=False)
        org_form_lib_ids = queryset.values_list('xf_id', flat=True)
        my_forms = XForm.objects.filter(user=request.user, deleted_xform=None).exclude(id__in=org_form_lib_ids)

        selected_form_ids = []
        selected_general_org_forms = queryset.filter(form_type=0, is_form_library=False)
        selected_scheduled_org_forms = queryset.filter(form_type=1,  is_form_library=False)
        organization_library_forms = queryset.filter(is_form_library=True)
        organization_library_forms = [{'id': form.id, 'xf_id': form.xf.id, 'title': form.xf.title}
                                      for form in organization_library_forms]
        selected_organization_library_forms = [{'id': form.id, 'xf_id': form.xf.id, 'title': form.xf.title}
                                               for form in queryset.distinct('xf_id')]

        general_forms = OrganizationGeneralScheduledFormSerializer(selected_general_org_forms, many=True)
        scheduled_forms = OrganizationGeneralScheduledFormSerializer(selected_scheduled_org_forms, many=True)

        forms = my_forms.exclude(id__in=list(selected_form_ids)).annotate(xf_id=F('id')).values('xf_id', 'title')

        return Response(status=status.HTTP_200_OK, data={'forms': forms,
                                                         'selected_forms':
                                                             {'general_forms': general_forms.data,
                                                              'scheduled_forms': scheduled_forms.data},
                                                             'organization_library_forms': organization_library_forms,
                                                         'selected_organization_library_forms':
                                                             selected_organization_library_forms
                                                         },
                        )

    def post(self, request, pk, format=None):
        xf_ids = request.data.get('xf_ids', None)
        id = request.data.get('id', None)
        form_type = request.data.get('form_type', None)
        schedule_level_id = request.data.get('schedule_level_id', None)
        date_range_start = request.data.get('date_range_start', None)
        date_range_end = request.data.get('date_range_end', None)
        selected_days = request.data.get('selected_days', None)
        default_submission_status = request.data.get('default_submission_status', None)
        frequency = request.data.get('frequency', None)
        month_day = request.data.get('month_day', None)
        is_form_library = request.data.get('is_form_library', False)

        if date_range_start:
            date_range_start = datetime.strptime(date_range_start, "%Y-%m-%d")

        if date_range_end:
            date_range_end = datetime.strptime(date_range_end, "%Y-%m-%d")

        if selected_days:
            selected_days_objs = []
            for days in selected_days:
                selected_days_objs.append(days)
        else:
            selected_days_objs = []

        if xf_ids and is_form_library is False:
            """
                Add default form in super organization
            """

            org_form_lib = OrganizationFormLibrary.objects.create(xf_id=xf_ids,
                                                                  organization_id=pk,
                                                                  form_type=form_type,
                                                                  schedule_level_id=schedule_level_id,
                                                                  date_range_start=date_range_start,
                                                                  date_range_end=date_range_end,
                                                                  default_submission_status=default_submission_status,
                                                                  frequency=frequency,
                                                                  month_day=month_day,
                                                                  is_form_library=is_form_library
                                                                  )
            org_form_lib.selected_days.add(*selected_days_objs)
            org_form_lib.save()

            task_obj = CeleryTaskProgress.objects.create(user=request.user, task_type=27, content_object=org_form_lib)
            if task_obj:
                task = add_forms_in_projects.delay(org_form_lib.id, task_obj.id)
                task_obj.task_id = task.id
                task_obj.save()

            selected_general_org_forms = OrganizationFormLibrary.objects.filter(organization_id=pk, form_type=0,
                                                                                deleted=False)
            selected_scheduled_org_forms = OrganizationFormLibrary.objects.filter(organization_id=pk, form_type=1,
                                                                                  deleted=False)

            general_forms = [{'id': general_form.xf.id,
                              'title': general_form.xf.title,
                              'form_type': general_form.get_form_type_display(),
                              'default_submission_status': general_form.get_default_submission_status_display()
                              } for general_form in selected_general_org_forms]

            scheduled_forms = [{'id': scheduled_form.xf.id,
                                'title': scheduled_form.xf.title,
                                'form_type': scheduled_form.get_form_type_display(),
                                'default_submission_status': scheduled_form.get_default_submission_status_display(),
                                'scheduled_type': scheduled_form.get_schedule_level_id_display(),
                                'start_date': scheduled_form.date_range_start,
                                'end_date': scheduled_form.date_range_end}
                               for scheduled_form in selected_scheduled_org_forms]

            return Response(status=status.HTTP_201_CREATED, data={'general_forms': general_forms,
                                                                  'scheduled_forms': scheduled_forms})

        elif xf_ids and is_form_library:
            """
                Add library form in super organization
            """

            org_form_lib_objs = []
            for xf_id in xf_ids:
                org_form_lib = OrganizationFormLibrary(xf_id=xf_id,
                                                       organization_id=pk,
                                                       is_form_library=is_form_library,
                                                       form_type=2

                                                       )
                org_form_lib_objs.append(org_form_lib)
            OrganizationFormLibrary.objects.bulk_create(org_form_lib_objs)
            organization_library_forms = OrganizationFormLibrary.objects.filter(organization_id=pk, deleted=False,
                                                                                is_form_library=True)
            organization_library_forms = [{'id': form.xf.id, 'title': form.xf.title} for form in
                                          organization_library_forms]

            return Response(status=status.HTTP_201_CREATED,
                            data={'organization_library_forms': organization_library_forms})

        elif id:
            """
                Remove default/library form super organization.
            """
            org_form_obj = OrganizationFormLibrary.objects.get(id=id, organization_id=pk)
            org_form_obj.deleted = True
            org_form_obj.save()

            return Response(status=status.HTTP_200_OK, data={'detail': 'successfully removed.'})

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'detail': 'xf_ids or id '
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


class GetOrganizationLocation(APIView):
    permission_classes = [IsAuthenticated, SuperOrganizationAdminPermission]

    def get(self, request, pk, *args, **kwargs):
        location = SuperOrganization.objects.get(id=pk).location

        return Response(status=status.HTTP_200_OK, data={'location': str(location)})


class OrganizationProjectsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Project.objects.all()
    serializer_class = TeamProjectSerializer
    permission_classes = [IsAuthenticated, SuperOrganizationAdminPermission]

    def get_queryset(self):
        return self.queryset.prefetch_related(Prefetch(
            'project_roles',
            queryset=UserRole.objects.filter(ended_at=None).distinct('user')
        ), Prefetch(
            'project_instances',
            queryset=FInstance.objects.filter(is_deleted=False)

        ), Prefetch(
            'project_region',
            queryset=Region.objects.filter(is_active=True, parent__isnull=True)
        ), Prefetch(
            'sites',
            queryset=Site.objects.filter(is_active=True, is_survey=False, site__isnull=True)
        )).filter(organization__parent__id=self.kwargs.get('pk'), is_active=True)

    def list(self, request, *args, **kwargs):
        projects = self.serializer_class(self.get_queryset(), many=True).data
        organization = SuperOrganization.objects.get(id=self.kwargs.get('pk'))

        data = {'projects': projects, 'breadcrumbs': {'name': 'Projects', 'organization': organization.name,
                                                      'organization_url': organization.get_absolute_url()}}

        return Response(data)


class OrganizationTeamsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Organization.objects.select_related('owner').prefetch_related('projects')
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated, SuperOrganizationAdminPermission]

    def get_queryset(self):
        return self.queryset.filter(parent_id=self.kwargs.get('pk'))

    def list(self, request, *args, **kwargs):
        organization = SuperOrganization.objects.get(id=self.kwargs.get('pk'))

        queryset = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(queryset, many=True)
        return Response({'teams': serializer.data, 'breadcrumbs': {'name': 'Teams list',
                                                                   'organization': organization.name,
                                                                   'organization_url': organization.get_absolute_url()}})

