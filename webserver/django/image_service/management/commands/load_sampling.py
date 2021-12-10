from django.core.management.base import BaseCommand
from image_service.models import Image, ImageSampling
from datetime import date
import json


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('json_file_path', type=str, help='Insert the path for the file which contains the images dictionary')

    def handle(self,*args,**options):

        images_ids = []
        for image in Image.objects.all():
            images_ids.append(image.project_id)

        f = open(options['json_file_path'],)

        data = json.load(f)

        f.close()

        for key in list(data.keys()):
            img_id = [s for s in images_ids if data[key] in s][0]
            image_sampling__obj = ImageSampling(
                image=Image.objects.filter(project_id=img_id)[0],
                insertion_date=str(date.today()),
                rank_position=int(key))
            image_sampling__obj.save()

        print(f'Added {len(data)} images to sampling')

