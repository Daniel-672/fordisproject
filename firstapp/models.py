from django.db import models

class Datalist(models.Model):
    name = models.CharField(max_length = 100)
    addr = models.CharField(max_length = 100)
    tel = models.CharField(max_length = 20)
    kind = models.CharField(max_length = 20)
    lat = models.FloatField(default=0.0)
    lng = models.FloatField(default=0.0)
# Create your models here.
