from django.core.management.base import BaseCommand, CommandError
from image_service.models import DataSet, Image, ImageMetaData
from xrayreader.data import Dataset as xrd
import os.path
import uuid
from optparse import make_option


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('dataset name', type=str, help='Insert the name of the dataset you are loading')
        parser.add_argument('folder path', type=str, help='Insert the path for the datasets folder')


    def handle(self,*args,**options):

        dataset_xrd = xrd(name=options['dataset name'], path=options['folder path'])

        image_data = dataset_xrd.get_data()['data']['images']
        metadata_data = dataset_xrd.get_data()['data']['metadata']



        list_of_formats=[]
        for index in range(len(image_data)-1):
            list_of_formats.append(image_data[index].extension)
        formatos = set(list_of_formats)

        dataset = DataSet(
            name=dataset_xrd.name,
            image_formats=formatos
        )
        dataset.save()
        self.stdout.write(self.style.SUCCESS('Added a new Dataset!'))

        for index in range(len(image_data)-1):
            #Building the correct path for the images:
            initial_path_splited = str.split(image_data[index].filename,'/')
            essential_parts_of_it = initial_path_splited[2:]
            image_correct_path=""
            for parts in range(len(essential_parts_of_it)):
                image_correct_path = os.path.join(image_correct_path, essential_parts_of_it[parts])

            #Building the images ids:
            dataset_name = dataset.name.lower().replace('_','')
            image_filename = image_data[index].imagename
            hashcode = uuid.uuid4()
            project_id = f"{dataset_xrd.name[:5]}_{image_filename}_{hashcode}"

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

        self.stdout.write(self.style.SUCCESS(f"Added {len(image_data)-1} new Images!"))
