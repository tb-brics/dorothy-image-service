from django.shortcuts import render
from rest_framework import viewsets
from .models import DataSet, Image, ImageMetaData, Report, ImageSampling
from .serializers import DataSetSerializer, ImageSerializer, ImageMetaDataSerializer, ReportSerializer, ImageSamplingSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from django.views.generic.detail import DetailView




class DataSetViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DataSet.objects.all()
    serializer_class = DataSetSerializer

class ImageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

class ImageFileView(DetailView):
    model = Image    
    def get(self, request, *args, **kwargs):
        image = self.image
        image_data = image.read()
        return HttpResponse(image_data, content_type="image/png")


class ImageMetaDataViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ImageMetaData.objects.all()
    serializer_class = ImageMetaDataSerializer
