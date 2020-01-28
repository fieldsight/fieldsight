from itertools import chain

from django.db.models import Q
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User, Permission
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import BasicAuthentication

from rest_framework.decorators import permission_classes, api_view, \
    authentication_classes
from rest_framework.generics import UpdateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from onadata.apps.fieldsight.models import UserInvite, Region, Project, Site, SuperOrganization, Organization
from onadata.apps.users.models import UserProfile
from onadata.apps.userrole.models import UserRole
from onadata.apps.eventlog.models import FieldSightLog
from onadata.apps.fv3.serializers.MyRolesSerializer import MyRolesSerializer, \
    UserInvitationSerializer, MyRegionSerializer, MySiteSerializer, \
    ChangePasswordSerializer
from onadata.apps.fsforms.enketo_utils import CsrfExemptSessionAuthentication
from onadata.apps.logger.models import XForm


class MySitesPagination(PageNumberPagination):
    page_size = 100


def is_project_manager_or_team_admin(project_obj, user):

    org = project_obj.organization

    if org.parent:
        super_org = org.parent
    else:
        super_org = None

    is_pm_admin = user.user_roles.select_related('user', 'group',
                                                                'site',
                                                                'organization',
                                                                'staff_project',
                                                                'project',
                                                                'region').\
        filter(Q(group__name__in=["Project Manager", "Project Donor"], project=project_obj,
                 project__is_active=True, ended_at=None) |
               Q(group__name="Organization Admin", organization=project_obj.organization,
                 organization__is_active=True, ended_at=None) |
               Q(group__name="Super Organization Admin", super_organization=super_org,
                 super_organization__is_active=True, ended_at=None)).exists()

    return is_pm_admin


def my_site_ids(project_obj, user):
    queryset = UserRole.objects.filter(user=user, project=project_obj).select_related('user',
                                                                                              'group',
                                                                                              'site',
                                                                                              'organization',
                                                                                              'staff_project',
                                                                                              'region')
    region_ids = queryset.filter(Q(group__name="Region Supervisor") |
                                 Q(group__name="Region Reviewer")).values_list('region', flat=True).distinct()
    region_site_ids = Site.objects.filter(region_id__in=region_ids).values_list('id', flat=True)

    site_ids = queryset.filter(Q(group__name="Site Supervisor") |
                               Q(group__name="Site Reviewer")).values_list('site', flat=True).distinct()

    merge_site_ids = list(chain(site_ids, region_site_ids))

    return merge_site_ids


def get_teams(user, org_id):
    my_teams = UserRole.objects.filter(user=user, ended_at=None).filter(
        Q(group__name="Organization Admin", organization__is_active=True) |
        Q(group__name="Project Manager", project__is_active=True) |
        Q(group__name="Project Donor", project__is_active=True) |
        Q(group__name="Region Supervisor", region__is_active=True) |
        Q(group__name="Region Reviewer", region__is_active=True) |
        Q(group__name="Site Supervisor", site__is_active=True) |
        Q(group__name="Reviewer", site__is_active=True)).distinct('organization').\
        values_list('organization_id', flat=True)

    return my_teams


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def my_roles(request):
    user_id = request.GET.get('profile', None)
    if user_id is not None:
        try:
            profile_obj = UserProfile.objects.select_related('user').get(user_id=int(user_id))
        except ObjectDoesNotExist:
            profile_obj = UserProfile.objects.create(user_id=int(user_id))
    else:
        try:
            profile_obj = UserProfile.objects.select_related('user').get(user=request.user)
        except ObjectDoesNotExist:
            profile_obj = UserProfile.objects.create(user=request.user)

    guide_popup = True if request.user.user_roles.all().count() == 0 or \
                          (request.user.user_roles.filter(group__name="Unassigned")
                           and request.user.user_roles.all().count() == 1) else False

    can_create_team = True

    if request.user.organizations.all().exists():
        can_create_team = False

    if user_id is not None:
        user = User.objects.get(id=user_id)
        can_create_team = False

    else:
        user = request.user

    profile = {'id': profile_obj.id, 'fullname': profile_obj.getname(), 'username': profile_obj.user.username,
               'email': profile_obj.user.email, 'address': profile_obj.address, 'phone': profile_obj.phone,
               'profile_picture': profile_obj.profile_picture.url, 'twitter': profile_obj.twitter,
               'whatsapp': profile_obj.whatsapp, 'skype': profile_obj.skype, 'google_talk': profile_obj.google_talk,
               'can_create_team': can_create_team, 'guide_popup': guide_popup}

    teams = UserRole.objects.filter(user=user, ended_at=None).select_related('user', 'group', 'site', 'organization',
                                                                      'staff_project', 'region').\
        filter(Q(group__name="Organization Admin", organization__is_active=True) |
               Q(group__name="Project Manager", project__is_active=True) |
               Q(group__name="Project Donor", project__is_active=True) |
               Q(group__name="Region Supervisor", region__is_active=True) |
               Q(group__name="Region Reviewer", region__is_active=True) |
               Q(group__name="Site Supervisor", site__is_active=True) |
               Q(group__name="Reviewer", site__is_active=True)).distinct('organization')

    teams = MyRolesSerializer(teams, many=True, context={'user': request.user})

    if user_id is not None:
        invitations = []
        invitations_serializer = UserInvitationSerializer(invitations, many=True, context={'request': request})

    else:
        invitations = UserInvite.objects.select_related('by_user', 'group').filter(email__icontains=request.user.email,
                                                                                   is_used=False, is_declied=False)
        invitations_serializer = UserInvitationSerializer(invitations, many=True, context={'request': request})

    return Response({'profile': profile, 'teams': teams.data, 'invitations': invitations_serializer.data})


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def my_regions(request):

    project_id = request.query_params.get('project', None)

    if project_id:
        try:
            project_obj = Project.objects.get(id=project_id)
        except ObjectDoesNotExist:
            return Response(data="Project Id does not exist.", status=status.HTTP_204_NO_CONTENT)

        if is_project_manager_or_team_admin(project_obj, request.user):
            data = Region.objects.filter(project=project_obj, is_active=True, parent=None)

            regions = MyRegionSerializer(data, many=True, context={'request': request})

        else:
            regions_id = request.roles.filter(project=project_obj).select_related('user', 'group', 'site',
                                                                                  'organization', 'staff_project',
                                                                                  'region').\
                filter(group__name__in=["Region Supervisor", "Region Reviewer"], region__is_active=True,
                       ended_at=None).values_list('region_id', flat=True)
            data = Region.objects.filter(id__in=regions_id)
            regions = MyRegionSerializer(data, many=True, context={'request': request})
        return Response({'regions': regions.data})

    else:
        return Response(data="Project Id params required.", status=status.HTTP_400_BAD_REQUEST)


class MySitesView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args,  **kwargs):

        project_id = request.query_params.get('project', None)
        search_param = self.request.query_params.get('q', None)

        if project_id:
            try:
                project_obj = Project.objects.get(id=project_id)
                paginator = PageNumberPagination()
                paginator.page_size = 200

                if is_project_manager_or_team_admin(project_obj, request.user):
                    if search_param:
                        data = Site.objects.filter(Q(name__icontains=search_param) |
                                                   Q(identifier__icontains=search_param), project=project_obj,
                                                   is_active=True, site__isnull=True, is_survey=False)

                    else:
                        data = Site.objects.filter(project=project_obj, is_active=True, site__isnull=True,
                                                   is_survey=False)

                    result_page = paginator.paginate_queryset(data, request)

                    sites = MySiteSerializer(result_page, many=True, context={'request': request})
                    return paginator.get_paginated_response({'data': sites.data, 'query': search_param})

                else:
                    region_ids = request.roles.filter(group__name__in=["Region Supervisor", "Region Reviewer"],
                                                      region__is_active=True, project=project_obj, ended_at=None).\
                        distinct('region_id').values_list('region_id', flat=True)
                    reg_sites = []

                    for reg in region_ids:
                        region = Region.objects.get(id=reg)
                        reg_sites.extend(region.get_sites_id())

                    sites_id = request.roles.select_related('user', 'group', 'site', 'organization',
                                                                          'staff_project', 'region').filter(
                        group__name__in=["Site Supervisor", "Reviewer"], ended_at=None, project=project_obj).\
                        distinct('site_id').values_list('site_id', flat=True)

                    total_sites = list(chain(reg_sites, sites_id))
                    if search_param:
                        data = Site.objects.filter(Q(name__icontains=search_param) |
                                                   Q(identifier__icontains=search_param),id__in=total_sites)
                    else:
                        data = Site.objects.filter(id__in=total_sites)

                    result_page = paginator.paginate_queryset(data, request)

                    sites = MySiteSerializer(result_page, many=True, context={'request': request})
                    return paginator.get_paginated_response({'data': sites.data, 'query': search_param})

            except Exception as e:
                return Response(data=str(e), status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(data="Project Id params required.", status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def submissions_map(request):
    type = request.query_params.get('type')
    project_id = request.query_params.get('project')

    if project_id:
        try:
            project_obj = Project.objects.get(id=project_id)

            if type == "submissions":

                if is_project_manager_or_team_admin(project_obj, request.user):
                    submission_history = FieldSightLog.objects.select_related('source').\
                        filter(type=16, source=request.user, project=project_obj).order_by('-date')

                    submission_history = [sub for sub in submission_history if sub.content_object.is_deleted is False]

                    data = [{'submitted_by': history.get_source_name(), 'form_name': history.get_event_name(),
                             'profile':  settings.SITE_URL + history.get_source_url(),
                             'form_url': settings.SITE_URL + str(history.get_event_url()),
                             'extra_object': history.get_extraobj_name(),
                             'extra_object_url':  settings.SITE_URL + history.get_extraobj_url(),
                             'date': history.date} for history in submission_history]

                    return Response(data=data)

                else:

                    merge_site_ids = my_site_ids(project_obj, request.user)

                    submission_history = FieldSightLog.objects.select_related('source').\
                        filter(type=16, source=request.user, site_id__in=merge_site_ids).order_by('-date')
                    submission_history = [sub for sub in submission_history if sub.content_object.is_deleted is False]

                    data = [{'submitted_by': history.get_source_name(),
                             'profile':  settings.SITE_URL + history.get_source_url(),
                             'form_name': history.get_event_name(),
                             'form_url': settings.SITE_URL +
                                         str(history.get_event_url()),
                             'extra_object': history.get_extraobj_name(),
                             'extra_object_url': settings.SITE_URL + history.get_extraobj_url(),
                             'date': history.date} for history in submission_history]

                    return Response(data=data)

            elif type == 'map':
                if is_project_manager_or_team_admin(project_obj, request.user):

                    submissions = settings.MONGO_DB.instances.aggregate(
                        [{"$match": {"fs_project": {"$in": [int(project_id), str(project_id), unicode(project_id)]},
                                     "_submitted_by": request.user.username, '_deleted_at': None}}, {
                            "$project": {
                                "_id": 0, "type": {"$literal": "Feature"},
                                "geometry": {"type": {"$literal": "Point"}, "coordinates": "$_geolocation"},
                                "properties": {
                                    "id": "$_id", "form_id_string": "$_xform_id_string",
                                    "submitted_by": "$_submitted_by",
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
                        item['properties']['detail_url'] = settings.SITE_URL + \
                                                           "/fieldsight/application/?submission={}#/submission-details".\
                                                               format(str(instance_id))
                    return Response(response_submissions)
                else:
                    int_merge_site_ids = my_site_ids(project_obj, request.user)
                    str_merge_site_ids = map(str, int_merge_site_ids)
                    merge_site_ids = list(set(int_merge_site_ids+str_merge_site_ids))

                    submissions = settings.MONGO_DB.instances.aggregate(
                        [{"$match": {"fs_site": {"$in": merge_site_ids}, "_submitted_by": request.user.username,
                                     '_deleted_at': None}}, {
                            "$project": {
                                "_id": 0, "type": {"$literal": "Feature"},
                                "geometry": {"type": {"$literal": "Point"}, "coordinates": "$_geolocation"},
                                "properties": {
                                    "id": "$_id", "form_id_string": "$_xform_id_string",
                                    "submitted_by": "$_submitted_by",
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
                        item['properties']['detail_url'] = settings.SITE_URL + \
                                                           "/fieldsight/application/?submission={}#/submission-details".\
                                                               format(str(instance_id))

                    return Response(response_submissions)
            else:
                return Response(data="type params required.", status=status.HTTP_400_BAD_REQUEST)

        except ObjectDoesNotExist:
            return Response(data="Project Id does not exist.", status=status.HTTP_204_NO_CONTENT)

    else:
        return Response(data="Project Id required.", status=status.HTTP_400_BAD_REQUEST)


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

        if invitation.teams.all().values_list('pk', flat=True).exists():
            teams_id = invitation.teams.all().values_list('pk', flat=True)
            for team_id in teams_id:
                userrole, created = UserRole.objects.get_or_create(user=user,
                                                                   group=invitation.group,
                                                                   organization_id=team_id)
        elif invitation.regions.all().values_list('pk', flat=True).exists():
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
                    try:
                        userrole, created = UserRole.objects.get_or_create(user=user, group=invitation.group,
                                                                           organization=invitation.organization,
                                                                           project_id=project_id, site=None)
                    except AttributeError:
                        invitation.is_used = True
                        invitation.save()

        if not project_ids:
            if invitation.group.name == 'Super Organization Admin':
                userrole, created = UserRole.objects.get_or_create(user=user, group=invitation.group,
                                                                   super_organization=invitation.super_organization,
                                                                   organization=None, project=None, site=None,
                                                                   region=None)

            if invitation.group.name == 'Organization Admin' and not invitation.teams.all().exists():
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

        if invitation.group.name == "Super Organization Admin":
            noti_type = 41
            content = invitation.super_organization

        elif invitation.group.name == "Organization Admin" and invitation.teams.all().exists():
            if invitation.teams.all().count() == 1:
                noti_type = 1
                content = invitation.teams.all()[0]
            else:
                noti_type = 42
                extra_msg = invitation.teams.all().count()
                content = invitation.teams.all()[0].parent

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
            # import ipdb;ipdb.set_trace()

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
        else:
            noti_type = None
            content = None

        noti = invitation.logs.create(source=user, type=noti_type, title="new Role",
                                      organization=invitation.organization,
                                      extra_message=extra_msg, project=project, site=site, content_object=content,
                                      extra_object=invitation.by_user,
                                      description=u"{0} was added as the {1} "
                                                  u"of {2} by {3}.".
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

        invitations = UserInvite.objects.filter(email__icontains=user.email, is_used=False, is_declied=False)

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
                        try:
                            userrole, created = UserRole.objects.get_or_create(user=user, group=invitation.group,
                                                                               organization=invitation.organization,
                                                                               project_id=project_id, site=None)
                        except AttributeError:
                            invitation.is_used = True
                            invitation.save()

            if not project_ids:

                if invitation.group.name == 'Super Organization Admin':
                    userrole, created = UserRole.objects.get_or_create(user=user, group=invitation.group,
                                                                       super_organization=invitation.organization,
                                                                       organization=None, project=None,
                                                                       site=None, region=None)

                if invitation.group.name == 'Organization Admin' and not invitation.teams.all().exists():
                    userrole, created = UserRole.objects.get_or_create(user=user, group=invitation.group,
                                                                       organization=invitation.organization,
                                                                       project=None,
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

            if invitation.group.name == "Super Organization Admin":
                noti_type = 41
                content = invitation.super_organization

            elif invitation.group.name == "Organization Admin" and invitation.teams.all().exists():
                if invitation.teams.all().count() == 1:
                    noti_type = 1
                    content = invitation.teams.all()[0]
                else:
                    noti_type = 42
                    extra_msg = invitation.teams.all().count()
                    content = invitation.teams.all()[0].parent

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

            else:
                noti_type = None
                content = None

            noti = invitation.logs.create(source=user, type=noti_type, title="new Role",
                                          organization=invitation.organization,
                                          extra_message=extra_msg, project=project, site=site, content_object=content,
                                          extra_object=invitation.by_user,
                                          description=u"{0} was added as the {1} of {2} by {3}.".
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


@csrf_exempt
def change_password(request):
    object = request.user
    serializer = ChangePasswordSerializer(data=request.POST)

    if serializer.is_valid():
        # Check old password
        if not object.check_password(
                serializer.data.get("old_password")):
            return JsonResponse({"old_password": ["Wrong password."]},
                            status=status.HTTP_400_BAD_REQUEST)
        # set_password also hashes the password that the user will get
        object.set_password(serializer.data.get("new_password"))
        object.save()
        response = {
            'status': 'success',
            'code': status.HTTP_200_OK,
            'message': 'Password updated successfully',
            'data': []
        }

        return JsonResponse(response)

    return JsonResponse(serializer.errors)