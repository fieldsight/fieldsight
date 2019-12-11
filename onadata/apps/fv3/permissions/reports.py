from rest_framework import permissions

from onadata.apps.fieldsight.models import Project
from onadata.apps.fsforms.models import ReportSyncSettings


class ReportSyncPermission(permissions.BasePermission):
    """
    Report sync permission only to Organization admin and project managers
    """

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated()):
            return False
        if request.is_super_admin:
            return True
        sheet_id = view.kwargs.get('pk')
        sheet = ReportSyncSettings.objects.get(id=sheet_id)

        project_id = sheet.project_id
        if project_id:
            project = Project.objects.get(pk=project_id)
            user_role_asorgadmin = request.roles.filter(
                organization_id=project.organization_id,
                group__name="Organization Admin")
            if user_role_asorgadmin:
                return True
            user_role = request.roles.filter(project_id=project_id,
                                             group__name="Project Manager")
            if user_role:
                return True

        return False
