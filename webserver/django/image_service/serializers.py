from rest_framework import serializers
from .models import DataSet, Image, ImageMetaData, DataBase

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
<<<<<<< HEAD
        fields = ['dataset_name', 'image', 'has_tb', 'original_report']
=======
        fields = ['dataset', 'image', 'has_tb', 'original_report']

class DataBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataBase
        fields = ['url' ,'image']
>>>>>>> 303193b4c0fcf1d2a4f6579c05cfd45ccbdd45bc
