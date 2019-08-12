from rest_framework import permissions

from onadata.apps.fieldsight.models import Project, Site


class ManageFormsPermission(permissions.BasePermission):
    """
    Manage forms permissions only to Organization aamin and project managers
    """

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated()):
            return False
        if request.is_super_admin:
            return True
        query_params = request.query_params
        site_id = query_params.get('site_id')
        project_id = query_params.get('project_id')
        if project_id or site_id:
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
            else:
                site = Site.objects.get(pk=site_id)
                user_role_asorgadmin = request.roles.filter(
                    organization_id=site.project.organization_id,
                    group__name="Organization Admin")
                if user_role_asorgadmin:
                    return True
                user_role = request.roles.filter(project_id=site.project_id,
                                                 group__name="Project Manager")
                if user_role:
                    return True
        return False
