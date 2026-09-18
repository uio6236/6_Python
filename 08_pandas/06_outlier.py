"""
    이상치 탐색
"""
# raw-prices.csv 파일을 읽어와서
#       'close' : int64 / float64 -> 콤마가 포함된 것도 변환
#       'date' : datetime64       -> 형식이 섞여있음. 모두 변환.
# 'code','date' 열을 기준으로 중복 제거 (첫번째 데이터를 남김.)
# 위 결과를 df 변수에 저장
import pandas as pd

from utils.config import RAW_PATH, ENCODING, step_path

df = pd.read_csv(RAW_PATH, encoding=ENCODING)
print(df.head())
df.info()

# 숫자 변환
NUM_COLS = ['open', 'high', 'low', 'close', 'volume', 'change', 'changeRate']
for col in NUM_COLS:
    df[col] = pd.to_numeric(
        df[col].astype(str).str.replace(',', '', regex=False),
        errors='coerce'
    )

# 날짜 변환
df['date'] = pd.to_datetime(df['date'], format='mixed')

# 중복 제거
df = df.drop_duplicates(subset=['code', 'date'], keep='first').reset_index(drop=True)

print(len(df))

step1_path = step_path('_step1.pkl')

# 파일로 데이터를 저장 (.pkl)
# df.to_pickle(경로) => 파일로 저장. 반환값 x
# 파일로부터 데이터 읽기 (.pkl)
# pd.read_pickle(경로) => 파일에 저장된 데이터를 DF으로 반환

print(" === 파일로 저장 === ")
df.to_pickle(step1_path)
print(" ----- 저장 완료 ----- ")

print("=" * 60)

print(" === 파일 읽어오기 === ")
df = pd.read_pickle(step1_path)
print(f"파일 불러오기 완료 : {len(df)}행")
print(df.head())
print("=" * 60)

# 이상치 확인하기
print(df['close'].describe().round(0))

# - median : 중앙값
# - mean : 평균

med = df.groupby('code')['close'].transform('median')
# print(med)
print(f"""
    [종목 중앙값과 비교]
    중앙값의 50배 초과 : {(df['close'] > med * 50).sum()}건
    중앙값의 5% 미만: {(df['close'] < med * 0.05).sum()}건
""")