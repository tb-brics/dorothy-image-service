from PIL import Image as pil_image

from  django.http import HttpResponse
from rest_framework import viewsets
from rest_framework import generics

from .models import DataSet, Image, ImageMetaData, Report, ImageSampling
from .serializers import (DataSetSerializer,
                          ImageSerializer,
                          ImageMetaDataSerializer,
                          ReportSerializer,
                          ImageSamplingSerializer,
                          ImageFileSerializer)
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.decorators import renderer_classes
from rest_framework.permissions import IsAuthenticated




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
