import os

from csv import DictReader
from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings
from image_service.models import Image, DataSet, ImageMetaData
#from webserver.django.image_service.models import Image, DataSet, ImageMetaData
import json


def csv_reader(file_path: str) -> iter:
    """
    Returns an iterator for the lines of the CSV file to be read
    """
    if not os.path.exists(file_path):
        raise FileExistsError("")
    with open(file_path) as csv_file:
        reader = DictReader(csv_file)
        for row in reader:
            yield row


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str,
                            help='Path to csv file with synthetic image information')

    def handle(self, *args, **options):
        for row in csv_reader(options["file_path"]):
            try:
                image_instance = Image()
                model_name = row["dataset_name"].lower().split("_")[1]
                image_instance.dataset = DataSet.objects.get(name=row["dataset_name"].lower())
                image_path = row["raw_image_path"].replace("//", "/").replace("/home/jodafons/public/brics_data/Shenzhen/", "")
                if not os.path.exists(os.path.join(settings.MEDIA_ROOT, image_path)):
                    raise FileNotFoundError()
                with open(os.path.join(settings.MEDIA_ROOT, image_path), mode="rb") as image_file:
                    image_instance.image = File(image_file, name=image_path)
                    image_instance.project_id = model_name + "_" + row["raw_image_path"].split("/")[-1]\
                        .lower().replace(".png", "").replace(".", "_").replace("-", "_")
                    image_instance.save()
            except Exception:
                self.stdout.write(self.style.ERROR(f"Failed to load image: %s" % row["raw_image_path"]))
                raise RuntimeError("Failed to create image instance.")
            try:
                metadata = ImageMetaData()
                metadata.image = image_instance
                metadata.additional_information = json.dumps(row, default=str)
                metadata.save()
            except Exception:
                self.stdout.write(self.style.ERROR(f"Failed to load image metadata from: %s" % row["raw_image_path"]))
                raise RuntimeError("Failed to create image metadata instance")
            self.stdout.write(self.style.SUCCESS(f"Synthetic images added!"))
