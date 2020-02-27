from django.contrib.auth.models import User, Group, Permission
from onadata.apps.userrole.models import UserRole
from .models import UserProfile
from social_django.models import UserSocialAuth
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib.auth import login
import urllib
from urlparse import urlparse
from django.core.files import File


# check if the email already exists for the user trying to login through gmail
def email_validate(strategy, backend, uid, user, response, *args, **kwargs):
    email = response.get('email')

    # check if given email is in use
    django_user_exists = User.objects.filter(email=email).exists()
    u = User.objects.filter(email=email)
    social_auth_user_exists = UserSocialAuth.objects.filter(user=u).exists()

    # user is not logged in, social profile with given uid doesn't exist
    # and email is in use
    if django_user_exists and not social_auth_user_exists:
        return {
            'user':user
        }
    else:
        return {
            'user':user
        }


# create a role as unassigned for the logged in user if the role is not created
def create_role(backend, uid, user, response, social=None, *args, **kwargs):
    email = response.get('email')
    if user and not social:
        social = backend.strategy.storage.user.create_social_auth(user, uid, backend.name)
   
    u = User.objects.get(email=email)

    codenames = ['add_asset', 'change_asset', 'delete_asset', 'view_asset', 'share_asset', 'add_finstance',
                 'change_finstance', 'add_instance', 'change_instance']
    permissions = Permission.objects.filter(codename__in=codenames)

    for permission in permissions:
        u.user_permissions.add(permission)

    group = Group.objects.get(name="Unassigned")
    userrole = UserRole.objects.filter(user=u)
    if not userrole:
        UserRole.objects.create(user=u, group=group)
    
    return {
        'social':social,
        'user':user,
    }


# create a profile for the logged in user if profile doesnot exist
def create_profile(strategy, backend, uid, user, response, social=None, *args, **kwargs):
    email = response.get('email')
    request = strategy.request
    redirect = strategy.redirect

    u = User.objects.get(email=email)
    username = u.username
    if '.' in username:
        update_username = username.replace('.', str(u.id))
        u.username = update_username
        u.save()
    else:
        pass
    try:
        profile = UserProfile.objects.get(user=u)
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
        return HttpResponseRedirect(reverse('dashboard'))

    except UserProfile.DoesNotExist:
        user_name = response.get('name')
        user_name = user_name.split(' ')
        u.first_name = user_name[0]
        u.last_name = user_name[1]
        u.save()

        profile = UserProfile.objects.create(user=u)

        #save profile picture from google
        picture = response.get('picture')
        name = urlparse(picture).path.split('/')[-1]
        content = urllib.urlretrieve(picture)
        profile.profile_picture.save(name, File(open(content[0])), save=True)

        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
        return HttpResponseRedirect(reverse('dashboard'))
