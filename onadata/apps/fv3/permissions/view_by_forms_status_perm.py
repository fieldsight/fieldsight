from django.core.exceptions import ObjectDoesNotExist
from rest_framework import permissions, status
from rest_framework.response import Response

from onadata.apps.fieldsight.models import Project
from onadata.apps.fsforms.models import FInstance
from onadata.apps.fv3.role_api_permissions import check_site_permission


class ViewDataPermission(permissions.BasePermission):
    """
    Project and site level view by forms and status permission.
    """

    def has_permission(self, request, view):
        project = request.query_params.get('project', None)
        site = request.query_params.get('site', None)

        if request.is_super_admin:
            return True

        if project is not None:
            try:
                project = Project.objects.select_related('organization').get(id=project)
            except ObjectDoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND, data={"detail": "Not found."})

            organization = project.organization
            organization_id = organization.id

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

        elif site is not None:
            return check_site_permission(request, site)


class DeleteFInstancePermission(permissions.BasePermission):

    def has_permission(self, request, view):

        try:
            finstance = FInstance.objects.get(instance_id=view.kwargs.get('pk'))

        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        form = finstance.fsxf

        if request.is_super_admin:
            return True

        if form.site is not None:
            project_id = form.site.project_id
        else:
            project_id = form.project_id
        organization_id = Project.objects.get(pk=project_id).organization.id
        user_role_asorgadmin = request.roles.filter(organization_id=organization_id, group__name="Organization Admin")
        if user_role_asorgadmin:
            return True
        if form.site is not None:
            site_id = form.site_id
            user_role = request.roles.filter(site_id=site_id, group__name="Reviewer")
            if user_role:
                return True
        else:
            project_id = form.project.id
        user_role = request.roles.filter(project_id=project_id, group__name="Project Manager")
        if user_role:
            return True
        if request.roles.filter(project_id=project_id, group__name__in=["Reviewer", "Region Reviewer"]).exists():
            return True
        return False