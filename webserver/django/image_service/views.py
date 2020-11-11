from django.shortcuts import render
from rest_framework import viewsets
from .models import DataSet, Image, ImageMetaData
from .serializers import DataSetSerializer, ImageSerializer, ImageMetaDataSerializer
from rest_framework.filters import SearchFilter, OrderingFilter

class DataSetViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DataSet.objects.all()
    serializer_class = DataSetSerializer

class ImageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = (['dataset__name'])


class ImageMetaDataViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ImageMetaData.objects.all()
    serializer_class = ImageMetaDataSerializer
