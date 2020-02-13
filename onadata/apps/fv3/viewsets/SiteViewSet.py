import json

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from django.core.serializers import serialize
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView

from onadata.apps.eventlog.models import CeleryTaskProgress
from onadata.apps.fieldsight.metaAttribsGenerator import generateSiteMetaAttribs
from onadata.apps.fieldsight.utils.siteMetaAttribs import get_site_meta_ans
from onadata.apps.fsforms.enketo_utils import CsrfExemptSessionAuthentication
from onadata.apps.fv3.serializers.SiteSerializer import SiteSerializer, FInstanceSerializer, StageFormSerializer, \
    SiteCropImageSerializer
from onadata.apps.fieldsight.models import Site, BluePrints
from onadata.apps.fieldsight.tasks import site_download_zipfile
from onadata.apps.fsforms.models import FInstance, Schedule, Stage, FieldSightXF

from onadata.apps.fsforms.reports_util import get_recent_images
from onadata.apps.fv3.role_api_permissions import SiteSubmissionPermission, \
    check_site_permission, SitePermissions
from onadata.apps.fv3.viewsets.utils import check_file_extension, readable_date


class SiteSubmissionsPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'


class SiteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Site.objects.select_related('project', 'region', 'type')
    serializer_class = SiteSerializer
    permission_classes = [IsAuthenticated, SitePermissions]

    def get_queryset(self):
        return self.queryset

    def get_serializer_context(self):
        return {'request': self.request}


@permission_classes([SiteSubmissionPermission,])
@api_view(['GET'])
def site_map(request, pk):
    if check_site_permission(request, int(pk)):
        pk = int(pk)
        obj = get_object_or_404(Site, pk=pk, is_active=True)
        data = serialize('custom_geojson', [obj], geometry_field='location',
                         fields=('name', 'public_desc', 'additional_desc', 'address', 'location', 'phone', 'id'))

        return Response(json.loads(data))
    else:
        return Response(status=status.HTTP_403_FORBIDDEN, data={"detail": "You do not have permission to perform this action."})


class SiteSubmissionsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FInstance.objects.select_related('instance', 'site_fxf__xf', 'submitted_by')
    serializer_class = FInstanceSerializer
    permission_classes = [IsAuthenticated, SiteSubmissionPermission]
    pagination_class = SiteSubmissionsPagination

    def get_queryset(self):
        site_id = self.request.query_params.get('site', None)
        site = get_object_or_404(Site, id=int(site_id))
        return self.queryset.filter(site=site, is_deleted=False).filter(Q(site_fxf__is_deleted=False) |
                                                                        Q(project_fxf__is_deleted=False)).order_by('-date')


class SiteForms(APIView):
    permission_classes = (IsAuthenticated, SitePermissions)

    def get(self, request, *args,  **kwargs):

        site_id = self.kwargs.get('pk', None)
        query_params = self.request.query_params.get('type')

        if site_id and query_params:
            site_id = int(site_id)
            try:
                project_id = get_object_or_404(Site, pk=int(site_id)).project.id

                if query_params == 'general':
                    generals = FieldSightXF.objects.select_related('xf').filter(is_staged=False, is_deleted=False,
                                                                                is_scheduled=False, is_survey=False,
                                                                                is_deployed=True). \
                        filter(Q(site__id=site_id, from_project=False) | Q(project__id=project_id))

                    data = [{'form_name': obj.xf.title, 'new_submission_url':
                             settings.SITE_URL + '/forms/new/' + str(site_id) + '/' + str(obj.id)} for obj in generals]

                    return Response({'general_forms': data})

                elif query_params == 'scheduled':

                    schedules = Schedule.objects.prefetch_related('schedule_forms__xf').\
                        filter(schedule_forms__is_deleted=False, schedule_forms__isnull=False,
                               schedule_forms__is_deployed=True).\
                        filter(Q(site__id=site_id, schedule_forms__from_project=False) |
                               Q(project__id=project_id))

                    data = [{'form_name': obj.schedule_forms.xf.title, 'new_submission_url':
                             settings.SITE_URL + '/forms/new/' + str(site_id) + '/' + str(obj.schedule_forms.id)} for obj in schedules]

                    return Response({'scheduled_forms': data})

                elif query_params == 'stage':
                    site = Site.objects.get(pk=site_id)

                    if site.type:
                        project_id = site.project.id
                        stages_queryset = Stage.objects.\
                            filter(stage__isnull=True).filter(Q(site__id=site_id, project_stage_id=0) |
                                                              Q (Q(project__id=project_id) &
                                                                 Q(tags__contains=[site.type_id])) |
                                                              Q(Q(project__id=project_id) & Q(tags=[])))
                    else:
                        project_id = site.project.id
                        stages_queryset = Stage.objects.filter(stage__isnull=True).filter(
                            Q(site__id=site_id, project_stage_id=0)
                            | Q(project__id=project_id))
                    stages = StageFormSerializer(stages_queryset, many=True, context={'site_id': site_id})

                    return Response({'stage_forms': stages.data})

                else:
                    return Response(data="Form of type " + str(query_params) + " not found.",
                                    status=status.HTTP_204_NO_CONTENT)

            except Exception as e:
                return Response(data=str(e), status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(data="Site Id and form type required.", status=status.HTTP_400_BAD_REQUEST)


class SiteCropImage(APIView):
    """
    Retrieve and update site logo.
    """
    authentication_classes = (CsrfExemptSessionAuthentication, SessionAuthentication, IsAuthenticated)
    permission_classes = [SitePermissions, ]

    def get_object(self, pk):
        try:
            return Site.objects.get(pk=int(pk))
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    #
    # def get(self, request, pk, format=None):
    #     site = self.get_object(pk)
    #     serializer = SiteCropImageSerializer(site)
    #     return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(int(pk))
        serializer = SiteCropImageSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def site_recent_pictures(request):
    query_params = request.query_params
    site_id = query_params.get('site')
    if check_site_permission(request, int(site_id)):
        try:
            site_featured_images = Site.objects.get(pk=int(site_id)).site_featured_images
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        recent_pictures = get_recent_images(int(site_id))
        return Response({'site_featured_images': site_featured_images,
                         'recent_pictures': recent_pictures})
    else:
        return Response(status=status.HTTP_403_FORBIDDEN,
                        data={"detail": "You do not have permission to perform this action."})


def doc_name(obj):
    if obj.name is not None:
        name = obj.name
    else:
        name = obj.get_name()

    return name


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def site_documents(request):
    query_params = request.query_params
    site_id = query_params.get('site_id')
    site_obj = get_object_or_404(Site, id=site_id)
    site_id = int(site_id)
    site_blueprints = BluePrints.objects.filter(site=site_obj).count()
    show_button = True if site_blueprints < 10 else False
    if check_site_permission(request, site_id):
        try:
            blueprints_obj = Site.objects.get(pk=site_id).blueprints.all()[:10]
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        data = [{'id': blueprint.id, 'name': doc_name(blueprint), 'file': blueprint.image.url, 'doc_type': blueprint.doc_type,
                 'added_date': readable_date(blueprint.added_date),
                 'type': check_file_extension((blueprint.image.url.lower()))}
                for blueprint in blueprints_obj]
        return Response(data={'show_button': show_button, 'documents': data, 'breadcrumbs': {'name': 'Site Documents', 'site': site_obj.name,
                                                                 'site_url': site_obj.get_absolute_url()}})
    else:
        return Response(status=status.HTTP_403_FORBIDDEN,
                        data={"detail": "You do not have permission to perform this action."})


@permission_classes([IsAuthenticated])
@api_view(['DELETE'])
def delete_blueprint(request, pk):
    blueprint = get_object_or_404(BluePrints, id=pk)
    if check_site_permission(request, blueprint.site.id):

        blueprint.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    else:
        return Response(status=status.HTTP_403_FORBIDDEN, data={"detail": "You do not have permission to perform this action."})


class BlueprintsPostDeleteView(APIView):
    """
    create and delete site blueprints.
    """
    authentication_classes = (CsrfExemptSessionAuthentication, SessionAuthentication, IsAuthenticated)

    def post(self, request, format=None):
        site = request.query_params.get('site', None)
        blueprint = request.query_params.get('blueprint', None)
        if site is not None:
            try:
                site = get_object_or_404(Site, id=site)
            except ObjectDoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND,  data={"detail": "Object not found."})
            if check_site_permission(request, site.id):
                files = request.FILES.getlist('files')
                doc_type = request.POST.get('doc_type')
                name = request.POST.get('name')

                if len(files) > 0:
                    objs = [
                        BluePrints(
                            site=site,
                            image=file,
                            name=name,
                            doc_type=doc_type
                        )
                        for file in files
                    ]
                    BluePrints.objects.bulk_create(objs)

                    return Response(status=status.HTTP_201_CREATED, data={"detail": "successfully created blueprints."})
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST, data={"detail": "Please select at least one file."})
            else:
                return Response(status=status.HTTP_403_FORBIDDEN,
                                data={"detail": "You do not have permission to perform this action."})

        elif blueprint is not None:
            try:
                blueprint = BluePrints.objects.get(id=blueprint)
            except ObjectDoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND,  data={"detail": "Object not found."})

            if check_site_permission(request, blueprint.site.id):

                blueprint.delete()
                return Response(status=status.HTTP_204_NO_CONTENT, data={"detail": "successfully deleted."})

            else:
                return Response(status=status.HTTP_403_FORBIDDEN,
                                data={"detail": "You do not have permission to perform this action."})

        else:
            return Response(status=status.HTTP_404_NOT_FOUND, data={'detail': 'site or blueprint params is required.'})


class ZipSiteImages(APIView):
    permission_classes = [IsAuthenticated, SitePermissions]

    def get(self, request, pk, size_code, format=None):
        user = self.request.user
        try:
            site = get_object_or_404(Site, pk=pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data={"detail": "Not found."})
        size = "-small"
        if size_code == '1':
            size = "-medium"
        elif size_code == '2':
            size = "-large"
        task_obj = CeleryTaskProgress.objects.create(user=user, content_object=site, task_type=6)

        if task_obj:
            task = site_download_zipfile.delay(task_obj.pk, size)
            task_obj.task_id = task.id
            task_obj.save()
            status, data = 200, {'status': 'true',
                                 'message': 'Sucess, the Zip file is being generated. You will be notified after the file is generated.'}
        else:
            status, data = 401, {'status': 'false', 'message': 'Error occured please try again.'}
        return Response(data, status=status)


class SiteMetaAttributes(APIView):
    permission_classes = [IsAuthenticated, SitePermissions]

    def get(self, request, pk):
        # metas = generateSiteMetaAttribs(int(pk))
        metas2 = get_site_meta_ans(int(pk))
        saved = Site.objects.get(pk=pk).all_ma_ans
        return Response({'saved': saved, 'current': metas2}, status=status.HTTP_200_OK)
