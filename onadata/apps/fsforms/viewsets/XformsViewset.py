from __future__ import unicode_literals
from django.db.models import Q
from rest_framework import viewsets

from onadata.apps.fsforms.serializers.XformSerializer import XFormListSerializer
from onadata.apps.logger.models import XForm
from onadata.apps.fsforms.utils import get_shared_asset_ids


class XFormViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing xforms.
    """
    queryset = XForm.objects.filter(deleted_xform=None)
    serializer_class = XFormListSerializer

    def get_queryset(self):
        asset_uids = get_shared_asset_ids(self.request.user)
        if self.request.user.user_roles.filter(group__name="Super Admin").exists():
            return self.queryset.filter(
                Q(user=self.request.user) |
                Q(user__user_profile__organization=self.request.user.user_profile.organization) |
                Q(id_string__in=asset_uids), deleted_xform=None)
        return self.queryset.filter(
            Q(user=self.request.user) |
            Q(user__user_profile__organization=self.request.user.user_profile.organization) |
            Q(id_string__in=asset_uids), deleted_xform=None)
