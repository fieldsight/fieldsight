from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import DjangoObjectPermissions
from rest_framework.response import Response
from rest_framework import status, permissions

from onadata.apps.fieldsight.models import Project, Site, Region
from onadata.apps.fsforms.models import FInstance


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


class SiteDashboardPermissions(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to View it.
    """

    def has_object_permission(self, request, view, obj):

        if request.is_super_admin:
            return True

        site = obj

        if site is not None:
            organization_id = site.project.organization_id
            user_role_org_admin = request.roles.filter(organization_id=organization_id, group__name="Organization Admin")

            if user_role_org_admin:
                return True

            project = site.project
            user_role_as_manager = request.roles.filter(project_id=project.id, group__name__in=["Project Manager",
                                                                                                "Project Donor"])

            if user_role_as_manager:
                return True

            user_role_reviewer = request.roles.filter(site_id=site.id, group__name="Reviewer")

            if user_role_reviewer:
                return True

            region = site.region
            if region is not None:
                user_role_as_region_reviewer_supervisor = request.roles.filter(region_id=region.id, group__name__in=["Region Reviewer",
                                                                                                                     "Region Supervisor"])
                if user_role_as_region_reviewer_supervisor:
                    return True

            user_role = request.roles.filter(site_id=site.id, group__name="Site Supervisor")
            if user_role:
                return True

            return False
        return False


class SiteSubmissionPermission(permissions.BasePermission):

    def has_permission(self, request, view):

        if request.is_super_admin:
            return True

        site_id = request.query_params.get('site', None)

        try:
            if site_id:
                site_id = int(site_id)
                try:
                    site = Site.objects.get(id=site_id)
                except ObjectDoesNotExist:
                    return Response({"message": "Site Id does not exist."}, status=status.HTTP_204_NO_CONTENT)

                organization_id = site.project.organization_id
                user_role_org_admin = request.roles.filter(organization_id=organization_id,
                                                           group__name="Organization Admin")

                if user_role_org_admin:
                    return True

                project = site.project
                user_role_as_manager = request.roles.filter(project_id=project.id, group__name__in=["Project Manager",
                                                                                                    "Project Donor"])

                if user_role_as_manager:
                    return True

                user_role_reviewer = request.roles.filter(site_id=site.id, group__name="Reviewer")

                if user_role_reviewer:
                    return True

                region = site.region
                if region is not None:
                    user_role_as_region_reviewer_supervisor = request.roles.filter(region_id=region.id,
                                                                                   group__name__in=["Region Reviewer",
                                                                                                    "Region Supervisor"])
                    if user_role_as_region_reviewer_supervisor:
                        return True

                user_role = request.roles.filter(site_id=site.id, group__name="Site Supervisor")
                if user_role:
                    return True

                return False
            return False

        except AssertionError:
            return Response({"message": "Site Id is required."}, status=status.HTTP_204_NO_CONTENT)


def check_site_permission(request, pk):

    if request.is_super_admin:
        return True

    site_id = int(pk)
    if site_id:
        try:
            site = Site.objects.get(id=site_id)
        except ObjectDoesNotExist:
            return Response({"message": "Site Id does not exist."}, status=status.HTTP_204_NO_CONTENT)

        organization_id = site.project.organization_id
        user_role_org_admin = request.roles.filter(organization_id=organization_id,
                                                   group__name="Organization Admin")

        if user_role_org_admin:
            return True

        project = site.project
        user_role_as_manager = request.roles.filter(project_id=project.id, group__name__in=["Project Manager",
                                                                                            "Project Donor"])

        if user_role_as_manager:
            return True

        user_role_reviewer = request.roles.filter(site_id=site.id, group__name="Reviewer")

        if user_role_reviewer:
            return True

        region = site.region
        if region is not None:
            user_role_as_region_reviewer_supervisor = request.roles.filter(region_id=region.id,
                                                                           group__name__in=["Region Reviewer",
                                                                                            "Region Supervisor"])
            if user_role_as_region_reviewer_supervisor:
                return True

        user_role = request.roles.filter(site_id=site.id, group__name="Site Supervisor")
        if user_role:
            return True

        return False


def has_write_permission_in_site(request, pk):

    if request.is_super_admin:
        return True

    site_id = int(pk)
    if site_id:
        try:
            site = Site.objects.get(id=site_id)
        except ObjectDoesNotExist:
            return Response({"message": "Site Id does not exist."}, status=status.HTTP_204_NO_CONTENT)

        organization_id = site.project.organization_id
        user_role_org_admin = request.roles.filter(organization_id=organization_id,
                                                   group__name="Organization Admin")

        if user_role_org_admin:
            return True

        project = site.project
        user_role_as_manager = request.roles.filter(project_id=project.id, group__name="Project Manager")

        if user_role_as_manager:
            return True

        region = site.region
        if region is not None:
            user_role_as_region_supervisor = request.roles.filter(region_id=region.id, group__name=["Region Supervisor"])
            if user_role_as_region_supervisor:
                return True

        user_role = request.roles.filter(site_id=site.id, group__name="Site Supervisor")
        if user_role:
            return True

        return False


def check_regional_perm(request, region):

    if request.is_super_admin:
        return True

    region_id = region

    try:
        if region_id:
            region_id = int(region_id)
            try:
                region = Region.objects.get(id=region_id)
            except ObjectDoesNotExist:
                return Response({"message": "Region Id does not exist."}, status=status.HTTP_204_NO_CONTENT)

            organization_id = region.project.organization_id
            user_role_org_admin = request.roles.filter(organization_id=organization_id,
                                                       group__name="Organization Admin")

            if user_role_org_admin:
                return True

            project = region.project
            user_role_as_manager = request.roles.filter(project_id=project.id, group__name__in=["Project Manager",
                                                                                                "Project Donor"])

            if user_role_as_manager:
                return True

            user_role_as_region_reviewer_supervisor = request.roles.filter(region_id=region.id,
                                                                           group__name__in=["Region Reviewer",
                                                                                            "Region Supervisor"])
            if user_role_as_region_reviewer_supervisor:
                return True

            return False
        return False

    except AssertionError:
        return Response({"message": "Region Id is required."}, status=status.HTTP_204_NO_CONTENT)


class RegionalPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        region_id = request.query_params.get('region', None)
        if check_regional_perm(request, region_id):
            return True
        else:
            return False

