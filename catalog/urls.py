from django.urls import path,include
from .views import Product
urlpatterns = [
    path('', Product.as_view(),name="product")
   
]



