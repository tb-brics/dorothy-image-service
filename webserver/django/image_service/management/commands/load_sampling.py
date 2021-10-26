from django.core.management.base import BaseCommand, CommandError
from image_service.models import Image, ImageSampling
import os.path
from optparse import make_option
from datetime import date
import ast


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('txt_file_path', type=str, help='Insert the path for the file which contains the images dictionary')

    def handle(self,*args,**options):

        images_ids = []
        for image in Image.objects.all():
            images_ids.append(image.project_id)

        with open(options['txt_file_path'], 'r') as f:
            contents = f.read()
            images_to_add_dict = ast.literal_eval(contents)
        f.close()

        for key in list(images_to_add_dict.keys()):
            img_id = [s for s in images_ids if images_to_add_dict[key] in s][0]
            image_sampling__obj = ImageSampling(
                image=Image.objects.filter(project_id=img_id)[0],
                insertion_date=str(date.today()),
                rank_position=key)
            image_sampling__obj.save()

        print(f'Added {len(images_to_add_dict)} images to sampling')

