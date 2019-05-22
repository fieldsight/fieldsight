from datetime import datetime

from django.db.models import Prefetch
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from onadata.apps.fieldsight.models import Project, Region, Site
from onadata.apps.fsforms.notifications import get_notifications_queryset
from onadata.apps.fv3.serializer import ProjectSerializer, SiteSerializer
from onadata.apps.userrole.models import UserRole
from onadata.apps.users.viewsets import ExtremeLargeJsonResultsSetPagination


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def supervisor_projects(request):
    regions = UserRole.objects.filter(user=request.user,
                                     ended_at=None,
                                     group__name="Region Supervisor"
                                     ).values_list('region', flat=True)
    "Distinct Regions when a user is assigned."

    project_ids = UserRole.objects.filter(user=request.user,
                                      ended_at=None,
                                      group__name__in=["Region Supervisor", "Site Supervisor"]
                                      ).values_list('project', flat=True)
    "Projects where a user is assigned as Region Supervisor or Site Supervisor"

    projects = Project.objects.filter(pk__in=project_ids).select_related('organization').prefetch_related(
        Prefetch("project_region", queryset=Region.objects.filter(pk__in=regions)))
    "Distinct Projects Where a user can be site supervisor or region reviewer"

    site_supervisor_role = UserRole.objects.filter(user=request.user,
                                     ended_at=None,
                                     group__name="Site Supervisor"
                                     ).values_list('project', flat=True).order_by('project').distinct()

    "If a user is assigned as site supervisor in a given project."
    for p in projects:
        if p.id in site_supervisor_role:
            p.has_site_role = True
        else:
            p.has_site_role = False
    data = ProjectSerializer(projects, many=True).data
    return Response(data)


class MySuperviseSitesViewset(viewsets.ModelViewSet):
    serializer_class = SiteSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = ExtremeLargeJsonResultsSetPagination
    renderer_classes = [JSONRenderer]

    def get_queryset(self):
        query_params = self.request.query_params
        region_id = query_params.get('region_id')
        project_id = query_params.get('project_id')
        last_updated = query_params.get('last_updated')

        if last_updated:
            try:
                last_updated = datetime.fromtimestamp(int(last_updated))#  Deleted and last updated sites.
            except:
                pass

        if region_id and last_updated:  # Region Reviewer Roles
            sites = Site.all_objects.filter(region=region_id, date_modified__gte=last_updated)
        elif region_id:
            sites = Site.objects.filter(region=region_id)
        elif project_id and last_updated:  # Site Supervisor Roles
            sites = Site.all_objects.filter(project=project_id, date_modified__gte=last_updated,
                                            site_roles__region__isnull=True,
                                            site_roles__group__name="Site Supervisor")
        elif project_id:  # Site Supervisor Roles
            sites = Site.objects.filter(project=project_id, site_roles__region__isnull=True,
                                        site_roles__group__name="Site Supervisor")
        else:
            sites = []

        return sites


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def site_blueprints(request):
    query_params = request.query_params
    site_id = query_params.get('site_id')
    data = Site.objects.get(pk=site_id).blueprints.all()
    urls = [m.image.url for m in data]
    return Response({'blueprints': urls})


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def supervisor_logs(request):
    email = request.user.email
    date = None
    last_updated = request.query_params.get('last_updated')
    if last_updated:
        try:
            date = datetime.fromtimestamp(int(last_updated))  # notifications newer than this date.
        except:
            pass
    notifications = get_notifications_queryset(email, date)
    return Response({'notifications': notifications})

