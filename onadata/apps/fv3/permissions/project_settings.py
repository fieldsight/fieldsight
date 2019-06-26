from rest_framework import permissions

from onadata.apps.fieldsight.models import Project


class ProjectSettingsPermission(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to View it.
    """

    def has_object_permission(self, request, view, obj):
        if request.group and request.group.name == "Super Admin":
            return True

        project_id = obj.id
        organization_id = Project.objects.get(pk=project_id).organization.id
        user_role_asorgadmin = request.roles.filter(organization_id=organization_id, group__name="Organization Admin")
        if user_role_asorgadmin:
            return True


        user_role = request.roles.filter(project_id=project_id, group__name="Project Manager")
        if user_role:
            return True

        return False
