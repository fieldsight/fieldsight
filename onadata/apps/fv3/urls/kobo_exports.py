from django.conf.urls import url

from onadata.apps.fv3.viewsets.KoboExportsViewset import ExportViewSet, OrganizationExportViewSet


kobo_exports_urlpatterns = [
    url(r'^api/kobo/exports/(?P<pk>\d+)/$', ExportViewSet.as_view({'get':'retrieve', 'post':'destroy'}),),
    url(r'^api/kobo/exports/$', ExportViewSet.as_view({'get': 'list', 'post': 'create'}), ),
    url(r'^api/kobo/organization-exports/$', OrganizationExportViewSet.as_view({'get': 'list', 'post': 'create'}), )

]
