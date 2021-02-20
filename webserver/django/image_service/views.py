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


# class ImageSamplingViewSet(viewsets.ModelViewSet):

#     sample_1_ids = [
#                     "china_CHNCXR_0441_1",
#                     "china_CHNCXR_0182_0",
#                     "china_CHNCXR_0492_1",
#                     "china_CHNCXR_0038_0",
#                     "china_CHNCXR_0450_1",
#                     "china_CHNCXR_0113_0",
#                     "china_CHNCXR_0370_1",
#                     "china_CHNCXR_0171_0",
#                     "china_CHNCXR_0642_1",
#                     "china_CHNCXR_0076_0",
#                     ]
#     sample_1_date = "2021-02-18"

#     for image in Image.objects.all():
#         if image.project_id in sample_1_ids:
#             image_sampling = ImageSampling(image = image.image, insertion_date = sample_1_date)
#             if image_sampling not in ImageSampling.objects.all():
#                 image_sampling.save()

#     queryset = ImageSampling.objects.all()
#     serializer_class = ImageSamplingSerializer
