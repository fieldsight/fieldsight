from guardian.shortcuts import assign_perm, get_users_with_perms


def share_m2m(users, forms):
    for user in users:
        for xform in forms:
            if not user.has_perm('view_xform', xform):
                assign_perm('change_xform', user, xform)
            if not user.has_perm('view_xform', xform):
                assign_perm('view_xform', user, xform)


def share_forms(user, forms):
    for xform in forms:
        if not user.has_perm('view_xform', xform):
            assign_perm('change_xform', user, xform)
        if not user.has_perm('view_xform', xform):
            assign_perm('view_xform', user, xform)


def share_form(users, xform):
    for user in users:
        if not user.has_perm('view_xform', xform):
            assign_perm('change_xform', user, xform)
        if not user.has_perm('view_xform', xform):
            assign_perm('view_xform', user, xform)


def share_o2o(user, xform):
    if not user.has_perm('view_xform', xform):
        assign_perm('change_xform', user, xform)
    if not user.has_perm('view_xform', xform):
        assign_perm('view_xform', user, xform)


def shared_users(xform):
    return get_users_with_perms(xform)
