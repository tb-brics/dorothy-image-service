from django.contrib import admin
from django.urls import path, include
from image_service.views import DataSetViewSet, ImageViewSet, ImageMetaDataViewSet, DataBaseViewSet
from rest_framework import routers

router = routers.DefaultRouter()
<<<<<<< HEAD
router.register(r'datasets', DataSetViewSet)
router.register(r'images', ImageViewSet)
router.register(r'images_meta_data', ImageMetaDataViewSet)
=======
router.register(r'dataset', DataSetViewSet)
router.register(r'image', ImageViewSet)
router.register(r'image_meta_data', ImageMetaDataViewSet)
router.register(r'database', DataBaseViewSet)
>>>>>>> 303193b4c0fcf1d2a4f6579c05cfd45ccbdd45bc

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
]
