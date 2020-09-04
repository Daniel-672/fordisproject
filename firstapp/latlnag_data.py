import json
import requests

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

orgAddressList = ['서울 마포구 모래내로1길 20',
               '서울시 중랑구 상봉동 101-1',
                '서울시 중랑구 상봉동 101-2',
                '서울시 중랑구 상봉동 101-3']

test = gotaddress(orgAddressList)

for chk in test:
    print(chk['address'], ',', chk['x'], ',', chk['y'])