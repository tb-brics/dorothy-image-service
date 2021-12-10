import logging
from re import I
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
            log.error(f'Image ID ({image}) received from report service does not exists! {e}')
            raise serializers.ValidationError({"image":"image does not exist"})

        try:
            json.loads(report_content)
        except TypeError as e:
            log.error(f'Report JSON format is not correct! Form validation failed! {e}')
            raise serializers.ValidationError({"report_content":"the JSON object must be str, bytes or bytearray"})

        log.info(f'Report content for image {image} successfully validated.')
        return data

    def create(self, validate_data):
        log.info('Creating report DB instance.')
        instance = Report()
        image_field = validate_data.get('image')
        image = Image.objects.get(project_id=image_field)

        instance.image = image
        instance.performed_by = validate_data.get("performed_by")
        instance.date_added = validate_data.get("date_added")
        instance.report_version = validate_data.get("report_version")
        instance.report_content = json.loads(validate_data.get("report_content"))

        instance.save()
        log.info(f'Report content for image {image_field} successfully saved to DB.')

        return instance

    class Meta:
        model = Report
        fields = ['image', 'performed_by', 'date_added', 'report_version', 'report_content']


class ImageSamplingSerializer(serializers.ModelSerializer):
    project_id = serializers.CharField(source='image.project_id', read_only=True)
    image_url = serializers.SerializerMethodField('get_image_url')

    def get_image_url(self, obj):
        request = self.context.get('request')
        url = reverse('image_file', kwargs={'project_id': obj.image.project_id})
        return request.build_absolute_uri(url)

    class Meta:
        model = ImageSampling
        fields = ['image_url', 'project_id', 'insertion_date', 'rank_position']


class ImageFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('image',)


class DataSetPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSet
        fields = ['name', 'image_formats']


class ImagePostSerializer(serializers.ModelSerializer):
    dataset_name = serializers.CharField(source="dataset.name")


    def validate(self, data):
        log.info('Starting dataset validation.')
        dataset_name = data.get("dataset").get("name")
        try:
            dataset = DataSet.objects.get(name=dataset_name)
        except DataSet.DoesNotExist as e:
            log.error(f'DataSet name ({dataset_name}) received does not exists! {e}')
            raise serializers.ValidationError({"dataset":"dataset does not exist"})

        log.info(f'Data successfully validated: {dataset_name}')
        return data

    def create(self, validate_data):
        log.info('Creating image DB instance.')
        instance = Image()
        dataset_name = validate_data.get("dataset").get("name")
        dataset = DataSet.objects.get(name=dataset_name)

        instance.dataset = dataset
        instance.image = validate_data.get("image")

        instance.save()
        log.info('Image content successfully saved to DB.')

        return instance

    class Meta:
        model = Image
        fields = ['dataset_name', 'image']


class PostMetaDataSerializer(serializers.ModelSerializer):
    image = serializers.CharField()

    def validate(self, data):
        image = data.get('image')

        try:
            image = Image.objects.get(project_id=image)
        except Image.DoesNotExist as e:
            log.error(f'Image ID ({image}) received from image service does not exists! {e}')
            raise serializers.ValidationError({"image":"image does not exist"})

        return data

    def create(self, validate_data):
        log.info('Creating metadata DB instance.')
        instance = ImageMetaData()

        image_field = validate_data.get('image')
        image = Image.objects.get(project_id=image_field)

        instance.image = image
        instance.has_tb = validate_data.get("has_tb")
        instance.original_report = validate_data.get("original_report")
        instance.gender = validate_data.get("gender")
        instance.age = validate_data.get("age")
        instance.date_exam = validate_data.get("date_exam")

        instance.save()
        log.info('successfully saved to DB.')

        return instance

    class Meta:
        model = ImageMetaData
        fields = ['image', 'has_tb', 'original_report', 'gender', 'age', 'date_exam']


class Post_Image_AND_MetaDataPostSerializer(serializers.ModelSerializer):
    image = ImagePostSerializer()

    def create(self, validate_data):
        log.info('Creating metadata DB instance.')
        instance = ImageMetaData()

        image_obj = Image()
        dataset_name = validate_data.get('image').get('dataset').get('name')
        image_obj.dataset = DataSet.objects.get(name=dataset_name)
        image_obj.image = validate_data.get("image").get("image")
        image_obj.save()

        instance.image = image_obj
        instance.has_tb = validate_data.get("has_tb")
        instance.original_report = validate_data.get("original_report")
        instance.gender = validate_data.get("gender")
        instance.age = validate_data.get("age")
        instance.date_exam = validate_data.get("date_exam")

        instance.save()
        log.info('successfully saved to DB.')

        return instance

    class Meta:
        model = ImageMetaData
        fields = ['image', 'has_tb', 'original_report', 'gender', 'age', 'date_exam']
