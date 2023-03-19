from django.contrib import admin
from django.urls import path, include, re_path
from image_service.views import (DataSetViewSet,
                                 ImageFileView,
                                 ImageViewSet,
                                 ReportViewSet,
                                 ImageSamplingViewSet,
                                 DataSetPostViewSet,
                                 ImagePostViewSet,
                                 MetaDataPostViewSet,
                                 Post_Image_AND_MetaDataPostViewSet,
                                 CrossValidationClusterViewSet,
                                 CrossValidationClusterFileView,
                                 DataQualityAnnotationViewSet,
                                 ImageValidationViewSet,
                                 ImageValidationFileView,
                                 ImageValidationPostViewSet,
                                 MetaDataValidationPostViewSet,
                                 Post_Image_AND_MetaDataValidationPostViewSet,
                                 DatasetCrossValidationListFoldFilesView,
                                 DatasetCrossValidationGetFoldFile,
                                 ImagePaginatedRequest
                                 )
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

router = routers.DefaultRouter()
router.register(r'datasets', DataSetViewSet)
router.register(r'datasets/cross_validation', DatasetCrossValidationListFoldFilesView)
router.register(r'images', ImageViewSet, basename='Image')
router.register(r'report', ReportViewSet)
router.register(r'imagesampling', ImageSamplingViewSet)
router.register(r'post_dataset', DataSetPostViewSet)
router.register(r'post_image', ImagePostViewSet)
router.register(r'post_metadata', MetaDataPostViewSet)
router.register(r'post_image_and_metadata', Post_Image_AND_MetaDataPostViewSet)
router.register(r'cross_validation/cluster', CrossValidationClusterViewSet)
router.register(r'annotation', DataQualityAnnotationViewSet, basename='DataQualityAnnotation')
router.register(r'image_validation', ImageValidationViewSet)
router.register(r'post_image_validation', ImageValidationPostViewSet)
router.register(r'post_metadata_validation', MetaDataValidationPostViewSet)
router.register(r'post_image_and_metadata_validation', Post_Image_AND_MetaDataValidationPostViewSet)

urlpatterns = [
    re_path(r'^image\/(?P<project_id>[a-zA-Z0-9\=\/\-\_]+)\/$', ImageFileView.as_view(), name="image_file"),
    re_path(r'^image_validation\/(?P<project_id>\w+)\/$', ImageValidationFileView.as_view(), name="image_validation_file"),
    re_path(r'^cross_validation\/cluster/(?P<cluster_id>\w+)\/$', CrossValidationClusterFileView.as_view(), name="cluster_file"),
    re_path(r'^dataset\/cross_validation\/(?P<dataset_name>[a-zA-Z0-9\=\/\-\_]+)$', DatasetCrossValidationGetFoldFile.as_view(),
            name="dataset_cross_validation_file"),
    re_path(r'^dataset\/(?P<dataset_name>[a-zA-Z0-9\=\/\-\_]+)\/images\/$', ImagePaginatedRequest.as_view(), name="dataset_images_paginate"),
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]
