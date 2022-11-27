from django.core.management.base import BaseCommand
from image_service.models import Image, ImageSampling
from datetime import date
import json


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('json_file_path', type=str, help='Insert the path for the file which contains the images dictionary')

    def handle(self, *args, **options):
        with open(options['json_file_path'], 'r') as file:
            ranked_ids = json.load(file)

        for dic in ranked_ids:
            rank_position = dic['rank_position']
            project_id = dic['project_id']

            image_sampling__obj = ImageSampling(
                image=Image.objects.filter(project_id=project_id)[0],
                insertion_date=str(date.today()),
                rank_position=int(rank_position))

            image_sampling__obj.save()

        print(f'Added {len(ranked_ids)} images to sampling')
