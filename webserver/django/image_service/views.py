from django.shortcuts import render
from rest_framework import viewsets
from .models import DataSet, Image, ImageMetaData
from .serializers import DataSetSerializer, ImageSerializer, ImageMetaDataSerializer

class DataSetViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DataSet.objects.all()
    serializer_class = DataSetSerializer

class ImageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

class ImageMetaDataViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ImageMetaData.objects.all()
    serializer_class = ImageMetaDataSerializer
