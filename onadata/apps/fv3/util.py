import time
import functools

from django.db import connection, reset_queries
from django.db.models import Q

from onadata.apps.fieldsight.models import Site, Project, Organization, SuperOrganization
from onadata.apps.userrole.models import UserRole


def debugger_queries(func):
    """Basic function to debug queries."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print("func: ", func.__name__)
        reset_queries()

        start = time.time()
        start_queries = len(connection.queries)

        result = func(*args, **kwargs)

        end = time.time()
        end_queries = len(connection.queries)

        print("queries:", end_queries - start_queries)
        print("took: %.2fs" % (end - start))
        return result

    return wrapper


def get_user_roles(role_obj, obj):
    queryset = UserRole.objects.filter(user=role_obj.user)
    if isinstance(obj, Site):
        roles = queryset.filter(site=obj, group__name__in=['Site Supervisor', 'Site Reviewer']).\
            values_list('group__name', flat=True)

    elif isinstance(obj, Project):
        roles = queryset.filter(project=obj, group__name__in=['Project Manager', 'Project Donor']).\
            values_list('group__name', flat=True)

    elif isinstance(obj, Organization):
        roles = queryset.filter(organization=obj, group__name="Organization Admin").\
            values_list('group__name', flat=True)

    elif isinstance(obj, SuperOrganization):
        teams = Organization.objects.filter(parent=obj, is_active=True).values_list('id', flat=True)
        roles = queryset.filter(Q(super_organization=obj, group__name='Super Organization Admin') |
                                Q(organization_id__in=teams)).values_list('group__name', flat=True)

    else:
        roles = ''

    return roles

