from django.core.management.base import BaseCommand, CommandError
from image_service.models import DataSet, Image, ImageMetaData
from xrayreader.data import Dataset as xrd
from optparse import make_option

class Command(BaseCommand):

    def handle(self, *args, **options):

        china_xrd = xrd(name='china', path="C:/Users/ms-lu/Desktop/Lucca/IC/DQ/ChinaSet_AllFiles")

        dataset = DataSet(
            database=china_xrd.name,
            image_formats=china_xrd.get_data()['data']['images'][0].extension
        )
        dataset.save()
        self.stdout.write(self.style.SUCCESS('Added Dataset!'))

        for index in range(len(china_xrd.get_data()['data']['images'])-1):#quero pegar imagem por imagem
            image = Image(
                dataset = dataset,
                image_path = china_xrd.get_data()['data']['images'][index].path
            )
            image.save()

            image_meta_data = ImageMetaData(
                dataset=dataset,
                image=image,
                has_tb=china_xrd.get_data()['data']['metadata'][index].check_normality,
                original_report=china_xrd.get_data()['data']['metadata'][index].report
            )
            image_meta_data.save()
        self.stdout.write(self.style.SUCCESS(f"Added {len(china_xrd.get_data()['data']['images'])-1} Images!"))
        self.stdout.write(self.style.SUCCESS(f"Added {len(china_xrd.get_data()['data']['images'])-1} Metadatas!"))
