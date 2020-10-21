"""Importing models module to create models classes"""
from django.db import models 
from django.conf import settings
import os

class DataSet(models.Model):
    """Class for datasets"""
    database = models.CharField("Data base name", unique=True, max_length = 50)
    image_formats = models.CharField(max_length = 50, default="")

    def __str__(self):
        return str(self.database)


class Image(models.Model):
    """Class for images"""
    dataset = models.ForeignKey(DataSet, on_delete=models.CASCADE,)
    image_path = models.Field

    def __str__(self):
        return str(self.dataset)

class ImageMetaData(models.Model):
    """Class for the meta data"""
    dataset = models.ForeignKey(DataSet, on_delete=models.CASCADE,)
    image = models.ImageField(upload_to='static/static_dirs/image/')
    has_tb = models.BooleanField()
    original_report = models.CharField(max_length = 50)

    def __str__(self):
        return str(self.image)

