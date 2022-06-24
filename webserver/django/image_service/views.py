from  django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework import generics
from rest_framework.views import APIView
from django.shortcuts import render

from .models import DataSet, Image, ImageMetaData, Report, ImageSampling, Folds
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
                          FoldSerializer)
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import BasePermission


def loginPage(request):
    context = {}
    return render(request, 'accounts/login.html', context)

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


class ImagePostViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, UploaderOnly,)
    queryset = Image.objects.all()
    serializer_class = ImagePostSerializer
    http_method_names = ['post']


class MetaDataPostViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, UploaderOnly,)
    queryset = ImageMetaData.objects.all()
    serializer_class = PostMetaDataSerializer
    http_method_names = ['post']


class Post_Image_AND_MetaDataPostViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, UploaderOnly,)
    queryset = ImageMetaData.objects.all()
    serializer_class = Post_Image_AND_MetaDataPostSerializer
    http_method_names = ['post']


class FoldsViewSet(APIView):
    def get(self, request):
        folds = Folds.objects.all()
        serializer = FoldSerializer(folds, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FoldSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)