from django.db.models import Q
from rest_framework import permissions

from onadata.apps.fieldsight.models import Project


class SubmissionDetailPermission(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to View it.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user
        finstance = obj.fieldsight_instance
        form = finstance.fsxf
        is_doner = False
        if request.group and request.group.name == "Super Admin":
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

        if form.site is not None:
            user_role = request.roles.filter(Q(site_id=form.site_id, group__name="Site Supervisor") |
                                             Q(project_id=form.site.project_id, group__name="Project Donor"))
            if user_role and request.roles.filter(project_id=form.site.project_id, group__name="Project Donor"):
                is_doner = True
        else:
            user_role = request.roles.filter(project_id=form.project_id, group__name="Project Donor")
            if user_role:
                is_doner = True

        if request.roles.filter(project_id=project_id, group__name__in=["Reviewer", "Region Reviewer"]).exists():
            return True

        if user_role:
            return True

        if request.roles.filter(project_id=project_id,
                                group__name__in=["Site Supervisor", "Region Supervisor"]).exists():
            return True

        return False


class SubmissionChangePermission(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to View it.
    """

    def has_object_permission(self, request, view, obj):
        finstance = obj.fieldsight_instance
        site = finstance.site
        has_acess = False
        if site:
            has_acess = False
            if request.roles.filter(site=site, group__name="Reviewer") or request.roles.filter(region=site.region,
                                                                                               group__name="Region Reviewer"):
                has_acess = True
            elif request.roles.filter(project=site.project, group__name="Project Manager") or \
                    request.roles.filter(organization=site.project.organization,
                                         group__name="Organization Admin") or request.roles.filter(
                group__name="Super Admin"):
                has_acess = True

        return has_acess