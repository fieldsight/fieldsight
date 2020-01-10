import ast, gc

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.db.models import Case, When, Sum, IntegerField

from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import viewsets

from onadata.apps.fieldsight.models import Project, Site, Region, SiteType
from onadata.apps.fsforms.models import FieldSightXF, Schedule, Stage, FInstance
from onadata.apps.fieldsight.tasks import generateSiteDetailsXls, generate_stage_status_report, \
    exportProjectSiteResponses, form_status_map, exportLogs, exportProjectUserstatistics, exportProjectstatistics
from .serializers import StageFormSerializer, ReportSettingsSerializer, PreviewSiteInformationSerializer
from .permissions import ReportingProjectFormsPermissions, ReportingSettingsPermissions
from .models import ReportSettings, REPORT_TYPES, METRICES_DATA, SITE_INFORMATION_VALUES_METRICS_DATA, \
    FORM_INFORMATION_VALUES_METRICS_DATA, USERS_METRICS_DATA, INDIVIDUAL_FORM_METRICS_DATA, FILTER_METRICS_DATA
from ..eventlog.models import CeleryTaskProgress
from ..fsforms.enketo_utils import CsrfExemptSessionAuthentication
from onadata.apps.reporting.tasks import new_export


class ReportingProjectFormData(APIView):
    permission_classes = [IsAuthenticated, ReportingProjectFormsPermissions]

    def get(self, request, pk, *args,  **kwargs):

        form_type = self.request.query_params.get('form_type')
        project_id = get_object_or_404(Project, pk=pk).id

        if form_type == 'general':

            generals_queryset = FieldSightXF.objects.select_related('xf')\
                .filter(is_staged=False, is_scheduled=False, is_deleted=False, project_id=project_id, is_survey=False).\
                values('xf__title', 'id')
            generals_data = [{'id': form['id'], 'title': form['xf__title']} for form in generals_queryset]

            return Response(status=status.HTTP_200_OK, data=generals_data)

        elif form_type == 'scheduled':

            schedules_queryset = Schedule.objects.select_related('project').prefetch_related('schedule_forms')\
                .filter(project_id=project_id, schedule_forms__is_deleted=False, site__isnull=True,
                        schedule_forms__isnull=False, schedule_forms__xf__isnull=False).\
                values('schedule_forms__id', 'schedule_forms__xf__title')

            schedules_data = [{'id': form['schedule_forms__id'], 'title': form['schedule_forms__xf__title']}
                              for form in schedules_queryset]

            return Response(status=status.HTTP_200_OK, data=schedules_data)

        elif form_type == 'stage':

            stages_queryset = Stage.objects.select_related('project').filter(stage__isnull=True, project_id=project_id,
                                                                             stage_forms__isnull=True).order_by('order')

            stages = StageFormSerializer(stages_queryset, many=True)

            return Response(status=status.HTTP_200_OK, data=stages.data)

        elif form_type == 'survey':

            surveys_queryset = FieldSightXF.objects.select_related('xf').\
                filter(is_staged=False, is_scheduled=False, is_deleted=False, project_id=project_id, is_survey=True).\
                values('id', 'xf__title')

            surveys_data = [{'id': form['id'], 'title': form['xf__title']} for form in surveys_queryset]
            return Response(status=status.HTTP_200_OK, data=surveys_data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND, data={'detail': 'form_type params is required.'})


class ReportSettingsViewSet(viewsets.ModelViewSet):
    serializer_class = ReportSettingsSerializer
    queryset = ReportSettings.objects.all().order_by('-id')
    permission_classes = [IsAuthenticated, ReportingProjectFormsPermissions]
    authentication_classes = [BasicAuthentication, CsrfExemptSessionAuthentication]

    def get_queryset(self):
        type = self.request.query_params.get('type')
        id = self.request.query_params.get('id')
        project_id = self.kwargs.get('pk')

        if type == 'custom':
            queryset = self.queryset.filter(project_id=project_id, add_to_templates=True)

        elif type == 'shared_with_me':
            queryset = self.queryset.filter(project_id=project_id, shared_with=self.request.user,
                                            add_to_templates=False)

        elif type == "my_reports":
            queryset = self.queryset.filter(project_id=project_id, add_to_templates=False, owner=self.request.user)

        elif id is not None:
            queryset = self.queryset.filter(id=id)

        else:
            queryset = self.queryset

        return queryset

    def list(self, request, *args, **kwargs):
        type = self.request.query_params.get('type')

        if type == 'custom':
            custom_data = {
                'custom_reports': ReportSettingsSerializer(self.get_queryset(), many=True).data
            }
            custom_data.update({
                'standard_reports': [{'title': 'Project Summary',
                                      'description': 'Contains high level overview of the project in form of numbers, '
                                                     'graphs and map.'},
                                     {'title': 'Site Information',
                                      'description': 'Export of key progress indicators like submission count, status '
                                                     'and site visits generated from Staged Forms.'},

                                     {'title': 'Progress Report',
                                      'description': 'Export of key progress indicators like submission count, '
                                                     'status and site visits generated from Staged Forms.'},

                                     {'title': 'Activity Report',
                                      'description': 'Export of sites visits, submissions and active users in a '
                                                     'selected time interval.'},

                                     {'title': 'Project Logs',
                                      'description': 'Export of all the logs in the project in a selected time '
                                                     'interval.'},

                                     {'title': 'User Activity Report',
                                      'description': 'Export of User Activities in a selected time interval.'},



                                     ]
            })
            return Response(custom_data)
        else:
            return Response(data=ReportSettingsSerializer(self.get_queryset(), many=True).data)

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user, project_id=self.kwargs.get('pk'))

    def update(self, request, pk=None):
        try:
            self.get_object()
        except Http404:
            return Response(
                {'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        return super(ReportSettingsViewSet, self).update(request, pk)


class GenerateStandardReports(APIView):
    permission_classes = [IsAuthenticated, ReportingProjectFormsPermissions]
    authentication_classes = [BasicAuthentication, CsrfExemptSessionAuthentication]

    def post(self, request, pk, *args,  **kwargs):

        report_type = self.request.query_params.get('report_type')
        project = get_object_or_404(Project, pk=pk)

        if report_type == 'site_information':

            source_user = self.request.user
            data = request.data
            site_type_ids = data.get('siteTypes', None)
            region_ids = data.get('regions', None)
            sync_to_drive = data.get('sync_to_drive', False)

            task_obj = CeleryTaskProgress.objects.create(user=source_user, content_object=project, task_type=8)
            if task_obj:
                task = generateSiteDetailsXls.delay(task_obj.pk, self.kwargs.get('pk'), region_ids, site_type_ids,
                                                    sync_to_drive)
                task_obj.task_id = task.id
                task_obj.save()
                status, data = 200, {'detail': 'The sites details xls file is being generated. '
                                               'You will be notified after the file is generated.'}
            else:
                status, data = 401, {'detail': 'Error occured please try again.'}
            return Response(status=status, data=data)

        elif report_type == 'progress_report':
            user = self.request.user
            data = request.data
            site_type_ids = data.get('siteTypes', None)
            region_ids = data.get('regions', None)
            sync_to_drive = data.get('sync_to_drive', False)

            task_obj = CeleryTaskProgress.objects.create(user=user, task_type=10, content_object=project)
            if task_obj:
                task = generate_stage_status_report.delay(task_obj.pk, project.id, site_type_ids, region_ids,
                                                          sync_to_drive)
                task_obj.task_id = task.id
                task_obj.save()
                status, data = 200, {'detail': 'Progress report is being generated. You will be notified upon '
                                               'completion. (It may take more time depending upon number of sites '
                                               'and submissions.)'}
            else:
                status, data = 401, {'detail': 'Report cannot be generated a the moment.'}
            return Response(status=status, data=data)

        elif report_type == 'form':
            base_url = self.request.get_host()
            user = self.request.user
            data = request.data
            fs_ids = data.get('fs_ids')
            start_date = data.get('start_date')
            end_date = data.get('end_date')
            region_ids = data.get('regions', None)
            site_type_ids = data.get('siteTypes', None)
            project = get_object_or_404(Project, pk=self.kwargs.get('pk'))

            task_obj = CeleryTaskProgress.objects.create(user=user, content_object=project, task_type=3)
            if task_obj:
                task = exportProjectSiteResponses.delay(task_obj.pk, self.kwargs.get('pk'), base_url, fs_ids,
                                                        start_date, end_date, region_ids, site_type_ids)
                task_obj.task_id = task.id
                task_obj.save()
                status, data = 200, {'detail': 'Success, the report is being generated. You will be notified after '
                                               'the report is generated.'}
            else:
                status, data = 401, {'detail': 'Error occured please try again.'}
            return Response(status=status, data=data)

        elif report_type == 'logs':
            user = self.request.user
            data = request.data
            reportType = data.get('type')
            start_date = data.get('start_date')
            end_date = data.get('end_date')

            if reportType == "Project":
                obj = get_object_or_404(Project, pk=self.kwargs.get('pk'))
            else:
                obj = get_object_or_404(Site, pk=self.kwargs.get('pk'))

            task_obj = CeleryTaskProgress.objects.create(user=user, content_object=obj, task_type=12)
            if task_obj:
                task = exportLogs.delay(task_obj.pk, self.kwargs.get('pk'), reportType, start_date, end_date)
                task_obj.task_id = task.id
                task_obj.save()
                status, data = 200, {'status': 'true',
                                     'message': 'Success, the report is being generated. You will be notified after '
                                                'the report is generated.'}
            else:
                status, data = 401, {'status': 'false', 'message': 'Error occured please try again.'}
            return Response(data, status=status)

        elif report_type == 'user_activity_report':

            user = request.user
            data = request.data
            start_date = data.get('start_date')
            end_date = data.get('end_date')

            task_obj = CeleryTaskProgress.objects.create(user=user, task_type=16, content_object=project)
            if task_obj:
                task = exportProjectUserstatistics.delay(task_obj.pk, project.id, start_date, end_date)
                task_obj.task_id = task.id
                task_obj.save()
                data = {'status': 'true',
                        'message': 'User Activity report is being generated. You will be notified upon completion.'}
            else:
                data = {'status': 'false', 'message': 'Report cannot be generated a the moment.'}
            return Response(data, status=200)

        elif report_type == 'activity_report':
            user = self.request.user
            data = request.data
            reportType = data.get('type')
            start_date = data.get('start_date')
            end_date = data.get('end_date')

            task_obj = CeleryTaskProgress.objects.create(user=user, content_object=project, task_type=11)
            if task_obj:
                task = exportProjectstatistics.delay(task_obj.pk, self.kwargs.get('pk'), reportType, start_date,
                                                     end_date)
                task_obj.task_id = task.id
                task_obj.save()
                status, data = 200, {'status': 'true',
                                     'message': 'Success, the report is being generated. You will be notified after '
                                                'the report is generated.'}
            else:
                status, data = 401, {'status': 'false', 'message': 'Error occured please try again.'}
            return Response(data, status=status)


class PreviewStandardReports(APIView):
    permission_classes = [IsAuthenticated, ReportingProjectFormsPermissions]
    authentication_classes = [BasicAuthentication, CsrfExemptSessionAuthentication]

    def post(self, request, pk, *args,  **kwargs):

        report_type = self.request.query_params.get('report_type')
        project = get_object_or_404(Project, pk=pk)

        if report_type == 'site_information':
            data = request.data
            site_type_ids = data.get('siteTypes', None)
            region_ids = data.get('regions', None)

            if region_ids is not None:
                region_ids = ast.literal_eval(data.get('regions', None))

            if site_type_ids is not None:
                site_type_ids = ast.literal_eval(data.get('siteTypes', None))

            if region_ids and site_type_ids:
                sites = project.sites.filter(is_active=True, region_id__in=region_ids, type_id__in=site_type_ids).\
                    order_by('identifier')[:7]
            elif region_ids:
                sites = project.sites.filter(is_active=True, region_id__in=region_ids). \
                    order_by('identifier')[:7]

            elif site_type_ids:
                sites = project.sites.filter(is_active=True, type_id__in=site_type_ids)[:7]

            else:
                sites = project.sites.filter(is_active=True)[:7]

            project_metas = project.site_meta_attributes
            metas_questions = [question['question_name'] for question in project_metas if
                               question['question_type'] != 'Link']

            for question in project_metas:
                if question['question_type'] == 'Link':
                    question_name = question['question_name']
                    try:
                        link_metas = question['metas'].values()[0]
                    except:
                        link_metas = []
                    for link_question in link_metas:

                        other_questions = question_name + "/" + link_question['question_name'],
                        metas_questions.extend(other_questions)

            rows_cols = {'rows': 0, 'cols': 0, 'cells': 0}

            return Response(status=status.HTTP_200_OK,
                            data={'sites': PreviewSiteInformationSerializer(sites, many=True).data,
                                  'metas_questions': metas_questions, 'rows_cols': rows_cols})

        elif report_type == 'progress_report':
            data = request.data
            site_type_ids = data.get('siteTypes', None)
            region_ids = data.get('regions', None)

            if region_ids is not None:
                region_ids = ast.literal_eval(data.get('regions', None))

            if site_type_ids is not None:
                site_type_ids = ast.literal_eval(data.get('siteTypes', None))

            data = []
            form_ids = []
            ss_index = []
            stages_rows = []
            query = {}

            stages = project.stages.filter(stage__isnull=True)

            for stage in stages:
                sub_stages = stage.parent.filter(stage_forms__isnull=False)
                stages_rows.append("Stage :" + stage.name)

                if len(sub_stages):
                    for ss in sub_stages:
                        form_ids.append(str(ss.stage_forms.id))
                        ss_index.append({'sub_name': ss.name, 'form_id': str(ss.stage_forms.id)})
                        stages_rows.append("Sub Stage :" + ss.name)

                        query[str(ss.stage_forms.id)] = Sum(
                            Case(
                                When(site_instances__project_fxf_id=ss.stage_forms.id, then=1),
                                default=0, output_field=IntegerField()
                            ))

            query['flagged'] = Sum(
                Case(
                    When(site_instances__form_status=2, site_instances__project_fxf_id__in=form_ids, then=1),
                    default=0, output_field=IntegerField()
                ))

            query['rejected'] = Sum(
                Case(
                    When(site_instances__form_status=1, site_instances__project_fxf_id__in=form_ids, then=1),
                    default=0, output_field=IntegerField()
                ))

            query['submission'] = Sum(
                Case(
                    When(site_instances__project_fxf_id__in=form_ids, then=1),
                    default=0, output_field=IntegerField()
                ))

            sites = Site.objects.filter(is_active=True)

            sites_filter = {'project_id': project.id}
            finstance_filter = {'project_fxf__in': form_ids}

            if site_type_ids:
                sites_filter['type_id__in'] = site_type_ids
                finstance_filter['site__type_id__in'] = site_type_ids

            if region_ids:
                sites_filter['region_id__in'] = region_ids
                finstance_filter['site_id__in'] = site_type_ids

            site_dict = {}

            # Redoing query because annotate and lat long did not go well in single query.
            # Probable only an issue because of old django version.

            for site_obj in sites.filter(**sites_filter).iterator():
                site_dict[str(site_obj.id)] = {'visits': 0, 'site_status': 'No Submission',
                                               'latitude': site_obj.latitude, 'longitude': site_obj.longitude}

            sites_status = FInstance.objects.filter(**finstance_filter).order_by('site_id', '-id').distinct(
                'site_id').values_list('site_id', 'form_status')

            for site_status in sites_status:
                try:
                    site_dict[str(site_status[0])]['site_status'] = form_status_map[site_status[1]]
                except:
                    pass
            sites_status = None
            gc.collect()

            site_visits = settings.MONGO_DB.instances.aggregate(
                [{"$match": {"fs_project": project.id, "fs_project_uuid": {"$in": form_ids}}}, {"$group": {
                    "_id": {
                        "fs_site": "$fs_site",
                        "date": {"$substr": ["$start", 0, 10]}
                    },
                }
                }, {"$group": {"_id": "$_id.fs_site", "visits": {
                    "$push": {
                        "date": "$_id.date"
                    }
                }
                               }}])['result']

            for site_visit in site_visits:
                try:
                    site_dict[str(site_visit['_id'])]['visits'] = len(site_visit['visits'])
                except:
                    pass

            site_visits = None
            gc.collect()

            sites = sites.filter(**sites_filter).values('id', 'identifier', 'name', 'region__identifier', 'address',
                                                        "current_progress").annotate(**query)[:7]

            for site in sites:
                try:
                    site_row = {'identifier': site['identifier'], 'name': site['name'],
                                'region': site['region__identifier'], 'address': site['address'],
                                'latitude': site_dict[str(site.get('id'))]['latitude'],
                                'longitude': site_dict[str(site.get('id'))]['longitude'],
                                'status': site_dict[str(site.get('id'))]['site_status'],
                                'current_progress': site['current_progress']}

                    for stage in ss_index:
                        site_row.update({"Sub Stage :" + stage['sub_name']: site.get(stage['form_id'], "")})

                    site_row.update({'visits': site_dict[str(site.get('id'))]['visits'],
                                     'submission': site['submission'], 'flagged': site['flagged'],
                                     'rejected': site['rejected']})

                    data.append(site_row)
                except Exception as e:
                    print e
            sites = None
            site_dict = None
            rows = sites.filter(**sites_filter).count() + 1
            gc.collect()
            rows_cols = {'rows': 0, 'cols': 0, 'cells': 0}

            return Response(status=status.HTTP_200_OK, data={'progress_report': data, 'stages_rows': stages_rows,
                                                             'rows_cols': rows_cols})


@permission_classes([IsAuthenticated,])
@api_view(['GET'])
def metrics_data(request, pk):
    project = get_object_or_404(Project, id=pk)
    meta_attributes = project.site_meta_attributes
    form_question_answer_status_form_metas = []
    report_types = [{'id': rep_type[0], 'name': rep_type[1]} for rep_type in REPORT_TYPES]
    regions = Region.objects.filter(project=project, is_active=True).values('id', 'name')
    site_types = SiteType.objects.filter(project=project).values('id', 'name')

    for meta in meta_attributes:

        if meta['question_type'] == 'Form' or meta['question_type'] == 'FormQuestionAnswerStatus':
            form_question_answer_status_form_metas.append(meta)

        else:
            meta['code'] = meta.pop('question_name')
            meta['label'] = meta.pop('question_text')
            meta['type'] = meta.pop('question_type')

            if 'question_placeholder' in meta:
                del meta['question_placeholder']

            if 'question_help' in meta:
                del meta['question_help']

    for meta in form_question_answer_status_form_metas:
        if meta['question']['type'] == 'integer':
            meta.update({'input_type': 'Number'})
        else:
            meta.update({'input_type': 'Text'})
        meta['code'] = meta.pop('question_name')
        meta['label'] = meta.pop('question_text')
        meta['type'] = meta.pop('question_type')

        if 'question_placeholder' in meta:
            del meta['question_placeholder']

        if 'question_help' in meta:
            del meta['question_help']

    metrics = []
    metrics.extend(METRICES_DATA)
    metrics.extend(USERS_METRICS_DATA)
    metrics.extend(INDIVIDUAL_FORM_METRICS_DATA)
    metrics.extend(SITE_INFORMATION_VALUES_METRICS_DATA)
    metrics.extend(FORM_INFORMATION_VALUES_METRICS_DATA)
    metrics.extend(FILTER_METRICS_DATA)
    form_types = [{'id': 1, 'code': 'general', 'label': 'General Forms'},
                  {'id': 2, 'code': 'scheduled', 'label': 'Scheduled Forms'},
                  {'id': 3, 'code': 'stage', 'label': 'Staged Forms'},
                  {'id': 4, 'code': 'survey', 'label': 'Survey Forms'},
                  ]

    return Response(status=status.HTTP_200_OK, data={'report_types': report_types,
                                                     'regions': regions,
                                                     'site_types': site_types,
                                                     'metrics': metrics, 'meta_attributes': meta_attributes,
                                                     'form_types': form_types})


class ReportExportView(APIView):
    permission_classes = [IsAuthenticated, ReportingSettingsPermissions]
    authentication_classes = [BasicAuthentication, CsrfExemptSessionAuthentication]

    def get(self, request, pk, *args,  **kwargs):

        report_obj = ReportSettings.objects.get(id=pk)

        export_type = self.request.query_params.get('export_type')

        if export_type == 'excel':
            task_obj = CeleryTaskProgress.objects.create(user=request.user, task_type=26, content_object=report_obj)
            if task_obj:
                task = new_export.delay(report_obj.id, task_obj.id)
                task_obj.task_id = task.id
                return Response(status=status.HTTP_201_CREATED, data={'detail': 'The excel report is being generated. '
                                                                                'You will be notified after the report '
                                                                                'is generated.'})

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'detail': 'export_type params is required.'})


class ReportActionView(APIView):
    permission_classes = [IsAuthenticated, ReportingSettingsPermissions]
    authentication_classes = [BasicAuthentication, CsrfExemptSessionAuthentication]

    def post(self, request, pk, *args,  **kwargs):

        action_type = self.request.data.get('action_type', None)
        shared_users = self.request.data.get('shared_users', None)

        try:
            report_obj = ReportSettings.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data={'detail': 'Report not found.'})

        if action_type == 'add_to_templates':
            report_obj.add_to_templates = True
            report_obj.save()

            response_status, data = status.HTTP_200_OK, {'detail': 'successfully added to Templates.'}

        elif action_type == 'share':
            shared_users = ast.literal_eval(shared_users)
            report_obj.shared_with.add(*shared_users)
            report_obj.save()

            response_status, data = status.HTTP_200_OK, {'detail': 'successfully shared with users'}

        else:
            response_status, data = status.HTTP_400_BAD_REQUEST, {'detail': 'required fields is add_to_templates'
                                                                            ' or share.'}

        return Response(status=response_status, data=data)