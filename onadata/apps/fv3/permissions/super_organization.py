from django.core.exceptions import ObjectDoesNotExist
from rest_framework import permissions, status
from rest_framework.response import Response

from onadata.apps.fieldsight.models import Project
from onadata.apps.fsforms.models import OrganizationFormLibrary


class SuperOrganizationAdminPermission(permissions.BasePermission):
    """
    super org admin permission
    """

    def has_permission(self, request, view):
        if view.kwargs.get('pk'):
            organization = view.kwargs.get('pk')
        else:
            organization = OrganizationFormLibrary.objects.get(id=view.kwargs.get('org_form_lib')).organization

        if request.is_super_admin:
            return True

        user_role_as_super_org_admin = request.roles.filter(super_organization_id=organization,
                                                            group__name="Super Organization Admin")
        if user_role_as_super_org_admin:
            return True

        else:
            return False
