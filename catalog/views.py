from django.shortcuts import render

# Create your views here.
from django.views import generic
from .models import Product
from .serializers import ProductSerializer

from rest_framework import generics

class Product(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
