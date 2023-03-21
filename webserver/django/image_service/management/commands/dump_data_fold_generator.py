import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from image_service.models import Image, DataSet, ImageMetaData, DatasetCrossValidationFolds


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('dataset_name', type=str,
                            help='Dataset name to generate fold')

    def handle(self, *args, **options):
        dataset = DataSet.objects.get(name=options['dataset_name'].lower())
        data = []
        images = Image.objects.filter(dataset=dataset)
        for image in images:
            metadata = ImageMetaData.objects.get(image=image)
            if metadata is not None:
                data.append({
                    'dataset_name': dataset.name,
                    'target': int(metadata.has_tb),
                    'project_id': image.project_id,
                    'insertion_date': image.insertion_date,
                    'date_acquisition': image.date_acquisition,
                })
            else:
                data.append({
                    'dataset_name': dataset.name,
                    'target': 0,
                    'project_id': image.project_id,
                    'insertion_date': image.insertion_date,
                    'date_acquisition': image.date_acquisition,
                })
            if not os.path.exists(os.path.join(settings.MEDIA_ROOT, 'dump_data_fold', f"{dataset.name}_cross_validation.json")):
                os.makedirs(os.path.join(settings.MEDIA_ROOT, 'dump_data_fold'))
                os.mknod(os.path.join(settings.MEDIA_ROOT, 'dump_data_fold', f"{dataset.name}_cross_validation.json"))
            with open(os.path.join(settings.MEDIA_ROOT, 'dump_data_fold', f"{dataset.name}_cross_validation.json"),
                      mode="w") as file:
                file.write(json.dumps(data, default=str))
            self.stdout.write(self.style.SUCCESS(f"Dump data generated!"))
