# ============================================================
# 2. 시각화 공통 설정
# ============================================================

import pandas as pd
import platform
import matplotlib.pyplot as plt
import seaborn as sns


# generate_data.py에서 만든 CSV 파일 불러오기
df = pd.read_csv(
    "business_data.csv",
    parse_dates=["기준월"]
)

print("데이터 크기:", df.shape)
print(df.head())

system_name = platform.system()
sns.set_theme(style="whitegrid")
if system_name == "Windows":
    plt.rcParams["font.family"] = "Malgun Gothic"
elif system_name == "Darwin":
    plt.rcParams["font.family"] = "AppleGothic"

plt.rcParams["axes.unicode_minus"] = False


# ============================================================
# 3. 과제용 TODO 템플릿
# 아래 함수는 일부러 미완성 상태입니다. TODO를 채운 뒤 호출하세요.
# ============================================================

def assignment_1(data):
    """과제 1: 데이터 품질 점검 + 국가별 핵심 규모 비교."""
    # TODO 1: 컬럼별 결측치 개수와 비율(%)을 표로 만드세요.
    na = data.isnull().sum()

    print(f"{'열':<18}{'결측 수':<12}{'비율':<12}")

    for col in data.columns:
        if na[col] > 0:
            print(
                f"{col:<18}"
                f"{na[col]:<12}"
                f"{na[col] / len(data) * 100:>8.2f}%"
            )

    print("-" * 60)

    # TODO 2: 입출국자수에 IQR 방식의 이상치 플래그를 만드세요.
    def is_outlier(values):
        q1, q3 = values.quantile([0.25, 0.75])
        iqr = q3 - q1
        lo = q1 - 1.5 * iqr
        hi = q3 + 1.5 * iqr

        return (values < lo) | (values > hi)

    out_mask = data.groupby(["국가", "여행구분"])["입출국자수"].transform(is_outlier)
    outliers = data[out_mask]

    print(f"입출국자 수 이상치 후보: {out_mask.sum()}건")
    print(
        outliers[
            ["기준월", "국가", "여행구분", "입출국자수"]
        ].to_string(index=False)
    )

    print("-" * 60)

    # TODO 3: 이상치를 제거하지 않은 원본 기준으로 국가·여행구분별 합계를 구하세요.
    country_summary = (
        data.groupby(["국가", "여행구분"], as_index=False)
        .agg(총입출국자수=("입출국자수", "sum"))
    )

    country_summary = country_summary.sort_values("총입출국자수", ascending=False)

    print("===== 국가별 입출국자 수 합계 =====")
    print(country_summary.to_string(index=False))

    # TODO 4: x=국가, y=입출국자수, hue=여행구분인 막대 차트를 작성하세요.
    fig, ax = plt.subplots(figsize=(13, 5))

    sns.barplot(
        data=country_summary,
        x="국가",
        y="총입출국자수",
        hue="여행구분",
        ax=ax
    )

    ax.set_title("국가별 연간 방한·해외여행객 수")
    ax.tick_params(axis="x", rotation=30)

    fig.tight_layout()
    plt.show()

def assignment_2(data):
    """과제 2: 체류일수와 지출액의 관계 및 비정상 관측치 탐색."""
    # TODO 1: 두 분석 변수의 결측치가 있는 행을 제외하세요.
    plot_data = df.dropna(subset=["평균체류일수","1인당평균지출액"]).copy()
    

    # TODO 2: 색상(hue)은 여행구분, 점 모양(style)은 권역으로 지정하세요.
    plt.figure(figsize=(11, 7))
    sns.scatterplot(
        data=plot_data,
        x="평균체류일수",
        y="1인당평균지출액",
        hue="여행구분",
        style="권역",
        s=80,
        alpha=0.7
    )

    # TODO 3: 전체 및 여행구분별 상관계수를 계산해 비교하세요.
    overall_corr = plot_data[["평균체류일수", "1인당평균지출액"]].corr()

    group_corr = {}
    for name, group in plot_data.groupby("여행구분"):
        corr_table = group[["평균체류일수", "1인당평균지출액"]].corr()
        group_corr[name] = corr_table.loc["평균체류일수", "1인당평균지출액"]

    plt.title("평균 체류일수와 1인당 지출액의 관계")
    plt.tight_layout()
    plt.show()


def assignment_3(data):
    """과제 3: 권역별 1인당 지출의 중앙값·분산·이상치 비교."""
    # TODO 1: 지출액 결측치를 제외한 데이터를 준비하세요.
    plot_data = data.dropna(subset=["1인당평균지출액"])

    # TODO 2: 권역별 표본 수, 중앙값, 평균, 표준편차를 요약하세요.
    region_stats = (
        plot_data.groupby(["권역", "여행구분"], as_index=False)
        .agg(
            표본수=("1인당평균지출액", "count"),
            중앙값=("1인당평균지출액", "median"),
            평균=("1인당평균지출액", "mean"),
            표준편차=("1인당평균지출액", "std"),
        )
    )
    print("===== 권역별 지출액 요약 =====")
    print(region_stats.round(0).to_string(index=False))

    # TODO 3: x=권역, y=1인당평균지출액, hue=여행구분인 Box Plot을 작성하세요.
    plt.figure(figsize=(12, 6))
    sns.boxplot(
        data=plot_data,
        x="권역",
        y="1인당평균지출액",
        hue="여행구분",
        showfliers=True
    )
    plt.tight_layout()
    plt.show()


def assignment_4(data):
    """과제 4: 국가·월별 출국/입국 규모 비율을 피벗 히트맵으로 비교."""
    # TODO 1: 기준월을 월 표시용 문자열(예: 2025-01)로 변환하세요.
    working = data.copy()
    working["월"] = (working["기준월"].dt.to_period("M").astype(str))

    # TODO 2: index=[국가, 월], columns=여행구분, values=입출국자수인 피벗을 만드세요.
    pivot = working.pivot_table(
        index=["국가", "월"],
        columns="여행구분",
        values="입출국자수",
        aggfunc="sum"
    )

    # TODO 3: 국민 해외여행객 / 방한 외래객 비율을 계산하세요.
    # 1보다 크면 해당 국가로 나가는 국민이, 1보다 작으면 해당 국가에서 오는 외래객이 더 많습니다.
    pivot["출국_대비_입국_비율"] = pivot["국민 해외여행객"] / pivot["방한 외래객"]

    # TODO 4: 국가×월 형태로 다시 피벗하고 히트맵을 작성하세요.
    ratio_heatmap = (
        pivot["출국_대비_입국_비율"]
        .reset_index()
        .pivot(index="국가", columns="월", values="출국_대비_입국_비율")
    )
    plt.figure(figsize=(14, 7))
    sns.heatmap(ratio_heatmap, cmap="RdBu_r", center=1, annot=False)
    plt.title("국가·월별 국민 출국자 대비 방한 외래객 비율")
    plt.tight_layout()
    plt.show()

def assignment_2_3d(data):
    """과제 2의 추가 시각화: 체류·지출·관광객 규모 3D 비교"""

    # 세 지표 중 결측치가 있는 행 제외
    plot_data = data.dropna(
        subset=[
            "평균체류일수",
            "1인당평균지출액",
            "입출국자수"
        ]
    ).copy()

    # 그래프의 숫자를 읽기 쉽게 단위 변경
    plot_data["지출액_만원"] = (
        plot_data["1인당평균지출액"] / 10_000
    )

    plot_data["입출국자수_만명"] = (
        plot_data["입출국자수"] / 10_000
    )

    # 3D 그래프 영역 생성
    fig = plt.figure(figsize=(12, 8))

    ax = fig.add_subplot(
        111,
        projection="3d"
    )

    # 여행구분별로 나눠 서로 다른 색상으로 표시
    for name, group in plot_data.groupby("여행구분"):
        ax.scatter(
            group["평균체류일수"],
            group["지출액_만원"],
            group["입출국자수_만명"],
            s=35,
            alpha=0.65,
            label=name
        )

    ax.set_title("체류기간·지출액·관광객 규모 3D 비교")
    ax.set_xlabel("평균 체류일수")
    ax.set_ylabel("1인당 평균 지출액(만원)")
    ax.set_zlabel("입출국자 수(만 명)")
    ax.legend()

    fig.tight_layout()
    plt.show()

if __name__ == "__main__":
    # generate_data.py에서 만든 business_data.csv를 불러와 사용합니다.
    # 과제 함수를 완성한 뒤 아래 주석을 하나씩 해제합니다.

    # assignment_1(df)
    # assignment_2(df)
    # assignment_3(df)
    # assignment_4(df)
    assignment_2_3d(df)