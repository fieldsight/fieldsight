from __future__ import absolute_import, unicode_literals
from celery import shared_task

import time
from celery import Celery
from .models import Organization, Project, Site
from onadata.apps.userrole.models import UserRole
app = Celery('tasks', backend='redis://localhost:6379/', broker='amqp://guest:guest@localhost:5672/')

@app.task(name='onadata.apps.fieldsight.tasks.printrand')
#@shared_task
def printrand():
    for i in range(10):
        a=str(i) + 'rand'
        time.sleep(5)
        print a
    return ' random users created with success!'

@app.task(name='onadata.apps.fieldsight.tasks.multiuserassignproject')
def multiuserassignproject(projects, users, group_id):
    for project_id in projects:
            project = Project.objects.get(pk=project_id)
            for user in users:
                role, created = UserRole.objects.get_or_create(user_id=user, project_id=project_id,
                                                               organization_id=project.organization.id,
                                                               group_id=group_id, ended_at=None)
