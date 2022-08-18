from io import BytesIO

from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.views import APIView
from django.shortcuts import render

from PIL import Image as PilImage
from PIL import ImageOps

from .models import DataSet, Image, ImageMetaData, Report, ImageSampling, \
    CrossValidationFolder, CrossValidationFold, CrossValidationCluster, CrossValidationFoldimages, \
    DataQualityAnnotation, ImageValidation, ImageMetaDataValidation
from .serializers import (DataSetSerializer,
                          ImageSerializer,
                          ImageMetaDataSerializer,
                          ReportSerializer,
                          ImageSamplingSerializer,
                          ImageFileSerializer,
                          DataSetPostSerializer,
                          ImagePostSerializer,
                          PostMetaDataSerializer,
                          Post_Image_AND_MetaDataPostSerializer,
                          CrossValidationClusterSerializer,
                          CrossValidationFolderSerializer,
                          CrossValidationFoldSerializer,
                          CrossValidationFoldImageSerializer,
                          CrossValidationClusterFileSerializer,
                          DataQualityAnnotationSerializer,
                          ImageValidationSerializer,
                          ImageMetaDataValidationSerializer,
                          ImageValidationFileSerializer)
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import BasePermission


def loginPage(request):
    context = {}
    return render(request, 'accounts/login.html', context)


class DataSetViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = DataSet.objects.all()
    serializer_class = DataSetSerializer


class DataQualityAnnotationViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = DataQualityAnnotationSerializer
    # filter_backends = SearchFilter
    # search_fields = (['project_id'])
    http_method_names = ['post', 'get']

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = DataQualityAnnotation.objects.all()
        project_id = self.request.query_params.get('project_id')
        if project_id is not None:
            queryset = queryset.filter(project_id=project_id)
        return queryset


class ImageViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = (['dataset__name', 'project_id'])


class ImageMetaDataViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = ImageMetaData.objects.all()
    serializer_class = ImageMetaDataSerializer


class ReportViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    filter_backends = SearchFilter
    search_fields = (['image__project_id', 'performed_by'])


class ImageSamplingViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = ImageSampling.objects.all()
    serializer_class = ImageSamplingSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    ordering_fields = (['rank_position'])


class ImageFileView(generics.RetrieveAPIView):
    serializer_class = ImageFileSerializer
    lookup_field = 'project_id'
    queryset = Image.objects.all()

    def retrieve(self, request, *args, **kwargs):
        gray_scale = request.query_params.get("gray_scale", False)
        height = request.query_params.get("height", None)
        width = request.query_params.get("width", None)
        image_resize = None
        if height or width:
            if not height and width:
                height = width
            if not width and height:
                width = height
            image_resize = (int(width), int(height))
        instance = self.get_object()
        image_path = instance.image.path
        image_object = None
        image_format = self.extract_image_format(image_path)
        content_type = f'image/{image_format}' if image_format else 'application/octet-stream'
        if image_resize:
            image_object = PilImage.open(image_path)
            image_object = ImageOps.exif_transpose(image_object)
            image_object = self._resize_image(image_object, image_resize)

        if gray_scale:
            if not image_object:
                image_object = PilImage.open(image_path)
                image_object = ImageOps.exif_transpose(image_object)
            image_object = self._convert_to_gray_scale(image_object)

        image_bytes = self._get_image_bytes(image_path=image_path, image_object=image_object, image_format=image_format or "PNG")
        try:
            return HttpResponse(image_bytes, content_type=content_type)
        except Exception as exc:
            return Response({'error': f'Could not read the file. ({exc})'})

    @staticmethod
    def _get_image_bytes(image_path, image_object: PilImage = None, image_format: str = "PNG"):
        if not image_object:
            with open(image_path, "rb") as image_file:
                image_bytes = image_file.read()
        else:
            buffer = BytesIO()
            image_object.save(buffer, format=image_format.upper())
            buffer.seek(0)
            image_bytes = buffer.read()
        return image_bytes

    @staticmethod
    def _resize_image(image: PilImage, size) -> PilImage:
        return image.resize(size)

    @staticmethod
    def _convert_to_gray_scale(image: PilImage) -> PilImage:
        return image.convert("L")

    @staticmethod
    def extract_image_format(image_path: str) -> str:
        image_format = str(image_path.split(".")[-1]).upper() or "PNG"
        if image_format == "JPG":
            image_format = "JPEG"
        if image_format not in ["PNG", "JPEG", "SVG"]:
            return None
        else:
            return image_format


# POST endpoints:

ALLOWED_METHODS = ['POST']


class UploaderOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(name='Uploaders').exists() and request.method in ['POST']:
            return True
        return False


class DataSetPostViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, UploaderOnly,)
    queryset = DataSet.objects.all()
    serializer_class = DataSetPostSerializer
    http_method_names = ['post']


class ImagePostViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, UploaderOnly,)
    queryset = Image.objects.all()
    serializer_class = ImagePostSerializer
    http_method_names = ['post']


class MetaDataPostViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, UploaderOnly,)
    queryset = ImageMetaData.objects.all()
    serializer_class = PostMetaDataSerializer
    http_method_names = ['post']


class Post_Image_AND_MetaDataPostViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, UploaderOnly,)
    queryset = ImageMetaData.objects.all()
    serializer_class = Post_Image_AND_MetaDataPostSerializer
    http_method_names = ['post']


class CrossValidationClusterViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = CrossValidationCluster.objects.all()
    serializer_class = CrossValidationClusterSerializer
    http_method_names = ['post', 'get']


class CrossValidationClusterFileView(generics.RetrieveAPIView):
    serializer_class = CrossValidationClusterFileSerializer
    lookup_field = 'cluster_id'
    queryset = CrossValidationCluster.objects.all()


    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        path = instance.file.path
        with open(path, "rb") as file:
            content = file.read()
        try:
            response = HttpResponse(content, content_type='application/octet-stream')
            response['Content-Disposition'] =f"attachment; filename={instance.cluster_id}.pkl"

            return response
        except Exception as exc:
            return Response({'error': f'Could not read the file. ({exc})'})


class CrossValidationFolderViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = CrossValidationFolder.objects.all()
    serializer_class = CrossValidationFolderSerializer
    http_method_names = ['post', 'get']


class CrossValidationFoldViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = CrossValidationFold.objects.all()
    serializer_class = CrossValidationFoldSerializer
    http_method_names = ['post', 'get']


class CrossValidationFoldImagesViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = CrossValidationFoldimages.objects.all()
    serializer_class = CrossValidationFoldImageSerializer
    http_method_names = ['post', 'get']


class ClusterImagesAPIView(APIView):

    def get(self, request):
        query_filter = dict()
        fold_type = request.query_params.get("fold_type", None)
        if request.query_params.get("cluster_id"):
            query_filter["CrossValidationFolder__cluster_id"] = request.query_params.get("cluster_id")
        if request.query_params.get("folder_id"):
            query_filter["CrossValidationFold__folder_id"] = request.query_params.get("folder_id")
        if request.query_params.get("fold_id"):
            query_filter["fold_id"] = request.query_params.get("fold_id")

        if fold_type:
            if fold_type == "train":
                query_set = CrossValidationFoldimages.objects.filter(train=True, **query_filter).all()
            elif fold_type == "test":
                query_set = CrossValidationFoldimages.objects.filter(test=True, **query_filter).all()
            else:
                query_set = CrossValidationFoldimages.objects.filter(validation=True, **query_filter).all()
        else:
            query_set = CrossValidationFoldimages.objects.filter(**query_filter).all()
        serializer = CrossValidationFoldImageSerializer(query_set, many=True)
        return Response(serializer.data)


# Validation
class ValidatorOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(name='Validators').exists() and request.method in ['GET']:
            return True
        return False

class ImageValidationViewSet(viewsets.ReadOnlyModelViewSet):
    #permission_classes = (IsAuthenticated, ValidatorOnly,)
    queryset = ImageValidation.objects.all()
    serializer_class = ImageValidationSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = (['dataset__name', 'project_id'])


class ImageValidationFileView(generics.RetrieveAPIView):
    serializer_class = ImageValidationFileSerializer
    lookup_field = 'project_id'
    queryset = ImageValidation.objects.all()

    def retrieve(self, request, *args, **kwargs):
        gray_scale = request.query_params.get("gray_scale", False)
        height = request.query_params.get("height", None)
        width = request.query_params.get("width", None)
        image_resize = None
        if height or width:
            if not height and width:
                height = width
            if not width and height:
                width = height
            image_resize = (int(width), int(height))
        instance = self.get_object()
        image_path = instance.image.path
        image_object = None
        image_format = self.extract_image_format(image_path)
        content_type = f'image/{image_format}' if image_format else 'application/octet-stream'
        if image_resize:
            image_object = PilImage.open(image_path)
            image_object = ImageOps.exif_transpose(image_object)
            image_object = self._resize_image(image_object, image_resize)

        if gray_scale:
            if not image_object:
                image_object = PilImage.open(image_path)
                image_object = ImageOps.exif_transpose(image_object)
            image_object = self._convert_to_gray_scale(image_object)

        image_bytes = self._get_image_bytes(image_path=image_path, image_object=image_object, image_format=image_format or "PNG")
        try:
            return HttpResponse(image_bytes, content_type=content_type)
        except Exception as exc:
            return Response({'error': f'Could not read the file. ({exc})'})

    @staticmethod
    def _get_image_bytes(image_path, image_object: PilImage = None, image_format: str = "PNG"):
        if not image_object:
            with open(image_path, "rb") as image_file:
                image_bytes = image_file.read()
        else:
            buffer = BytesIO()
            image_object.save(buffer, format=image_format.upper())
            buffer.seek(0)
            image_bytes = buffer.read()
        return image_bytes

    @staticmethod
    def _resize_image(image: PilImage, size) -> PilImage:
        return image.resize(size)

    @staticmethod
    def _convert_to_gray_scale(image: PilImage) -> PilImage:
        return image.convert("L")

    @staticmethod
    def extract_image_format(image_path: str) -> str:
        image_format = str(image_path.split(".")[-1]).upper() or "PNG"
        if image_format == "JPG":
            image_format = "JPEG"
        if image_format not in ["PNG", "JPEG", "SVG"]:
            return None
        else:
            return image_format



class ImageMetaDataValidationViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated, ValidatorOnly,)
    queryset = ImageMetaDataValidation.objects.all()
    serializer_class = ImageMetaDataValidationSerializer