from django.conf.urls import url
from onadata.apps.fv3.viewsets.SiteViewSet import SiteViewSet, site_map, SiteSubmissionsViewSet, SiteForms, \
    SiteCropImage, site_documents, site_recent_pictures, BlueprintsPostDeleteView, ZipSiteImages


site_dashboard_urlpatterns = [
    url(r'^api/site/(?P<pk>\d+)/$', SiteViewSet.as_view({'get': 'retrieve'}), name='site'),
    url(r'^api/site-map/(?P<pk>\d+)/$', site_map, name='site_map'),
    url(r'^api/site-submissions/$', SiteSubmissionsViewSet.as_view({'get': 'list'}), name='site_submissions'),
    url(r'^api/blueprints/$', BlueprintsPostDeleteView.as_view(), name='create_delete_blueprint'),
    url(r'^api/site/documents/$', site_documents, name='site_documents'),
    url(r'^api/site-forms/(?P<pk>\d+)/$', SiteForms.as_view(), name='site_forms'),
    url(r'^api/site-crop-image/(?P<pk>[0-9]+)/$', SiteCropImage.as_view(), name='site_crop_image'),
    url(r'^api/site-recent-pictures/$', site_recent_pictures, name='site_recent_pictures'),
    url(r'^api/zip-site-images/(?P<pk>[0-9]+)/(?P<size_code>[0-9]+)/$', ZipSiteImages.as_view(), name='zip_site_images'),

]