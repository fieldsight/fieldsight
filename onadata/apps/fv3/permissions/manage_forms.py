from rest_framework import permissions

from onadata.apps.fieldsight.models import Project, Site
from onadata.apps.fsforms.models import Stage


class ManageFormsPermission(permissions.BasePermission):
    """
    Manage forms permissions only to Organization admin and project managers
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


class StagePermission(permissions.BasePermission):
    """
    Manage forms permissions only to Organization admin and project managers
    """

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated()):
            return False
        if request.is_super_admin:
            return True
        query_params = request.query_params
        stage_id = query_params.get('stage_id')
        stage = Stage.objects.get(pk=stage_id)
        project_id, site_id = None, None
        if stage.project:
            project_id = stage.project_id
        elif stage.site:
            site_id = stage.site_id
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


class DeployFormsPermission(permissions.BasePermission):
    """
    Deploy  forms permissions only to Organization admin and project managers
    """

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated()):
            return False
        if request.is_super_admin:
            return True
        query_params = request.query_params
        type = query_params.get('type')
        if not type:
            return False
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
                print(user_role)
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
