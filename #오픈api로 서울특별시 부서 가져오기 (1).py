#오픈api로 서울특별시 부서 가져오기
# 출처 : http://data.seoul.go.kr/dataList/OA-2277/A/1/datasetView.do

import requests
import xml.etree.ElementTree as ET
import pandas as pd

BASE_URL = "http://openapi.seoul.go.kr:8088/your_api_code/xml/SeoulOrganizationService"
START_INDEX, END_INDEX = 1,1000 #num1 : 
data = []

while(True):
    
    url = f"{BASE_URL}/{START_INDEX}/{END_INDEX}"
    response = requests.get(url)
    
    # Step 2: XML 파싱, 예외처리
    if response.status_code != 200:
       print(f"Request status code: {response.status_code}")
       break

    try: root = ET.fromstring(response.text)
    except ET.ParseError as e: 
        print(f"Error parsing XML: {e}")
        break

    # Step 3: <row> 데이터 추출
    rows = root.findall(".//row")  # <row> 태그 모두 찾기

    for row in rows:
        mem_nm = row.find("MEM_NM").text if row.find("MEM_NM") is not None else "N/A"
        posit_cd_nm = row.find("POSIT_CD_NM").text if row.find("POSIT_CD_NM") is not None else "N/A"
        offi_tel_num = row.find("OFFI_TEL_NUM").text if row.find("OFFI_TEL_NUM") is not None else "N/A"
        assign_work = row.find("ASSIGN_WORK").text if row.find("ASSIGN_WORK") is not None else "N/A"
        dept_nm = row.find("DEPT_NM").text if row.find("DEPT_NM") is not None else "N/A"
        dept_loc = row.find("DEPT_LOC").text if row.find("DEPT_LOC") is not None else "N/A"
        full_deptname = row.find("FULL_DEPTNAME").text if row.find("FULL_DEPTNAME") is not None else "N/A"
        ordr = row.find("ORDR").text if row.find("ORDR") is not None else "N/A"

        # 데이터 저장
        data.append({
            "MEM_NM": mem_nm,
            "POSIT_CD_NM": posit_cd_nm,
            "OFFI_TEL_NUM": offi_tel_num,
            "ASSIGN_WORK": assign_work,
            "DEPT_NM": dept_nm,
            "DEPT_LOC": dept_loc,
            "FULL_DEPTNAME": full_deptname,
            "ORDR": ordr
        })
    START_INDEX += 1000 
    END_INDEX += 1000

# Step 4: 결과 출력
for item in data:
    print(item)
    
df = pd.DataFrame(data)
print(df)
df.to_csv("서울시_조직도.csv", index=False, encoding="utf-8-sig")
