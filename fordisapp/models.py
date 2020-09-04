from django.db import models
import os
from django.conf import settings

from uuid import uuid4
from django.utils import timezone

def date_upload_to(instance, filename):
  # upload_to="%Y/%m/%d" 처럼 날짜로 세분화
  #ymd_path = timezone.now().strftime('%Y/%m/%d')
  # 길이 32 인 uuid 값
  #uuid_name = uuid4().hex
  # 확장자 추출
  uuid_name = 'photo/'
  extension = os.path.splitext(filename)[-1].lower()
  # 결합 후 return
  return '/'.join([
    #ymd_path,
    uuid_name + instance.userEmail + extension,
  ])


def report_upload_to(instance, filename):
  # upload_to="%Y/%m/%d" 처럼 날짜로 세분화
  #ymd_path = timezone.now().strftime('%Y/%m/%d')
  # 길이 32 인 uuid 값
  #uuid_name = uuid4().hex
  # 확장자 추출
  uuid_name = 'report/'
  extension = os.path.splitext(filename)[-1].lower()
  # 결합 후 return
  return '/'.join([
    #ymd_path,
    uuid_name + instance.reportPhotoId + extension,
  ])


def get_image_url(self):
    return '%s%s' %(settings.MEDIA_URL, self.image)


class Users(models.Model):
    userEmail = models.EmailField(max_length=30, primary_key=True, verbose_name="이메일(아이디)")
    nickName = models.CharField(max_length=12, verbose_name="닉네임")
    password = models.CharField(max_length=12, verbose_name="비밀번호")
    registerDate = models.DateField(auto_now_add=True, verbose_name="가입시간")
    guardianName = models.CharField(blank=True, max_length=12, verbose_name="보호자명")
    guardianCallNum = models.CharField(blank=True, max_length=12, verbose_name="보호자전화번호")
    guardianBasicMsg = models.CharField(blank=True, max_length=100, verbose_name="보호자기본메세지")
#    photo = models.ImageField(blank=True, height_field=50, width_field=50, upload_to=date_upload_to, null=True)
    photo = models.FileField(blank=True, upload_to=date_upload_to)

def __str__(self):
    return  f"[{self.__class__.__name__}] userEmail={self.userEmail}"


class Article(models.Model):
    awriter = models.ForeignKey('Users', db_column='userEmail', blank=False, null=False, on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    content = models.TextField()
    viewcnt = models.IntegerField(null=True)

    boardType = models.CharField(blank=True, null=True,max_length=2)
    reportPhotoId = models.CharField(max_length=100, blank=True, null=True)
    reportPhoto = models.ImageField(blank=True, null=True, upload_to=report_upload_to)
    reportLong = models.CharField(blank=True, null=True, max_length=20)
    reportLati = models.CharField(blank=True, null=True, max_length=20)
    reportAddress = models.TextField(blank=True, null=True,)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    cwriter = models.ForeignKey('Users', db_column='userEmail', blank=False, null=False, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)


class Comment2(models.Model):
    c2writer = models.ForeignKey('Users', db_column='userEmail', blank=False, null=False, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)


class Qnaboard(models.Model):
    qnawriter = models.ForeignKey('Users', db_column='userEmail', blank=False, null=False, on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    nickName = models.CharField(max_length=20)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    admin_content = models.TextField()