# Generated by Django 3.1.8 on 2021-05-28 16:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('image_service', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='image_quality',
        ),
        migrations.RemoveField(
            model_name='report',
            name='reason_low_quality',
        ),
    ]
