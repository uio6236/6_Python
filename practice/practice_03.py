"""
    실습용 사이트에서
        종목 메뉴 페이지(SSR)의 섹터를 "IT서비스"로 검색한 결과 데이터를 추출

    - 요청 주소: ??
    TODO: 오늘(09/15) 18시까지 이메일로 제출
"""
import requests, json, csv
from bs4 import BeautifulSoup

from config import BASE, TIMEOUT, HEADERS
from parsers import parse_stocks

resp = requests.get(f"{BASE}/stocks", headers=HEADERS, timeout=TIMEOUT)
resp.raise_for_status()    # 응답 코드가 200이 아니면 예외 발생

html = resp.text

soup = BeautifulSoup(html, 'lxml')