from bs4 import BeautifulSoup
import requests
import time
import pandas as pd

# Fetch the web page
href_data = []
for i in range(1,200):
    url = f"https://opengov.seoul.go.kr/civilappeal/list?page={i}"
    base_detail_url = "https://opengov.seoul.go.kr"
    response = requests.get(url)
    if response.status_code != 200:
            continue
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    for a_tag in soup.find_all("a", href=True):
        if "/civilappeal/" in a_tag['href']:  # URL 패턴 필터링
            full_url = base_detail_url + a_tag['href']
            href_data.append(full_url)
    print("추출된 URL 목록:")
    for url in href_data:
        print(url)
        
print(href_data)

unique_urls = list(set(href_data))

# Step 2: '/civilappeal/' 경로가 포함된 URL 필터링
filtered_urls = [url for url in unique_urls if '/civilappeal/' in url and 'list' not in url]

# Step 3: 데이터프레임으로 저장 (선택적)
df = pd.DataFrame(filtered_urls, columns=['Filtered_URL'])

# Step 4: 결과 확인 및 CSV 저장
df.to_csv("filtered_urls.csv", index=False, encoding="utf-8-sig")
print(df)