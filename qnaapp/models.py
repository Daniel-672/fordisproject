from django.db import models
from django.conf import settings
import os
# Create your models here.

class Users(models.Model):
    useremail = models.EmailField(max_length=30, primary_key=True, verbose_name="이메일(아이디)")
    username = models.CharField(max_length=12, verbose_name="닉네임")
    password = models.CharField(max_length=12, verbose_name="비밀번호")
    registerDate = models.DateField(auto_now_add=True, verbose_name="가입시간", null=True)

def __str__(self):
    return self.username

class Qnaboard(models.Model):
    qnawriter = models.ForeignKey('Users', db_column='userEmail', blank=False, null=False, on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    nickName = models.CharField(max_length=20)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    admin_content = models.TextField()



