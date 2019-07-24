from itertools import chain

from django.db.models import Q
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User, Permission
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authentication import BasicAuthentication

from rest_framework.decorators import permission_classes, api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from onadata.apps.fieldsight.models import UserInvite, Region, Project, Site
from onadata.apps.users.models import UserProfile
from onadata.apps.userrole.models import UserRole
from onadata.apps.eventlog.models import FieldSightLog
from onadata.apps.fv3.serializers.MyRolesSerializer import MyRolesSerializer, UserInvitationSerializer, \
    LatestSubmissionSerializer, MyRegionSerializer, MySiteSerializer
from onadata.apps.fsforms.enketo_utils import CsrfExemptSessionAuthentication
from onadata.apps.logger.models import XForm
from onadata.apps.fsforms.models import FInstance


class MySitesPagination(PageNumberPagination):
    page_size = 100


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def my_roles(request):

    profile_obj = UserProfile.objects.select_related('user').get(user=request.user)
    profile = {'id': profile_obj.user.id, 'fullname': profile_obj.getname(), 'username': profile_obj.user.username, 'email': profile_obj.user.email,
               'address': profile_obj.address, 'phone': profile_obj.phone, 'profile_picture': profile_obj.profile_picture.url,
               'twitter': profile_obj.twitter, 'whatsapp': profile_obj.whatsapp, 'skype': profile_obj.skype,
               'google_talk': profile_obj.google_talk}

    teams = UserRole.objects.filter(user=request.user).select_related('user', 'group', 'site', 'organization',
                                                                      'staff_project', 'region').filter(Q(group__name="Organization Admin", organization__is_active=True)|
                                                                   Q(group__name="Project Manager", project__is_active=True)|
                                                                   Q(group__name="Project Donor", project__is_active=True)|
                                                                   Q(group__name="Region Supervisor", region__is_active=True)|
                                                                   Q(group__name="Region Reviewer", region__is_active=True)|
                                                                   Q(group__name="Site Supervisor", site__is_active=True)|
                                                                   Q(group__name="Site Reviewer", site__is_active=True)|
                                                                   Q(group__name="Staff Project Manager", staff_project__is_deleted=False)

                                                                   ).distinct('organization')
    teams = MyRolesSerializer(teams, many=True)

    invitations = UserInvite.objects.select_related('by_user').filter(email=request.user.email, is_used=False, is_declied=False)

    invitations_serializer = UserInvitationSerializer(invitations, many=True)

    return Response({'profile': profile, 'teams': teams.data, 'invitations': invitations_serializer.data})


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def my_regions(request):

    project_id = request.query_params.get('project', None)

    if project_id:
        try:
            project_obj = Project.objects.get(id=project_id)
            is_project_manager_or_team_admin = UserRole.objects.filter(user=request.user).select_related('user', 'group', 'site', 'organization',
                                                                      'staff_project', 'region').filter(Q(group__name="Project Manager",
                                                         project=project_obj, project__is_active=True)|Q(group__name="Organization Admin",
                                                         organization=project_obj.organization, organization__is_active=True)).exists()

            if is_project_manager_or_team_admin:
                data = Region.objects.filter(project=project_obj, is_active=True, parent=None)

                regions = MyRegionSerializer(data, many=True, context={'request': request})

            else:
                regions_id = UserRole.objects.filter(user=request.user, project=project_obj).select_related('user', 'group', 'site', 'organization',
                                                                      'staff_project', 'region').filter(
                                                                   Q(group__name="Region Supervisor", region__is_active=True)|
                                                                   Q(group__name="Region Reviewer", region__is_active=True)).values_list('region_id', flat=True)
                data = Region.objects.filter(parent=None, id__in=regions_id)
                regions = MyRegionSerializer(data, many=True, context={'request': request})
            return Response({'regions': regions.data})

        except ObjectDoesNotExist:
            return Response(data="Project Id does not exist.", status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(data="Project Id params required.", status=status.HTTP_400_BAD_REQUEST)


class MySitesView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args,  **kwargs):

        project_id = request.query_params.get('project', None)

        if project_id:
            try:
                project_obj = Project.objects.get(id=project_id)
                is_project_manager_or_team_admin = UserRole.objects.select_related().filter(user=request.user).filter(Q(group__name="Project Manager",
                                                             project=project_obj, project__is_active=True)|
                                                                           Q(group__name="Organization Admin",
                                                             organization=project_obj.organization, organization__is_active=True)).exists()

                paginator = PageNumberPagination()
                paginator.page_size = 50

                if is_project_manager_or_team_admin:
                    data = Site.objects.filter(project=project_obj, is_active=True)

                    result_page = paginator.paginate_queryset(data, request)

                    sites = MySiteSerializer(result_page, many=True, context={'request': request})
                    return paginator.get_paginated_response(sites.data)

                else:
                    sites_id = UserRole.objects.filter(user=request.user, project=project_obj).select_related('user', 'group', 'site', 'organization',
                                                                          'staff_project', 'region').filter(
                                                                       Q(group__name="Site Supervisor", site__is_active=True)|
                                                                       Q(group__name="Site Reviewer", site__is_active=True)).values_list('site_id', flat=True)
                    data = Site.objects.filter(id__in=sites_id)
                    result_page = paginator.paginate_queryset(data, request)
                    sites = MySiteSerializer(result_page, many=True, context={'request': request})
                    return paginator.get_paginated_response(sites.data)

            except Exception as e:
                return Response(data=str(e), status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(data="Project Id params required.", status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def submissions_map(request):
    type = request.query_params.get('type')
    project_id = request.query_params.get('project')

    if type == "submissions" and project_id:
        try:
            project_obj = Project.objects.get(id=project_id)
            is_project_manager_or_team_admin = UserRole.objects.filter(user=request.user).select_related('user',
                                                                                                         'group',
                                                                                                         'site',
                                                                                                         'organization',
                                                                                                         'staff_project',
                                                                                                         'region').filter(
                Q(group__name="Project Manager",
                  project=project_obj, project__is_active=True) | Q(group__name="Organization Admin",
                                                                    organization=project_obj.organization,
                                                                    organization__is_active=True)).exists()

            if is_project_manager_or_team_admin:
                submission_history = FieldSightLog.objects.select_related('source').filter(type=16, source=request.user, project=project_obj).order_by('-date')

                data = [{'submitted_by': history.get_source_name, 'form_name': history.get_event_name(), 'form_url': settings.SITE_URL+
                                                                                                      str(history.get_event_url()),
                         'extra_object': history.get_extraobj_name(), 'extra_object_url': history.get_extraobj_url(), 'date': history.date} for history in submission_history]

                return Response(data=data)

            else:
                queryset = UserRole.objects.filter(user=request.user, project=project_obj).select_related('user',
                                                                                                            'group',
                                                                                                            'site',
                                                                                                            'organization',
                                                                                                            'staff_project',
                                                                                                            'region')
                region_ids = queryset.filter(Q(group__name="Region Supervisor")|
                                             Q(group__name="Region Reviewer")).values_list('region', flat=True).distinct()
                region_site_ids = Site.objects.filter(region_id__in=region_ids).values_list('id', flat=True)

                site_ids = queryset.filter(Q(group__name="Site Supervisor")|
                                             Q(group__name="Site Reviewer")).values_list('site', flat=True).distinct()

                merge_site_ids = list(chain(site_ids, region_site_ids))

                submission_history = FieldSightLog.objects.select_related('source').filter(type=16, source=request.user,
                                                                                           site_id__in=merge_site_ids).order_by('-date')

                data = [{'submitted_by': history.get_source_name, 'form_name': history.get_event_name(),
                         'form_url': settings.SITE_URL +
                                     str(history.get_event_url()),
                         'extra_object': history.get_extraobj_name(), 'extra_object_url': history.get_extraobj_url(),
                         'date': history.date} for history in submission_history]

                return Response(data=data)

        except ObjectDoesNotExist:
            return Response(data="Project Id does not exist.", status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(data="type params required.", status=status.HTTP_400_BAD_REQUEST)


class AcceptInvite(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):

        try:
            user = User.objects.get(username=self.kwargs.get('username', None))
        except ObjectDoesNotExist:
            return Response(data='Username does not exist.', status=status.HTTP_400_BAD_REQUEST)

        try:
            invitation = UserInvite.objects.get(id=self.kwargs.get('pk'), is_used=False)
        except ObjectDoesNotExist:
            return Response(data='Invitation Id does not exist.', status=status.HTTP_400_BAD_REQUEST)

        profile = user.user_profile
        if not profile.organization:
            profile.organization = invitation.organization
            profile.save()
        if user.user_roles.all()[0].group.name == "Unassigned":
            previous_group = UserRole.objects.filter(user=user, group__name="Unassigned")
            previous_group.delete()

        site_ids = invitation.site.all().values_list('pk', flat=True)
        project_ids = invitation.project.all().values_list('pk', flat=True)
    
        if invitation.regions.all().values_list('pk', flat=True).exists():
            regions_id = invitation.regions.all().values_list('pk', flat=True)
            for region_id in regions_id:
                project_id = Region.objects.get(id=region_id).project.id
                userrole, created = UserRole.objects.get_or_create(user=user, group=invitation.group,
                                                                   organization=invitation.organization,
                                                                   project_id=project_id,
                                                                   site_id=None, region_id=region_id)

        else:
            for project_id in project_ids:
                for site_id in site_ids:
                    userrole, created = UserRole.objects.get_or_create(user=user, group=invitation.group,
                                                                       organization=invitation.organization,
                                                                       project_id=project_id, site_id=site_id)
                if not site_ids:
                    userrole, created = UserRole.objects.get_or_create(user=user, group=invitation.group,
                                                                       organization=invitation.organization,
                                                                       project_id=project_id, site=None)

        if not project_ids:
            userrole, created = UserRole.objects.get_or_create(user=user, group=invitation.group,
                                                               organization=invitation.organization, project=None,
                                                               site=None, region=None)
            if invitation.group_id == 1:
                permission = Permission.objects.filter(codename='change_finstance')
                user.user_permissions.add(permission[0])

        invitation.is_used = True
        invitation.save()
        extra_msg = ""
        site = None
        project = None
        region = None
        if invitation.group.name == "Organization Admin":
            noti_type = 1
            content = invitation.organization

        elif invitation.group.name == "Project Manager":
            if invitation.project.all().count() == 1:
                noti_type = 2
                content = invitation.project.all()[0]
            else:
                noti_type = 26
                extra_msg = invitation.project.all().count()
                content = invitation.organization
            project = invitation.project.all()[0]

        elif invitation.group.name == "Reviewer":
            if invitation.site.all().count() == 1:
                noti_type = 3
                content = invitation.site.all()[0]
            else:
                noti_type = 27
                extra_msg = invitation.site.all().count()
                content = invitation.project.all()[0]
            project = invitation.project.all()[0]

        elif invitation.group.name == "Site Supervisor":
            if invitation.site.all().count() == 1:
                noti_type = 4
                content = invitation.site.all()[0]
            else:
                noti_type = 28
                extra_msg = invitation.site.all().count()
                content = invitation.project.all()[0]
            project = invitation.project.all()[0]

        elif invitation.group.name == "Region Reviewer":
            if invitation.regions.all().count() == 1:
                noti_type = 37
                content = invitation.regions.all()[0]
            else:
                noti_type = 39
                extra_msg = invitation.regions.all().count()
                content = invitation.project.all()[0]
            project = invitation.project.all()[0]

        elif invitation.group.name == "Region Supervisor":
            if invitation.regions.all().count() == 1:
                noti_type = 38
                content = invitation.regions.all()[0]
            else:
                noti_type = 40
                extra_msg = invitation.regions.all().count()
                content = invitation.project.all()[0]
            project = invitation.project.all()[0]

        elif invitation.group.name == "Unassigned":
            noti_type = 24
            content = invitation.organization

        elif invitation.group.name == "Project Donor":
            noti_type = 25
            content = invitation.project.all()[0]

        noti = invitation.logs.create(source=user, type=noti_type, title="new Role",
                                      organization=invitation.organization,
                                      extra_message=extra_msg, project=project, site=site, content_object=content,
                                      extra_object=invitation.by_user,
                                      description="{0} was added as the {1} of {2} by {3}.".
                                      format(user.username, invitation.group.name, content.name, invitation.by_user))

        return Response(data='Accept Invitation Successfully.', status=status.HTTP_200_OK)


class AcceptAllInvites(APIView):

    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):

        try:
            user = get_object_or_404(User, username=self.kwargs.get('username', None))

        except ObjectDoesNotExist:
            return Response(data='Username does not exist.', status=status.HTTP_400_BAD_REQUEST)

        invitations = UserInvite.objects.filter(email=user.email, is_used=False, is_declied=False)

        profile = user.user_profile
        if not profile.organization:
            profile.organization = invitations[0].organization
            profile.save()
        if user.user_roles.all()[0].group.name == "Unassigned":
            previous_group = UserRole.objects.filter(user=user, group__name="Unassigned")
            previous_group.delete()

        for invitation in invitations:

            site_ids = invitation.site.all().values_list('pk', flat=True)
            project_ids = invitation.project.all().values_list('pk', flat=True)
            if invitation.regions.all().values_list('pk', flat=True).exists():
                regions_id = invitation.regions.all().values_list('pk', flat=True)
                for region_id in regions_id:
                    project_id = Region.objects.get(id=region_id).project.id
                    userrole, created = UserRole.objects.get_or_create(user=user, group=invitation.group,
                                                                       organization=invitation.organization,
                                                                       project_id=project_id,
                                                                       site_id=None, region_id=region_id)

            else:
                for project_id in project_ids:
                    for site_id in site_ids:
                        userrole, created = UserRole.objects.get_or_create(user=user, group=invitation.group,
                                                                           organization=invitation.organization,
                                                                           project_id=project_id, site_id=site_id)
                    if not site_ids:
                        userrole, created = UserRole.objects.get_or_create(user=user, group=invitation.group,
                                                                           organization=invitation.organization,
                                                                           project_id=project_id, site=None)

            if not project_ids:
                userrole, created = UserRole.objects.get_or_create(user=user, group=invitation.group,
                                                                   organization=invitation.organization, project=None,
                                                                   site=None, region=None)
                if invitation.group_id == 1:
                    permission = Permission.objects.filter(codename='change_finstance')
                    user.user_permissions.add(permission[0])

            invitation.is_used = True
            invitation.save()
            extra_msg = ""
            site = None
            project = None
            region = None
            if invitation.group.name == "Organization Admin":
                noti_type = 1
                content = invitation.organization

            elif invitation.group.name == "Project Manager":
                if invitation.project.all().count() == 1:
                    noti_type = 2
                    content = invitation.project.all()[0]
                else:
                    noti_type = 26
                    extra_msg = invitation.project.all().count()
                    content = invitation.organization
                project = invitation.project.all()[0]

            elif invitation.group.name == "Reviewer":
                if invitation.site.all().count() == 1:
                    noti_type = 3
                    content = invitation.site.all()[0]
                else:
                    noti_type = 27
                    extra_msg = invitation.site.all().count()
                    content = invitation.project.all()[0]
                project = invitation.project.all()[0]

            elif invitation.group.name == "Site Supervisor":
                if invitation.site.all().count() == 1:
                    noti_type = 4
                    content = invitation.site.all()[0]
                else:
                    noti_type = 28
                    extra_msg = invitation.site.all().count()
                    content = invitation.project.all()[0]
                project = invitation.project.all()[0]

            elif invitation.group.name == "Region Reviewer":
                if invitation.regions.all().count() == 1:
                    noti_type = 37
                    content = invitation.regions.all()[0]
                else:
                    noti_type = 39
                    extra_msg = invitation.regions.all().count()
                    content = invitation.project.all()[0]
                project = invitation.project.all()[0]

            elif invitation.group.name == "Region Supervisor":
                if invitation.regions.all().count() == 1:
                    noti_type = 38
                    content = invitation.regions.all()[0]
                else:
                    noti_type = 40
                    extra_msg = invitation.regions.all().count()
                    content = invitation.project.all()[0]
                project = invitation.project.all()[0]

            elif invitation.group.name == "Unassigned":
                noti_type = 24
                content = invitation.organization

            elif invitation.group.name == "Project Donor":
                noti_type = 25
                content = invitation.project.all()[0]

            noti = invitation.logs.create(source=user, type=noti_type, title="new Role",
                                          organization=invitation.organization,
                                          extra_message=extra_msg, project=project, site=site, content_object=content,
                                          extra_object=invitation.by_user,
                                          description="{0} was added as the {1} of {2} by {3}.".
                                          format(user.username, invitation.group.name, content.name, invitation.by_user))

        return Response(data='Accept all invitations Successfully.', status=status.HTTP_200_OK)


class DeclineInvite(APIView):
    """
        A ViewSet for deleting the xform from my forms
        """
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            invitation = UserInvite.objects.get(pk=self.kwargs.get('pk'), is_used=False)
        except ObjectDoesNotExist:
            return Response(data='Invitation Id does not exist.', status=status.HTTP_400_BAD_REQUEST)

        invitation.is_used = True
        invitation.is_declined = True
        invitation.save()
        return Response(data='Decline Invitation Successfully.', status=status.HTTP_200_OK)


# get the submissions made my user along with the location point
# used for the my profile page
@permission_classes([IsAuthenticated, ])
@api_view(['GET'])
def latest_submission(request):
    # submissions are to be extracted from mongodb to retrieve the submission data along with latlong points
    submissions = settings.MONGO_DB.instances.aggregate([{"$match": {"_submitted_by": request.user.username}}, {
        "$project": {
            "_id": 0, "type": {"$literal": "Feature"},
            "geometry": {"type": {"$literal": "Point"}, "coordinates": "$_geolocation"}, "properties": {
                "id": "$_id", "form_id_string": "$_xform_id_string", "submitted_by": "$_submitted_by",
                "status": "$fs_status"
            }
        }
    }])
    response_submissions = list(submissions["result"])
    for item in response_submissions:
        id_string = item['properties']['form_id_string']
        xf = XForm.objects.get(id_string=id_string).title
        item['properties']['form'] = xf

        instance_id = item['properties']['id']
        item['properties']['detail_url'] = "/#/submission-details/{}".format(instance_id)

    return Response(response_submissions)

