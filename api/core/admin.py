from django.contrib import admin
from .models import DataSet, Image, ImageMetaData
# Register your models here.

admin.site.register(DataSet)
admin.site.register(Image)
admin.site.register(ImageMetaData)
