from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.core.cache import cache
from django.contrib.auth.models import User


def clear_user_cache(sender, user, request, **kwargs):
    cache.delete('roles_{}'.format(user.id))


user_logged_out.connect(clear_user_cache, sender=User)

