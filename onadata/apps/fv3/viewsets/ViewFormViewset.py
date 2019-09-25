from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Q, Case, When, F, IntegerField

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from onadata.apps.fieldsight.models import Project, Site
from onadata.apps.fsforms.models import FieldSightXF, Schedule, Stage
from onadata.apps.fv3.serializers.ViewFormSerializer import ViewGeneralsFormSerializer, ViewScheduledFormSerializer, \
    ViewStageFormSerializer


class ProjectSiteResponsesView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, format=None):
        project = request.query_params.get('project', None)
        site = request.query_params.get('site', None)
        type = request.query_params.get('type', None)

        if type == 'general':
            base_queryset = FieldSightXF.objects.select_related('xf').filter(is_staged=False, is_scheduled=False,
                                                                             is_deleted=False, is_survey=False)
            if project is not None:
                try:
                    project = Project.objects.get(id=project, is_active=True)

                except ObjectDoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND, data={"detail": "Not found."})

                is_project = True
                generals_queryset = base_queryset.filter(project=project).annotate(response_count=
                                                                                   Count('project_form_instances'))
                generals = ViewGeneralsFormSerializer(generals_queryset, context={'is_project': is_project},
                                                     many=True).data

                general_deleted_qs = FieldSightXF.objects.filter(is_staged=False, is_scheduled=False,
                                                                    is_survey=False, is_deleted=True, project=project).\
                    annotate(response_count=Count('project_form_instances'))
                general_deleted_forms = ViewGeneralsFormSerializer(general_deleted_qs, context={'is_project':
                                                                                                          is_project},
                                                                      many=True).data
                return Response(status=status.HTTP_200_OK, data={'generals_forms': generals,
                                                                 'deleted_forms': general_deleted_forms})

            elif site is not None:
                try:
                    site = Site.objects.get(id=site, is_active=True)
                except ObjectDoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND, data={"detail": "Not found."})
                project_id = site.project_id

                if site.type and site.region:

                    generals_queryset = base_queryset.filter(Q(site__id=site.id, from_project=False)
                                               | Q(project__id=project_id, settings__isnull=True)
                                               | Q(project__id=project_id, settings__types__contains=[site.type_id]),
                                               settings__regions__contains=[site.region_id])
                elif site.type:
                    generals_queryset = base_queryset.filter(Q(site__id=site.id, from_project=False)
                                               | Q(project__id=project_id, settings__isnull=True)
                                               | Q(project__id=project_id, settings__types__contains=[site.type_id]))
                elif site.region:
                    generals_queryset = base_queryset.filter(Q(site__id=site.id, from_project=False)
                                               | Q(project__id=project_id, settings__isnull=True)
                                               | Q(project__id=project_id,
                                                   settings__regions__contains=[site.region_id]))
                else:
                    generals_queryset = base_queryset.filter(Q(site__id=site.id, from_project=False) |
                                                             Q(project__id=project_id))
                generals_queryset = generals_queryset.annotate(site_response_count=Count("site_form_instances"),
                                                               response_count=Count(Case(When(project__isnull=False,
                                                                                              project_form_instances__site__id=site.id,
                                                                                              then=F('project_form_instances')),
                                                                                         output_field=IntegerField(),),
                                                                                    distinct=True))
                generals = ViewGeneralsFormSerializer(generals_queryset, many=True).data
                general_deleted_qs = FieldSightXF.objects.filter(is_staged=False, is_scheduled=False,
                                                                 is_survey=False, is_deleted=True, project=project).\
                    annotate(site_response_count=Count("site_form_instances"))
                general_deleted_forms = ViewGeneralsFormSerializer(general_deleted_qs,
                                                                      many=True).data
                return Response(status=status.HTTP_200_OK, data={'generals_forms': generals,
                                                                 'deleted_forms': general_deleted_forms})

        elif type == 'scheduled':
            base_queryset = Schedule.objects.filter(schedule_forms__isnull=False, schedule_forms__is_deleted=False)

            if project is not None:
                try:
                    project = Project.objects.get(id=project, is_active=True)

                except ObjectDoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND, data={"detail": "Not found."})

                is_project = True
                schedule_queryset = base_queryset.filter(project=project).annotate(response_count=
                                                                                   Count('schedule_forms__project_form_instances'))
                scheduled = ViewScheduledFormSerializer(schedule_queryset, context={'is_project': is_project},
                                                         many=True).data

                scheduled_deleted_qs = Schedule.objects.filter(schedule_forms__isnull=False,
                                                             schedule_forms__is_deleted=True, project=project). \
                    annotate(response_count=Count('schedule_forms__project_form_instances'))
                general_deleted_forms = ViewScheduledFormSerializer(scheduled_deleted_qs, context={'is_project':
                                                                                                       is_project},
                                                                      many=True).data
                return Response(status=status.HTTP_200_OK, data={'scheduled_forms': scheduled,
                                                                 'deleted_forms': general_deleted_forms})
            elif site is not None:
                try:
                    site = Site.objects.get(id=site, is_active=True)
                except ObjectDoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND, data={"detail": "Not found."})
                project_id = site.project_id

                if site.type and site.region:

                    scheduled_queryset = base_queryset.filter(Q(site__id=site.id)
                                               | Q(project__id=project_id, schedule_forms__settings__isnull=True)
                                               | Q(project__id=project_id,
                                                   schedule_forms__settings__types__contains=[site.type_id]),
                                               schedule_forms__settings__regions__contains=[site.region_id])
                elif site.type:
                    scheduled_queryset = base_queryset.filter(Q(site__id=site.id)
                                               | Q(project__id=project_id, schedule_forms__settings__isnull=True)
                                               | Q(project__id=project_id,
                                                   schedule_forms__settings__types__contains=[site.type_id]))
                elif site.region:
                    scheduled_queryset = base_queryset.filter(Q(site__id=site.id, )
                                               | Q(project__id=project_id, schedule_forms__settings__isnull=True)
                                               | Q(project__id=project_id,
                                                   schedule_forms__settings__regions__contains=[site.region_id]))
                else:
                    scheduled_queryset = base_queryset.filter(Q(site__id=site.id) | Q(project__id=project_id))

                scheduled_queryset = scheduled_queryset.annotate(
                    site_response_count=Count(
                        "schedule_forms__site_form_instances", ),
                    response_count=Count(Case(
                        When(project__isnull=False,
                             schedule_forms__project_form_instances__site__id=site.id,
                             then=F('schedule_forms__project_form_instances')),
                        output_field=IntegerField(),
                    ), distinct=True)

                ).select_related('schedule_forms', 'schedule_forms__xf',
                                 'schedule_forms__em')
                scheduled = ViewScheduledFormSerializer(scheduled_queryset, many=True).data
                scheduled_deleted_qs = Schedule.objects.filter(schedule_forms__isnull=False,
                                                               schedule_forms__is_deleted=True, project=project). \
                    annotate(site_response_count=Count("schedule_forms__site_form_instances"))
                general_deleted_forms = ViewGeneralsFormSerializer(scheduled_deleted_qs,
                                                                   many=True).data
                return Response(status=status.HTTP_200_OK, data={'scheduled_forms': scheduled,
                                                                 'deleted_forms': general_deleted_forms})

        elif type == 'stage':
            base_queryset = Stage.objects.filter(stage_forms__isnull=True,
                                                 stage__isnull=True).order_by('order', 'date_created')

            if project is not None:
                try:
                    project = Project.objects.get(id=project, is_active=True)

                except ObjectDoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND, data={"detail": "Not found."})

                is_project = True
                stage_queryset = base_queryset.filter(project=project).annotate(response_count=
                                                                                   Count('stage_forms__project_form_instances'))
                stage = ViewStageFormSerializer(stage_queryset, context={'is_project': is_project},
                                                        many=True).data

                stage_deleted_qs = Stage.objects.filter(stage_forms__isnull=False, stage_forms__is_deleted=True,
                                                        project=project). \
                    annotate(response_count=Count('stage_forms__project_form_instances'))
                stage_deleted_forms = ViewStageFormSerializer(stage_deleted_qs, context={'is_project':
                                                                                                       is_project},
                                                                      many=True).data
                return Response(status=status.HTTP_200_OK, data={'stage_forms': stage,
                                                                 'deleted_forms': stage_deleted_forms})
            elif site is not None:
                try:
                    site = Site.objects.get(id=site, is_active=True)
                except ObjectDoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND, data={"detail": "Not found."})
                project_id = site.project_id

                if site.type and site.region:

                    scheduled_queryset = base_queryset.filter(Q(site__id=site.id)
                                               | Q(project__id=project_id, schedule_forms__settings__isnull=True)
                                               | Q(project__id=project_id,
                                                   schedule_forms__settings__types__contains=[site.type_id]),
                                               schedule_forms__settings__regions__contains=[site.region_id])
                elif site.type:
                    scheduled_queryset = base_queryset.filter(Q(site__id=site.id)
                                               | Q(project__id=project_id, schedule_forms__settings__isnull=True)
                                               | Q(project__id=project_id,
                                                   schedule_forms__settings__types__contains=[site.type_id]))
                elif site.region:
                    scheduled_queryset = base_queryset.filter(Q(site__id=site.id, )
                                               | Q(project__id=project_id, schedule_forms__settings__isnull=True)
                                               | Q(project__id=project_id,
                                                   schedule_forms__settings__regions__contains=[site.region_id]))
                else:
                    scheduled_queryset = base_queryset.filter(Q(site__id=site.id) | Q(project__id=project_id))

                scheduled_queryset = scheduled_queryset.annotate(
                    site_response_count=Count(
                        "schedule_forms__site_form_instances", ),
                    response_count=Count(Case(
                        When(project__isnull=False,
                             schedule_forms__project_form_instances__site__id=site.id,
                             then=F('schedule_forms__project_form_instances')),
                        output_field=IntegerField(),
                    ), distinct=True)

                ).select_related('schedule_forms', 'schedule_forms__xf',
                                 'schedule_forms__em')
                scheduled = ViewStageFormSerializer(scheduled_queryset, many=True).data
                scheduled_deleted_qs = Schedule.objects.filter(schedule_forms__isnull=False,
                                                               schedule_forms__is_deleted=True, project=project). \
                    annotate(site_response_count=Count("schedule_forms__site_form_instances"))
                general_deleted_forms = ViewStageFormSerializer(scheduled_deleted_qs,
                                                                   many=True).data
                return Response(status=status.HTTP_200_OK, data={'scheduled_forms': scheduled,
                                                                 'deleted_forms': general_deleted_forms})