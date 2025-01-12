from bs4 import BeautifulSoup
import requests
import time
import pandas as pd

# Fetch the web page
'''
title_data = []
for i in range(1,11):
    url = f"https://opengov.seoul.go.kr/civilappeal/list?page={i}"
    response = requests.get(url)

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find("table")  # <table> 태그 찾기
    rows = table.find_all("tr")
    headers = [th.text.strip() for th in rows[0].find_all("th")]

    for row in rows[1:]:
        cols = row.find_all("td")
        title_data.append([col.text.strip() for col in cols])
print(title_data)
'''

# Extract specific elements
url = pd.read_csv('filtered_urls.csv')
data = []
for i in range(len(url)):
    try:
        page_url = url.iloc[i, 0]
        response = requests.get(page_url)
        
        # 페이지가 유효하지 않을 경우 다음으로 이동
        if response.status_code != 200:
            continue
        soup = BeautifulSoup(response.text, "html.parser")
        
        # h3 및 h4 태그 가져오기
        title = soup.find("h3", class_="title-article")
        title = title.text.strip() if title else "N/A"

        # 문서 본문 (h4 태그와 그 하위 내용)
        content_header = soup.find("h4")  # h4 태그 내용
        content_header = content_header.text.strip() if content_header else "N/A"
        
        content_body = soup.find("div", class_="line-all")
        content_body = content_body.text.strip() if content_body else "N/A"
        
        doc_info_table = soup.find("div", class_="comm-view-article print-yes")
        
        doc_info = {}
        if doc_info_table:
            rows = doc_info_table.find_all("div")
            for row in rows:
                try:
                    key, value = row.text.split(":")
                    doc_info[key.strip()] = value.strip()
                except ValueError:
                    continue

        # 데이터 저장
        data.append({
            "Title": title,
            "Content Header": content_header,
            "Content Body": content_body,
            "Document Info": doc_info
        })
    except Exception as e:
        print(f"Error processing {url}: {e}")

# Step 3: DataFrame 생성
df = pd.DataFrame(data)

# Step 4: 결과 출력 및 저장
print(df)
df.to_csv("parsed_data.csv", index=False, encoding="utf-8-sig")