#조직도 가져오기
from bs4 import BeautifulSoup
import pandas as pd
import requests
import re

#1. 강동구
url = 'https://www.gangdong.go.kr/web/newportal/empSearch/list'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

data = []

#table 데이터 가져오기
while response.status_code == 200:
    # 모든 h4 태그(class="title-green") 가져오기
    titles = soup.find_all("h4", class_="title-green")
    title_texts = [re.sub(r'\s+', ' ', re.sub(r'[\r\n\t]+', ' ', title.text.strip())) for title in titles]  # 각 Title 정리

    # 모든 <div class="table01 table02"> 가져오기
    table_contents = soup.find_all("div", class_="table01 table02")

    # Title과 Table 매칭
    if len(titles) == len(table_contents):  # 제목과 테이블 수가 동일한 경우 매칭
        for title, table_content in zip(title_texts, table_contents):  # Title과 테이블 병렬 처리
            rows = table_content.find("tbody").find_all("tr")  # tbody 내 모든 tr 태그 가져오기
            
            for row in rows:  # 각 tr 태그에서 td 태그 데이터 추출
                cells = row.find_all("td")
                cell_values = [cell.text.strip() for cell in cells]
                data.append({
                    "Title": title,  # 해당 테이블의 Title
                    "Row Data": cell_values  # 각 행의 <td> 데이터
                })
    else:
        print("Warning: Number of titles and tables do not match!")

    break

# 결과 출력
for row_data in data:
    print(row_data)
    
df = pd.DataFrame(data)
print(df)
df.to_csv("강동구_조직도.csv", index=False, encoding="utf-8-sig")