import pandas as pd
from sklearn.linear_model import LinearRegression

# 1. 엑셀 파일로부터 학습 데이터 불러오기
try:
    # 엑셀 파일을 읽어 df(데이터프레임) 변수에 저장
    df = pd.read_excel("선박데이터_학습용.xlsx")
    print("✅ 데이터를 성공적으로 불러왔습니다.")
    #print(df.head()) # 데이터 상단 5줄 출력하여 확인
except FileNotFoundError:
    print("❌ 파일이 없습니다. '선박데이터_학습용.xlsx' 파일명을 확인해주세요.")

# 2. AI 모델 학습을 위한 입력 데이터(X)와 정답 데이터(y) 분리
# 입력값(X): 길이(L), 폭(B), 깊이(D)
# 결과값(y): 강재중량(Weight)
X = df[['길이(L)', '폭(B)', '깊이(D)']]
y = df['강재중량(Weight)']

# 3. 선형 회귀(Linear Regression) 모델 생성 및 학습
model = LinearRegression()
model.fit(X, y)
print("\n🤖 AI 모델 학습 완료!")

# 4. 새로운 선박 제원을 입력하여 중량 예측하기
# 예: 길이 220m, 폭 35m, 깊이 21m인 선박의 중량은?
#new_ship_specs = [[220, 35, 21]] 
#predicted_weight = model.predict(new_ship_specs)
# 경고를 제거하기 위해 predict 입력도 DataFrame 형태로 변경
new_ship_specs_data = [[220, 35, 21]]
new_ship_specs_df = pd.DataFrame(new_ship_specs_data, columns=X.columns) # X의 컬럼명 사용
predicted_weight = model.predict(new_ship_specs_df)

print("-" * 30)
print(f"🚢 입력 제원: L={new_ship_specs_data[0][0]}, B={new_ship_specs_data[0][1]}, D={new_ship_specs_data[0][2]}")
print(f"⚖️ 예측된 강재 중량: 약 {predicted_weight[0]:.2f} 톤")
print("-" * 30)

# 5. (추가) 예측 결과를 엑셀로 저장하기
# 학습 데이터 뒤에 예측값을 붙여서 확인해보고 싶을 때 사용
df['AI_예측중량'] = model.predict(X)
df.to_excel("선박중량_예측결과_리포트.xlsx", index=False)
print("📊 전체 데이터에 대한 예측 리포트가 저장되었습니다.")
