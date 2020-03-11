from rest_framework import permissions

from onadata.apps.fieldsight.models import Project, Organization
from .models import ReportSettings


class ReportingProjectFormsPermissions(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to View it.
    """

    def has_object_permission(self, request, view, obj):
        if request.is_super_admin:
            return True

        project = obj.project

        if project is not None:
            organization_id = project.organization_id

            organization = Organization.objects.get(id=organization_id)

            if organization.parent:
                if organization.parent.id in request.roles.filter(super_organization=organization.parent,
                                                                  group__name="Super Organization Admin"). \
                        values_list('super_organization_id', flat=True):

                    return True

            user_role_org_admin = request.roles.filter(organization_id=organization_id,
                                                       group__name="Organization Admin")

            if user_role_org_admin:
                return True

            user_role_as_manager = request.roles.filter(project_id=project.id, group__name__in=["Project Manager",
                                                                                                "Project Donor"])

            if user_role_as_manager:
                return True

        return False

    def has_permission(self, request, view):

        if request.is_super_admin:
            return True

        project_id = view.kwargs.get('pk', None)

        project = Project.objects.get(id=project_id)

        if project is not None:
            organization_id = project.organization_id

            organization = Organization.objects.get(id=organization_id)

            if organization.parent:
                if organization.parent.id in request.roles.filter(super_organization=organization.parent,
                                                                  group__name="Super Organization Admin"). \
                        values_list('super_organization_id', flat=True):
                    return True

            user_role_org_admin = request.roles.filter(organization_id=organization_id,
                                                       group__name="Organization Admin")

            if user_role_org_admin:
                return True

            user_role_as_manager = request.roles.filter(project_id=project.id, group__name__in=["Project Manager",
                                                                                                "Project Donor"])

            if user_role_as_manager:
                return True

        return False


class ReportingSettingsPermissions(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to create/edit it.
    """

    def has_permission(self, request, view):

        if request.is_super_admin:
            return True

        obj = ReportSettings.objects.get(id=view.kwargs.get('pk', None))

        project = obj.project

        if project is not None:
            organization_id = project.organization_id
            user_role_org_admin = request.roles.filter(organization_id=organization_id,
                                                       group__name="Organization Admin")

            if user_role_org_admin:
                return True

            user_role_as_manager = request.roles.filter(project_id=project.id, group__name__in=["Project Manager",
                                                                                                "Project Donor"])

            if user_role_as_manager:
                return True

        return False


class ReportingLogsPermissions(permissions.BasePermission):
    """
    Custom Report File Log permission
    """

    def has_permission(self, request, view):

        if request.is_super_admin:
            return True

        obj = ReportSettings.objects.get(id=request.query_params.get('id', None))

        project = obj.project

        if project is not None:
            organization_id = project.organization_id
            user_role_org_admin = request.roles.filter(organization_id=organization_id,
                                                       group__name="Organization Admin")

            if user_role_org_admin:
                return True

            user_role_as_manager = request.roles.filter(project_id=project.id, group__name__in=["Project Manager",
                                                                                                "Project Donor"])

            if user_role_as_manager:
                return True

        return False
