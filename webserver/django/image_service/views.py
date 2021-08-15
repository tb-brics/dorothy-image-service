from PIL import Image as pil_image
from django.db.models import query
from django.db.models.query import QuerySet

from  django.http import HttpResponse
from django.http.response import JsonResponse
from rest_framework import viewsets
from rest_framework import generics

from .models import DataSet, Image, ImageMetaData, Report, ImageSampling 
from .serializers import (DataSetSerializer,
                          ImageSerializer,
                          ImageMetaDataSerializer,
                          ReportSerializer,
                          ImageSamplingSerializer,
                          ImageFileSerializer,
                          DataSetPostSerializer,
                          ImagePostSerializer,
                          PostMetaDataSerializer,
                          Post_Image_AND_MetaDataPostSerializer)
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.decorators import renderer_classes, api_view
from rest_framework.permissions import IsAuthenticated, IsAdminUser



class DataSetViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = DataSet.objects.all()
    serializer_class = DataSetSerializer


class ImageViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = (['dataset__name','project_id'])


class ImageMetaDataViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = ImageMetaData.objects.all()
    serializer_class = ImageMetaDataSerializer


class ReportViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Report.objects.all()
    serializer_class = ReportSerializer


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
        instance = self.get_object()
        image_path = instance.image.path
        try:
            with open(image_path, 'rb') as img:
                return HttpResponse(img.read(), content_type='image/png')
        except Exception as exc:
            return Response({'error': f'Could not read the file. ({exc})'})



class DataSetPostViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsAdminUser,)
    queryset = DataSet.objects.all()
    serializer_class = DataSetPostSerializer
    http_method_names = ['post']


class ImagePostViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsAdminUser,)
    queryset = Image.objects.all()
    serializer_class = ImagePostSerializer
    http_method_names = ['post']

class MetaDataPostViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsAdminUser,)
    queryset = ImageMetaData.objects.all()
    serializer_class = PostMetaDataSerializer
    http_method_names = ['post']

class Post_Image_AND_MetaDataPostViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsAdminUser,)
    queryset = ImageMetaData.objects.all()
    serializer_class = Post_Image_AND_MetaDataPostSerializer
    http_method_names = ['post']
