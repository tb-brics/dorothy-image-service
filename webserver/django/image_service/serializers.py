import http
import logging
from hashlib import sha1
from time import time
from re import I
from django.urls import reverse
from rest_framework import serializers
from .models import DataSet, Image, ImageMetaData, Report, ImageSampling, \
    CrossValidationFold, CrossValidationFolder, CrossValidationCluster, CrossValidationFoldimages, \
    DataQualityAnnotation, ImageValidation, ImageMetaDataValidation

import json


def get_time_hash(length: int) -> str:
    """
    Generate a fixed-length hash based on current date & time.
    Args:
        length (int): hash length
    Returns:
        str
    """
    hash_object = sha1()
    hash_object.update(str(time()).encode("utf-8"))
    return hash_object.hexdigest()[:length]


log = logging.getLogger(__name__)


class DataSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSet
        fields = ['name', 'image_formats', 'number_images']


class DataQualityAnnotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataQualityAnnotation
        fields = [
            'project_id',
            'under_penetrated',
            'over_penetrated',
            'costophrenic_cropped',
            'apices_cropped',
            'reliable_radiography',
            'minimum_interpretation_quality'
        ]


class ImageMetaDataSerializer(serializers.ModelSerializer):
    dataset_name = serializers.CharField(source="dataset.name", read_only=True)

    class Meta:
        model = ImageMetaData
        fields = ['dataset_name', 'gender', 'age', 'has_tb', 'original_report', 'date_exam', 'synthetic',
                  'additional_information']


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
            raise serializers.ValidationError({"image": "image does not exist"})

        try:
            json.loads(report_content)
        except TypeError as e:
            log.error(f'Report JSON format is not correct! Form validation failed! {e}')
            raise serializers.ValidationError({"report_content": "the JSON object must be str, bytes or bytearray"})

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
            raise serializers.ValidationError({"dataset": "dataset does not exist"})

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
            raise serializers.ValidationError({"image": "image does not exist"})

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


class CrossValidationClusterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrossValidationCluster
        fields = '__all__'


class CrossValidationClusterFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrossValidationCluster
        fields = ('file',)


class CrossValidationFolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrossValidationFolder
        fields = '__all__'

    def validate(self, data):
        # Verificar se o cluster_id existe
        if data.get("cluster_id"):
            return data
        else:
            log.error("Missing required field 'cluster_id'.")
            raise serializers.ValidationError(
                {"cluster_id": "Missing required field 'cluster_id'."},
                code=http.HTTPStatus.BAD_REQUEST)

    def create(self, validated_data):
        instance = CrossValidationFolder()
        cluster_id = validated_data.get("cluster_id")
        instance.folder_id = cluster_id.cluster_id + "_folder_" + get_time_hash(8)
        instance.cluster_id = cluster_id
        instance.save()
        return instance


class CrossValidationFoldSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrossValidationFold
        fields = '__all__'

    def validate(self, data):
        if not data.get("folder_id"):
            log.error("Missing required field 'folder_id'.")
            raise serializers.ValidationError(
                {"fold": "Missing required field 'folder_id'."},
                code=http.HTTPStatus.BAD_REQUEST)
        return data

    def create(self, validated_data):
        instance = CrossValidationFold()
        if validated_data.get("fold_id"):
            instance.fold_id = validated_data.get("fold_id")
        else:
            instance.fold_id = validated_data.get("folder_id").folder_id + "_fold_" + get_time_hash(8)
        instance.folder_id = validated_data.get("folder_id")
        instance.save()
        return instance


class CrossValidationFoldImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrossValidationFoldimages
        fields = '__all__'

    def validate(self, data):
        is_train_data = data.get("train")
        is_test_data = data.get("test")
        is_validation_data = data.get("validation")

        if (is_train_data and is_test_data) or (is_train_data and is_validation_data) or (is_validation_data and is_test_data):
            log.error("The Image can only assume one role inside a fold (train, test, or validation).")
            raise serializers.ValidationError(
                {"project_id": "The Image can only assume one role inside a fold (train, test, or validation)."},
                code=http.HTTPStatus.BAD_REQUEST)
        return data

    def create(self, validated_data):
        instance = CrossValidationFoldimages(**validated_data)
        instance.save()
        return instance


class ImageMetaDataValidationSerializer(serializers.ModelSerializer):
    dataset_name = serializers.CharField(source="dataset.name", read_only=True)

    class Meta:
        model = ImageMetaDataValidation
        fields = ['dataset_name', 'gender', 'age', 'has_tb', 'original_report', 'date_exam', 'synthetic',
                  'additional_information']


class ImageValidationSerializer(serializers.ModelSerializer):
    dataset_name = serializers.CharField(source="dataset.name", read_only=True)
    metadata = ImageMetaDataValidationSerializer(required=True)
    number_reports = serializers.IntegerField(default=0)
    image_url = serializers.SerializerMethodField('get_image_url')

    def count_reports(self, obj):
        return obj.number_reports.count()

    def get_image_url(self, obj):
        request = self.context.get('request')
        url = reverse('image_file', kwargs={'project_id': obj.project_id})
        return request.build_absolute_uri(url)

    class Meta:
        model = ImageValidation
        fields = ['dataset_name',
                  'image_url',
                  'project_id',
                  'insertion_date',
                  'metadata',
                  'date_acquisition',
                  'number_reports']
