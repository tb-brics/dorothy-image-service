from django.core.files import File as FileWrapper

def _handle_directory(self, directory_path, directory):
    for root, subFolders, files in os.walk(directory_path):
        for filename in files:
            self.cnt_files += 1
            new_file = File(
                 directory=directory, filename=filename,
                 file=os.path.join(root, filename),
                 uploader=self.uploader)
            with open(os.path.join(root, filename), 'r') as f:
                file_wrapper = FileWrapper(f)
                new_file = File(
                    directory=directory, filename=filename,
                    file=file_wrapper,
                    uploader=self.uploader)
                new_file.save()

"""Importing models module to create models classes"""
from django.db import models
from django.conf import settings
import os

class DataSet(models.Model):
    """Class for datasets"""
    name = models.CharField(unique=True, max_length = 10000)
    image_formats = models.CharField(max_length = 10000, default="")

    def __str__(self):
        return str(self.name)


class Image(models.Model):
    """Class for images"""
    dataset = models.ForeignKey(DataSet, on_delete=models.CASCADE,)
    image_path = models.URLField()

    def __str__(self):
        return str(self.dataset)

class ImageMetaData(models.Model):
    """Class for the meta data"""
    dataset = models.ForeignKey(DataSet, on_delete=models.CASCADE,)
    image = models.ImageField(upload_to='static/image_service/image/')
    has_tb = models.BooleanField()
    original_report = models.CharField(max_length = 10000, null=True)

    def __str__(self):
        return str(self.image)
