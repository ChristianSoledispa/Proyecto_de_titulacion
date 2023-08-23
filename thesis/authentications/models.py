# from django.db import models
from djongo import models


class Authentication(models.Model):
    username = models.CharField(max_length=70, blank=True, default='')
    email = models.CharField(max_length=200, blank=False)
    password = models.CharField(max_length=200, blank=False)
    is_superuser = models.BooleanField(default=False)
    
