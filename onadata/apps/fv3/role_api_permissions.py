from rest_framework.permissions import DjangoObjectPermissions
from rest_framework.response import Response
from rest_framework import status

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
