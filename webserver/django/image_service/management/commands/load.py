from django.core.management.base import BaseCommand, CommandError
from image_service.models import DataSet, Image, ImageMetaData
from xrayreader.data import Dataset as xrd
import os.path
import uuid
from optparse import make_option


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('dataset_name', type=str, help='Insert the name of the dataset you are loading')
        parser.add_argument('folder_path', type=str, help='Insert the path for the datasets folder')


    def handle(self,*args,**options):

        dataset_xrd = xrd(name=options['dataset_name'], path=options['folder_path'])

        images_dict = dataset_xrd.get_data()['data']['images']
        metadatas_dict = dataset_xrd.get_data()['data']['metadata']

        keys=[]
        image_data=[]
        metadata_data=[]
        for key in metadatas_dict:
            keys.append(key)
            image_data.append(images_dict[key])
            metadata_data.append(metadatas_dict[key])

        list_of_formats=[]
        for index in range(len(metadata_data)):
            list_of_formats.append(image_data[index].extension)
        formatos = set(list_of_formats)

        dataset = DataSet(
            name=dataset_xrd.name,
            image_formats=formatos
        )
        dataset.save()
        self.stdout.write(self.style.SUCCESS('Added a new Dataset!'))

        for index in range(len(image_data)):
            #Building the correct path for the images:
            initial_path_splited = str.split(image_data[index].filename,'/')
            essential_parts_of_it = initial_path_splited[2:]
            image_correct_path=""
            for parts in range(len(essential_parts_of_it)):
                image_correct_path = os.path.join(image_correct_path, essential_parts_of_it[parts])

            image_file = Image(
                dataset=dataset,
                image=image_correct_path,
            )
            image_file.save()


            image_meta_data = ImageMetaData(
                image=image_file,
                gender=metadata_data[index].gender,
                age=metadata_data[index].age,
                has_tb=metadata_data[index].check_normality,
                original_report=metadata_data[index].report
            )

            image_meta_data.save()

        self.stdout.write(self.style.SUCCESS(f"Added {len(image_data)} new Images!"))
