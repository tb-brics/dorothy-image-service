import os
from csv import DictReader
from hashlib import sha256

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand
from image_service.models import Image, DataSet, ImageMetaData


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


def get_china_project_id(images_path: str, image_name: str) -> str:
    image_path = os.path.join(images_path, image_name)
    with open(os.path.join(settings.MEDIA_ROOT, image_path), mode="rb") as image_file:
        hash = sha256()
        hash.update(image_file.read())
        image_hash = hash.hexdigest().upper()
    return f"china_{image_name.replace('.png', '')}_{image_hash[:6]}"


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str,
                            help='Path to csv file with synthetic image information')
        parser.add_argument('china_files_path', type=str, help='Path to china files in imagesrep')
        parser.add_argument('ignore_errors', type=bool, default=True,
                            help='')

    def handle(self, *args, **options):
        for row in csv_reader(options["file_path"]):
            pix2pix_project_id = None
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
                    pix2pix_project_id = f"{str(image_instance.dataset)[:5]}_{image_hash[:6]}_{path_hash.hexdigest().upper()[:16]}"
                china_file_name = "_".join(row["raw_image_path"].split("/")[-1].split(".")[0].split("_")[:3]) + ".png"
                china_project_id = get_china_project_id(options["china_files_path"], china_file_name)
                china_metadata: ImageMetaData = ImageMetaData.objects.get(image__project_id=china_project_id)
                pix2pix_metadata: ImageMetaData = ImageMetaData.objects.get(image__project_id=pix2pix_project_id)
                pix2pix_metadata.gender = china_metadata.gender
                pix2pix_metadata.age = china_metadata.age
                pix2pix_metadata.has_tb = china_metadata.has_tb
                pix2pix_metadata.original_report = china_metadata.original_report
                pix2pix_metadata.synthetic = True if str(row["raw_image_path"]).find("_fake_") >= 0 else False
                pix2pix_metadata.date_exam = china_metadata.date_exam
                pix2pix_metadata.save()
                self.stdout.write(self.style.SUCCESS("Metadata updated"))
            except Exception as error:
                self.stdout.write(self.style.ERROR(f"Failed to update image metadata: %s. Error: %s" % (row["raw_image_path"], error.args)))
                if not options["ignore_errors"]:
                    raise RuntimeError("Failed to update image metadata.")
        self.stdout.write(self.style.SUCCESS(f"Synthetic images metadata updated!"))
