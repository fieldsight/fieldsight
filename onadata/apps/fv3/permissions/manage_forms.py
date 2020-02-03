from rest_framework import permissions

from onadata.apps.fieldsight.models import Project, Site, Organization
from onadata.apps.fsforms.models import Stage, FieldSightXF


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
                organization = project.organization
                if organization.parent:
                    if organization.parent.id in request.roles.filter(super_organization=organization.parent,
                                                                      group__name="Super Organization Admin"). \
                            values_list('super_organization_id', flat=True):
                        return True
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
                organization = site.project.organization
                if organization.parent:
                    if organization.parent.id in request.roles.filter(super_organization=organization.parent,
                                                                      group__name="Super Organization Admin"). \
                            values_list('super_organization_id', flat=True):
                        return True
                user_role_asorgadmin = request.roles.filter(
                    organization_id=site.project.organization_id,
                    group__name="Organization Admin")
                if user_role_asorgadmin:
                    return True
                user_role = request.roles.filter(project_id=site.project_id,
                                                 group__name="Project Manager")
                if user_role:
                    return True

                user_role_as_supervisor_or_reviewer = request.roles.\
                    filter(site=site, group__name__in=["Site Supervisor", "Reviewer"])
                if user_role_as_supervisor_or_reviewer:
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
                organization = project.organization
                if organization.parent:
                    if organization.parent.id in request.roles.filter(super_organization=organization.parent,
                                                                      group__name="Super Organization Admin"). \
                            values_list('super_organization_id', flat=True):
                        return True

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
                site = Site.objects.filter(pk=site_id).select_related('project')[0]
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


class FormsPermission(permissions.BasePermission):
    """
    Manage forms permissions only to Organization admin and project managers
    """

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated()):
            return False
        if request.is_super_admin:
            return True
        project_ids = request.GET.getlist('project_id')
        projects_acess = request.roles.filter(
            project__id__in=project_ids,
            group__name__in=["Site Supervisor",
                             "Region Supervisor"]).values_list("project__id", flat=True).distinct()
        if project_ids:
            for project in project_ids:
                if int(project) not in projects_acess:
                    return False
            return True
        return False


class FormsSettingsPermission(permissions.BasePermission):
    """
    Manage forms permissions only to Organization admin and project managers
    """

    def has_permission(self, request, view):
        if request.is_super_admin:
            return True
        if request.method == "GET":
            form_id = request.query_params.get('form_id')
        elif request.method == "POST":
            form_id = request.data.get('form')
        elif request.method == "PUT":
            return True
        if form_id:
            pk, project_id, organization_id, site_id, site_project_id, site_project_organization_id = \
                FieldSightXF.objects.filter(pk=form_id).values_list(
                    'pk', 'project_id',
                    'project__organization_id',
                    'site_id', 'site__project_id', 'site__project__organization_id')[0]

            if project_id:
                organization = Organization.objects.get(id=organization_id)
                if organization.parent:
                    if organization.parent.id in request.roles.filter(super_organization=organization.parent,
                                                                      group__name="Super Organization Admin"). \
                            values_list('super_organization_id', flat=True):
                        return True
                user_role_asorgadmin = request.roles.filter(
                    organization_id=organization_id,
                    group__name="Organization Admin")
                if user_role_asorgadmin:
                    return True
                user_role = request.roles.filter(project_id=project_id,
                                                 group__name="Project Manager")
                if user_role:
                    return True
            else:
                organization = Organization.objects.get(id=site_project_organization_id)
                if organization.parent:
                    if organization.parent.id in request.roles.filter(super_organization=organization.parent,
                                                                      group__name="Super Organization Admin"). \
                            values_list('super_organization_id', flat=True):
                        return True
                user_role_asorgadmin = request.roles.filter(
                    organization_id=site_project_organization_id,
                    group__name="Organization Admin")
                if user_role_asorgadmin:
                    return True
                user_role = request.roles.filter(project_id=site_project_id,
                                                 group__name="Project Manager")
                if user_role:
                    return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.is_super_admin:
            return True
        form_id = obj.form_id
        pk, project_id, organization_id, site_id, site_project_id, site_project_organization_id = \
            FieldSightXF.objects.filter(pk=form_id).values_list(
                'pk', 'project_id',
                'project__organization_id',
                'site_id', 'site__project_id', 'site__project__organization_id')[0]

        if project_id:
            user_role_asorgadmin = request.roles.filter(
                organization_id=organization_id,
                group__name="Organization Admin")
            if user_role_asorgadmin:
                return True
            user_role = request.roles.filter(project_id=project_id,
                                             group__name="Project Manager")
            if user_role:
                return True
        else:
            user_role_asorgadmin = request.roles.filter(
                organization_id=site_project_organization_id,
                group__name="Organization Admin")
            if user_role_asorgadmin:
                return True
            user_role = request.roles.filter(project_id=site_project_id,
                                             group__name="Project Manager")
            if user_role:
                return True
