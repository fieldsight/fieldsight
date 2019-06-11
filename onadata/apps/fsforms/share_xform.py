from guardian.shortcuts import assign_perm, get_users_with_perms
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType


def share_m2m(users, forms):
    for user in users:
        for xform in forms:
            if not user.has_perm('change_xform', xform):
                assign_perm('change_xform', user, xform)
            if not user.has_perm('change_xform', xform):
                assign_perm('view_xform', user, xform)


def share_forms(user, forms):
    from onadata.appps.fsforms.models import ObjectPermission, Asset
    for xform in forms:
        try:
            codenames = ['view_asset', 'change_asset']
            permissions = Permission.objects.filter(content_type__app_label='kpi', codename__in=codenames)
            for perm in permissions:
                existing_perms = ObjectPermission.objects.filter(
                    user=user,
                )
                identical_existing_perm = existing_perms.filter(
                    inherited=False,
                    permission_id=perm.pk,
                    deny=False,
                )
                if identical_existing_perm.exists():
                    # The user already has this permission directly applied
                    return identical_existing_perm.first()
                # Remove any explicitly-defined contradictory grants or denials
                contradictory_perms = existing_perms.filter(user=user,
                                                            permission_id=perm.pk,
                                                            deny=not False,
                                                            inherited=False
                                                            )
                contradictory_perms.delete()

                object_id = Asset.objects.get(uid=xform.xf.id_string).id
                content_type = ContentType.objects.get(id=21)

                # Create the new permission
                new_permission = ObjectPermission.objects.create(
                    object_id=object_id,
                    content_type=content_type,
                    user=user,
                    permission_id=perm.pk,
                    deny=False,
                    inherited=False
                )

        except Exception as e:
            print(e)
            return False
        else:
            return True


def share_form(users, xform):
    from onadata.apps.fsforms.models import ObjectPermission, Asset
    for user in users:
        try:
            codenames = ['view_asset', 'change_asset']
            permissions = Permission.objects.filter(content_type__app_label='kpi', codename__in=codenames)
            for perm in permissions:
                existing_perms = ObjectPermission.objects.filter(
                    user=user,
                )
                identical_existing_perm = existing_perms.filter(
                    inherited=False,
                    permission_id=perm.pk,
                    deny=False,
                )
                if identical_existing_perm.exists():
                    # The user already has this permission directly applied
                    return identical_existing_perm.first()
                # Remove any explicitly-defined contradictory grants or denials
                contradictory_perms = existing_perms.filter(user=user,
                                                            permission_id=perm.pk,
                                                            deny=not False,
                                                            inherited=False
                                                            )
                contradictory_perms.delete()

                object_id = Asset.objects.get(uid=xform.id_string).id
                content_type = ContentType.objects.get(id=21)

                # Create the new permission
                new_permission = ObjectPermission.objects.create(
                    object_id=object_id,
                    content_type=content_type,
                    user=user,
                    permission_id=perm.pk,
                    deny=False,
                    inherited=False
                )

        except Exception as e:
            return False
        else:
            return True


def share_o2o(user, xform):
    if not user.has_perm('change_xform', xform):
        assign_perm('change_xform', user, xform)
    if not user.has_perm('view_xform', xform):
        assign_perm('view_xform', user, xform)


def shared_users(xform):
    return get_users_with_perms(xform)
