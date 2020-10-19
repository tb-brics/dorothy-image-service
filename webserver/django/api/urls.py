from django.contrib import admin
from django.urls import path, include
from image_service.views import DataSetViewSet, ImageViewSet, ImageMetaDataViewSet
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static
import os

router = routers.DefaultRouter()
router.register(r'dataset', DataSetViewSet)
router.register(r'image', ImageViewSet)
router.register(r'image_meta_data', ImageMetaDataViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

