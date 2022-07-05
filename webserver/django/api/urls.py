from django.contrib import admin
from django.urls import path, include, re_path
from image_service.views import (DataSetViewSet,
                                 ImageFileView,
                                 ImageViewSet,
                                 ImageMetaDataViewSet,
                                 ReportViewSet,
                                 ImageSamplingViewSet,
                                 DataSetPostViewSet,
                                 ImagePostViewSet,
                                 MetaDataPostViewSet,
                                 Post_Image_AND_MetaDataPostViewSet,
                                 ClusterImagesAPIView,
                                 CrossValidationFoldImagesViewSet,
                                 CrossValidationFoldViewSet,
                                 CrossValidationFolderViewSet,
                                 CrossValidationClusterViewSet
                                 )
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static
import os
from rest_framework.authtoken.views import obtain_auth_token


router = routers.DefaultRouter()
router.register(r'datasets', DataSetViewSet)
router.register(r'images', ImageViewSet)
router.register(r'images_meta_data', ImageMetaDataViewSet)
router.register(r'report', ReportViewSet)
router.register(r'imagesampling', ImageSamplingViewSet)
router.register(r'post_dataset', DataSetPostViewSet)
router.register(r'post_image', ImagePostViewSet)
router.register(r'post_metadata' , MetaDataPostViewSet)
router.register(r'post_image_and_metadata', Post_Image_AND_MetaDataPostViewSet)
router.register(r'cross_validation/cluster', CrossValidationClusterViewSet)
router.register(r'cross_validation/folder', CrossValidationFolderViewSet)
router.register(r'cross_validation/fold', CrossValidationFoldViewSet)
router.register(r'cross_validation/fold_image', CrossValidationFoldImagesViewSet)



urlpatterns = [
    re_path('^image/(?P<project_id>\w+)/$', ImageFileView.as_view(), name="image_file"),
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api-token-auth/', obtain_auth_token, name = 'api_token_auth'),
    path('cross_validation/images', ClusterImagesAPIView.as_view()),

]
