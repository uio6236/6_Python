"""관광청 BI 시각화 실습용 가상 데이터 생성 및 과제 템플릿."""

# ============================================================
# 1. 완전 실행형 데이터 생성 코드
#    - Python 3.11.9
#    - 데이터 생성에는 pandas와 numpy만 사용
#    - 결과: 240행, 8개 컬럼, business_data.csv
# ============================================================

import numpy as np
import pandas as pd


SEED = 20260922
rng = np.random.default_rng(SEED)

country_info = {
    "일본": {"region": "동북아", "inbound": 240_000, "outbound": 210_000, "stay": 4.1, "spend": 1_150_000},
    "중국": {"region": "동북아", "inbound": 180_000, "outbound": 120_000, "stay": 6.5, "spend": 1_650_000},
    "대만": {"region": "동북아", "inbound": 115_000, "outbound": 45_000, "stay": 4.8, "spend": 1_250_000},
    "미국": {"region": "미주", "inbound": 100_000, "outbound": 130_000, "stay": 9.5, "spend": 2_450_000},
    "호주": {"region": "대양주", "inbound": 25_000, "outbound": 42_000, "stay": 10.5, "spend": 2_700_000},
    "베트남": {"region": "동남아", "inbound": 55_000, "outbound": 50_000, "stay": 6.8, "spend": 1_350_000},
    "태국": {"region": "동남아", "inbound": 35_000, "outbound": 65_000, "stay": 5.7, "spend": 1_500_000},
    "필리핀": {"region": "동남아", "inbound": 40_000, "outbound": 35_000, "stay": 7.2, "spend": 1_300_000},
    "말레이시아": {"region": "동남아", "inbound": 30_000, "outbound": 25_000, "stay": 5.5, "spend": 1_450_000},
    "싱가포르": {"region": "동남아", "inbound": 24_000, "outbound": 26_000, "stay": 5.0, "spend": 1_900_000},
}

months = pd.date_range("2025-01-01", periods=12, freq="MS")

# 방학·연휴·봄/가을 관광 성수기를 단순화한 월별 계절성 지수
seasonality = {
    1: 0.93,
    2: 0.98,
    3: 1.05,
    4: 1.10,
    5: 1.08,
    6: 0.96,
    7: 1.12,
    8: 1.16,
    9: 0.97,
    10: 1.11,
    11: 1.02,
    12: 1.13,
}

purpose_options = ["관광/휴양", "업무/출장", "친지 방문", "교육/연수"]
purpose_probability = {
    "방한 외래객": [0.58, 0.23, 0.12, 0.07],
    "국민 해외여행객": [0.69, 0.16, 0.10, 0.05],
}

rows = []

for month in months:
    for country, info in country_info.items():
        for travel_type, base_key in [
            ("방한 외래객", "inbound"),
            ("국민 해외여행객", "outbound"),
        ]:
            # 매월 완만한 회복/성장 추세 + 계절성 + 국가별 자연 변동
            month_index = month.month - 1
            growth = 1 + month_index * (0.006 if travel_type == "방한 외래객" else 0.004)
            noise = rng.normal(loc=1.0, scale=0.075)
            visitor_count = int(max(1_000, info[base_key] * seasonality[month.month] * growth * noise))

            # 출국자는 장거리 여행 시 체류기간과 1인당 지출이 조금 더 높다는 가정
            direction_stay_factor = 1.08 if travel_type == "국민 해외여행객" else 1.0
            direction_spend_factor = 1.12 if travel_type == "국민 해외여행객" else 1.0

            avg_stay_days = round(
                max(1.0, info["stay"] * direction_stay_factor + rng.normal(0, 0.65)),
                1,
            )
            avg_spend = int(
                max(
                    300_000,
                    info["spend"] * direction_spend_factor * rng.normal(1.0, 0.11),
                )
            )

            main_purpose = rng.choice(
                purpose_options,
                p=purpose_probability[travel_type],
            )

            rows.append(
                {
                    "기준월": month,
                    "여행구분": travel_type,
                    "국가": country,
                    "권역": info["region"],
                    "주요목적": main_purpose,
                    "입출국자수": visitor_count,
                    "평균체류일수": avg_stay_days,
                    "1인당평균지출액": avg_spend,
                }
            )

df = pd.DataFrame(rows)

# ------------------------------------------------------------
# 현업형 데이터 품질 이슈 삽입
# ------------------------------------------------------------
# 이상치: 정상 범위와 크게 다른 집계값/지출값 2건씩 삽입
df.loc[[37, 214], "입출국자수"] = (
    df.loc[[37, 214], "입출국자수"] * np.array([5.8, 0.08])
).astype(int)
df.loc[[82, 191], "1인당평균지출액"] = (
    df.loc[[82, 191], "1인당평균지출액"] * np.array([6.5, 0.18])
).astype(int)

# 결측치: 컬럼별 약 3~5% 삽입. 이상치 행과 겹치지 않도록 제외
protected_rows = {37, 214, 82, 191}
candidate_rows = np.array([i for i in df.index if i not in protected_rows])

missing_plan = {
    "주요목적": 8,          # 8 / 240 = 3.3%
    "평균체류일수": 12,    # 12 / 240 = 5.0%
    "1인당평균지출액": 10, # 10 / 240 = 4.2%
}

already_selected = set()
for column, missing_count in missing_plan.items():
    available = np.array([i for i in candidate_rows if i not in already_selected])
    selected = rng.choice(available, size=missing_count, replace=False)
    df.loc[selected, column] = np.nan
    already_selected.update(selected.tolist())

# 날짜형을 YYYY-MM-DD 형태로 CSV에 저장
df.to_csv("business_data.csv", index=False, encoding="utf-8-sig", date_format="%Y-%m-%d")

print("데이터 생성 완료:", df.shape)
print("\n컬럼별 결측치 개수")
print(df.isna().sum())
print("\n미리보기")
print(df.head())