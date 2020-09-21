from rest_framework import serializers
from .models import DadosMontgomery

class DadosMontgomerySerializer(serializers.ModelSerializer):
    class Meta:
        model = DadosMontgomery
        fields = ['database', 'count', 'image_formats', 'images', 'dados']
