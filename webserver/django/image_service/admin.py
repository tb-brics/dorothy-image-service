from django.contrib import admin
from .models import DataSet, Image, ImageMetaData, Report, ImageSampling, CrossValidationCluster, CrossValidationFold, CrossValidationFolder, CrossValidationFoldimages,DataQualityAnnotation
# Register your models here.

admin.site.register(DataSet)
admin.site.register(Image)
admin.site.register(ImageMetaData)
admin.site.register(Report)
admin.site.register(ImageSampling)
admin.site.register(CrossValidationCluster)
admin.site.register(CrossValidationFolder)
admin.site.register(CrossValidationFold)
admin.site.register(CrossValidationFoldimages)
admin.site.register(DataQualityAnnotation)
