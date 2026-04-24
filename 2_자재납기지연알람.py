import pandas as pd
from datetime import datetime

# 1. 자재 리스트 불러오기
df = pd.read_excel("자재리스트.xlsx")

# 2. 날짜 형식으로 변환 및 오늘 날짜 설정
df['납기예정일'] = pd.to_datetime(df['납기예정일'])
today = datetime.now()

# 3. 지연된 항목만 필터링 (오늘보다 이전 날짜이면서 미입고인 경우)
delayed = df[(df['납기예정일'] < today) & (df['입고여부'] == 'N')]

# 4. 결과 출력 및 저장
print(f"⚠️ 현재 지연된 자재는 총 {len(delayed)}건입니다.")
delayed.to_excel("긴급_지연자재_명단.xlsx")
