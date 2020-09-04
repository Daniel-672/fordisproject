from django.db import models
import os
from django.conf import settings


class Map_wc(models.Model):
    x = models.FloatField(default=0.0) # 위도
    y = models.FloatField(default=0.0) # 경도
    info = models.CharField(max_length=30)  # 상세정보
    tel = models.CharField(max_length=30) # 전화번호
    location = models.CharField(max_length=40) # 장소명

class Map_washroom(models.Model):
    location = models.CharField(max_length=40) # 장소명
    x = models.FloatField(default=0.0) # 위도
    y = models.FloatField(default=0.0) # 경도