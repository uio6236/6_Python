# ============================================================
# 2026-10-02 데이터 분석 과제
# Titanic : Machine Learning from Disaster
# ============================================================
from pathlib import Path

import pandas as pd
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import seaborn as sns

# titanic.py가 들어 있는 폴더
BASE_DIR = Path(__file__).resolve().parent

# 실수 출력 형식
pd.set_option("display.float_format", "{:.2f}".format)

# 출력할 때 열이 너무 많이 생략되지 않도록 설정
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 160)

# Windows 한글 폰트 설정
plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False

# ============================================================
# 1번
# pandas를 사용하여 train.csv 파일 데이터를 불러와
# DataFrame으로 저장하시오.
# ============================================================
print("\n\n1번")
df = pd.read_csv(BASE_DIR / "train.csv")
print(f"행 열 개수: {df.shape}")

# ============================================================
# 2번
# 저장된 데이터에서 상위 5개 행을 출력하시오.
# ============================================================
print("\n\n2번")
print(f"{df.head()}")

# ============================================================
# 3번
# 각 열의 이름, 결측치 여부, 데이터 타입(dtype)을
# 한 번에 확인하시오.
#
# df.info()를 실행한 후 출력 결과를 바탕으로 다음을 기술하시오.
# - 결측치가 존재하는 열과 결측 개수
# - dtype이 예상과 다르거나 주의가 필요한 열
# ============================================================
print("\n\n3번")
df.info()

# Age 177개, Cabin 687개, Embarked 2개
# Age가 int가 아닌 float64이라 주의

# ============================================================
# 4번
# Age(나이), Fare(요금) 열의
# 평균값, 최솟값, 최댓값을 구하시오.
# ============================================================
print("\n\n4번")
summary = df[["Age", "Fare"]].agg(["mean", "min", "max"])

print(summary.round(2))

# ============================================================
# 5번
# 탑승객 중 생존자와 사망자가 각각 몇 명인지 계산하시오.
#
# 생존자 : Survived = 1
# 사망자 : Survived = 0
# ============================================================
print("\n\n5번")
survived_count = (df["Survived"] == 1).sum()
dead_count = (df["Survived"] == 0).sum()

print(f"생존자: {survived_count}명")
print(f"사망자: {dead_count}명")

# ============================================================
# 6번
# 객실 등급(Pclass)별로 탑승객이 몇 명인지 계산하시오.
# ============================================================
print("\n\n6번")
print(df["Pclass"].value_counts().sort_index())

# ============================================================
# 7번
# 나이가 50세 이상인 탑승객만 추출하여
# 새로운 데이터프레임을 만드시오.
# ============================================================
print("\n\n7번")
age_50_over = df[df["Age"] >= 50].copy()

print(age_50_over)
print(f"50세 이상 승객 데이터프레임 수 확인: {len(age_50_over)}")

# ============================================================
# 8번
# 탑승객을 나이대 기준으로 그룹화하여
# 새로운 열 AgeGroup을 추가한 후 상위 5개 행을 확인하시오.
#
# 나이대 구분 기준
# 0세 이상 ~ 10세 미만  : '아동'
# 10세 이상 ~ 20세 미만 : '10대'
# 20세 이상 ~ 30세 미만 : '20대'
# 30세 이상 ~ 40세 미만 : '30대'
# 40세 이상 ~ 50세 미만 : '40대'
# 50세 이상 ~ 60세 미만 : '50대'
# 60세 이상              : '60대 이상'
# 결측치(NaN)            : '미확인'
#
# pd.cut() 또는 조건식(if-else / np.where)을
# 자유롭게 사용해도 됩니다.
# ============================================================
import numpy as np
print("\n\n8번")
df["AgeGroup"] = np.where(
    df["Age"].isna(), "미확인",
    np.where(df["Age"] < 10, "아동",
    np.where(df["Age"] < 20, "10대",
    np.where(df["Age"] < 30, "20대",
    np.where(df["Age"] < 40, "30대",
    np.where(df["Age"] < 50, "40대",
    np.where(df["Age"] < 60, "50대", "60대 이상")
    ))))))

print(df[["Age", "AgeGroup"]].head())

# ============================================================
# 9번
# 성별(Sex)과 객실 등급(Pclass)을 기준으로 그룹화하여
# 각각의 평균 생존율을 계산하시오.
# ============================================================
print("\n\n9번")
survival_by_sex_class = df.groupby(["Sex", "Pclass"])["Survived"].mean() * 100

print(survival_by_sex_class.round(2))

# ============================================================
# 10번
# 나이대별 평균 생존율을 계산하시오.
#
# 8번에서 생성한 AgeGroup 열을 기준으로 그룹화하여 계산하시오.
# ============================================================
print("\n\n10번")
survival_by_age = df.groupby("AgeGroup")["Survived"].mean() * 100

print(survival_by_age.round(2))

# ============================================================
# 11번
# 각 열에 존재하는 결측치(NaN)의 총 개수와
# 전체 데이터 대비 비율을 계산하여 내림차순으로 출력하시오.
# ============================================================
print("\n\n11번")
missing_count = df.isna().sum()
missing_ratio = missing_count / len(df) * 100

missing_table = pd.DataFrame({
    "결측 개수": missing_count,
    "결측 비율(%)": missing_ratio
})

missing_table = missing_table.sort_values("결측 개수", ascending=False)

print(missing_table.round(2))

# ============================================================
# 12번
# Sex 열의 'male'은 0으로, 'female'은 1로 변경하여
# Gender_Encoded라는 새로운 열을 추가하시오.
#
# map(), replace(), apply() 중 편한 방식을 사용해도 됩니다.
# ============================================================
print("\n\n12번")
df["Gender_Encoded"] = df["Sex"].map({
    "male": 0,
    "female": 1
})

print(df[["Sex", "Gender_Encoded"]].head())

# ============================================================
# 13번
# 탑승지(Embarked)별로 승객이 지불한 요금(Fare)의
# 평균을 계산하시오.
# ============================================================
print("\n\n13번")
fare_by_embarked = df.groupby("Embarked")["Fare"].mean()

print(fare_by_embarked.round(2))

# ============================================================
# 14번
# Pclass를 인덱스로, Sex를 컬럼으로,
# 값으로 Fare의 평균을 사용하여 피벗 테이블을 생성하시오.
# ============================================================
print("\n\n14번")
fare_pivot = df.pivot_table(
    index="Pclass",
    columns="Sex",
    values="Fare",
    aggfunc="mean"
)

print(fare_pivot.round(2))

# ============================================================
# 15번
# SibSp(형제/배우자 수)와 Parch(부모/자녀 수)를 합산하여
# FamilySize 열을 추가하고,
# 이 열의 요약 통계를 확인하시오.
# ============================================================
print("\n\n15번")
df["FamilySize"] = df["SibSp"] + df["Parch"]

print(df["FamilySize"].describe().round(2))

# ============================================================
# 16번
# Name 열에서 호칭(Mr., Mrs., Miss., Master. 등)을
# 정규 표현식 또는 문자열 함수를 사용하여 추출하고
# Title이라는 새로운 열을 생성한 뒤,
# 가장 흔한 5개의 호칭을 출력하시오.
#
# 정규 표현식 예시
# r', ([A-Za-z]+)\.'
#
# 성(Last name) 뒤에 오는 호칭을 추출한다.
# ============================================================
print("\n\n16번")
def get_title(name):
    after_comma = name.split(",")[1]
    title = after_comma.split(".")[0]
    return title.strip()


df["Title"] = df["Name"].map(get_title)

print(df["Title"].value_counts().head(5))

# ============================================================
# 17번
# 16번에서 생성한 Title 열을 기준으로 그룹화하여
# 각 호칭별 다음 정보를 한 번에 계산하시오.
#
# - 승객 수
# - 평균 나이
# - 평균 생존율
#
# groupby().agg()의 Named Aggregation을 활용하면
# 집계 결과 열 이름을 직접 지정할 수 있다.
# ============================================================
print("\n\n17번")
title_summary = df.groupby("Title").agg(
    승객수=("PassengerId", "count"),
    평균나이=("Age", "mean"),
    평균생존율=("Survived", "mean")
)

title_summary["평균생존율"] = title_summary["평균생존율"] * 100

print(title_summary.round(2))

# ============================================================
# 18번
# 생존한 사람과 사망한 사람의 나이(Age) 분포를
# 비교할 수 있도록 시각화하시오.
#
# 히스토그램 또는 KDE(밀도) 플롯 중 하나를 사용하시오.
#
# 그래프에 반드시 포함할 요소
# - 제목 (set_title)
# - x축 라벨 (set_xlabel)
# - y축 라벨 (set_ylabel)
# - 생존/사망 구분 범례 (legend)
#
# 결과를 화면에 출력하지 않고
# 이미지 파일로 저장하시오. (savefig 사용)
# ============================================================
print("\n\n18번")
survived_age = df.loc[df["Survived"] == 1, "Age"].dropna()
dead_age = df.loc[df["Survived"] == 0, "Age"].dropna()

fig, ax = plt.subplots(figsize=(10, 5))

bins = list(range(0, 86, 5))

ax.hist(
    dead_age,
    bins=bins,
    alpha=0.5,
    color="indianred",
    label="사망"
)

ax.hist(
    survived_age,
    bins=bins,
    alpha=0.5,
    color="steelblue",
    label="생존"
)

ax.set_title("생존 여부에 따른 나이 분포")
ax.set_xlabel("나이")
ax.set_ylabel("승객 수")
ax.legend()
fig.tight_layout()
fig.savefig(BASE_DIR / "18_age_distribution.png", dpi=120)
plt.close(fig)

print("18_age_distribution.png 저장 완료")

# ============================================================
# 19번
# 16번에서 추출한 Title과 Pclass를 동시에 고려하여
# 해당 그룹의 나이 중앙값으로 Age 열의 결측치를 대치하시오.
# (원본 데이터프레임에 적용)
#
# 예:
# 'Master' 타이틀을 가진 1등급 승객 그룹의 나이 중앙값으로
# 해당 그룹의 Age 결측치를 채운다.
#
# groupby().transform("median")을 활용하면
# 그룹별 중앙값을 원본과 같은 길이로 얻을 수 있다.
#
# 주의:
# 반드시 16번 완료 후 진행할 것.
# Title 열이 존재해야 그룹 기준으로 사용할 수 있다.
# ============================================================
print("\n\n19번")
before_missing = df["Age"].isna().sum()

group_median = (
    df.groupby(["Title", "Pclass"])["Age"].transform("median")
)

df["Age"] = df["Age"].fillna(group_median)

after_missing = df["Age"].isna().sum()

print(f"처리 전 결측 개수: {before_missing}")
print(f"처리 후 결측 개수: {after_missing}")

# ============================================================
# 20번
# Survived, Pclass, Age, SibSp, Parch, Fare 등의
# 수치형 변수들 간의 상관관계 행렬을 계산하고,
# 그 결과를 히트맵(Heatmap)으로 시각화하시오.
#
# corr() : 상관관계 행렬 계산 함수
#
# 예시:
# sns.heatmap(..., annot=True, cmap="coolwarm", center=0)
#
# 값이 각 셀 안에 표시되도록 작성한다.
#
# 결과를 화면에 출력하지 않고
# 이미지 파일로 저장하시오. (savefig 사용)
# ============================================================
print("\n\n20번")
numeric_columns = ["Survived", "Pclass", "Age", "SibSp", "Parch", "Fare"]
corr = df[numeric_columns].corr()

print(corr.round(2))

fig, ax = plt.subplots(figsize=(9, 7))

sns.heatmap(
    corr,
    annot=True,
    fmt=".2f",
    cmap="coolwarm",
    center=0,
    vmin=-1,
    vmax=1,
    ax=ax
)

ax.set_title("타이타닉 수치형 변수 간 상관관계")
fig.tight_layout()
fig.savefig(BASE_DIR / "20_correlation_heatmap.png", dpi=120)
plt.close(fig)

print("20_correlation_heatmap.png 저장 완료")