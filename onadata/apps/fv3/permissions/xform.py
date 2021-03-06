from django.db.models import Q
from django.conf import settings
from rest_framework import permissions
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from onadata.apps.fsforms.models import ObjectPermission, Asset


class XFormSharePermission(permissions.BasePermission):
    """
    Object-level permission to allow only users with share_asset permission in xform to share a xform
    """

    def has_object_permission(self, request, view, obj):
        user = request.user
        permission = Permission.objects.get(content_type__app_label='kpi', codename='share_asset')
        content_type = ContentType.objects.get(id=settings.ASSET_CONTENT_TYPE_ID)
        object = Asset.objects.get(uid=obj.id_string)

        if user == object.owner or ObjectPermission.objects.filter(
                object_id=object.id,
                content_type=content_type,
                user=user,
                permission_id=permission.id,
                deny=False,
                inherited=False
        ).exists():
            has_access = True

        else:
            has_access = False

        return has_access


class XFormDeletePermission(permissions.BasePermission):
    """
    Object-level permissions to allow modifications to xform if the user is the owner of the form
    """

    def has_object_permission(self, request, view, obj):
        user = request.user
        permission = Permission.objects.get(content_type__app_label='kpi', codename='delete_asset')
        content_type = ContentType.objects.get(id=settings.ASSET_CONTENT_TYPE_ID)
        object = Asset.objects.get(uid=obj.id_string)

        if user == object.owner or ObjectPermission.objects.filter(
                object_id=object.id,
                content_type=content_type,
                user=user,
                permission_id=permission.id,
                deny=False,
                inherited=False
        ).exists():
            has_access = True
        else:
            has_access = False

        return has_access


class XFormEditPermission(permissions.BasePermission):
    """
        Object-level permissions to allow modifications to xform if the user is the owner of the form
        """

    def has_object_permission(self, request, view, obj):
        user = request.user
        permission = Permission.objects.get(content_type__app_label='kpi', codename='change_asset')
        content_type = ContentType.objects.get(id=settings.ASSET_CONTENT_TYPE_ID)
        object = Asset.objects.get(uid=obj.id_string)

        if user == object.owner or ObjectPermission.objects.filter(
                object_id=object.id,
                content_type=content_type,
                user=user,
                permission_id=permission.id,
                deny=False,
                inherited=False
        ).exists():
            has_access = True
        else:
            has_access = False

        return has_access
