from django.core.management.base import BaseCommand, CommandError
from image_service.models import DataSet, Image, ImageMetaData
from xrayreader.data import Dataset as xrd
from optparse import make_option


class Command(BaseCommand):


    def handle(self, *args, **options):


        india_xrd = xrd(name='india', path="C:/Users/ms-lu/Desktop/Lucca/IC/DQ/IndianDataSet")

        list_of_formats = []
        for index in range(len(india_xrd.get_data()['data']['images'])-1):
            list_of_formats.append(india_xrd.get_data()['data']['images'][index].extension)

        dataset  = DataSet(
            name=india_xrd.name,
            image_formats= list_of_formats
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
                original_report= india_xrd.get_data()['data']['metadata'][index].report
            )
            image_meta_data.save()
        self.stdout.write(self.style.SUCCESS(f"Added {len(india_xrd.get_data()['data']['images'])-1} Images!"))
        self.stdout.write(self.style.SUCCESS(f"Added {len(india_xrd.get_data()['data']['images'])-1} Metadatas!"))
