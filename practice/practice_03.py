"""
    실습용 사이트에서
        종목 메뉴 페이지(SSR)의 섹터를 "IT서비스"로 검색한 결과 데이터를 추출

    - 요청 주소:
      https://kh-lab.rockua.ai.kr/stocks?sector=S08
"""

import requests

from config import BASE, TIMEOUT, HEADERS
from parsers import parse_stocks

params = {"sector": "S08"}
resp = requests.get(
    f"{BASE}/stocks",
    params=params,
    headers=HEADERS,
    timeout=TIMEOUT
)

resp.raise_for_status()
print(f"요청 주소: {resp.url}")
print(f"응답 코드: {resp.status_code}")
print("=" * 80)

stocks = parse_stocks(resp.text)

print(f"추출된 종목 수: {len(stocks)}개")
print("=" * 80)

print(
    f"{'코드':<8}"
    f"{'종목명':<16}"
    f"{'섹터':<12}"
    f"{'현재가':>12}"
    f"{'등락률':>10}"
    f"{'거래량':>14}"
    f"{'시장':>12}"
)

for stock in stocks:
    print(
        f"{stock['code']:<8}"
        f"{stock['name']:<16}"
        f"{stock['sector']:<12}"
        f"{stock['price']:>12,}"
        f"{stock['rate']:>10}"
        f"{stock['volume']:>14,}"
        f"{stock['market']:>12}"
    )