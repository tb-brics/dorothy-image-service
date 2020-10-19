"""Importing models module to create models classes"""
from django.db import models

class DataSet(models.Model):
    """Class for datasets"""
    name = models.CharField(unique=True, max_length = 50)
    image_formats = models.CharField(max_length = 50, default="")

    def __str__(self):
        return str(self.name)


class Image(models.Model):
    """Class for images"""
    dataset = models.ForeignKey(DataSet, on_delete=models.CASCADE,)
    image_path = models.CharField(max_length = 50)

    def __str__(self):
        return str(self.dataset)

class ImageMetaData(models.Model):
    """Class for the meta data"""
    dataset = models.ForeignKey(DataSet, on_delete=models.CASCADE,)
    image = models.ForeignKey(Image, on_delete=models.CASCADE,)
    has_tb = models.BooleanField()
    original_report = models.CharField(max_length = 50, null=True)

    def __str__(self):
        return str(self.image)

class DataBase(models.Model):
    url = models.CharField(max_length = 200)
    image = models.ForeignKey(Image, on_delete=models.CASCADE,)
     
