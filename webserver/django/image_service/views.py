from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import viewsets
from .models import DataSet, Image, ImageMetaData, Report, ImageSampling
from .serializers import DataSetSerializer, ImageSerializer, ImageMetaDataSerializer, ReportSerializer, ImageSamplingSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response



class DataSetViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DataSet.objects.all()
    serializer_class = DataSetSerializer


class ImageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = (['dataset__name','project_id'])


class ImageMetaDataViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ImageMetaData.objects.all()
    serializer_class = ImageMetaDataSerializer


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer


class ImageSamplingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ImageSampling.objects.all()
    serializer_class = ImageSamplingSerializer
