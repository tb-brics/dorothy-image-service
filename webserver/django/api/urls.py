from django.contrib import admin
from django.urls import path, include
from image_service.views import DataSetViewSet, ImageViewSet, ImageMetaDataViewSet, ReportViewSet, ImageSamplingViewSet
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static
import os





router = routers.DefaultRouter()
router.register(r'datasets', DataSetViewSet)
router.register(r'images', ImageViewSet)
router.register(r'images_meta_data', ImageMetaDataViewSet)
router.register(r'report', ReportViewSet)
router.register(r'imagesampling', ImageSamplingViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
