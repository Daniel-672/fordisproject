from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, FileResponse
from .models import Map_wc, Map_washroom
from fordisapp.models import *

import csv, json

# wheelchair.csv 파일 불러오기
# with open('Seoul_wheelchair.csv', 'r', encoding='utf-8') as f:
#     dr = csv.DictReader(f)
#     s = pd.DataFrame(dr)
    #print(s)

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


def mymap(request):
    return render(request, 'mapservice.html', logincheck(request))
    #return render(request, "mapservice.html")
    #return render(request, "test.html")

def w_map(request):
    w_map_location = []
    w_map_tel = []
    w_map_x = []
    w_map_y = []
    w_map_info = []
    list = Map_wc.objects.all()
    for data in list:
        w_map_x.append(data.x)
        w_map_y.append(data.y)
        w_map_info.append(data.info)
        w_map_tel.append(data.tel)
        w_map_location.append(data.location)
    w_map = {"w_map_location": w_map_location, "w_map_tel": w_map_tel, "w_map_x": w_map_x,
             "w_map_y": w_map_y, "w_map_info":w_map_info}
    return JsonResponse(w_map, json_dumps_params={'ensure_ascii':False})


def washmap(request):
    washmap_location = []
    washmap_x = []
    washmap_y = []
    list = Map_washroom.objects.all()
    for data in list:
        washmap_location.append(data.location)
        washmap_x.append(data.x)
        washmap_y.append(data.y)
    washmap = {"washmap_location": washmap_location, "washmap_x": washmap_x, "washmap_y": washmap_y}
    return JsonResponse(washmap, json_dumps_params={'ensure_ascii':False})
