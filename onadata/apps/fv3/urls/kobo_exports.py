from django.conf.urls import url

from onadata.apps.fv3.viewsets.KoboExportsViewset import ExportViewSet



kobo_exports_urlpatterns = [
    url(r'^api/kobo/exports/(?P<pk>\d+)/$', ExportViewSet.as_view({'get':'retrieve', 'post':'destroy'}),),
    url(r'^api/kobo/exports/$', ExportViewSet.as_view({'get': 'list', 'post': 'create'}), )

]
