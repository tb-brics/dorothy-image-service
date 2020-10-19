from django.shortcuts import render
from rest_framework import viewsets
from .models import DataSet, Image, ImageMetaData
from .serializers import DataSetSerializer, ImageSerializer, ImageMetaDataSerializer
# Create your views here.

class DataSetViewSet(viewsets.ModelViewSet):
    queryset = DataSet.objects.all()
    serializer_class = DataSetSerializer

class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

class ImageMetaDataViewSet(viewsets.ModelViewSet):
    queryset = ImageMetaData.objects.all()
    serializer_class = ImageMetaDataSerializer

