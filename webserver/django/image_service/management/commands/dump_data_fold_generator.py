import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from webserver.django.image_service.models import Image, DataSet, ImageMetaData, DatasetCrossValidationFolds


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('dataset_name', type=str,
                            help='Dataset name to generate fold')

    def handle(self, *args, **options):
        dataset = DataSet.objects.get(name=options['dataset_name'].lower())
        if not DatasetCrossValidationFolds.objects.get(dataset=dataset):
            data = []
            images = Image.objects.filter(dataset=dataset)
            for image in images:
                metadata = ImageMetaData.objects.get(image=image)
                if metadata is not None:
                    data.append({
                        'dataset_name': dataset.name,
                        'target': int(metadata.has_tb),
                        'image_url': str(image.image),
                        'project_id': image.project_id,
                        'insertion_date': image.insertion_date,
                        'metadata': metadata,
                        'date_acquisition': image.date_acquisition,
                    })
                else:
                    data.append({
                        'dataset_name': dataset.name,
                        'target': 0,
                        'image_url': str(image.image),
                        'project_id': image.project_id,
                        'insertion_date': image.insertion_date,
                        'metadata': None,
                        'date_acquisition': image.date_acquisition,
                    })
            with open(os.path.join(settings.MEDIA_ROOT, f"{dataset.name}_cross_validation.json"), mode="w") as file:
                file.write(json.dumps(data, default=str))
