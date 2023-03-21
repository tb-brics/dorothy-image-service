import os

from datetime import date
from csv import DictReader, DictWriter
from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings
from image_service.models import Image, DataSet, ImageMetaData, DatasetCrossValidationFolds
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
    file_exists = os.path.exists(file_path)
    with open(file_path, 'a') as csvfile:
        writer = DictWriter(csvfile, fieldnames=fieldnames, delimiter=',', lineterminator='\n')
        if not file_exists or csvfile.tell() == 0:
            writer.writeheader()
        writer.writerow(value)


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str,
                            help='Path to csv file with synthetic image information')
        parser.add_argument('force_dataset', type=str,
                            help='Load images into this dataset name')
        parser.add_argument('replace_path', type=str, default="/home/brics/public/brics_data/",
                            help='Load images into this dataset name')
        parser.add_argument('build_hash_with', type=str, default="/home/brics/public/brics_data/",
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
            dataset = DataSet.objects.get(name=options["force_dataset"].lower())
        dataset_hash = sha256()
        for row in csv_reader(input_file_path):
            image_path = row.get("image_path", None) or row.get("raw_image_path")
            image_data = {}
            image_path = image_path.replace("//", "/").replace(options["replace_path"], "synthetic/")
            image_data['image_path'] = row.get("image_path", None) or row.get("raw_image_path")
            image_data['dataset_name'] = dataset.name
            image_data['test'] = row['test']
            image_data['sort'] = row['sort']
            image_data['type'] = row['type']
            image_data['dataset_type'] = 'synthetic'
            try:
                image_instance = Image()
                image_instance.dataset = dataset
                if not os.path.exists(os.path.join(settings.MEDIA_ROOT, image_path)):
                    raise FileNotFoundError("file not found in path: %s" % os.path.join(settings.MEDIA_ROOT, image_path))
                with open(os.path.join(settings.MEDIA_ROOT, image_path), mode="rb") as image_file:
                    image_instance.image = File(image_file, name=image_path)
                    hashsha = sha256()
                    image_content = image_file.read()
                    hashsha.update(image_content)
                    image_hash = hashsha.hexdigest().upper()
                    dataset_name = dataset.name.lower().replace('_', '')
                    image_identifier = str(row[options['build_hash_with']]).replace(".", "_").replace("__", "_")
                    image_identifier_hash = sha256()
                    image_identifier_hash.update(image_identifier.encode('utf-8'))
                    image_project_id = f"{dataset_name[:5]}_{image_identifier_hash.hexdigest().upper()[:9]}_{image_hash[:6]}"
                    image_data["project_id"] = image_project_id
                    image_instance.project_id = image_project_id
                    try:
                        if not Image.objects.filter(project_id=image_project_id):
                            image_instance.save()
                            dataset_hash.update(image_content)
                            self.stdout.write(self.style.SUCCESS(f"Synthetic image created: %s" % image_instance.project_id))
                        else:
                            image_instance = None
                            self.stdout.write(self.style.WARNING(f"Duplicated iproject_id: %s" % image_project_id))
                    except Exception as error:
                        image_instance = None
                        self.stdout.write(
                            self.style.WARNING(f"Possible duplicated image. Error: %s" % error.args))
                csv_writer(new_csv_path, image_data)
            except Exception as error:
                image_instance = None
                self.stdout.write(self.style.ERROR(f"Failed to load image: %s. Error: %s" % (image_path, error.args)))
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
                self.stdout.write(self.style.ERROR(f"Failed to load image metadata from: %s" % image_path))
                if not options["ignore_errors"]:
                    raise RuntimeError("Failed to create image metadata instance")

        try:
            dataset.current_state_hash = dataset_hash.hexdigest().upper()
            dataset.save()
        except Exception:
            self.stdout.write(self.style.ERROR(f"Failed to update dataset hash"))
            if not options["ignore_errors"]:
                raise RuntimeError("Failed to update dataset hash")
        try:
            fold = DatasetCrossValidationFolds()
            fold.dataset = dataset
            fold.file_type = "csv"
            with open(new_csv_path, mode="rb") as fold_file:
                fold.file = File(fold_file, name=new_csv_path)
                fold.save()
        except Exception as error:
            self.stdout.write(self.style.ERROR(f"Failed create dataset cross validation file: %s" % error.args))
            if not options["ignore_errors"]:
                raise RuntimeError("Failed create dataset cross validation file")
        self.stdout.write(self.style.SUCCESS(f"Synthetic images added!"))
