from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import permissions
from django.core.exceptions import PermissionDenied

class ProjectPermission(permissions.BasePermission):
	def has_permission(self, request, view):
		if not request.user.is_authenticated():
            return False
        
        if request.group:
            if request.group.name == "Super Admin":
                return True

        project = Project.objects.get(pk=view.kwargs.get('pk'))
        user_role = request.roles.filter(
        	project_id = project.id,
        	group_id=2
        )
        
        if user_role:
            return True

        user_role_asorgadmin = request.roles.filter(
        	organization_id = project.organization.id,
        	group_id=1
        )
        
        if user_role_asorgadmin:
            return True

        return False


class SyncScheduleViewSet(viewsets.ModelViewSet):
    queryset = SyncSchedule.objects.all()
    serializer_class = SyncScheduleSerializer
    permission_classes = (ProjectPermission,)

    def list(self, request, *args, **kwargs):
    	pk = self.kwargs['pk'] 
       	data=[]
        data['schedule_forms'] = FieldSightXF.objects.select_related('xf', 'sync_schedule', 'schedule').filter(project_id=pk, is_scheduled = True, is_staged=False, is_survey=False, sync_schedule__isnull=False).values('xf__title', 'sync_schedule__id', 'sync_schedule__schedule', 'sync_schedule__date', 'sync_schedule__end_of_month')
        mainstage=[]
        stages = Stage.objects.filter(project_id=pk)
        for stage in stages:
            if stage.stage_id is None:
                substages=stage.get_sub_stage_list(sync_details=True, values_list=True)
                main_stage = {'id':stage.id, 'title':stage.name, 'sub_stages':substages}
                mainstage.append(main_stage)

        data['stage_forms'] = mainstage
        data['survey_forms'] = FieldSightXF.objects.select_related('xf', 'sync_schedule').filter(project_id=pk, is_scheduled = False, is_staged=False, is_survey=True, sync_schedule__isnull=False).values('xf__title', 'sync_schedule__id','sync_schedule__schedule', 'sync_schedule__date', 'sync_schedule__end_of_month')

        data['general_forms'] = FieldSightXF.objects.select_related('xf', 'sync_schedule').filter(project_id=pk, is_scheduled = False, is_staged=False, is_survey=False, sync_schedule__isnull=False).values('xf__title', 'sync_schedule__id', 'sync_schedule__schedule', 'sync_schedule__date', 'sync_schedule__end_of_month')
        return Response(data)


class ProjectSyncScheduleViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSyncScheduleSerializer
    permission_classes = (ProjectPermission,)
    
    def destroy(self, request, *args, **kwargs):
    	raise PermissionDenied()