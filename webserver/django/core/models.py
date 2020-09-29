from django.db import models


class Formats(models.Model):
    """
    class for defining  image formats available
    """
    formats = models.CharField(max_length=30)

    class Meta:
        ordering = ['formats']

    def __str__(self):
        return self.formats

class DataSet(models.Model):
    """
    
    """
    database = models.CharField("Data base name", max_length = 50)
    count = models.IntegerField() #Deixar de lado por hora
    image_formats = models.ManyToManyField(Formats, verbose_name = 'list of formats')

    def __str__(self):
        return self.database


class Image(models.Model):
    dataset = models.ForeignKey(DataSet, on_delete=models.CASCADE,)
    image_path = models.CharField(max_length = 50)

    def __str__(self):
        return self.dataset #Precisa de alteração

class ImageMetaData(models.Model):
    dataset = models.ForeignKey(DataSet, on_delete=models.CASCADE,)
    image = models.ForeignKey(Image, on_delete=models.CASCADE,)
    has_tb = models.BooleanField()
    original_report = models.CharField(max_length = 50)

    def __str__(self):
        return self.image
