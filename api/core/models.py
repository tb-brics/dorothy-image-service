from django.db import models
from . import file_reader


class DadosMontgomery(models.Model):
    def images():
        lista_dados = []
        images_list = []
        for file in file_reader.DataMontgomery:
            lista_dados.append(file)
        for file_index in range(len(lista_dados)):
            images = {'metadata': {'id': file_index, 'filename':str(lista_dados[file_index].filename), 'has_tb':'', 'original_report': str(lista_dados[file_index].report)}}
            images_list.append(images)
        return images_list
    database = 'Montgomery'
    count = len(file_reader.montgomery_general_data_list)#Number of images
    image_formats = ["png"] #list of image_formats
    dados = str(file_reader.montgomery_general_data_list)
    images = images()


    def __str__(self):
        return self.database

class DadosChina(models.Model):
    pass
