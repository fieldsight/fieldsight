from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from onadata.apps.userrole.models import UserRole as Role
from rest_framework.authtoken.models import Token
from django.contrib.auth import logout
from django.core.cache import cache

from django.shortcuts import render



def clear_roles(request):
    request.roles = Role.objects.none()
    request.is_super_admin = False
    return request


class RoleMiddleware(object):
    def process_request(self, request):

        if request.META.get('HTTP_AUTHORIZATION'):
            token_key = request.META.get('HTTP_AUTHORIZATION').split(' ')[-1]
            try:
                request.user = Token.objects.get(key=token_key).user
            except:
                pass

        if not request.user.is_anonymous():
            roles = cache.get('roles_{}'.format(request.user.id))
            is_admin = cache.get('admin_{}'.format(request.user.id), False)
            if roles:
                request.roles = roles
                request.is_super_admin = is_admin

            if not roles:
                print("no roles in cache")
                roles = Role.get_active_roles(request.user)
                if roles:
                    cache.set('roles_{}'.format(request.user.id), roles,
                              20 * 60)
                    if roles.filter(group__name="Super Admin").exists():
                        request.is_super_admin = True
                        cache.set('admin_{}'.format(request.user.id), True,
                                  20 * 60)
                    else:
                        request.is_super_admin = False
                        cache.set('admin_{}'.format(request.user.id), False,
                                  20 * 60)
                    request.roles = roles
            
            if not roles:
                print(" user have no roles")

                logout(request)
                # return render(request, 'fieldsight/permission_denied.html')

        else:
            clear_roles(request)

    def authenticate(self, request):
        pass

