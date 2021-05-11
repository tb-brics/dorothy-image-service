import logging
from django.urls import reverse
from rest_framework import serializers
from .models import DataSet, Image, ImageMetaData, Report, ImageSampling

import json


log = logging.getLogger(__name__)

class DataSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSet
        fields = ['name', 'image_formats', 'number_images']


class ImageMetaDataSerializer(serializers.ModelSerializer):
    dataset_name = serializers.CharField(source="dataset.name", read_only=True)

    class Meta:
        model = ImageMetaData
        fields = ['dataset_name', 'gender', 'age', 'has_tb', 'original_report', 'date_exam']


class ImageSerializer(serializers.ModelSerializer):
    dataset_name = serializers.CharField(source="dataset.name", read_only=True)
    metadata = ImageMetaDataSerializer(required=True)
    number_reports = serializers.IntegerField(default=0)
    image_url = serializers.SerializerMethodField('get_image_url')

    def count_reports(self, obj):
        return obj.number_reports.count()

    def get_image_url(self, obj):
        request = self.context.get('request')
        url = reverse('image_file', kwargs={'project_id': obj.project_id})
        return request.build_absolute_uri(url)

    class Meta:
        model = Image
        fields = ['dataset_name',
                  'image_url',
                  'project_id',
                  'insertion_date',
                  'metadata',
                  'date_acquisition',
                  'number_reports']

class ReportSerializer(serializers.ModelSerializer):
    image = serializers.CharField()

    def validate(self, data):
        log.info('Starting report form validation.')

        image = data.get('image')
        report_content = data.get('report_content')

        try:
            image = Image.objects.get(project_id=image)
        except Image.DoesNotExist as e:
            log.error('Image ID (%s) received from report service does not exists! %s', image, e)
            raise serializers.ValidationError({"image":"image does not exist"})

        try:
            json.loads(report_content)
        except TypeError as e:
            log.error('Report JSON format is not correct! Form validation failed! %s', e)
            raise serializers.ValidationError({"report_content":"the JSON object must be str, bytes or bytearray"})

        log.info('Report content for image %s successfully validated.', image)
        return data

    def create(self, validate_data):
        log.info('Creating report DB instance.')
        instance = Report()
        image_field = validate_data.get('image')
        image = Image.objects.get(project_id=image_field)

        instance.image = image
        instance.performed_by = validate_data.get("performed_by")
        instance.date_added = validate_data.get("date_added")
        instance.image_quality = validate_data.get("image_quality")
        instance.reason_low_quality = validate_data.get("reason_low_quality")
        instance.report_version = validate_data.get("report_version")
        instance.report_content = json.loads(validate_data.get("report_content"))

        instance.save()
        log.info('Report content for image %s successfully saved to DB.', image_field)

        return instance

    class Meta:
        model = Report
        fields = ['image', 'performed_by', 'date_added', 'image_quality',
                'reason_low_quality', 'report_version', 'report_content']


class ImageSamplingSerializer(serializers.ModelSerializer):
    project_id = serializers.CharField(source='image.project_id', read_only=True)
    image = serializers.ImageField(source='image.image')

    class Meta:
        model = ImageSampling
        fields = ['image', 'project_id', 'insertion_date', 'rank_position']


class ImageFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('image',)
