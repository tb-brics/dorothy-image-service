from django.contrib import admin
from django.urls import path, include
from image_service.views import DataSetViewSet, ImageViewSet, ImageMetaDataViewSet, DataBaseViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'dataset', DataSetViewSet)
router.register(r'image', ImageViewSet)
router.register(r'image_meta_data', ImageMetaDataViewSet)
router.register(r'database', DataBaseViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
]
