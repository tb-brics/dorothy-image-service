from rest_framework import serializers
from .models import DataSet, Image, ImageMetaData, Report, ImageSampling
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

    class Meta:
        model = Image
        fields = ['dataset_name', 'image','project_id' ,'insertion_date', 'metadata', 'date_acquisition', 'number_reports']

    def count_reports(self,obj):
        return obj.number_reports.count()


class ReportSerializer(serializers.ModelSerializer):
    project_id = serializers.CharField(source="image.project_id")

    def validate(self, data):
        image = data.get('image')
        project_id = image.get('project_id')
        print(project_id)
        print(image)
        try:
            image = Image.objects.get(project_id=project_id)
        except Image.DoesNotExist:
            raise serializers.ValidationError({"project_id":"image does not exist"})
        return data

    def create(self, validate_data):
        instance = Report()
        image_field = validate_data.get('image')
        project_id = image_field.get('project_id')
        image = Image.objects.get(project_id= project_id)
        instance.image = image
        instance.performed_byform = validate_data.get("performed_by")
        instance.date_added = validate_data.get("date_added")
        instance.image_quality = validate_data.get("image_quality")
        instance.reason_low_quality = validate_data.get("reason_low_quality")
        instance.report_version = validate_data.get("report_version")
        instance.report_content = validate_data.get("report_content")
        print(instance)
        return instance

    class Meta:
        model = Report
        fields = ['project_id', 'performed_by', 'date_added', 'image_quality',
                'reason_low_quality', 'report_version', 'report_content' ]


class ImageSamplingSerializer(serializers.ModelSerializer):

    class Meta:
        model = ImageSampling
        fields = [ 'image', 'insertion_date']
