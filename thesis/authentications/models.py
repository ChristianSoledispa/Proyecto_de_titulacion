# from django.db import models
# from djongo import models
from django.db import models


class History(models.Model):
    hasUser = models.BooleanField(default=False)
    email = models.CharField(max_length=70, blank=True, default='')
    userId = models.CharField(max_length=200)
    user_scrapping = models.CharField(max_length=70, default="", blank=True)
    web_scrapping = models.CharField(max_length=200, default="", blank=True)

    # user_search = ArrayField(models.CharField(max_length=100), blank=True, null=True)

class Authentication(models.Model):
    username = models.CharField(max_length=70, blank=True, default='')
    email = models.CharField(max_length=200, blank=False, unique=True)
    password = models.CharField(max_length=200, blank=False)
    is_superuser = models.BooleanField(default=False)




