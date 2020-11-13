"""Importing models module to create models classes"""
from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
import os
import uuid



class DataSet(models.Model):
    """Class for datasets"""
    name = models.CharField(unique=True, max_length = 1000)
<<<<<<< HEAD
    image_formats = models.CharField(max_length = 1000, default="")
=======
    image_formats = (models.CharField(max_length = 1000, default=""))
>>>>>>> 1c2791c0c03225977edc253fdf3dad7f08a2f160

    def __str__(self):
        return str(self.name)


class Image(models.Model):
    """Class for images"""
    dataset = models.ForeignKey(DataSet, on_delete=models.CASCADE)
    image = models.ImageField()
<<<<<<< HEAD
    project_id = models.Charfield(max_length = 100) 

def save(self, *args, **kwargs):
        dataset_name = self.dataset.name.lower().replace('_','')
        image_filename = os.path.basename(self.image.name).lower().replace('_','')
        hashcode = uuid.uuid4()
        self.project_id = f"{dataset_name[:5]}_{image_filename}_{hashcode}"
        super(Image, self).save(*args, **kwargs)
=======
    project_id = models.CharField(max_length = 100)

>>>>>>> 1c2791c0c03225977edc253fdf3dad7f08a2f160

class ImageMetaData(models.Model):
    """Class for the meta data"""
    image = models.OneToOneField(Image,
                                 related_name='metadata',
                                 primary_key=True,
                                 on_delete=models.CASCADE)
    has_tb = models.BooleanField()
    original_report = models.TextField(null=True)
