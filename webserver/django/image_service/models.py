"""Importing models module to create models classes"""
from django.db import models
from django.conf import settings
import os
import uuid


class DataSet(models.Model):
    """Class for datasets"""
    name = models.CharField(unique=True, max_length = 10000)
    image_formats = models.CharField(max_length = 10000, default="")

    def __str__(self):
        return str(self.name)


class Image(models.Model):
    """Class for images"""
    dataset = models.ForeignKey(DataSet, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='static/image_service/image/')

    
    def save(self, *args, **kwargs):
        dataset_name = self.dataset.name.tolower().replace('_','')
        image_filename = os.path.basename(self.image.name).tolower().replace('_','')
        hashcode = uuid.uuid4()
        self.project_id = f"{self.name'_'self.image_formats'}
        super(Image, self).save(*args, **kwargs)


   


class ImageMetaData(models.Model):
    """Class for the meta data"""
<<<<<<< HEAD
    dataset = models.ForeignKey(DataSet, on_delete=models.CASCADE,)
    image = models.ImageField(upload_to='static/imageservice/image/')
    image = models.OneToOneField(Image,
                                 related_name='metadata',
                                 primary_key=True,
                                 on_delete=models.CASCADE)

