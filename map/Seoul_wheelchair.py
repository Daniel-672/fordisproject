import json, urllib.request
import pandas as pd

apikey = '567a4449796a68703131386c4652425a'

startRow = 1
endRow = 1000
seoul_data = []

url = 'http://openapi.seoul.go.kr:8088/'+apikey+'/json/MgisRapidCharge/'+str(startRow)+'/'+str(endRow)+'/'
data = urllib.request.urlopen(url).read()
output = json.loads(data)
output = output['MgisRapidCharge']
output = output['row']

#print(output[0].keys())
#print(output[0]['COT_ADDR_FULL_OLD'])
#print(output[1].values())

for i in range(0, (len(output))):
    seoul_data.append(output[i]['COT_ADDR_FULL_OLD'])
    seoul_data.append(output[i]['COT_COORD_X'])
    seoul_data.append(output[i]['COT_COORD_Y'])
    seoul_data.append(output[i]['COT_VALUE_04'])
    seoul_data.append(output[i]['COT_TEL_NO'])

# print(seoul_data)

n = 5
result = [seoul_data[i*n:(i+1)*n] for i in range((len(seoul_data) + n-1)//n)]
# print(result)

df = pd.DataFrame(result, columns=['location', 'x', 'y', 'info', 'tel'])
df.to_csv('Seoul_wheelchair.csv', index=False, encoding='utf8')
