import ast

from django.shortcuts import get_object_or_404
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import viewsets

from onadata.apps.fieldsight.models import Project
from onadata.apps.fsforms.models import FieldSightXF, Schedule, Stage
from onadata.apps.fieldsight.tasks import generateSiteDetailsXls, generate_stage_status_report, \
    exportProjectSiteResponses
from .serializers import StageFormSerializer, ReportSettingsSerializer, PreviewSiteInformationSerializer
from .permissions import ReportingProjectFormsPermissions
from .models import ReportSettings, REPORT_TYPES, METRICES_DATA
from ..eventlog.models import CeleryTaskProgress
from ..fsforms.enketo_utils import CsrfExemptSessionAuthentication


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
                values('schedule_forms__xf__id', 'schedule_forms__xf__title')

            schedules_data = [{'id': form['schedule_forms__xf__id'], 'title': form['schedule_forms__xf__title']}
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
    queryset = ReportSettings.objects.all()
    permission_classes = [IsAuthenticated, ReportingProjectFormsPermissions]
    authentication_classes = [BasicAuthentication, CsrfExemptSessionAuthentication]

    def get_queryset(self):
        type = self.request.query_params.get('type')
        project_id = self.kwargs.get('pk')

        if type == 'custom':
            queryset = self.queryset.filter(project_id=project_id, add_to_templates=True)

        elif type == 'shared_with_me':
            queryset = self.queryset.filter(project_id=project_id, shared_with=self.request.user,
                                            add_to_templates=False)

        else:
            queryset = self.queryset.filter(project_id=project_id, add_to_templates=False, owner=self.request.user)
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

            return Response(status=status.HTTP_200_OK,
                            data={'sites': PreviewSiteInformationSerializer(sites, many=True).data,
                                  'metas_questions': metas_questions})

        # elif report_type == 'progress_report':
        #     data = []
        #     ss_index = []
        #     form_ids = []
        #     stages_rows = []
        #     # head_row = ["Site ID", "Name", "Region ID", "Address", "Latitude", "longitude", "Status", "Progress"]
        #
        #     query = {}
        #
        #     stages = project.stages.filter(stage__isnull=True)
        #     for stage in stages:
        #         sub_stages = stage.parent.filter(stage_forms__isnull=False)
        #         if len(sub_stages):
        #             for ss in sub_stages:
        #                 ss_index.append(str(ss.stage_forms.id))
        #                 form_ids.append(str(ss.stage_forms.id))
        #                 query[str(ss.stage_forms.id)] = Sum(
        #                     Case(
        #                         When(site_instances__project_fxf_id=ss.stage_forms.id, then=1),
        #                         default=0, output_field=IntegerField()
        #                     ))
        #
        #     query['flagged'] = Sum(
        #         Case(
        #             When(site_instances__form_status=2, site_instances__project_fxf_id__in=form_ids, then=1),
        #             default=0, output_field=IntegerField()
        #         ))
        #
        #     query['rejected'] = Sum(
        #         Case(
        #             When(site_instances__form_status=1, site_instances__project_fxf_id__in=form_ids, then=1),
        #             default=0, output_field=IntegerField()
        #         ))
        #
        #     query['submission'] = Sum(
        #         Case(
        #             When(site_instances__project_fxf_id__in=form_ids, then=1),
        #             default=0, output_field=IntegerField()
        #         ))
        #
        #     head_row.extend(["Site Visits", "Submission Count", "Flagged Submission", "Rejected Submission"])
        #     data.append(head_row)
        #
        #     sites = Site.objects.filter(is_active=True)
        #
        #     sites_filter = {'project_id': project.id}
        #     finstance_filter = {'project_fxf__in': form_ids}
        #
        #     if site_type_ids:
        #         sites_filter['type_id__in'] = site_type_ids
        #         finstance_filter['site__type_id__in'] = site_type_ids
        #
        #     if region_ids:
        #         sites_filter['region_id__in'] = region_ids
        #         finstance_filter['site_id__in'] = site_type_ids
        #
        #     site_dict = {}
        #
        #     # Redoing query because annotate and lat long did not go well in single query.
        #     # Probable only an issue because of old django version.
        #
        #     for site_obj in sites.filter(**sites_filter).iterator():
        #         site_dict[str(site_obj.id)] = {'visits': 0, 'site_status': 'No Submission',
        #                                        'latitude': site_obj.latitude, 'longitude': site_obj.longitude}
        #
        #     sites_status = FInstance.objects.filter(**finstance_filter).order_by('site_id', '-id').distinct(
        #         'site_id').values_list('site_id', 'form_status')
        #
        #     for site_status in sites_status:
        #         try:
        #             site_dict[str(site_status[0])]['site_status'] = form_status_map[site_status[1]]
        #         except:
        #             pass
        #     sites_status = None
        #     gc.collect()
        #
        #     site_visits = settings.MONGO_DB.instances.aggregate(
        #         [{"$match": {"fs_project": project.id, "fs_project_uuid": {"$in": form_ids}}}, {"$group": {
        #             "_id": {
        #                 "fs_site": "$fs_site",
        #                 "date": {"$substr": ["$start", 0, 10]}
        #             },
        #         }
        #         }, {"$group": {"_id": "$_id.fs_site", "visits": {
        #             "$push": {
        #                 "date": "$_id.date"
        #             }
        #         }
        #                        }}])['result']
        #
        #     for site_visit in site_visits:
        #         try:
        #             site_dict[str(site_visit['_id'])]['visits'] = len(site_visit['visits'])
        #         except:
        #             pass
        #
        #     site_visits = None
        #     gc.collect()
        #
        #     sites = sites.filter(**sites_filter).values('id', 'identifier', 'name', 'region__identifier', 'address',
        #                                                 "current_progress").annotate(**query)
        #
        #     for site in sites:
        #         # import pdb; pdb.set_trace();
        #         try:
        #             site_row = [site['identifier'], site['name'], site['region__identifier'], site['address'],
        #                         site_dict[str(site.get('id'))]['latitude'], site_dict[str(site.get('id'))]['longitude'],
        #                         site_dict[str(site.get('id'))]['site_status'], site['current_progress']]
        #
        #             for stage in ss_index:
        #                 site_row.append(site.get(stage, ""))
        #
        #             site_row.extend([site_dict[str(site.get('id'))]['visits'], site['submission'], site['flagged'],
        #                              site['rejected']])
        #
        #             data.append(site_row)
        #         except Exception as e:
        #             print e
        #
        #     sites = None
        #     site_dict = None
        #     gc.collect()
        #
        #     p.save_as(array=data, dest_file_name="media/stage-report/{}_stage_data.xls".format(project.id))
        #
        #     with open("media/stage-report/{}_stage_data.xls".format(project.id), 'rb') as fin:
        #         buffer = BytesIO(fin.read())
        #         buffer.seek(0)
        #         path = default_storage.save(
        #             "media/stage-report/{}_stage_data.xls".format(project.id),
        #             ContentFile(buffer.getvalue())
        #         )
        #         buffer.close()
        #
        #     task.file.name = path
        #     task.status = 2
        #     task.save()


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def metrics_data(request):
    report_types = [{'key': rep_type[0], 'value': rep_type[1]} for rep_type in REPORT_TYPES]
    metrics = METRICES_DATA

    return Response(status=status.HTTP_200_OK, data={'report_types': report_types, 'metrics': metrics})