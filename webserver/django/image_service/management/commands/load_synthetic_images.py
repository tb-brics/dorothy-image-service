import os

from csv import DictReader, DictWriter
from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings
from image_service.models import Image, DataSet, ImageMetaData
import json
from hashlib import sha256


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


def csv_writer(file_path: str, value: dict) -> None:
    fieldnames = list(value.keys())
    if not os.path.exists(file_path):
        os.mknod(file_path)
    if os.path.getsize(file_path) == 0:
        with open(file_path, 'w', newline='') as csvfile:
            writer = DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow(value)
    else:
        with open(file_path, 'w+') as csvfile:
            writer = DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow(value)


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str,
                            help='Path to csv file with synthetic image information')
        parser.add_argument('ignore_errors', type=bool, default=True,
                            help='')

    def handle(self, *args, **options):
        new_csv_name = options["file_path"].split("/")[-1].replace(".csv", "") + "_project_id_mapping.csv"
        new_csv_path = os.path.join("/".join(options["file_path"].split("/")[:-1]), new_csv_name)
        for row in csv_reader(options["file_path"]):
            try:
                image_instance = Image()
                image_instance.dataset = DataSet.objects.get(name=row["dataset_name"].lower())
                image_path = row["raw_image_path"].replace("//", "/").replace("/home/jodafons/public/brics_data/Shenzhen/", "")
                if not os.path.exists(os.path.join(settings.MEDIA_ROOT, image_path)):
                    raise FileNotFoundError("file not %s found" % os.path.exists(os.path.join(settings.MEDIA_ROOT, image_path)))
                with open(os.path.join(settings.MEDIA_ROOT, image_path), mode="rb") as image_file:
                    image_instance.image = File(image_file, name=image_path)
                    hash = sha256()
                    hash.update(image_file.read())
                    image_hash = hash.hexdigest().upper()
                    path_hash = sha256()
                    path_hash.update("".join(image_path.split("/")[-4:]).encode("utf-8"))
                    image_instance.project_id = f"{str(image_instance.dataset)[:5]}_{image_hash[:6]}_{path_hash.hexdigest().upper()[:16]}"
                    image_instance.save()
                row["dataset_name"] = row["dataset_name"].lower()
                row["project_id"] = image_instance.project_id
                csv_writer(new_csv_path, row)
            except Exception as error:
                image_instance = None
                self.stdout.write(self.style.ERROR(f"Failed to load image: %s. Error: %s" % (row["raw_image_path"], error.args)))
                if not options["ignore_errors"]:
                    raise RuntimeError("Failed to create image instance.")
            try:
                if image_instance is not None:
                    metadata = ImageMetaData()
                    metadata.image = image_instance
                    metadata.additional_information = json.dumps(row, default=str)
                    metadata.save()
            except Exception:
                self.stdout.write(self.style.ERROR(f"Failed to load image metadata from: %s" % row["raw_image_path"]))
                if not options["ignore_errors"]:
                    raise RuntimeError("Failed to create image metadata instance")
        self.stdout.write(self.style.SUCCESS(f"Synthetic images added!"))
