from django.core.management.base import BaseCommand, CommandError
from image_service.models import DataSet, Image, ImageMetaData
from xrayreader.data import Dataset as xrd
from optparse import make_option

class Command(BaseCommand):

    def handle(self, *args, **options):


        montgomery_xrd = xrd(name='montgomery', path="C:/Users/ms-lu/Desktop/Lucca/IC/DQ/MontgomerySet")

        dataset  = DataSet(
            database=montgomery_xrd.name,
            image_formats= montgomery_xrd.get_data()['data']['images'][0].extension
        )
        dataset.save()
        self.stdout.write(self.style.SUCCESS('Added Dataset!'))


        for index in range(len(montgomery_xrd.get_data()['data']['images'])-1):#quero pegar imagem por imagem
            image = Image(
                dataset = dataset,
                image_path = montgomery_xrd.get_data()['data']['images'][index].path
            )
            image.save()

            image_meta_data = ImageMetaData(
                dataset= dataset,
                image=image,
                has_tb=montgomery_xrd.get_data()['data']['metadata'][index].check_normality,
                original_report=montgomery_xrd.get_data()['data']['metadata'][index].report
            )
            image_meta_data.save()
        self.stdout.write(self.style.SUCCESS(f"Added {len(montgomery_xrd.get_data()['data']['images'])-1} Images!"))
        self.stdout.write(self.style.SUCCESS(f"Added {len(montgomery_xrd.get_data()['data']['images'])-1} Metadatas!"))
