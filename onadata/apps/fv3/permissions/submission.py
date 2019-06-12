from rest_framework import permissions


class SubmissionDetailPermission(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to View it.
    """

    def has_object_permission(self, request, view, obj):
        pk = request.user
        return True