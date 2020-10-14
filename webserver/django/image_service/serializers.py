from rest_framework import serializers
from .models import DataSet, Image, ImageMetaData, DataBase

class DataSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSet
        fields = ['database', 'image_formats']

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['dataset', 'image_path']

class ImageMetaDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageMetaData
        fields = ['dataset', 'image', 'has_tb', 'original_report']

class DataBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataBase
        fields = ['url' ,'image']
