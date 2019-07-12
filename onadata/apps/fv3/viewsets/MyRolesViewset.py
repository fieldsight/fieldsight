from django.db.models import Q
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from onadata.apps.fieldsight.models import UserInvite
from onadata.apps.users.models import UserProfile
from onadata.apps.userrole.models import UserRole
from onadata.apps.fv3.serializers.MyRolesSerializer import MyRolesSerializer, UserInvitationSerializer


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def my_roles(request):

    profile_obj = UserProfile.objects.select_related('user').get(user=request.user)
    profile = {'fullname': profile_obj.getname(), 'username': profile_obj.user.username, 'email': profile_obj.user.email,
               'address': profile_obj.address, 'phone': profile_obj.phone, 'profile_picture': profile_obj.profile_picture.url}

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
