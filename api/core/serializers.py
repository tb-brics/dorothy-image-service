from rest_framework import serializers
from .models import DataSet, Image, ImageMetaData

class DataSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSet
        fields = ['database', 'count', 'image_formats']

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['dataset', 'image_path']

class ImageMetaDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageMetaData
        fields = ['dataset', 'image', 'has_tb', 'original_report']
