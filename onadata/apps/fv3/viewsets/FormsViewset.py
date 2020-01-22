from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.db.models import Q, Prefetch, Count

from rest_framework import viewsets, status
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db import IntegrityError, transaction
from django.conf import settings
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from onadata.apps.fieldsight.models import Project, Organization
from onadata.apps.fsforms.models import FieldSightXF, ObjectPermission, Asset, \
    DeletedXForm, Schedule, Stage
from onadata.apps.fv3.permissions.manage_forms import FormsPermission
from onadata.apps.fv3.serializers.FormSerializer import XFormSerializer, \
    ShareFormSerializer, \
    ShareProjectFormSerializer, ShareTeamFormSerializer, \
    ShareGlobalFormSerializer, \
    AddLanguageSerializer, CloneFormSerializer, ProjectFormSerializer, \
    MyFormDeleteSerializer, \
    ShareUserListSerializer, ShareTeamListSerializer, \
    ShareProjectListSerializer, FSXFormSerializer, SchedueFSXFormSerializer, \
    ScheduleSerializer, StageSerializer, SurveyFSXFormSerializer
from onadata.apps.logger.models import XForm
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from onadata.apps.userrole.models import UserRole
from onadata.apps.eventlog.models import CeleryTaskProgress
from onadata.apps.fv3.permissions.xform import XFormSharePermission, XFormDeletePermission, XFormEditPermission
from onadata.apps.fsforms.enketo_utils import CsrfExemptSessionAuthentication


class MyFormsViewSet(viewsets.ReadOnlyModelViewSet):
    """
        A simple ViewSet for viewing myforms.
        """
    authentication_classes = ([SessionAuthentication,BasicAuthentication])
    queryset = XForm.objects.all()
    serializer_class = XFormSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user, deleted_xform=None)

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def get_serializer_context(self):
        context = super(MyFormsViewSet, self).get_serializer_context()
        context['request'] = self.request
        return context


class ShareUserListViewSet(viewsets.ReadOnlyModelViewSet):
    """
        A ViewSet for getting the list of shareable users for sharing form
        """
    authentication_classes = ([SessionAuthentication, BasicAuthentication])
    queryset = User.objects.all()
    serializer_class = ShareUserListSerializer

    def get_queryset(self):
        if self.request.roles.filter(group__name="Super Admin").exists():
            return self.queryset.filter(user_roles__group__name="Project Manager")
        projects = self.request.roles.filter(
            ended_at__isnull=True, group__name="Project Manager").\
            values_list("project", flat=True).order_by('project').distinct()

        return self.queryset.filter(user_roles__project_id__in=projects).distinct()


class ShareTeamListViewSet(viewsets.ReadOnlyModelViewSet):
    """
            A ViewSet for getting the list of shareable team for sharing form
            """
    authentication_classes = ([SessionAuthentication, BasicAuthentication])
    queryset = Organization.objects.all()
    serializer_class = ShareTeamListSerializer

    def get_queryset(self):
        if self.request.roles.filter(group__name="Super Admin").exists():
            return self.queryset
        teams = self.request.roles.filter(
            ended_at__isnull=True, group__name="Organization Admin").values_list(
            "organization", flat=True).distinct()
        return self.queryset.filter(id__in=teams)


class ShareProjectListViewSet(viewsets.ReadOnlyModelViewSet):
    """
        A ViewSet for getting the list of shareable projects for sharing form
        """
    authentication_classes = ([SessionAuthentication, BasicAuthentication])
    queryset = Project.objects.all()
    serializer_class = ShareProjectListSerializer

    def get_queryset(self):
        if self.request.roles.filter(group__name="Super Admin").exists():
            return self.queryset
        projects = self.request.roles.filter(
            ended_at__isnull=True, group__name="Project Manager").values_list(
            "project", flat=True).order_by('project').distinct()
        return self.queryset.filter(id__in=projects)


class MyProjectFormsViewSet(viewsets.ReadOnlyModelViewSet):
    """
        A simple ViewSet for viewing my  project forms.
        forms assigned in my project is project forms
        """
    authentication_classes = ([SessionAuthentication,BasicAuthentication])
    queryset = Project.objects.all()
    serializer_class = ProjectFormSerializer

    def get_queryset(self):
        projects = self.request.roles.filter(
            ended_at__isnull=True).values_list("project", flat=True).order_by('project').distinct()
        organizations = self.request.roles.filter(
            ended_at__isnull=True, group__name="Organization Admin").values_list(
            "organization", flat=True)
        admin_projects = Project.objects.filter(organization__pk__in=organizations).values_list("pk", flat=True)
        projects = [p for p in projects] + [p for p in admin_projects]
        projects = Project.objects.filter(id__in=projects).order_by('id')
        return projects

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def get_serializer_context(self):
        context = super(MyProjectFormsViewSet, self).get_serializer_context()
        context['request'] = self.request
        return context


class ShareFormViewSet(APIView):
    """
        A ViewSet for sharing the form to users
        """
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, XFormSharePermission)

    def post(self, request, **kwargs):
        serializer = ShareFormSerializer(data=request.data)
        if serializer.is_valid(raise_exception=False):

            xf = XForm.objects.get(id_string=request.data['id_string'])
            self.check_object_permissions(request, xf)

            task_obj = CeleryTaskProgress.objects.create(user=request.user,
                                                         description="Share Forms Individual",
                                                         task_type=19, content_object=xf)
            if task_obj:
                from onadata.apps.fsforms.tasks import api_share_form
                try:
                    with transaction.atomic():
                        api_share_form.delay(xf.id, request.data['share_id'], task_obj.id)
                except IntegrityError:
                    pass
                return Response({"message": "Form shared successfully."}, status=status.HTTP_201_CREATED)
            else:
                return Response({"message": "Error while sharing form."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ShareProjectFormViewSet(APIView):
    """
        A ViewSet for sharing a form to the project managers of a project and the organization admin
        """

    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, XFormSharePermission)

    def post(self, request, **kwargs):
        serializer = ShareProjectFormSerializer(data=request.data)
        if serializer.is_valid(raise_exception=False):
            xf = XForm.objects.get(id_string=request.data['id_string'])
            self.check_object_permissions(request, xf)

            task_obj = CeleryTaskProgress.objects.create(user=request.user,
                                                         description="Share Forms Project Manager and Admin",
                                                         task_type=20, content_object=xf)
            if task_obj:
                from onadata.apps.fsforms.tasks import api_share_form
                try:
                    with transaction.atomic():
                        if isinstance(request.data['share_id'], list):
                            project = Project.objects.filter(id__in=request.data['share_id'])
                            userrole = UserRole.objects.filter(project__in=project,
                                                               group__name__in=["Project Manager", "Organization Admin"],
                                                               ended_at__isnull=True)
                            users = User.objects.filter(user_roles__in=userrole)
                            user_ids = []
                            for item in users:
                                user_ids.append(item.id)
                            api_share_form.delay(xf.id, user_ids, task_obj.id)
                        else:
                            project = Project.objects.get(id=request.data['share_id'])
                            userrole = UserRole.objects.filter(project=project,
                                                               group__name__in=["Project Manager",
                                                                                "Organization Admin"],
                                                               organization=project.organization,
                                                               ended_at__isnull=True)
                            users = User.objects.filter(user_roles__in=userrole)
                            user_ids = []
                            for item in users:
                                user_ids.append(item.id)
                            api_share_form.delay(xf.id, user_ids, task_obj.id)

                except IntegrityError:
                    pass
            return Response({"message": "Form shared successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ShareTeamFormViewSet(APIView):
    """
        A ViewSet for sharing a form to all the team members(project managers and organization admin)
        """

    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, XFormSharePermission)

    def post(self, request, **kwargs):
        serializer = ShareTeamFormSerializer(data=request.data)
        if serializer.is_valid(raise_exception=False):

            xf = XForm.objects.get(id_string=request.data['id_string'])
            self.check_object_permissions(request, xf)
            task_obj = CeleryTaskProgress.objects.create(user=request.user, description="Share XForm to Team",
                                                         task_type=21, content_object=xf)
            if task_obj:
                from onadata.apps.fsforms.tasks import api_share_form
                try:
                    with transaction.atomic():
                        if isinstance(request.data['share_id'], list):
                            userrole = UserRole.objects.filter(organization_id__in=request.data['share_id'],
                                                               group__name__in=["Project Manager", "Organization Admin"],
                                                               ended_at__isnull=True)
                            users = User.objects.filter(user_roles__in=userrole)
                            user_ids = []
                            for item in users:
                                user_ids.append(item.id)
                            api_share_form.delay(xf.id, user_ids, task_obj.id)
                        else:
                            userrole = UserRole.objects.filter(organization_id=request.data['share_id'],
                                                               group__name__in=["Project Manager",
                                                                                "Organization Admin"],
                                                               ended_at__isnull=True)
                            users = User.objects.filter(user_roles__in=userrole)
                            user_ids = []
                            for item in users:
                                user_ids.append(item.id)
                            api_share_form.delay(xf.id, user_ids, task_obj.id)

                except IntegrityError:
                    pass
                return Response({"message": "Form shared successfully."}, status=status.HTTP_201_CREATED)
            else:
                return Response({"message": "Error while sharing form."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ShareGlobalFormViewSet(APIView):
    """
        A ViewSet for sharing a form globally
        """

    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, XFormSharePermission)

    def post(self, request, **kwargs):
        serializer = ShareGlobalFormSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        xf = XForm.objects.get(id_string=request.data['id_string'])
        self.check_object_permissions(request, xf)

        from onadata.apps.fsforms.share_xform import share_form_global
        shared = share_form_global(xf)
        if shared:
            return Response({"message": "Form shared successfully",
                             'share_link': settings.KPI_URL + '#/forms/' + xf.id_string},
                            status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CloneFormViewSet(APIView):
    """
        A ViewSet for cloning a form
        """
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, )

    def post(self, request, **kwargs):
        serializer = CloneFormSerializer(data=request.data)
        if serializer.is_valid():
            xf = XForm.objects.get(id_string=request.data['id_string'])
            task_obj = CeleryTaskProgress.objects.create(user=request.user, description="Clone Form",
                                                         task_type=22, content_object=xf)
            if task_obj:
                from onadata.apps.fsforms.tasks import api_clone_form
                api_clone_form.delay(xf.id, request.user.id, task_obj.id)
                return Response({"message": "Form cloned successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
       

class FormAddLanguageViewSet(APIView):
    """
        A ViewSet for adding languages to a form
        """
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, XFormEditPermission)

    def post(self, request, *args,  **kwargs):
        serializer = AddLanguageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        xf = XForm.objects.get(id_string=request.data['id_string'])
        self.check_object_permissions(request, xf)
        a = Asset.objects.get(uid=xf.id_string)
        if 'default_language' not in a.content['settings']:
            return Response({'message': "This form has no default language defined yet."})
        translation = u'' + request.data['language'] + ' ' + '(' + request.data['code'] + ')'
        if 'translations' in a.content:
            a.content['translations'].append(translation)
            if 'survey' in a.content:
                sheet = a.content['survey']
                for row in sheet:
                    if 'label' in row:
                        row['label'].append(None)
            a.save()
            return Response({"message": "Language added successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "This form has no languages defined yet."}, status=status.HTTP_400_BAD_REQUEST)


class MyFormDeleteViewSet(APIView):
    """
        A ViewSet for deleting the xform from my forms
        """
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, XFormDeletePermission)

    def post(self, request, *args, **kwargs):
        serializer = MyFormDeleteSerializer(data=request.data)
        if serializer.is_valid(raise_exception=False):
            xf = XForm.objects.get(id_string=request.data['id_string'])
            self.check_object_permissions(request, xf)
            obj, created = DeletedXForm.objects.get_or_create(xf=xf)
            if obj or created:
                return Response({"message": "Form deleted successfully."}, status=status.HTTP_201_CREATED)
            else:
                return Response({"message": "Error occurred while deleting form"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MySharedFormViewSet(viewsets.ReadOnlyModelViewSet):
    """
        A simple ViewSet for viewing my shared forms.
        """
    authentication_classes = ([SessionAuthentication, BasicAuthentication])
    queryset = XForm.objects.all()
    serializer_class = XFormSerializer

    def get_queryset(self):
        codenames = ['view_asset', 'change_asset']
        permissions = Permission.objects.filter(content_type__app_label='kpi', codename__in=codenames)
        content_type = ContentType.objects.get(id=settings.ASSET_CONTENT_TYPE_ID)
        obj_perm = ObjectPermission.objects.filter(user=self.request.user,
                                                   content_type=content_type,
                                                   permission__in=permissions,
                                                   deny=False,
                                                   inherited=False)
        asset_uids = []
        for item in obj_perm:
            a = Asset.objects.get(id=item.object_id)
            asset_uids.append(a.uid)

        return self.queryset.filter(id_string__in=asset_uids)


class FormsView(APIView):
    permission_classes = (IsAuthenticated, FormsPermission)
    """
    List all forms in given projects.
    """
    def get(self, request, format=None):
        project_ids = request.GET.getlist('project_id')
        fieldsight_forms = FieldSightXF.objects.filter(
            is_deleted=False,  is_deployed=True).filter(Q(
            project__id__in=project_ids) | Q(site__project_id__in=project_ids,
                                            from_project=False,
                                             site__is_active=True)
            ).select_related("xf", "em", "xf__user", "site", "settings").prefetch_related("em__em_images")
        list(fieldsight_forms)
        general_forms = [f for f in fieldsight_forms if (f.is_staged == False
                    and f.is_survey == False and f.is_scheduled == False)]
        survey_forms = [f for f in fieldsight_forms if f.is_survey]
        schedule_forms = [f for f in fieldsight_forms if f.is_scheduled]
        schedule_forms_data = SchedueFSXFormSerializer(schedule_forms,
                                                       many=True).data
        form_with_schedule = []
        if schedule_forms:
            schedules = Schedule.objects.filter(Q(
                project__id__in=project_ids) | Q(
                site__project__id__in=project_ids)).prefetch_related(
                "selected_days")
            schedule_information = ScheduleSerializer(schedules, many=True).data
            schedule_information_dict = {}
            for schedule in schedule_information:
                schedule_information_dict[schedule['id']] = schedule
            for form in schedule_forms_data:
                form['schedule'] = schedule_information_dict[form['schedule']]
                form_with_schedule.append(form)

        general_form_data = FSXFormSerializer(general_forms, many=True).data
        survey_form_data = SurveyFSXFormSerializer(survey_forms, many=True).data
        stages = Stage.objects.filter(is_deleted=False, stage__isnull=True).filter(
            Q(project__id__in=project_ids) | Q(
                site__project__id__in=project_ids, project_stage_id=0, site__site_roles__user=request.user)).\
            select_related("site").prefetch_related(
            Prefetch(
                'parent',
                queryset=Stage.objects.filter(stage__isnull=False, is_deleted=False,stage_forms__isnull=False,
                                       stage_forms__is_deleted=False,
                                       stage_forms__is_deployed=True).select_related(
                    "stage_forms", "stage_forms__xf", "stage_forms__settings", "stage_forms__site",
                    "stage_forms__em",  "stage_forms__xf__user")  #.prefetch_related("stage_forms__em__em_images")
            ),

            )
        stage_data = StageSerializer(stages, many=True).data
        return Response({"general": general_form_data,
                         "survey": survey_form_data,
                         "schedule": form_with_schedule,
                         "stage": stage_data,
                         })
