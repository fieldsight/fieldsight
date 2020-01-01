from rest_framework import permissions


class SuperAdminPermission(permissions.BasePermission):

    def has_permission(self, request, view):

        if request.is_super_admin:
            return True
