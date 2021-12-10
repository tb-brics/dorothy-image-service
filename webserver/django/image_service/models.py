"""Importing models module to create models classes"""
import hashlib
from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
import datetime
import os
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.conf import settings

class DataSet(models.Model):
    """Class for datasets"""
    name = models.CharField(unique=True, max_length = 100)
    image_formats = models.CharField(max_length = 50, default="")
    @property
    def number_images (self):
        return Image.objects.filter(dataset=self.id).count()


    def __str__(self):
        return str(self.name)


def get_upload_path(instance,filename):
        if not os.path.exists(os.path.join(settings.MEDIA_ROOT,instance.dataset.name)):
            os.mkdir(os.path.join(settings.MEDIA_ROOT,instance.dataset.name))
        return os.path.join(instance.dataset.name,filename)

class Image(models.Model):
    """Class for images"""
    dataset = models.ForeignKey(DataSet, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_upload_path)
    insertion_date = models.DateField(auto_now_add=True ,auto_now=False)
    project_id = models.CharField(max_length = 10000, default="")
    date_acquisition = models.DateField(auto_now_add=True, auto_now=False, blank=True, null=True)

    def __str__(self):
        return self.project_id

    def save(self, *args, **kwargs):
        dataset_name = str(self.dataset).lower().replace('_','')
        image_filename = str(os.path.splitext(os.path.basename(str(self.image)))[0])
        hash = hashlib.sha256()
        hash.update(self.image.read())
        image_hash = hash.hexdigest().upper()
        self.project_id = f"{dataset_name[:5]}_{image_filename}_{image_hash[:6]}"
        super(Image, self).save(*args, **kwargs)


class ImageMetaData(models.Model):
    """Class for the meta data"""

    GENDER_CHOICES = [('M', _('Male')), ('F', _('Female'))]

    image = models.OneToOneField(Image,
                                 related_name='metadata',
                                 primary_key=True,
                                 on_delete=models.CASCADE)
    has_tb = models.BooleanField(null=True)
    original_report = models.TextField(null=True)
    gender = models.CharField(max_length=50, null=True, choices= GENDER_CHOICES)
    age = models.IntegerField(null=True)
    date_exam = models.DateField(auto_now_add=False ,auto_now=False, blank=True, null=True)


class Report(models.Model):
    """Class for the reports"""

    YES_NO_CHOICES = [('Y', _('Yes')), ('N', _('No'))]

    WHY_LOW_QUALITY_CHOICES = [
        ('PoorIns', _('Poor inspiration')),
        ('UnderPen', _('Under-penetrated')),
        ('OverPen', _('Over-penetrated')),
        ('CropCost', _('Costophrenic are cropped')),
        ('CropApices', _('Apices are cropped')),
        ('Art', _('Artifacts jeopardizing interpretation')),
        ('Rotated', _('Rotated')),
    ]

    image = models.ForeignKey(Image, on_delete=models.PROTECT, verbose_name=_('X-Ray image'))

    #Radiologist information
    performed_by = models.CharField(max_length = 100, null=False, blank=False,verbose_name=_('Radiologist ID'))
    date_added = models.DateTimeField(auto_now_add=False, verbose_name=_('Date of CXR evaluation'))

    report_version = models.PositiveSmallIntegerField(verbose_name=_('Report version'))
    report_content = JSONField(verbose_name=_('Report content'))


class ImageSampling(models.Model):
    """class for the image sampling"""
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    insertion_date = models.DateField(auto_now_add=False, auto_now=False)
    rank_position = models.IntegerField(null=True)
