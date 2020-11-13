from django.core.management.base import BaseCommand, CommandError
from image_service.models import DataSet, Image, ImageMetaData
from xrayreader.data import Dataset as xrd
import os.path
import uuid
from optparse import make_option

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('dataset name', type=str, help='Write the name of the dataset')
        parser.add_argument('folder path', type=str, help='Write the path for the datasets folder on your computer')

    def handle(self, *args, **options):

        dataset_xrd = xrd(name=f"{options['dataset name']}", path=f"{options['folder path']}")

        list_of_formats = []
        for index in range(len(dataset_xrd.get_data()['data']['images'])-1):
            list_of_formats.append(dataset_xrd.get_data()['data']['images'][index].extension)

        dataset = DataSet(
            name=dataset_xrd.name,
            image_formats=list_of_formats
        )
        dataset.save()
        self.stdout.write(self.style.SUCCESS('Added Dataset!'))

        for index in range(len(dataset_xrd.get_data()['data']['images'])-1):
            image = Image(
                dataset = dataset,
                image_path = os.path.join(dataset_xrd.get_data()['data']['images'][index].path, f"{dataset_xrd.get_data()['data']['images'][index].imagename}.{dataset_xrd.get_data()['data']['images'][index].extension}")
        )
            image.save()

            image_meta_data = ImageMetaData(
                dataset=dataset,
                image=image.image_path,
                has_tb=dataset_xrd.get_data()['data']['metadata'][index].check_normality,
                original_report=dataset_xrd.get_data()['data']['metadata'][index].report
            )
            image_meta_data.save()
        self.stdout.write(self.style.SUCCESS(f"Added {len(dataset_xrd.get_data()['data']['images'])-1} Images!"))
        self.stdout.write(self.style.SUCCESS(f"Added {len(dataset_xrd.get_data()['data']['images'])-1} Metadatas!"))
