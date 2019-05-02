from django.conf.urls import url

from onadata.apps.fv3.views import supervisor_projects, MySuperviseSitesViewset, site_blueprints, supervisor_logs

urlpatterns = [

    url(r'^api/supervisor/projects/', supervisor_projects, name='supervisor_projects'),
    url(r'^api/supervisor/sites/', MySuperviseSitesViewset.as_view({'get': 'list'}),  name='supervisor_sites'),
    url(r'^api/site/blueprint/', site_blueprints, name='site_blueprints'),
    url(r'^api/user/logs/', supervisor_logs, name='supervisor_logs'),
    ]
