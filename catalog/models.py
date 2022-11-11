from sys import maxsize
from unittest.util import _MAX_LENGTH
from django.db import models
import uuid
# Create your models here.


class Product(models.Model):
    title = models.CharField(max_length=30)
    price = models.IntegerField()


    def __str__(self):
        return self.title