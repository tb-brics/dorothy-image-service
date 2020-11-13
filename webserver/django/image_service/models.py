"""Importing models module to create models classes"""
from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
import os
import uuid



class DataSet(models.Model):
    """Class for datasets"""
    name = models.CharField(unique=True, max_length = 1000)
    image_formats = (models.CharField(max_length = 1000, default=""))

    def __str__(self):
        return str(self.name)


class Image(models.Model):
    """Class for images"""
    dataset = models.ForeignKey(DataSet, on_delete=models.CASCADE)
    image = models.ImageField()
    project_id = models.CharField(max_length = 100)


class ImageMetaData(models.Model):
    """Class for the meta data"""
    image = models.OneToOneField(Image,
                                 related_name='metadata',
                                 primary_key=True,
                                 on_delete=models.CASCADE)
    has_tb = models.BooleanField()
    original_report = models.TextField(null=True)
