from rest_framework import serializers
from .models import DataSet, Image, ImageMetaData, Report

class DataSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSet
        fields = ['name', 'image_formats']


class ImageMetaDataSerializer(serializers.ModelSerializer):
    dataset_name = serializers.CharField(source="dataset.name", read_only=True)
    class Meta:
        model = ImageMetaData
        fields = ['dataset_name', 'gender', 'age', 'has_tb', 'original_report', 'date_exam']


class ImageSerializer(serializers.ModelSerializer):
    dataset_name = serializers.CharField(source="dataset.name", read_only=True)
    metadata = ImageMetaDataSerializer(required=True)

    class Meta:
        model = Image
        fields = ['dataset_name', 'image','project_id' ,'insertion_date', 'metadata']

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['image', 'report_insertion_date', 'report', 'form_version', 'image_quality',
                'image_quality', 'reason_low_quality', 'doctor_id' ]
