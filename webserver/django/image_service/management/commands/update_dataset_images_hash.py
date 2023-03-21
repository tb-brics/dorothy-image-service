from hashlib import sha256

from django.core.management.base import BaseCommand

from image_service.models import Image, DataSet, ImageMetaData


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('dataset_name', type=str,
                            help='Dataset name to update hash')

    def handle(self, *args, **options):
        dataset = DataSet.objects.get(name=options['dataset_name'].lower())
        for image in Image.objects.filter(dataset=dataset).all():
            with open(image.image.path, mode="rb") as image_file:
                hashsha = sha256()
                hashsha.update(image_file.read())
                image_hash = hashsha.hexdigest().upper()
            image_metadata: ImageMetaData = ImageMetaData.objects.filter(image=image).first()
            if image_metadata:
                image_metadata.image_hash = image_hash
                image_metadata.save()
            self.stdout.write(self.style.SUCCESS(f"Image %s hash updated!" % image.project_id))
