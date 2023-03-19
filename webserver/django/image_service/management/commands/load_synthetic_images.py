import os

from datetime import date
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
        with open(file_path, 'w+', newline='') as csvfile:
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
        parser.add_argument('force_dataset', type=str,
                            help='Load images into this dataset name')
        parser.add_argument('ignore_errors', type=bool, default=True,
                            help='')

    def handle(self, *args, **options):
        input_file_path = options["file_path"].replace("//", "/")
        new_csv_name = input_file_path.split("/")[-1].replace(".csv", "") + "_dorothy_generated.csv"
        new_csv_path = os.path.join("/".join(input_file_path.split("/")[:-1]), new_csv_name)
        if not os.path.exists(new_csv_path):
            os.mknod(new_csv_path)
        if not options["force_dataset"].lower() in [obj.name for obj in DataSet.objects.all()]:
            dataset = DataSet()
            dataset.name = options["force_dataset"].lower()
            dataset.public = True
            dataset.synthetic = True
            dataset.last_update = date.today()
            dataset.absolute_path_location = "/".join(input_file_path.split("/")[:-1])
            dataset.current_state_hash = None
            dataset.save()
        else:
            dataset = DataSet.objects.get(name=options["force_dataset"].lower()).first()
        for row in csv_reader(input_file_path):
            try:
                image_instance = Image()
                image_instance.dataset = dataset
                image_path = row["raw_image_path"].replace("//", "/").replace("/home/brics/public/brics_data/", "synthetic/")
                if not os.path.exists(os.path.join(settings.MEDIA_ROOT, image_path)):
                    raise FileNotFoundError("file not %s found" % os.path.exists(os.path.join(settings.MEDIA_ROOT, image_path)))
                with open(os.path.join(settings.MEDIA_ROOT, image_path), mode="rb") as image_file:
                    image_instance.image = File(image_file, name=image_path)
                    hashsha = sha256()
                    hashsha.update(image_file.read())
                    image_hash = hashsha.hexdigest().upper()
                    dataset_name = dataset.name.lower().replace('_', '')
                    image_filename = str(os.path.splitext(os.path.basename(str(image_instance.image)))[0]).replace(".", "_").replace("-",
                                                                                                                           "_")
                    image_project_id = f"{dataset_name[:5]}_{image_filename}_{image_hash[:6]}"
                    image_instance.project_id = image_project_id
                    try:
                        image_instance.save()
                        self.stdout.write(self.style.SUCCESS(f"Synthetic image created: %s" % image_instance.project_id))
                    except Exception as error:
                        image_instance = None
                        self.stdout.write(
                            self.style.WARNING(f"Possible duplicated image. Error: %s" % error.args))
                row["dataset_name"] = dataset.name
                row["project_id"] = image_project_id
                csv_writer(new_csv_path, row)
            except Exception as error:
                image_instance = None
                self.stdout.write(self.style.ERROR(f"Failed to load image: %s. Error: %s" % (row["raw_image_path"], error.args)))
                if not options["ignore_errors"]:
                    raise RuntimeError("Failed to create image instance.")
            try:
                if image_instance is not None:
                    metadata: ImageMetaData = ImageMetaData()
                    metadata.image = image_instance
                    metadata.additional_information = json.dumps(row, default=str)
                    metadata.synthetic = True
                    metadata.image_hash = image_hash
                    metadata.save()
            except Exception:
                self.stdout.write(self.style.ERROR(f"Failed to load image metadata from: %s" % row["raw_image_path"]))
                if not options["ignore_errors"]:
                    raise RuntimeError("Failed to create image metadata instance")
        self.stdout.write(self.style.SUCCESS(f"Synthetic images added!"))
