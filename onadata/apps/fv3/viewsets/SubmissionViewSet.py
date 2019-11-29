import datetime

from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models import Prefetch
from rest_framework import viewsets, status
from rest_framework.authentication import BasicAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from onadata.apps.fsforms.enketo_utils import CsrfExemptSessionAuthentication
from onadata.apps.fsforms.models import FInstance, InstanceStatusChanged, EditedSubmission, InstanceImages
from onadata.apps.fsforms.utils import send_message_flagged
from onadata.apps.fv3.permissions.submission import SubmissionDetailPermission, SubmissionChangePermission
from onadata.apps.fv3.serializers.SubmissionSerializer import \
    SubmissionSerializer, AlterInstanceStatusSerializer, \
    EditSubmissionAnswerSerializer, MyFinstanceSerializer, \
    MyFinstanceSerializerV2
from onadata.apps.logger.models import Instance


class SubmissionAnswerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = EditedSubmission.objects.all()
    serializer_class = EditSubmissionAnswerSerializer
    permission_classes = [IsAuthenticated]

    # def get_queryset(self):
    #     return self.queryset.select_related("old__xform","old__xform__user", "user").prefetch_related(
    #         Prefetch('fieldsight_instance',
    #                  queryset=FInstance.objects.all().select_related(
    #                      'site', 'site_fxf', 'project_fxf')
    #                  ))

    def get_serializer_context(self):
        return {'request': self.request, 'kwargs': self.kwargs,}


class SubmissionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Instance.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = [IsAuthenticated, SubmissionDetailPermission]

    def get_queryset(self):
        return self.queryset.select_related("xform", "xform__user", "user").prefetch_related(
            Prefetch('fieldsight_instance',
                     queryset=FInstance.objects.all().select_related(
                         'site', 'site_fxf', 'project_fxf').prefetch_related("comments", "edits")
                     ))

    def get_serializer_context(self):
        return {'request': self.request, 'kwargs': self.kwargs,}


class AlterSubmissionStatusViewSet(viewsets.ModelViewSet):
    queryset = [InstanceStatusChanged.objects.first()]
    serializer_class = AlterInstanceStatusSerializer
    authentication_classes = [CsrfExemptSessionAuthentication, BasicAuthentication,]
    permission_classes = [IsAuthenticated, SubmissionChangePermission]
    parser_classes = [MultiPartParser]

    def create(self, request, * args, **kwargs):
        images = []
        for k, v in self.request.data.items():
            if "image_" in k:
                images.append(v)
        # request.data.pop("images")
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance_status = serializer.save(user=request.user)
            for image in images:
                InstanceImages.objects.create(instance_status=instance_status, image=image)
            fi = instance_status.finstance
            fi.form_status = instance_status.new_status
            fi.date = datetime.date.today()
            fi.comment = instance_status.message
            fi.save()
            if fi.site:
                extra_object = fi.site
                extra_message = ""
            else:
                extra_object = fi.project
                extra_message = "project"
            org = fi.project.organization if fi.project else fi.site.project.organization
            instance_status.logs.create(source=self.request.user,
                                        type=17,
                                        title="form status changed",
                                        organization=org,
                                        project=fi.project,
                                        site=fi.site,
                                        content_object=fi,
                                        extra_object=extra_object,
                                        extra_message=extra_message
                                        )
            comment_url = reverse("forms:instance_status_change_detail",
                                  kwargs={'pk': instance_status.id})
            send_message_flagged(fi, instance_status.message, comment_url)
            url = instance_status.images.first()
            if url:
                try:
                    url = url.image.url
                except:
                    url = None
            data = {
                "comment": instance_status.message,
                "date": instance_status.date,
                "get_new_status_display": instance_status.new_status_display(),
                "user_name": instance_status.user.username,
                "user_full_name": instance_status.user.first_name + ' ' + instance_status.user.last_name,
                "user_profile_picture": instance_status.user.user_profile.profile_picture.url,
                "url": reverse_lazy("forms:instance_status_change_detail",
                                    kwargs={'pk': instance_status.id}),
                "media_img":url
            }
            headers = self.get_success_headers(serializer.data)
            return Response(data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MySubmissionsPagination(PageNumberPagination):
    page_size = 500
    page_size_query_param = 'page_size'


class MySubmissions(viewsets.ReadOnlyModelViewSet):
    queryset = FInstance.objects.filter(form_status__in=[2, 1])
    serializer_class = MyFinstanceSerializer
    pagination_class = MySubmissionsPagination
    authentication_classes = [CsrfExemptSessionAuthentication, BasicAuthentication, ]

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(submitted_by=user).select_related(
            'site', 'project', 'project_fxf', 'project_fxf__xf', 'site_fxf', 'site_fxf__xf').order_by('-date')


class MySubmissionsV2(viewsets.ReadOnlyModelViewSet):
    queryset = InstanceStatusChanged.objects.filter(new_status__in=[2, 1])
    serializer_class = MyFinstanceSerializerV2
    pagination_class = MySubmissionsPagination
    authentication_classes = [CsrfExemptSessionAuthentication, BasicAuthentication, ]

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(
            finstance__submitted_by=user).select_related('finstance',
            'finstance__site', 'finstance__project', 'finstance__project_fxf',
                                                         'finstance__project_fxf__xf',
                                                         'finstance__site_fxf', 'finstance__site_fxf__xf').order_by('-date')



