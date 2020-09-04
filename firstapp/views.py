from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, FileResponse
from .models import Datalist
from fordisapp.models import *

import csv
import math

# 사용자 로긴 체크 후 사용자 정보를 모두 context에 담음
def logincheck(request) :
    context = None
    if 'user' in request.session:
        user = Users.objects.get(userEmail=request.session.get('user'))

        context = {'loginyn':True,
                   'useremail':user.userEmail,
                   'nickname': user.nickName,
                   'photopath': user.photo.url,
                   'guardianName':  user.guardianName,
                   'guardianCallNum': user.guardianCallNum,
                   'guardianBasicMsg': user.guardianBasicMsg
                   }
        return context
    else:
        context = {'loginyn': False}
        return context


def mapping(request):
    maplist = Datalist.objects.all()
    context = {"maplist": maplist}
    context.update(logincheck(request))
    return render(request, "map.html",context)

def pointing(request):
    pin_lat=[]
    pin_lng=[]
    pin_name = []
    pin_addr = []
    pin_tel = []
    pin_kind = []
    points = Datalist.objects.all()
    for data in points:
        pin_lat.append(data.lat)
        pin_lng.append(data.lng)
        pin_name.append(data.name)
        pin_addr.append(data.addr)
        pin_tel.append(data.tel)
        pin_kind.append(data.kind)
    pin = {"pin_lat": pin_lat, "pin_lng": pin_lng,
           "pin_name":pin_name, "pin_addr": pin_addr,
           "pin_tel": pin_tel, "pin_kind": pin_kind}
    return JsonResponse(pin, json_dumps_params={'ensure_ascii':False})


def sahoe(request):
    sahoe_name = []
    sahoe_addr = []
    sahoe_tel = []
    sahoe_lat = []
    sahoe_lng = []
    list = Datalist.objects.filter(kind="장애인지역사회재활시설")
    for data in list:
        sahoe_name.append(data.name)
        sahoe_addr.append(data.addr)
        sahoe_tel.append(data.tel)
        sahoe_lat.append(data.lat)
        sahoe_lng.append(data.lng)
    sahoe = {"sahoe_name": sahoe_name, "sahoe_addr": sahoe_addr, "sahoe_tel": sahoe_tel,
             "sahoe_lat": sahoe_lat, "sahoe_lng": sahoe_lng }
    return JsonResponse(sahoe, json_dumps_params={'ensure_ascii':False})

def geoju(request):
    geoju_name = []
    geoju_addr = []
    geoju_tel = []
    geoju_lat = []
    geoju_lng = []
    list = Datalist.objects.filter(kind="장애인거주시설")
    for data in list:
        geoju_name.append(data.name)
        geoju_addr.append(data.addr)
        geoju_tel.append(data.tel)
        geoju_lat.append(data.lat)
        geoju_lng.append(data.lng)
    geoju = {"geoju_name": geoju_name, "geoju_addr": geoju_addr, "geoju_tel": geoju_tel,
             "geoju_lat": geoju_lat, "geoju_lng": geoju_lng }
    return JsonResponse(geoju, json_dumps_params={'ensure_ascii':False})

def job(request):
    job_name = []
    job_addr = []
    job_tel = []
    job_lat = []
    job_lng = []
    list = Datalist.objects.filter(kind="장애인직업재활시설")
    for data in list:
        job_name.append(data.name)
        job_addr.append(data.addr)
        job_tel.append(data.tel)
        job_lat.append(data.lat)
        job_lng.append(data.lng)
    job = {"job_name": job_name, "job_addr": job_addr, "job_tel": job_tel,
             "job_lat": job_lat, "job_lng": job_lng }
    return JsonResponse(job, json_dumps_params={'ensure_ascii':False})
# Create your views here.
