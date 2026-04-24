import pandas as pd
import matplotlib.pyplot as plt

# 한글 폰트 설정 (윈도우 기준)
plt.rc('font', family='Malgun Gothic')

# 1. 엑셀 파일로부터 학습 데이터 불러오기
try:
    # 엑셀 파일을 읽어 df(데이터프레임) 변수에 저장
    df = pd.read_excel("공정데이터.xlsx")
    print("✅ 데이터를 성공적으로 불러왔습니다.")
    #print(df.head()) # 데이터 상단 5줄 출력하여 확인
except FileNotFoundError:
    print("❌ 파일이 없습니다. '공정데이터.xlsx' 파일명을 확인해주세요.")

# 2. 그래프 그리기
plt.figure(figsize=(10, 6))
bars = plt.bar(df['공정단계'], df['실제시간(h)'], color='skyblue')
bars[5].set_color('red') # 가장 오래 걸리는 '탑재' 공정 강조

plt.title("공정별 평균 소요 시간 (Bottleneck 분석)")
plt.ylabel("시간 (Hour)")
plt.show()
