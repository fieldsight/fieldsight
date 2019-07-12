from django.conf.urls import url
from onadata.apps.fv3.viewsets.MyRolesViewset import my_roles

my_roles_urlpatterns = [

    url(r'^api/myroles/$', my_roles, name='my_roles'),
    ]