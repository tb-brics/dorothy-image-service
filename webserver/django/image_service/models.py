"""Importing models module to create models classes"""
import hashlib
import os
from datetime import date

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models import JSONField
from django.conf import settings


class DataSet(models.Model):
    """Class for datasets"""
    name = models.CharField(unique=True, max_length=100)
    image_formats = models.CharField(max_length=50, default="")
    public = models.BooleanField(default=True)
    synthetic = models.BooleanField(default=False)
    absolute_path_location = models.CharField(max_length=2000, default=None, null=True)
    last_update = models.DateField(default=date.today)
    current_state_hash = models.CharField(max_length=500, default=None, null=True)

    @property
    def number_images(self):
        return Image.objects.filter(dataset=self.id).count()

    def __str__(self):
        return str(self.name)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.last_update = date.today()
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)


def get_upload_path(instance, filename):
    if not os.path.exists(os.path.join(settings.MEDIA_ROOT, instance.dataset.name)):
        os.mkdir(os.path.join(settings.MEDIA_ROOT, instance.dataset.name))
    return os.path.join(os.path.join(settings.MEDIA_ROOT, instance.dataset.name), filename)


def get_cluster_upload_path(instance, filename):
    directory_path = os.path.join(settings.MEDIA_ROOT, "clusters")
    if not os.path.exists(directory_path):
        os.mkdir(directory_path)
    return os.path.join(directory_path, filename)


class Image(models.Model):
    """Class for images"""
    dataset = models.ForeignKey(DataSet, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_upload_path, max_length=500)
    insertion_date = models.DateField(auto_now_add=True, auto_now=False)
    project_id = models.CharField(max_length=10000, unique=True)
    date_acquisition = models.DateField(auto_now_add=True, auto_now=False, blank=True, null=True)

    def __str__(self):
        return self.project_id

    def save(self, *args, **kwargs):
        if not self.project_id:
            dataset_name = str(self.dataset).lower().replace('_', '')
            image_filename = str(os.path.splitext(os.path.basename(str(self.image)))[0]).replace(".", "_").replace("-", "_")
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
    gender = models.CharField(max_length=50, null=True, choices=GENDER_CHOICES)
    age = models.IntegerField(null=True)
    date_exam = models.DateField(auto_now_add=False, auto_now=False, blank=True, null=True)
    synthetic = models.BooleanField(default=False)
    image_hash = models.CharField(max_length=500, null=True, default=None)
    additional_information = JSONField(null=True)


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

    # Radiologist information
    performed_by = models.CharField(max_length=100, null=False, blank=False, verbose_name=_('Radiologist ID'))
    date_added = models.DateTimeField(auto_now_add=False, verbose_name=_('Date of CXR evaluation'))

    report_version = models.PositiveSmallIntegerField(verbose_name=_('Report version'))
    report_content = JSONField(verbose_name=_('Report content'))


class ImageSampling(models.Model):
    """class for the image sampling"""
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    insertion_date = models.DateField(auto_now_add=False, auto_now=False)
    rank_position = models.IntegerField(null=True)


class CrossValidationCluster(models.Model):
    cluster_id = models.CharField(max_length=20, unique=True)
    dataset = models.ForeignKey(DataSet, on_delete=models.CASCADE)
    file = models.FileField(upload_to=get_cluster_upload_path, default=None)

    def __str__(self):
        return self.cluster_id

    def save(self, *args, **kwargs):
        self.file.name = f"{self.cluster_id}"
        super(CrossValidationCluster, self).save(*args, **kwargs)


class CrossValidationFolder(models.Model):
    folder_id = models.CharField(max_length=30, unique=True)
    cluster_id = models.ForeignKey(CrossValidationCluster, to_field='cluster_id', db_column='cluster_id',
                                   on_delete=models.CASCADE)


class CrossValidationFold(models.Model):
    fold_id = models.CharField(max_length=50, unique=True)
    folder_id = models.ForeignKey(CrossValidationFolder, to_field='folder_id', db_column='folder_id', on_delete=models.CASCADE)


class CrossValidationFoldimages(models.Model):
    fold_id = models.ForeignKey(CrossValidationFold, to_field='fold_id', db_column='fold_id', on_delete=models.CASCADE)
    project_id = models.ForeignKey(Image, to_field='project_id', db_column='project_id', on_delete=models.CASCADE)
    train = models.BooleanField(default=False)
    test = models.BooleanField(default=False)
    validation = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['project_id', 'fold_id'], name='cross_validation_fold_image_unique')
        ]


class DataQualityAnnotation(models.Model):
    project_id = models.ForeignKey(Image, to_field="project_id", db_column='project_id', on_delete=models.CASCADE)
    under_penetrated = models.BooleanField(null=True)
    over_penetrated = models.BooleanField(null=True)
    costophrenic_cropped = models.BooleanField(null=True)
    apices_cropped = models.BooleanField(null=True)
    insertion_date = models.DateField(auto_now_add=True, auto_now=False)
    reliable_radiography = models.BooleanField(null=True)
    minimum_interpretation_quality = models.BooleanField(null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['project_id'], name='data_quality_annotation_unique')
        ]


class ImageValidation(models.Model):
    dataset = models.ForeignKey(DataSet, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_upload_path)
    insertion_date = models.DateField(auto_now_add=True, auto_now=False)
    project_id = models.CharField(max_length=10000, unique=True)
    date_acquisition = models.DateField(auto_now_add=True, auto_now=False, blank=True, null=True)

    def __str__(self):
        return self.project_id

    def save(self, *args, **kwargs):
        dataset_name = str(self.dataset).lower().replace('_', '')
        image_filename = str(os.path.splitext(os.path.basename(str(self.image)))[0])
        hash = hashlib.sha256()
        hash.update(self.image.read())
        image_hash = hash.hexdigest().upper()
        self.project_id = f"{dataset_name[:5]}_{image_filename}_{image_hash[:6]}"
        super(ImageValidation, self).save(*args, **kwargs)


class ImageMetaDataValidation(models.Model):
    """Class for the meta data"""

    GENDER_CHOICES = [('M', _('Male')), ('F', _('Female'))]

    image = models.OneToOneField(ImageValidation,
                                 related_name='metadata',
                                 primary_key=True,
                                 on_delete=models.CASCADE)
    has_tb = models.BooleanField(null=True)
    original_report = models.TextField(null=True)
    gender = models.CharField(max_length=50, null=True, choices=GENDER_CHOICES)
    age = models.IntegerField(null=True)
    date_exam = models.DateField(auto_now_add=False, auto_now=False, blank=True, null=True)
    synthetic = models.BooleanField(default=False)
    additional_information = JSONField(null=True)
