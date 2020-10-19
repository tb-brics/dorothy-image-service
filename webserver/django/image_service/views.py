from django.shortcuts import render
from rest_framework import viewsets
<<<<<<< HEAD
from .models import DataSet, Image, ImageMetaData
from .serializers import DataSetSerializer, ImageSerializer, ImageMetaDataSerializer

=======
from .models import DataSet, Image, ImageMetaData, DataBase
from .serializers import DataSetSerializer, ImageSerializer, ImageMetaDataSerializer, DataBaseSerializer
# Create your views here.
>>>>>>> 303193b4c0fcf1d2a4f6579c05cfd45ccbdd45bc

class DataSetViewSet(viewsets.ModelViewSet):
    queryset = DataSet.objects.all()
    serializer_class = DataSetSerializer

class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

class ImageMetaDataViewSet(viewsets.ModelViewSet):
    queryset = ImageMetaData.objects.all()
    serializer_class = ImageMetaDataSerializer

class DataBaseViewSet(viewsets.ModelViewSet):
    queryset = DataBase.objects.all()
    serializer_class = DataBaseSerializer
