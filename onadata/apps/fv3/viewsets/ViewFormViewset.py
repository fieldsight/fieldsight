import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Q, Case, When, F, IntegerField

from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from onadata.apps.fieldsight.models import Project, Site, SuperOrganization
from onadata.apps.fsforms.models import FieldSightXF, Schedule, Stage, FInstance, XformHistory, OrganizationFormLibrary
from onadata.apps.fsforms.reports_util import delete_form_instance
from onadata.apps.fsforms.templatetags.fs_filters import get_xform_version
from onadata.apps.fv3.serializers.ViewFormSerializer import ViewGeneralsAndSurveyFormSerializer, \
    ViewScheduledFormSerializer, ViewStageFormSerializer, ViewSubmissionStatusSerializer, FormSubmissionSerializer, \
    ViewSubStageFormSerializer, SubmissionsVersionSerializer
from onadata.apps.fv3.permissions.view_by_forms_status_perm import ViewDataPermission, DeleteFInstancePermission
from onadata.apps.logger.models import XForm


class SubmissionStatusPagination(PageNumberPagination):
    page_size = 200


class ProjectSiteResponsesView(APIView):
    permission_classes = (IsAuthenticated, ViewDataPermission)

    def get_breadcrumbs(self, is_project, object):
        if is_project:

            breadcrumbs = {'project_name': object.name, 'project_url': object.get_absolute_url(),
                           'current_page': 'Responses'}
        else:
            breadcrumbs = {'site_name': object.name, 'site_url': object.get_absolute_url(), 'current_page': 'Responses'}

        return breadcrumbs

    def get(self, request, format=None):
        project = request.query_params.get('project', None)
        site = request.query_params.get('site', None)
        form_type = request.query_params.get('form_type', None)

        if form_type == 'general':
            base_queryset = FieldSightXF.objects.filter(is_staged=False, is_scheduled=False, is_deleted=False, is_survey=False)
            if project is not None:
                is_project = True
                generals_queryset = base_queryset.filter(project_id=project).select_related('xf', 'xf__user', 'project').\
                    prefetch_related('xf__fshistory', 'project_form_instances')
                generals = ViewGeneralsAndSurveyFormSerializer(generals_queryset, context={'is_project': is_project},
                                                               many=True).data

                general_deleted_qs = FieldSightXF.objects.select_related('xf', 'xf__user', 'project').\
                    prefetch_related('xf__fshistory', 'project_form_instances').filter(is_staged=False,
                                                                                       is_scheduled=False,
                                                                                       is_survey=False,
                                                                                       is_deleted=True,
                                                                                       project_id=project)
                general_deleted_forms = ViewGeneralsAndSurveyFormSerializer(general_deleted_qs, context={'is_project':
                                                                                                          is_project},
                                                                      many=True).data
                project = Project.objects.get(id=project)

                return Response(status=status.HTTP_200_OK, data={'generals_forms': generals,
                                                                 'deleted_forms': general_deleted_forms,
                                                                 'breadcrumbs': self.get_breadcrumbs(True, project)
                                                                 })

            elif site is not None:
                try:
                    site = Site.objects.get(id=site)
                except ObjectDoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND, data={"detail": "Not found."})

                project_id = site.project_id
                project = site.project
                types_count = project.types.count()

                if project.cluster_sites and types_count:
                    if not site.type:
                        site.type_id = 0
                    if not site.region:
                        site.region_id = 0
                    generals_queryset = base_queryset.filter(Q(site__id=site.id, from_project=False)
                                               | Q(project__id=project_id, settings__isnull=True)
                                               | Q(project__id=project_id, settings__types__contains=[site.type_id],
                                                   settings__regions__contains=[site.region_id]))
                elif project.cluster_sites:
                    if not site.region:
                        site.region_id = 0
                    generals_queryset = base_queryset.filter(Q(site__id=site.id, from_project=False)
                                               | Q(project__id=project_id, settings__isnull=True)
                                               | Q(project__id=project_id,
                                                   settings__regions__contains=[site.region_id]))
                elif types_count > 0:
                    if not site.type:
                        site.type_id = 0
                    generals_queryset = base_queryset.filter(Q(site__id=site.id, from_project=False)
                                               | Q(project__id=project_id, settings__isnull=True)
                                               | Q(project__id=project_id, settings__types__contains=[site.type_id]))
                else:
                    generals_queryset = base_queryset.filter(Q(site__id=site.id, from_project=False) |
                                                             Q(project__id=project_id))

                generals_queryset = generals_queryset.\
                    select_related('xf', 'xf__user', 'site', 'project').prefetch_related('xf__fshistory',
                                                                                         'site_form_instances')
                generals = ViewGeneralsAndSurveyFormSerializer(generals_queryset, many=True,
                                                               context={'site': site.id}).data
                general_deleted_qs = FieldSightXF.objects.filter(is_staged=False, is_scheduled=False,
                                                                 is_survey=False, is_deleted=True)\
                    .filter(Q(site__id=site.id, from_project=False) | Q(project__id=project_id))\
                            .select_related('xf', 'xf__user', 'site', 'project').prefetch_related('xf__fshistory',
                                                                                         'site_form_instances')
                general_deleted_forms = ViewGeneralsAndSurveyFormSerializer(general_deleted_qs,
                                                                      many=True, context={'site': site.id}).data
                return Response(status=status.HTTP_200_OK, data={'generals_forms': generals,
                                                                 'deleted_forms': general_deleted_forms,
                                                                 'breadcrumbs': self.get_breadcrumbs(False, site)
                                                                 })

        elif form_type == 'scheduled':
            base_queryset = Schedule.objects.filter(schedule_forms__isnull=False, schedule_forms__is_deleted=False)

            if project is not None:

                is_project = True
                schedule_queryset = base_queryset.select_related('schedule_forms', 'schedule_forms__xf',
                                                                 'schedule_forms__xf__user').\
                    prefetch_related('schedule_forms__project_form_instances', 'schedule_forms__xf__fshistory').\
                    filter(project_id=project)
                scheduled = ViewScheduledFormSerializer(schedule_queryset, context={'is_project': is_project},
                                                         many=True).data

                scheduled_deleted_qs = Schedule.objects.select_related('schedule_forms', 'schedule_forms__xf',
                                                                 'schedule_forms__xf__user').\
                    prefetch_related('schedule_forms__project_form_instances', 'schedule_forms__xf__fshistory')\
                    .filter(schedule_forms__is_staged=False, schedule_forms__is_scheduled=True,
                            schedule_forms__is_survey=False, schedule_forms__is_deleted=True, project_id=project)
                scheduled_deleted_forms = ViewScheduledFormSerializer(scheduled_deleted_qs, context={'is_project':
                                                                                                       is_project},
                                                                      many=True).data
                project = Project.objects.get(id=project)

                return Response(status=status.HTTP_200_OK, data={'scheduled_forms': scheduled,
                                                                 'deleted_forms': scheduled_deleted_forms,
                                                                 'breadcrumbs': self.get_breadcrumbs(True, project)

                                                                 })
            elif site is not None:
                try:
                    site = Site.objects.get(id=site)
                except ObjectDoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND, data={"detail": "Not found."})
                project_id = site.project_id
                project = site.project
                types_count = project.types.count()

                if project.cluster_sites and types_count:
                    if not site.type:
                        site.type_id = 0
                    if not site.region:
                        site.region_id = 0
                    scheduled_queryset = base_queryset.filter(Q(site__id=site.id)
                                               | Q(project__id=project_id, schedule_forms__settings__isnull=True)
                                               | Q(project__id=project_id,
                                                   schedule_forms__settings__types__contains=[site.type_id],
                                                   schedule_forms__settings__regions__contains=[site.region_id]))
                elif types_count > 0:
                    if not site.type_id:
                        site.type_id = 0
                    scheduled_queryset = base_queryset.filter(Q(site__id=site.id)
                                               | Q(project__id=project_id, schedule_forms__settings__isnull=True)
                                               | Q(project__id=project_id,
                                                   schedule_forms__settings__types__contains=[site.type_id]))
                elif project.cluster_sites:
                    if not site.region:
                        site.region_id = 0
                    scheduled_queryset = base_queryset.filter(Q(site__id=site.id)
                                               | Q(project__id=project_id, schedule_forms__settings__isnull=True)
                                               | Q(project__id=project_id,
                                                   schedule_forms__settings__regions__contains=[site.region_id]))
                else:
                    scheduled_queryset = base_queryset.filter(Q(site__id=site.id) | Q(project__id=project_id))

                scheduled_queryset = scheduled_queryset.select_related('schedule_forms', 'schedule_forms__xf',
                                                                       'schedule_forms__xf__user', 'project', 'site').\
                    prefetch_related('schedule_forms__site_form_instances', 'schedule_forms__xf__fshistory')
                scheduled = ViewScheduledFormSerializer(scheduled_queryset, context={'site': site.id},
                                                        many=True).data
                scheduled_deleted_qs = Schedule.objects.select_related('schedule_forms', 'schedule_forms__xf',
                                                                       'schedule_forms__xf__user', 'project',
                                                                       'site'). \
                    prefetch_related('schedule_forms__site_form_instances', 'schedule_forms__xf__fshistory').\
                    filter(schedule_forms__is_staged=False, schedule_forms__is_scheduled=True,
                           schedule_forms__is_survey=False, schedule_forms__is_deleted=True, project_id=project).\
                    filter(Q(schedule_forms__site__id=site.id, schedule_forms__from_project=False) |
                           Q(project__id=project_id))

                scheduled_deleted_forms = ViewScheduledFormSerializer(scheduled_deleted_qs,
                                                                   many=True).data
                return Response(status=status.HTTP_200_OK, data={'scheduled_forms': scheduled,
                                                                 'deleted_forms': scheduled_deleted_forms,
                                                                 'breadcrumbs': self.get_breadcrumbs(False, site)

                                                                 })

        elif form_type == 'stage':
            base_queryset = Stage.objects.filter(stage__isnull=True).order_by('order', 'date_created')

            if project is not None:
                is_project = True

                stage_queryset = base_queryset.filter(project_id=project)
                stage = ViewStageFormSerializer(stage_queryset, context={'is_project': is_project}, many=True).data

                stage_deleted_qs = Stage.objects.order_by('order', 'date_created').select_related('stage_forms',
                                                                                                  'stage_forms__xf',
                                                                                                  'stage_forms__xf__user').\
                    prefetch_related('stage_forms__project_form_instances', 'stage_forms__xf__fshistory')\
                    .filter(stage_forms__is_staged=True, stage_forms__is_scheduled=False,
                            stage_forms__is_survey=False, stage_forms__is_deleted=True, stage_forms__project_id=project)
                stage_deleted_forms = ViewStageFormSerializer(stage_deleted_qs, context={'is_project': is_project},
                                                              many=True).data
                project = Project.objects.get(id=project)

                return Response(status=status.HTTP_200_OK, data={'stage_forms': stage,
                                                                 'deleted_forms': stage_deleted_forms,
                                                                 'breadcrumbs': self.get_breadcrumbs(True, project)

                                                                 })

            elif site is not None:
                try:
                    site = Site.objects.get(id=site)
                except ObjectDoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND, data={"detail": "Not found."})
                project_id = site.project_id
                project = site.project

                types_count = project.types.count()
                if project.cluster_sites and types_count:
                    if not site.type:
                        site.type_id = 0
                    if not site.region:
                        site.region_id = 0
                    stage_queryset = base_queryset.filter(Q(site__id=site.id, project_stage_id=0)
                                                          | Q(project__id=project_id, tags__contains=[site.type_id])
                                                          | Q(project__id=project_id, regions__contains=[site.region_id])
                                               )
                if types_count:
                    if not site.type:
                        site.type_id = 0
                    stage_queryset = base_queryset.filter(Q(site__id=site.id,
                                                 project_stage_id=0)
                                               | Q(project__id=project_id, tags__contains=[site.type_id])

                                               )
                if project.cluster_sites:
                    if not site.region:
                        site.region_id = 0
                    stage_queryset = base_queryset.filter(Q(site__id=site.id,
                                                 project_stage_id=0)
                                               | Q(project__id=project_id, regions__contains=[site.region_id])
                                               )
                else:
                    stage_queryset = base_queryset.filter(
                        Q(site__id=site.id, project_stage_id=0)
                        | Q(project__id=project_id))
                stage = ViewStageFormSerializer(stage_queryset, context={'site': site.id}, many=True).data
                stage_deleted_qs = Stage.objects.order_by('order', 'date_created').select_related('stage_forms',
                                                                                                  'stage_forms__xf',
                                                                                                  'stage_forms__xf__user'). \
                    prefetch_related('stage_forms__project_form_instances', 'stage_forms__xf__fshistory') \
                    .filter(stage_forms__is_staged=True, stage_forms__is_scheduled=False,
                            stage_forms__is_survey=False, stage_forms__is_deleted=True, project_id=project)
                stage_deleted_forms = ViewSubStageFormSerializer(stage_deleted_qs, context={'site': site.id},
                                                                 many=True).data
                return Response(status=status.HTTP_200_OK, data={'stage_forms': stage,
                                                                 'deleted_forms': stage_deleted_forms,
                                                                 'breadcrumbs': self.get_breadcrumbs(False, site)

                                                                 })

        elif form_type == 'survey':
            is_project = True
            base_queryset = FieldSightXF.objects.filter(is_staged=False, is_scheduled=False, project_id=project,
                                                        is_survey=True)

            survey_qs = base_queryset.select_related('xf', 'xf__user').\
                prefetch_related('project_form_instances', 'xf__fshistory').\
                filter(is_deleted=False)

            survey_forms = ViewGeneralsAndSurveyFormSerializer(survey_qs, many=True,
                                                               context={'is_project': is_project}).data

            survey_deleted_qs = base_queryset.select_related('xf', 'xf__user').\
                prefetch_related('project_form_instances', 'xf__fshistory').\
                filter(is_deleted=True)
            survey_deleted_forms = ViewGeneralsAndSurveyFormSerializer(survey_deleted_qs, many=True,
                                                                       context={'is_project': is_project}).data
            project = Project.objects.get(id=project)

            return Response(status=status.HTTP_200_OK, data={'survey_forms': survey_forms,
                                                             'deleted_forms': survey_deleted_forms,
                                                             'breadcrumbs': self.get_breadcrumbs(True, project)

                                                             })

        else:
            return Response(status=status.HTTP_404_NOT_FOUND, data={'detail': 'Required params are form_type and project or site'})


class ProjectSiteSubmissionStatusView(APIView):
    permission_classes = (IsAuthenticated, ViewDataPermission)
    pagination_class = SubmissionStatusPagination

    def response_paginated_data(self, queryset, is_project, object):
        page = self.paginate_queryset(queryset)

        if is_project:
            breadcrumbs = {'project_name': object[0].name, 'project_url': object[0].get_absolute_url(),
                           'current_page': 'Responses'}
        else:
            breadcrumbs = {'site_name': object.name, 'site_url': object.get_absolute_url(), 'current_page': 'Responses'}

        if page is not None:
            serializer = ViewSubmissionStatusSerializer(page, many=True)

            return self.get_paginated_response({'data': serializer.data, 'breadcrumbs': breadcrumbs})

    def get(self, request, format=None):
        project = request.query_params.get('project', None)
        site = request.query_params.get('site', None)
        submission_status = request.query_params.get('submission_status', None)

        if submission_status == 'rejected':
            base_queryset = FInstance.objects.\
                filter(form_status='1').order_by('-date')
            if project is not None:

                rejected_queryset = base_queryset.select_related('project_fxf__xf', 'submitted_by').filter(project_id=project, project_fxf_id__isnull=False)
                project = Project.objects.filter(id=project).only('name')

                return self.response_paginated_data(rejected_queryset, True, project)
            elif site is not None:
                try:
                    site = Site.objects.get(id=site)
                except ObjectDoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND, data={"detail": "Not found."})

                rejected_queryset = base_queryset.filter(site=site)
                return self.response_paginated_data(rejected_queryset, False, site)

        if submission_status == 'flagged':
            base_queryset = FInstance.objects.select_related('project_fxf__xf', 'site_fxf__xf', 'submitted_by').\
                filter(form_status='2').order_by('-date')
            if project is not None:

                flagged_queryset = base_queryset.filter(project_id=project, project_fxf_id__isnull=False)
                project = Project.objects.filter(id=project).only('name')

                return self.response_paginated_data(flagged_queryset, True, project)
            elif site is not None:
                try:
                    site = Site.objects.get(id=site)
                except ObjectDoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND, data={"detail": "Not found."})

                flagged_queryset = base_queryset.filter(site=site)
                return self.response_paginated_data(flagged_queryset, False, site)

        if submission_status == 'pending':
            base_queryset = FInstance.objects.select_related('project_fxf__xf', 'site_fxf__xf', 'submitted_by').\
                filter(form_status='0').order_by('-date')
            if project is not None:

                pending_queryset = base_queryset.filter(project_id=project, project_fxf_id__isnull=False)
                project = Project.objects.filter(id=project).only('name')

                return self.response_paginated_data(pending_queryset, True, project)

            elif site is not None:
                try:
                    site = Site.objects.get(id=site)
                except ObjectDoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND, data={"detail": "Not found."})

                pending_queryset = base_queryset.filter(site=site)
                return self.response_paginated_data(pending_queryset, False, site)

        if submission_status == 'approved':
            base_queryset = FInstance.objects.\
                filter(form_status='3').order_by('-date')
            if project is not None:

                approved_queryset = base_queryset.select_related('project_fxf__xf', 'submitted_by').filter(
                    project_id=project, project_fxf_id__isnull=False)
                project = Project.objects.filter(id=project).only('name')

                return self.response_paginated_data(approved_queryset, True, project)

            elif site is not None:
                try:
                    site = Site.objects.get(id=site)
                except ObjectDoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND, data={"detail": "Not found."})

                approved_queryset = base_queryset.filter(site=site)
                return self.response_paginated_data(approved_queryset, False, site)

    @property
    def paginator(self):
        """
        The paginator instance associated with the view, or `None`.
        """
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        """
        Return a single page of results, or `None` if pagination is disabled.
        """
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        """
        Return a paginated style `Response` object for the given output data.
        """
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)


class FormSubmissionsView(APIView):
    permission_classes = (IsAuthenticated, ViewDataPermission)
    pagination_class = SubmissionStatusPagination

    def get_breadcrumbs(self, is_project, object, form_name, is_organization=False):
        if is_project:

            breadcrumbs = {'project_name': object[0].name,
                           'project_url': object[0].get_absolute_url(),
                           'responses': 'Responses',
                           'responses_url': '/fieldsight/application/#/project-responses/{}/general'.format(object[0].id),
                           'current_page': form_name
                           }

        elif is_organization:
            breadcrumbs = {'organization_name': object[0].name,
                           'organization_url': object[0].get_absolute_url(),
                           'responses': 'Responses',
                           'responses_url': '/fieldsight/application/#/organization-responses/{}/general'.format(
                               object[0].id),
                           'current_page': form_name
                           }

        else:
            breadcrumbs = {'site_name': object[0].name,
                           'site_url': object[0].get_absolute_url(),
                           'responses': 'Responses',
                           'responses_url': '/fieldsight/application/#/site-responses/{}/general'.format(object[0].id),
                           'current_page': form_name
                           }

        return breadcrumbs

    def get(self, request, format=None):
        project = request.query_params.get('project', None)
        org_form_lib = request.query_params.get('org_form_lib', None)
        site = request.query_params.get('site', None)
        fsxf_id = request.query_params.get('fsxf_id', None)
        search_param = request.query_params.get('q', None)

        if org_form_lib and project is not None:

            is_organization = True
            try:
                org_form_lib_obj = OrganizationFormLibrary.objects.get(id=org_form_lib)

            except ObjectDoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND, data={"detail": "Not found."})
            # if search_param:
            #     queryset = FInstance.objects.select_related('site', 'submitted_by', 'instance').filter(
            #         Q(project_fxf=fsxf.id) &
            #         (
            #                 Q(site__name__icontains=search_param) |
            #                 Q(site__identifier__icontains=search_param) |
            #                 Q(submitted_by__first_name__icontains=search_param) |
            #                 Q(submitted_by__last_name__icontains=search_param)
            #         )
            #     )
            # else:

            queryset = FInstance.objects.select_related('site', 'submitted_by', 'instance').\
                filter(organization_fxf__organization_form_lib=org_form_lib_obj, project_id=project).order_by('-id')

            page = self.paginate_queryset(queryset)

            if page is not None:
                serializer = FormSubmissionSerializer(page, many=True, context={'is_organization': is_organization})
                organization = SuperOrganization.objects.filter(id=org_form_lib_obj.organization.id).only('name')
                form_name = org_form_lib_obj.xf.title
                return self.get_paginated_response({'data': serializer.data,
                                                    'form_name': form_name, 'is_survey': False,
                                                    'form_id_string': org_form_lib_obj.xf.id_string,
                                                    'query': search_param,
                                                    'breadcrumbs': self.get_breadcrumbs(False, organization, form_name,
                                                                                        is_organization=True)
                                                    })

        if project and fsxf_id is not None:
            try:
                Project.objects.get(id=project)
            except Exception as e:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={'detail': str(e)})

            is_project = True
            try:
                fsxf = FieldSightXF.objects.get(pk=fsxf_id)

            except ObjectDoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND, data={"detail": "Not found."})
            if search_param:
                queryset = FInstance.objects.select_related('site', 'submitted_by', 'instance').filter(
                    Q(project_fxf=fsxf.id) &
                    (
                            Q(site__name__icontains=search_param) |
                            Q(site__identifier__icontains=search_param) |
                            Q(submitted_by__first_name__icontains=search_param) |
                            Q(submitted_by__last_name__icontains=search_param)
                    )
                )
            else:
                queryset = FInstance.objects.select_related('site', 'submitted_by', 'instance').filter(
                    project_fxf=fsxf.id).order_by('-id')

            page = self.paginate_queryset(queryset)

            if page is not None:
                serializer = FormSubmissionSerializer(page, many=True, context={'is_project': is_project})
                project = Project.objects.filter(id=project).only('name')
                form_name = fsxf.xf.title
                return self.get_paginated_response({'data': serializer.data, 'form_name': form_name, 'is_survey':
                    fsxf.is_survey, 'form_id_string': fsxf.xf.id_string, 'query': search_param,
                                                    'breadcrumbs': self.get_breadcrumbs(True, project, form_name)
                                                    })

        elif site and fsxf_id is not None:
            is_project = False
            try:
                fsxf = FieldSightXF.objects.get(pk=fsxf_id)

            except ObjectDoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND, data={"detail": "Not found."})

            if not fsxf.from_project:
                if search_param:
                    queryset = FInstance.objects.select_related('site', 'submitted_by', 'instance').filter(
                        Q(site_fxf=fsxf.id) &
                        (
                                Q(submitted_by__first_name__icontains=search_param) |
                                Q(submitted_by__last_name__icontains=search_param)
                        )
                    )
                else:
                    queryset = FInstance.objects.select_related('site', 'submitted_by', 'instance').filter(
                        site_fxf=fsxf_id).order_by('-id')
            else:
                if search_param:
                    queryset = FInstance.objects.select_related('site', 'submitted_by', 'instance').filter(
                        Q(project_fxf=fsxf_id) &
                        (
                                Q(submitted_by__first_name__icontains=search_param) |
                                Q(submitted_by__last_name__icontains=search_param)
                        )
                    )
                else:
                    queryset = FInstance.objects.select_related('site', 'submitted_by', 'instance').filter(
                        project_fxf=fsxf_id, site_id=site).order_by('-id')
            page = self.paginate_queryset(queryset)

            if page is not None:
                serializer = FormSubmissionSerializer(page, many=True, context={'is_project': is_project})
                site = Site.objects.filter(id=site).only('name')
                form_name = fsxf.xf.title
                return self.get_paginated_response({'data': serializer.data, 'form_name': form_name, 'is_survey':
                    fsxf.is_survey, 'form_id_string': fsxf.xf.id_string, 'query': search_param,
                                                    'breadcrumbs': self.get_breadcrumbs(False, site, form_name)

                                                    })

    @property
    def paginator(self):
        """
        The paginator instance associated with the view, or `None`.
        """
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        """
        Return a single page of results, or `None` if pagination is disabled.
        """
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        """
        Return a paginated style `Response` object for the given output data.
        """
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)


class DeleteFInstanceView(APIView):
    permission_classes = (IsAuthenticated, DeleteFInstancePermission)

    def get(self, request, *args, **kwargs):
        try:
            finstance = FInstance.objects.get(instance_id=self.kwargs.get('pk'))

        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data={'detail': 'Not found.'})

        try:
            finstance.is_deleted = True
            finstance.save()
            instance = finstance.instance
            instance.deleted_at = datetime.datetime.now()
            instance.save()
            delete_form_instance(int(self.kwargs.get('pk')))

            if finstance.site:
                extra_object = finstance.site
                site_id = extra_object.id
                project_id = extra_object.project_id
                organization_id = extra_object.project.organization_id
                extra_message = "site"
            else:
                extra_object = finstance.project
                site_id = None
                project_id = extra_object.id
                organization_id = extra_object.organization_id
                extra_message = "project"
            extra_json = {}
            extra_json['submitted_by'] = finstance.submitted_by.user_profile.getname()
            noti = finstance.logs.create(source=self.request.user, type=33, title="deleted response" + self.kwargs.get('pk'),
                                         organization_id=organization_id,
                                         project_id=project_id,
                                         site_id=site_id,
                                         extra_json=extra_json,
                                         extra_object=extra_object,
                                         extra_message=extra_message,
                                         content_object=finstance)
            return Response(status=status.HTTP_204_NO_CONTENT, data={'detail': 'Response successfully Deleted.'})

        except Exception as e:
            return Response(status=status.HTTP_404_NOT_FOUND, data={'detail': 'Response deleted unsuccessfull ' + str(e)})


class SubmissionsVersions(APIView):
    permission_classes = (IsAuthenticated,)

    def get_breadcrumbs(self, is_project, object, fsf):
        if is_project:

            breadcrumbs = {'project_name': object.name,
                           'project_url': object.get_absolute_url(),
                           'responses': 'Responses',
                           'responses_url': '/fieldsight/application/#/project-responses/{}/general/'.format(object.id),
                           'current_page': u'Versions of {}'.format(fsf.xf.title)
                           }
        else:
            breadcrumbs = {'site_name': object.name,
                           'site_url': object.get_absolute_url(),
                           'responses': 'Responses',
                           'responses_url': '/fieldsight/application/#/site-responses/{}/general/'.format(object.id),
                           'current_page': u'Versions of {}'.format(fsf.xf.title)
                           }

        return breadcrumbs

    def get(self, request, is_project, pk, fsxf_id, format=None):

        if is_project == '1' and fsxf_id is not None:
            fsf = FieldSightXF.objects.select_related('xf__user').get(pk=fsxf_id)
            project = fsf.project

            form_version = get_xform_version(fsf.xf)
            latest = FInstance.objects.filter(project_fxf=fsf, version=form_version).last()
            if latest:
                date = latest.date.strftime("%b %d, %Y at %I:%M %p")
            else:
                date = ''
            count = FInstance.objects.filter(project_fxf=fsf, version=form_version).count()
            versions = XformHistory.objects.filter(xform=fsf.xf).order_by('-date')

            serializer = SubmissionsVersionSerializer(versions, many=True, context={'is_project': 1, 'fsf': fsf})
            latest = {'title': fsf.xf.title, 'version': 'Latest', 'overidden_date': 'Latest', 'last_response': date,
                      'total_submissions': count, 'download_url': '/{}/exports/{}/xls/1/{}/0/{}/'.\
                    format(fsf.xf.user.username, fsf.xf.id_string, fsf.id, form_version), 'version_id': form_version}
            return Response(status=status.HTTP_200_OK, data={'data': {'latest': latest, 'versions': serializer.data,
                                                                      'breadcrumbs':
                                                                          self.get_breadcrumbs(True, project, fsf)}})

        elif is_project == '0' and fsxf_id is not None:
            site_obj = Site.objects.get(pk=pk)
            project = site_obj.project
            fsf = FieldSightXF.objects.select_related('xf__user').get(pk=fsxf_id)
            versions = XformHistory.objects.filter(xform=fsf.xf).order_by('-date')
            latest = fsf.xf

            form_version = get_xform_version(fsf.xf)
            if fsf.project:
                latest = FInstance.objects.filter(project_fxf=fsf, version=form_version, site=site_obj).last()
                if latest:
                    date = latest.date.strftime("%b %d, %Y at %I:%M %p")
                else:
                    date = ''
                count = FInstance.objects.filter(project_fxf=fsf, version=form_version, site=site_obj).count()

            elif fsf.site:
                latest = FInstance.objects.filter(site_fxf=fsf, version=form_version, site=site_obj).last()
                if latest:
                    date = latest.date.strftime("%b %d, %Y at %I:%M %p")
                else:
                    date = ''
                count = FInstance.objects.filter(site_fxf=fsf, version=form_version, site=site_obj).count()

            else:
                count = 0
                date = ''
            versions = XformHistory.objects.filter(xform=fsf.xf).order_by('-date')

            serializer = SubmissionsVersionSerializer(versions, many=True, context={'is_project': 0, 'fsf': fsf,
                                                                                    'site': pk})
            latest = {'title': fsf.xf.title, 'version': 'Latest', 'overidden_date': 'Latest', 'last_response': date,
                      'total_submissions': count, 'download_url': '/{}/exports/{}/xls/1/{}/0/{}/'. \
                    format(fsf.xf.user.username, fsf.xf.id_string, fsf.id, form_version)}
            return Response(status=status.HTTP_200_OK, data={'data': {'latest': latest, 'versions': serializer.data,
                                                                      'breadcrumbs':
                                                                          self.get_breadcrumbs(False, site_obj, fsf)}})



