# coding: utf-8
import sys
import requests
import csv, json
import pandas as pd

def gotaddress(addressList):
    conResult = []
    for add in addressList:
        try:
            result = getLatLng(add)
            match_first = result['documents'][0]['address']
        except:
            match_first = {'x': '999', 'y': '999'}      #주소가 이상하면 999로 셋팅
        context = {'address': add, 'x': float(match_first['x']), 'y': float(match_first['y'])}
        conResult.append(context)

    return (conResult)

def getLatLng(addr):
    url = 'https://dapi.kakao.com/v2/local/search/address.json?query=' + addr
    headers = {"Authorization": "KakaoAK 1af4a3b899028e9720c99fc752d7986c"}
    result = json.loads(str(requests.get(url, headers=headers).text))
    return result

########################## 아래 테스트 ##########################

with open('C:\DJANGOexam\mapservice\map\Seoul_all.csv', 'r', encoding='utf-8') as f:
    dr = csv.DictReader(f)
    s = pd.DataFrame(dr)
    #print(s)

ss = []
for i in range(len(s)):
    st = [s['서울덕수초등학교'][i], s['서울시 중구 퇴계로22길 17'][i], s['02-735-7225'][i]]
    ss.append(st)
#print(ss)mana
#print(s)
orgAddressList = []

for i in range(len(s)):
    mylist = s['서울시 중구 퇴계로22길 17'][i]
    orgAddressList.append(mylist)

#print(len(orgAddressList))
# 'NoneType' object is not subscriptable 에러 제거하는 작업 .sort
orgAddressList.sort()
# temp = orgAddressList[400:1000]
# temp = orgAddressList[1000:1500]
temp = orgAddressList[2000:2555]
#print(temp)

# test1 = gotaddress(temp)
# sys.stdout = open('latlong_washroom.csv','w', encoding='utf-8')
# cnt = 0
# for chk in test1:
#     cnt += 1
#     print(cnt,"," ,chk['address'],",", chk['x'], ',', chk['y'], end='\n', sep=' ')

test1 = gotaddress(temp)
sys.stdout = open('latlong_washroom.csv','a', encoding='utf-8')
cnt = 1100
for chk in test1:
    cnt += 1
    print(cnt,"," ,chk['address'],",", chk['x'], ',', chk['y'], end='\n', sep=' ')