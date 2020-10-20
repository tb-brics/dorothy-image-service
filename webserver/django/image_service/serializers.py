from rest_framework import serializers
from .models import DataSet, Image, ImageMetaData

class DataSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSet
        fields = ['name', 'image_formats']

class ImageSerializer(serializers.ModelSerializer):
    dataset_name = serializers.CharField(source="dataset.name", read_only=True)
    image_path = serializers.CharField(source="image.image_path", read_only=True)

    class Meta:
        model = Image
        fields = ['dataset_name', 'image_path']

class ImageMetaDataSerializer(serializers.ModelSerializer):
    dataset_name = serializers.CharField(source="dataset.name", read_only=True)
    class Meta:
        model = ImageMetaData
        fields = ['dataset_name', 'image', 'has_tb', 'original_report']
