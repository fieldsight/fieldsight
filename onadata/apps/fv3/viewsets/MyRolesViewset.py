from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User, Permission
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import permission_classes, api_view, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from onadata.apps.fieldsight.models import UserInvite, Region
from onadata.apps.users.models import UserProfile
from onadata.apps.userrole.models import UserRole
from onadata.apps.fv3.serializers.MyRolesSerializer import MyRolesSerializer, UserInvitationSerializer
from onadata.apps.fsforms.enketo_utils import CsrfExemptSessionAuthentication


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def my_roles(request):

    profile_obj = UserProfile.objects.select_related('user').get(user=request.user)
    profile = {'fullname': profile_obj.getname(), 'username': profile_obj.user.username, 'email': profile_obj.user.email,
               'address': profile_obj.address, 'phone': profile_obj.phone, 'profile_picture': profile_obj.profile_picture.url,
               'twitter': profile_obj.twitter, 'whatsapp': profile_obj.whatsapp, 'skype': profile_obj.skype,
               'google_talk': profile_obj.google_talk}

    roles = UserRole.objects.filter(user=request.user).select_related('user', 'group', 'site', 'organization',
                                                                      'staff_project', 'region').filter(Q(group__name="Organization Admin", organization__is_active=True)|
                                                                   Q(group__name="Project Manager", project__is_active=True)|
                                                                   Q(group__name="Project Donor", project__is_active=True)|
                                                                   Q(group__name="Region Supervisor", region__is_active=True)|
                                                                   Q(group__name="Region Reviewer", region__is_active=True)|
                                                                   Q(group__name="Site Supervisor", site__is_active=True)|
                                                                   Q(group__name="Site Reviewer", site__is_active=True)|
                                                                   Q(group__name="Staff Project Manager", staff_project__is_deleted=False)

                                                                   )
    roles = MyRolesSerializer(roles, many=True)
    invitations = UserInvite.objects.select_related('by_user').filter(email=request.user.email, is_used=False, is_declied=False)

    invitations_serializer = UserInvitationSerializer(invitations, many=True)
    return Response({'profile': profile, 'roles': roles.data, 'invitations': invitations_serializer.data})


@permission_classes([IsAuthenticated])
@api_view(['POST'])
def accept_invite(request, pk, username):

    try:
        user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        return Response(data='Username does not exist.', status=status.HTTP_400_BAD_REQUEST)

    try:
        invitation = UserInvite.objects.get(id=pk)
    except ObjectDoesNotExist:
        return Response(data='UserInvite does not exist.', status=status.HTTP_400_BAD_REQUEST)

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


@permission_classes([IsAuthenticated])
@api_view(['POST'])
def accept_all_invites(request, username):

    try:
        user = get_object_or_404(User, username=username)

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


@permission_classes([IsAuthenticated, ])
@api_view(['POST'])
def decline_invite(request, pk):

    try:
        invitation = UserInvite.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return Response(data='Invitation Id does not exist.', status=status.HTTP_400_BAD_REQUEST)

    invitation.is_used = True
    invitation.is_declined = True
    invitation.save()

    return Response(data='Decline Invitation Successfully.', status=status.HTTP_200_OK)

