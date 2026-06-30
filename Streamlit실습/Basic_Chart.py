
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# 웹사이트 방문자 수 데이터 만들기
dates = [datetime.now() - timedelta(days=x) for x in range(30, 0, -1)]
visitors = np.random.randint(100, 500, 30)

visitor_df = pd.DataFrame({
    'Date': dates,
    'Visitors': visitors
})

st.title('기본 차트 예시')
st.subheader('웹사이트 일일 방문자 수')
st.line_chart(visitor_df.set_index('Date')['Visitors'])


# 도시별 인구 비교
population_data = {
    '서울': 9720000,
    '부산': 3390000,
    '인천': 2950000,
    '대구': 2410000,
    '대전': 1490000
}

population_df = pd.DataFrame(list(population_data.items()), columns=['도시', '인구수'])
st.subheader('주요 도시 인구 비교')
st.bar_chart(population_df.set_index('도시')['인구수'])


# 월별 매출 구성 비교
monthly_data = pd.DataFrame({
    'Date': dates,
    '온라인_매출': np.random.randint(50, 150, 30),
    '오프라인_매출': np.random.randint(80, 200, 30),
    '모바일_매출': np.random.randint(30, 100, 30)
})

st.subheader('채널별 매출 구성 변화')
st.area_chart(monthly_data.set_index('Date'))