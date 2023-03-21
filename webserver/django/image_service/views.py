import os.path
from io import BytesIO

from PIL import Image as PilImage
from PIL import ImageOps
from django.conf import settings
from django.core.files import File
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import generics
from rest_framework import status
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import BasePermission
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.paginator import Paginator

from .models import DataSet, Image, ImageMetaData, Report, ImageSampling, \
    DatasetCrossValidationFolds, CrossValidationCluster, \
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
                          CrossValidationClusterFileSerializer,
                          CrossValidationClusterSerializer,
                          DatasetCrossValidationListFoldsSerializer,
                          DataQualityAnnotationSerializer,
                          ImageValidationSerializer,
                          ImageMetaDataValidationSerializer,
                          ImageValidationFileSerializer,
                          ImageValidationPostSerializer,
                          PostMetaDataValidationSerializer,
                          Post_Image_AND_MetaDataValidationPostSerializer,
                          DatasetCrossValidationGetFoldsFileSerializer)


def loginPage(request):
    context = {}
    return render(request, 'accounts/login.html', context)


class DataSetViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = DataSet.objects.all()
    serializer_class = DataSetSerializer
    pagination_class = None


class DataQualityAnnotationViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = DataQualityAnnotationSerializer
    # filter_backends = SearchFilter
    # search_fields = (['project_id'])
    http_method_names = ['post', 'get']
    pagination_class = None

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
    serializer_class = ImageSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = (['=dataset__name', '=project_id'])
    pagination_class = None

    def get_queryset(self):
        queryset = Image.objects.all()

        group_names = [group['name'] for group in self.request.user.groups.all().values()]

        if "Validators" not in group_names:
            datasets = DataSet.objects.filter(public=True)
            return queryset.filter(dataset__in=datasets)
        else:
            return queryset


class ImagePaginatedRequest(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ImageSerializer
    filter_backends = SearchFilter
    lookup_field = 'dataset_name'
    default_limit = 100
    limit_query_param = 'limit'
    offset_query_param = 'offset'

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def list(self, request, dataset_name, *args, **kwargs):
        queryset = Image.objects.filter(dataset__name=dataset_name)
        group_names = [group['name'] for group in self.request.user.groups.all().values()]
        if group_names:
            if "Validators" not in group_names:
                datasets = DataSet.objects.filter(public=True)
                queryset = queryset.filter(dataset__in=datasets)
        results = self.paginate_queryset(queryset)
        serializer = self.get_serializer(data=results, many=True)
        serializer.is_valid()
        return self.get_paginated_response(data=serializer.data)


class ImageMetaDataViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = ImageMetaData.objects.all()
    serializer_class = ImageMetaDataSerializer
    pagination_class = None


class ReportViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    filter_backends = [SearchFilter]
    search_fields = ['image__project_id', 'performed_by']
    pagination_class = None


class ImageSamplingViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = ImageSampling.objects.all()
    serializer_class = ImageSamplingSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    ordering_fields = (['rank_position'])
    pagination_class = None


class ImageFileView(generics.RetrieveAPIView):
    serializer_class = ImageFileSerializer
    lookup_field = 'project_id'
    queryset = Image.objects.all()
    pagination_class = None

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
    pagination_class = None


class ImagePostViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, UploaderOnly,)
    queryset = Image.objects.all()
    serializer_class = ImagePostSerializer
    http_method_names = ['post']
    pagination_class = None

    def create(self, request, *args, **kwargs):
        if request.data.get("image_path"):
            path = os.path.join(settings.MEDIA_ROOT, request.data.get("image_path"))
            if not os.path.exists(path):
                return Response({"error": "File not found."}, status=status.HTTP_404_NOT_FOUND)
            with open(path, mode="rb") as file:
                data = {}
                data.update(request.data)
                data.pop("image_path")
                data["image"] = File(file, name=os.path.join(settings.MEDIA_ROOT, request.data.get("image_path")))
                serializer = self.get_serializer(data=data)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return super().create(request, *args, **kwargs)


class MetaDataPostViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, UploaderOnly,)
    queryset = ImageMetaData.objects.all()
    serializer_class = PostMetaDataSerializer
    http_method_names = ['post']
    pagination_class = None


class Post_Image_AND_MetaDataPostViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, UploaderOnly,)
    queryset = ImageMetaData.objects.all()
    serializer_class = Post_Image_AND_MetaDataPostSerializer
    http_method_names = ['post']
    pagination_class = None


class CrossValidationClusterViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = CrossValidationCluster.objects.all()
    serializer_class = CrossValidationClusterSerializer
    lookup_field = 'cluster_id'
    http_method_names = ['post', 'get']
    pagination_class = None


class DatasetCrossValidationListFoldFilesView(viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)
    filter_backends = (SearchFilter, OrderingFilter)
    serializer_class = DatasetCrossValidationListFoldsSerializer
    search_fields = ['=dataset_name']
    queryset = DatasetCrossValidationFolds.objects.all()
    pagination_class = None

    def get_queryset(self):
        queryset = DatasetCrossValidationFolds.objects.all()

        group_names = [group['name'] for group in self.request.user.groups.all().values()]

        if "Validators" not in group_names:
            datasets = DataSet.objects.filter(public=True)
            return queryset.filter(dataset__in=datasets)
        else:
            return queryset


class DatasetCrossValidationGetFoldFile(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = DatasetCrossValidationGetFoldsFileSerializer
    queryset = DatasetCrossValidationFolds.objects.all()
    lookup_field = 'dataset_name'
    pagination_class = None

    def retrieve(self, request, dataset_name, *args, **kwargs):
        fold: DatasetCrossValidationFolds = self.queryset.filter(dataset__name=dataset_name).first()
        path = fold.file.path
        with open(path, "rb") as file:
            content = file.read()
        try:
            response = HttpResponse(content, content_type='application/octet-stream')
            response['Content-Disposition'] = f"attachment; filename={fold.dataset.name}.{fold.file_type}"

            return response
        except Exception as exc:
            return Response({'error': f'Could not read the file. ({exc})'})


class CrossValidationClusterFileView(generics.RetrieveAPIView):
    serializer_class = CrossValidationClusterFileSerializer
    queryset = CrossValidationCluster.objects.all()
    lookup_field = 'cluster_id'
    pagination_class = None

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        path = instance.file.path
        with open(path, "rb") as file:
            content = file.read()
        try:
            response = HttpResponse(content, content_type='application/octet-stream')
            response['Content-Disposition'] = f"attachment; filename={instance.cluster_id}.pkl"

            return response
        except Exception as exc:
            return Response({'error': f'Could not read the file. ({exc})'})


# Validation
class ValidatorOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(name='Validators').exists() and request.method in ['GET']:
            return True
        return False


class ImageValidationViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated, ValidatorOnly,)
    queryset = ImageValidation.objects.all()
    serializer_class = ImageValidationSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = (['dataset__name', 'project_id'])
    pagination_class = None


class ImageValidationFileView(generics.RetrieveAPIView):
    serializer_class = ImageValidationFileSerializer
    lookup_field = 'project_id'
    queryset = ImageValidation.objects.all()
    pagination_class = None

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
    pagination_class = None


class ImageValidationPostViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, UploaderOnly,)
    queryset = ImageValidation.objects.all()
    serializer_class = ImageValidationPostSerializer
    http_method_names = ['post']
    pagination_class = None

class MetaDataValidationPostViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, UploaderOnly,)
    queryset = ImageMetaDataValidation.objects.all()
    serializer_class = PostMetaDataValidationSerializer
    http_method_names = ['post']
    pagination_class = None


class Post_Image_AND_MetaDataValidationPostViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, UploaderOnly,)
    queryset = ImageMetaDataValidation.objects.all()
    serializer_class = Post_Image_AND_MetaDataValidationPostSerializer
    http_method_names = ['post']
    pagination_class = None
