# Generated by Django 3.1 on 2020-10-19 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image_service', '0017_auto_20201014_0939'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
