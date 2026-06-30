import streamlit as st
import pandas as pd

grade_df = pd.DataFrame(
    {"학기": ["1-1", "1-2", "2-1", "2-2", "3-1", "3-2", "4-1"],
     "평점": [3.8, 4.1, 3.8, 4.1, 4.2, 4.5, 4.3]}
).set_index("학기")

st.title("나의 성적 분석기")
target = st.sidebar.slider("목표 학점", 0.0, 4.5, 4.0)
st.write(f"나의 목표는 {target}점!")
st.write("## 성적표")
st.write(grade_df)
st.bar_chart(grade_df)
st.write("앱이 실행되었습니다!")