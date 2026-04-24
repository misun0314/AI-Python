"""
프로그램 : 반복적인 엑셀 취합 도구
여러 폴더에 흩어진 협력사별 납기 현황 엑셀을 하나로 합치는 코드
"""
import pandas as pd
import glob

# 1. 특정 폴더 내의 모든 엑셀 파일 목록 가져오기
files = glob.glob("납기현황_*.xlsx") # 예: 납기현황_A사.xlsx, 납기현황_B사.xlsx

all_data = []

# 2. 반복문으로 파일 읽어서 리스트에 담기
for file in files:
    df = pd.read_excel(file)
    df['업체명'] = file.split('_')[1].replace('.xlsx', '') # 파일명에서 업체명 추출
    all_data.append(df)

# 3. 하나로 합치고 엑셀로 저장
total_df = pd.concat(all_data, ignore_index=True)
total_df.to_excel("통합_납기현황_리포트.xlsx", index=False)

print("✅ 모든 엑셀 파일이 하나로 합쳐졌습니다!")
