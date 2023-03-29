from django.core.management.base import BaseCommand

from image_service.models import Fold


class Command(BaseCommand):

    def handle(self, *args, **options):
        for x in range(10):
            for y in range(9):
                instance = Fold()
                instance.test = x
                instance.sort = y
                instance.save()
