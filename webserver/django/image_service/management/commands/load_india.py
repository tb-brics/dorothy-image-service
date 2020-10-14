from django.core.management.base import BaseCommand, CommandError
from image_service.models import DataSet, Image, ImageMetaData
from xrayreader.data import Dataset as xrd
from optparse import make_option

def check_report():
    india_xrd = xrd(name='india', path="C:/Users/ms-lu/Desktop/Lucca/IC/DQ/IndianDataSet")
    for index in range(len(india_xrd.get_data()['data']['images'])-1):
        if india_xrd.get_data()['data']['metadata'][index].report == None:
            return 0

class Command(BaseCommand):


    def handle(self, *args, **options):


        india_xrd = xrd(name='india', path="C:/Users/ms-lu/Desktop/Lucca/IC/DQ/IndianDataSet")

        dataset  = DataSet(
            database=india_xrd.name,
            image_formats= india_xrd.get_data()['data']['images'][0].extension
        )
        dataset.save()
        self.stdout.write(self.style.SUCCESS('Added Dataset!'))


        for index in range(len(india_xrd.get_data()['data']['images'])-1):#quero pegar imagem por imagem
            image = Image(
                dataset = dataset,
                image_path = india_xrd.get_data()['data']['images'][index].path
            )
            image.save()

            image_meta_data = ImageMetaData(
                dataset= dataset,
                image=image,
                has_tb=india_xrd.get_data()['data']['metadata'][index].check_normality,
                original_report= check_report()
            )
            image_meta_data.save()
        self.stdout.write(self.style.SUCCESS(f"Added {len(india_xrd.get_data()['data']['images'])-1} Images!"))
        self.stdout.write(self.style.SUCCESS(f"Added {len(india_xrd.get_data()['data']['images'])-1} Metadatas!"))
