# project to api from xlsx file.

import pandas as pd
import requests
from bs4 import BeautifulSoup
import json

url = "http://openapi.seoul.go.kr:8088/51684b7749623130313230526e78446a/xml/tvCorona19VaccinestatNew/1/100/"
CoronaInfor = {}
req = requests.get(url)
html = req.text
soup = BeautifulSoup(html, "xml")
# data = soup.find_all('item')

attr_to_find_list =['S_VC_DT','FIR_SUB','FIR_INC1', 'FIR_INC', 'FIR_INC_RATE']
for each_attr in attr_to_find_list:
    finded_attr = soup.find_all(each_attr)
    if CoronaInfor.get(each_attr) is None:
        CoronaInfor[each_attr]=[x.text for x in finded_attr]
    else :
        CoronaInfor[each_attr] = CoronaInfor[each_attr] + [x.text for x in finded_attr]
df = pd.DataFrame(CoronaInfor)
print(df)