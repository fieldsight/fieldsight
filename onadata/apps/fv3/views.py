from django.db.models import Prefetch
from rest_framework.decorators import api_view
from rest_framework.response import Response

from onadata.apps.fieldsight.models import Project, Region, Site
from onadata.apps.fv3.serializer import ProjectSerializer
from onadata.apps.userrole.models import UserRole


@api_view(['GET'])
def supervisor_projects(request):
    regions = UserRole.objects.filter(user=request.user,
                                     ended_at=None,
                                     group__name="Region Supervisor"
                                     ).values_list('region', flat=True)

    project_ids = UserRole.objects.filter(user=request.user,
                                      ended_at=None,
                                      group__name__in=["Region Supervisor", "Site Supervisor"]
                                      ).values_list('project', flat=True)

    projects = Project.objects.filter(pk__in=project_ids).select_related('organization').prefetch_related(
        Prefetch("project_region", queryset=Region.objects.filter(pk__in=regions)))
    
    projects_with_unassigned_sites = UserRole.objects.filter(user=request.user,
                                     ended_at=None,
                                     group__name="Site Supervisor"
                                     ).values_list('project', flat=True).order_by('project').distinct()
    for p in projects:
        if p.id in projects_with_unassigned_sites:
            p.has_unassigned_sites = True
        else:
            p.has_unassigned_sites = False
    data = ProjectSerializer(projects, many=True).data
    return Response(data)
