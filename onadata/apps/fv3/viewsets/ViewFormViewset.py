from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Q, Case, When, F, IntegerField

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from onadata.apps.fieldsight.models import Project, Site
from onadata.apps.fsforms.models import FieldSightXF, Schedule, Stage, FInstance
from onadata.apps.fv3.serializers.ViewFormSerializer import ViewGeneralsAndSurveyFormSerializer, \
    ViewScheduledFormSerializer, ViewStageFormSerializer, ViewSubmissionStatusSerializer, FormSubmissionSerializer


class ProjectSiteResponsesViewSet(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, format=None):
        project = request.query_params.get('project', None)
        site = request.query_params.get('site', None)
        form_type = request.query_params.get('form_type', None)

        if form_type == 'general':
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
                generals = ViewGeneralsAndSurveyFormSerializer(generals_queryset, context={'is_project': is_project},
                                                     many=True).data

                general_deleted_qs = FieldSightXF.objects.filter(is_staged=False, is_scheduled=False,
                                                                    is_survey=False, is_deleted=True, project=project).\
                    annotate(response_count=Count('project_form_instances'))
                general_deleted_forms = ViewGeneralsAndSurveyFormSerializer(general_deleted_qs, context={'is_project':
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
                generals = ViewGeneralsAndSurveyFormSerializer(generals_queryset, many=True).data
                general_deleted_qs = FieldSightXF.objects.filter(is_staged=False, is_scheduled=False,
                                                                 is_survey=False, is_deleted=True, project=project).\
                    annotate(site_response_count=Count("site_form_instances"))
                general_deleted_forms = ViewGeneralsAndSurveyFormSerializer(general_deleted_qs,
                                                                      many=True).data
                return Response(status=status.HTTP_200_OK, data={'generals_forms': generals,
                                                                 'deleted_forms': general_deleted_forms})

        elif form_type == 'scheduled':
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
                general_deleted_forms = ViewGeneralsAndSurveyFormSerializer(scheduled_deleted_qs,
                                                                   many=True).data
                return Response(status=status.HTTP_200_OK, data={'scheduled_forms': scheduled,
                                                                 'deleted_forms': general_deleted_forms})

        elif form_type == 'stage':
            base_queryset = Stage.objects.filter(stage__isnull=True).order_by('order', 'date_created')

            if project is not None:
                try:
                    project = Project.objects.get(id=project, is_active=True)

                except ObjectDoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND, data={"detail": "Not found."})

                stage_queryset = base_queryset.filter(project=project)
                stage = ViewStageFormSerializer(stage_queryset, many=True).data

                # stage_deleted_qs = FieldSightXF.objects.filter(is_staged=True,  is_scheduled=False,
                #                                                is_survey=False, is_deleted=True, project=project)
                # stage_deleted_forms = ViewStageFormSerializer(stage_deleted_qs, many=True).data
                return Response(status=status.HTTP_200_OK, data={'stage_forms': stage,})
                                                                 # 'deleted_forms': stage_deleted_forms})
            elif site is not None:
                try:
                    site = Site.objects.get(id=site, is_active=True)
                except ObjectDoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND, data={"detail": "Not found."})
                project_id = site.project_id

                if site.type and site.region:
                    stage_queryset = base_queryset.filter(Q(site__id=site.id, project_stage_id=0)
                                                    | Q(project__id=project_id, tags__contains=[site.type_id])
                                                    | Q(project__id=project_id, regions__contains=[site.region_id])
                                                    )
                elif site.type:
                    stage_queryset = base_queryset.filter(Q(site__id=site.id, project_stage_id=0)
                                                    | Q(project__id=project_id, tags__contains=[site.type_id])
                                                    )
                elif site.region:
                    stage_queryset = base_queryset.filter(Q(site__id=site.id, project_stage_id=0)
                                                    | Q(project__id=project_id, regions__contains=[site.region_id])
                                                    )
                else:
                    stage_queryset = base_queryset.filter(
                        Q(site__id=site.id, project_stage_id=0)
                        | Q(project__id=project_id))
                stage = ViewStageFormSerializer(stage_queryset, many=True).data
                # stage_deleted_qs = FieldSightXF.objects.filter(is_staged=True, is_scheduled=False, is_survey=False,
                #                                                is_deleted=True).filter(Q(site__id=site.id,
                #                                                                          from_project=False)
                #                                                                        | Q(project__id=project_id))
                # stage_deleted_forms = ViewStageFormSerializer(stage_deleted_qs, many=True).data
                return Response(status=status.HTTP_200_OK, data={'stage_forms': stage})
                                                                 # 'deleted_forms': stage_deleted_forms})

        elif form_type == 'survey':
            try:
                project = Project.objects.get(id=project, is_active=True)

            except ObjectDoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND, data={"detail": "Not found."})

            is_project = True
            base_queryset = FieldSightXF.objects.filter(is_staged=False, is_scheduled=False, project=project,
                                                        is_survey=True)

            survey_qs = base_queryset.filter(is_deleted=False).annotate(response_count=Count('project_form_instances'))

            survey_forms = ViewGeneralsAndSurveyFormSerializer(survey_qs, many=True, context={'is_project': is_project}).data

            survey_deleted_qs = base_queryset.filter(is_deleted=True).\
                annotate(response_count=Count('project_form_instances'))
            survey_deleted_forms = ViewGeneralsAndSurveyFormSerializer(survey_deleted_qs, many=True, context={'is_project':
                                                                                                       is_project}).data
            return Response(status=status.HTTP_200_OK, data={'survey_forms': survey_forms,
                                                             'deleted_forms': survey_deleted_forms})


class ProjectSiteSubmissionStatusViewSet(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, format=None):
        project = request.query_params.get('project', None)
        site = request.query_params.get('site', None)
        submission_status = request.query_params.get('submission_status', None)

        if submission_status == 'rejected':
            base_queryset = FInstance.objects.select_related('project_fxf__xf', 'site_fxf__xf', 'submitted_by').\
                filter(form_status='1').order_by('-date')
            if project is not None:
                try:
                    project = Project.objects.get(id=project, is_active=True)

                except ObjectDoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND, data={"detail": "Not found."})

                rejected_queryset = base_queryset.filter(project=project, project_fxf_id__isnull=False)
                rejected_submissions = ViewSubmissionStatusSerializer(rejected_queryset, many=True).data

                return Response(status=status.HTTP_200_OK, data={'rejected_submissions': rejected_submissions})
            elif site is not None:
                try:
                    site = Site.objects.get(id=site, is_active=True)
                except ObjectDoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND, data={"detail": "Not found."})

                rejected_queryset = base_queryset.filter(site=site)
                rejected_submissions = ViewSubmissionStatusSerializer(rejected_queryset, many=True).data

                return Response(status=status.HTTP_200_OK, data={'rejected_submissions': rejected_submissions})

        if submission_status == 'flagged':
            base_queryset = FInstance.objects.select_related('project_fxf__xf', 'site_fxf__xf', 'submitted_by').\
                filter(form_status='2').order_by('-date')
            if project is not None:
                try:
                    project = Project.objects.get(id=project, is_active=True)

                except ObjectDoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND, data={"detail": "Not found."})

                flagged_queryset = base_queryset.filter(project=project, project_fxf_id__isnull=False)
                flagged_submissions = ViewSubmissionStatusSerializer(flagged_queryset, many=True).data

                return Response(status=status.HTTP_200_OK, data={'flagged_submissions': flagged_submissions})
            elif site is not None:
                try:
                    site = Site.objects.get(id=site, is_active=True)
                except ObjectDoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND, data={"detail": "Not found."})

                flagged_queryset = base_queryset.filter(site=site)
                flagged_submissions = ViewSubmissionStatusSerializer(flagged_queryset, many=True).data

                return Response(status=status.HTTP_200_OK, data={'flagged_submissions': flagged_submissions})

        if submission_status == 'pending':
            base_queryset = FInstance.objects.select_related('project_fxf__xf', 'site_fxf__xf', 'submitted_by').\
                filter(form_status='0').order_by('-date')
            if project is not None:
                try:
                    project = Project.objects.get(id=project, is_active=True)

                except ObjectDoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND, data={"detail": "Not found."})

                pending_queryset = base_queryset.filter(project=project, project_fxf_id__isnull=False)
                pending_submissions = ViewSubmissionStatusSerializer(pending_queryset, many=True).data

                return Response(status=status.HTTP_200_OK, data={'pending_submissions': pending_submissions})
            elif site is not None:
                try:
                    site = Site.objects.get(id=site, is_active=True)
                except ObjectDoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND, data={"detail": "Not found."})

                pending_queryset = base_queryset.filter(site=site)
                pending_submissions = ViewSubmissionStatusSerializer(pending_queryset, many=True).data

                return Response(status=status.HTTP_200_OK, data={'pending_submissions': pending_submissions})

        if submission_status == 'approved':
            base_queryset = FInstance.objects.select_related('project_fxf__xf', 'site_fxf__xf', 'submitted_by').\
                filter(form_status='3').order_by('-date')
            if project is not None:
                try:
                    project = Project.objects.get(id=project, is_active=True)

                except ObjectDoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND, data={"detail": "Not found."})

                approved_queryset = base_queryset.filter(project=project, project_fxf_id__isnull=False)
                approved_submissions = ViewSubmissionStatusSerializer(approved_queryset, many=True).data

                return Response(status=status.HTTP_200_OK, data={'approved_submissions': approved_submissions})
            elif site is not None:
                try:
                    site = Site.objects.get(id=site, is_active=True)
                except ObjectDoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND, data={"detail": "Not found."})

                approved_queryset = base_queryset.filter(site=site)
                approved_submissions = ViewSubmissionStatusSerializer(approved_queryset, many=True).data

                return Response(status=status.HTTP_200_OK, data={'approved_submissions': approved_submissions})


class FormSubmissionsViewSet(APIView):

    def get(self, request, format=None):
        project = request.query_params.get('project', None)
        site = request.query_params.get('site', None)
        fsxf_id = request.query_params.get('fsxf_id', None)

        if project and fsxf_id is not None:
            try:
                fsxf = FieldSightXF.objects.get(pk=fsxf_id)

            except ObjectDoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND, data={"detail": "Not found."})

            queryset = FInstance.objects.filter(project_fxf=fsxf.id)
            data = FormSubmissionSerializer(queryset, many=True).data

            return Response(status=status.HTTP_200_OK, data=data)

