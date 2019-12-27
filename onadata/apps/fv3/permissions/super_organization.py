from django.core.exceptions import ObjectDoesNotExist
from rest_framework import permissions, status
from rest_framework.response import Response

from onadata.apps.fieldsight.models import Project


class SuperOrganizationAdminPermission(permissions.BasePermission):
    """
    Project and site level view by forms and status permission.
    """

    def has_permission(self, request, view):
        organization = view.kwargs.get('pk')

        if request.is_super_admin:
            return True
