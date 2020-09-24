from django.db import models
from . import file_reader

class DataSet(models.Model):
    database = models.CharField(max_length = 50)
    count = models.IntegerField()
    image_formats = models.ManyToManyField('self')

    def __str__(self):
        return self.database

class Image(models.Model):
    dataset = models.ForeignKey(DataSet, on_delete=models.CASCADE,)
    image_path = models.CharField(max_length = 50)

    def __str__(self):
        return self.dataset

class ImageMetaData(models.Model):
    dataset = models.ForeignKey(DataSet, on_delete=models.CASCADE,)
    image = models.ForeignKey(Image, on_delete=models.CASCADE,)
    has_tb = models.BooleanField()
    original_report = models.CharField(max_length = 50)

    def __str__(self):
        return self.image
