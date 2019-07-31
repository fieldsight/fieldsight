from rest_framework.permissions import DjangoObjectPermissions
from rest_framework.response import Response
from rest_framework import status, permissions

from onadata.apps.fieldsight.models import Project


class ProjectRoleApiPermissions(DjangoObjectPermissions):
    """
    Object-level permission to only allow owners of an object to edit, update and delete it and also model-level
    permission.
    """

    def has_permission(self, request, view):

        if request.is_super_admin:
            return True

        project_id = request.query_params.get('project', None)

        try:
            if project_id:

                user_id = request.user.id
                user_role = request.roles.filter(user_id=user_id, project_id=int(project_id), group__name="Project Manager")
                if user_role:
                    return True

                organization_id = Project.objects.get(pk=int(project_id)).organization.id
                user_role_asorgadmin = request.roles.filter(user_id=user_id, organization_id=organization_id, group_id=1)

                if user_role_asorgadmin:
                    return True

                return False

            elif view.get_object():
                obj = view.get_object()

                try:
                    project_id = obj.project.id
                except:
                    project_id = obj.id

                user_id = request.user.id
                user_role = request.roles.filter(user_id=user_id, project_id=project_id, group__name="Project Manager")

                if user_role:
                    return True

                organization_id = Project.objects.get(pk=project_id).organization.id
                user_role_asorgadmin = request.roles.filter(user_id=user_id, organization_id=organization_id, group_id=1)

                if user_role_asorgadmin:
                    return True

                return False

            else:
                return False
        except AssertionError:
            return Response({"message": "Project Id is required."}, status=status.HTTP_204_NO_CONTENT)

    def has_object_permission(self, request, view, obj):

        if request.is_super_admin:
            return True

        elif obj:

            try:
                project_id = obj.project.id
            except:
                project_id = obj.id

            user_id = request.user.id
            user_role = request.roles.filter(user_id=user_id, project_id=project_id, group__name="Project Manager")

            if user_role:
                return True

            organization_id = Project.objects.get(pk=project_id).organization.id
            user_role_asorgadmin = request.roles.filter(user_id=user_id, organization_id=organization_id, group_id=1)

            if user_role_asorgadmin:
                return True

            return False

        else:
            return False


class SubmissionDetailPermission(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to View it.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user
        finstance = obj.fieldsight_instance
        form = finstance.fsxf
        is_doner = False
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