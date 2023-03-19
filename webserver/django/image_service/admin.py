from django.contrib import admin
from .models import DataSet, Image, ImageMetaData, ImageMetaDataValidation, ImageValidation, Report, ImageSampling, CrossValidationCluster, DatasetCrossValidationFolds ,DataQualityAnnotation
# Register your models here.

admin.site.register(DataSet)
admin.site.register(ImageMetaData)
admin.site.register(Report)
admin.site.register(ImageSampling)
admin.site.register(CrossValidationCluster)
admin.site.register(DataQualityAnnotation)
admin.site.register(ImageValidation)
admin.site.register(ImageMetaDataValidation)
admin.site.register(DatasetCrossValidationFolds)


class ImageAdmin(admin.ModelAdmin):
    model = Image
    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        group_names = [group['name'] for group in request.user.groups.all().values()]

        if "Validators" not in group_names:
            datasets = DataSet.objects.filter(public=True)
            
            return queryset.filter(dataset__in=datasets)
        else:
            return queryset

admin.site.register(Image, ImageAdmin)
