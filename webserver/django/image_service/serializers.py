from rest_framework import serializers
from .models import DataSet, Image, ImageMetaData

class DataSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSet
        fields = ['name', 'image_formats']


class ImageMetaDataSerializer(serializers.ModelSerializer):
    dataset_name = serializers.CharField(source="dataset.name", read_only=True)
    class Meta:
        model = ImageMetaData
        fields = ['dataset_name', 'has_tb', 'original_report']


class ImageSerializer(serializers.ModelSerializer):
    dataset_name = serializers.CharField(source="dataset.name", read_only=True)
    metadata = ImageMetaDataSerializer(required=True)

    class Meta:
        model = Image
        fields = ['dataset_name', 'image', 'metadata']
