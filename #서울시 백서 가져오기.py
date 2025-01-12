#서울시 백서 가져오기
import requests
from bs4 import BeautifulSoup
import os
import pandas as pd
df = pd.read_csv('paper_filtered_urls.csv')

# Step 1: 대상 URL 설정
BASE_URL = "https://opengov.seoul.go.kr"  # 기본 URL
save_folder = os.path.join(os.getcwd(), "서울생활백서") 
os.makedirs(save_folder, exist_ok=True)

for i in range(len(df)):
    page_url = df['Filtered_URL'][i]  # 다운로드 버튼이 포함된 페이지 URL

    # Step 2: 페이지 요청 및 파싱
    response = requests.get(page_url)
    if response.status_code != 200:
        print(f"Failed to fetch the page: {response.status_code}")
        exit()

    soup = BeautifulSoup(response.text, "html.parser")

    # Step 3: <a> 태그에서 href 추출
    download_link = soup.find("a", class_="btn btn-download btn-original")
    if not download_link:
        print("Download link not found.")
        continue

    href = download_link.get("href")
    if not href:
        print("No href attribute found in the download link.")
        continue

    # Step 4: 다운로드 링크 생성
    download_url = f"{BASE_URL}{href}"  # 절대 경로 생성
    file_name = href.split("dname=")[-1]  # 파일 이름 추출 (URL에서 dname 파라미터 사용)

    # Step 5: 파일 다운로드
    try:
        file_response = requests.get(download_url, stream=True)
        file_response.raise_for_status()  # HTTP 오류 발생 시 예외 처리

        # 파일 저장
        decoded_name = requests.utils.unquote(file_name)  # URL 인코딩 해제
        save_path = os.path.join(save_folder, decoded_name)
        with open(save_path, "wb") as file:
            for chunk in file_response.iter_content(chunk_size=8192):
                file.write(chunk)

        print(f"File downloaded successfully: {save_path}")
    except Exception as e:
        print(f"Failed to download the file: {e}")
