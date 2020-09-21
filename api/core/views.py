from django.shortcuts import render
from rest_framework import viewsets
from .models import DadosMontgomery
from .serializers import DadosMontgomerySerializer
# Create your views here.

class DadosViewSet(viewsets.ModelViewSet):
    queryset = DadosMontgomery.objects.all()
    serializer_class = DadosMontgomerySerializer
