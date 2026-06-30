import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta

# --- 페이지 설정 ---
st.set_page_config(page_title="주식 분석 대시보드", layout="wide", initial_sidebar_state="expanded")

st.title("📊 실시간 주식 분석 대시보드")
st.markdown("yfinance와 Streamlit을 이용한 인터랙티브 주가 분석 도구입니다.")
st.markdown("---")

# --- 사이드바: 조건 설정 ---
st.sidebar.header("🔍 검색 및 설정")

# 티커 입력 (예: 애플 AAPL, 삼성전자 005930.KS)
ticker_symbol = st.sidebar.text_input("주식 티커 입력", value="AAPL").upper()

# 날짜 선택기
default_start = datetime.today() - timedelta(days=365)
start_date = st.sidebar.date_input("시작일", default_start)
end_date = st.sidebar.date_input("종료일", datetime.today())

# 기술적 지표 선택
st.sidebar.subheader("📈 기술적 지표")
show_ma = st.sidebar.checkbox("이동평균선(MA) 표시", value=True)
ma_window1 = st.sidebar.slider("소형 MA 기간", min_value=5, max_value=50, value=20)
ma_window2 = st.sidebar.slider("대형 MA 기간", min_value=20, max_value=200, value=50)

show_rsi = st.sidebar.checkbox("RSI (상대강도지수) 표시", value=False)
rsi_window = st.sidebar.slider("RSI 기간", min_value=5, max_value=30, value=14)

# --- 데이터 불러오기 ---
@st.cache_data(ttl=3600)  # 1시간 동안 데이터 캐싱
def load_data(ticker, start, end):
    stock = yf.Ticker(ticker)
    df = stock.history(start=start, end=end)
    info = stock.info
    return df, info

try:
    df, info = load_data(ticker_symbol, start_date, end_date)
    
    if df.empty:
        st.error("데이터를 가져오지 못했습니다. 티커명이 올바른지 확인해주세요. (예: 미국주식 'AAPL', 한국주식 '005930.KS')")
    else:
        # --- 1. 기업 정보 표시 ---
        st.subheader(f"🏢 {info.get('longName', ticker_symbol)} 기업 정보")
        
        # 주요 지표를 카드 형태로 배치
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("현재가", f"{info.get('currentPrice', 'N/A')} {info.get('currency', '')}")
        with col2:
            st.metric("시가총액", f"{info.get('marketCap', 0):,}")
        with col3:
            st.metric("PER (주가수익비율)", f"{info.get('trailingPE', 'N/A')}")
        with col4:
            st.metric("52주 최고가", f"{info.get('fiftyTwoWeekHigh', 'N/A')} {info.get('currency', '')}")
            
        # 기업 요약 설명 (접고 펼칠 수 있는 Expand 기능 사용)
        with st.expander("📝 기업 개요 보기"):
            st.write(info.get('longBusinessSummary', '정보가 제공되지 않습니다.'))
        
        st.markdown("---")

        # --- 데이터 가공 (기술적 지표 계산) ---
        if show_ma:
            df['MA_Short'] = df['Close'].rolling(window=ma_window1).mean()
            df['MA_Long'] = df['Close'].rolling(window=ma_window2).mean()
            
        if show_rsi:
            delta = df['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=rsi_window).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=rsi_window).mean()
            rs = gain / (loss + 1e-10) # 0으로 나누기 방지
            df['RSI'] = 100 - (100 / (1 + rs))

        # --- 2. 주가 및 거래량 차트 (Plotly 서브플롯) ---
        st.subheader("📈 주가 및 거래량 트렌드")
        
        # 레이아웃 구성: 행 개수 결정 (RSI 선택 여부에 따라 분기)
        if show_rsi:
            fig = make_subplots(rows=3, cols=1, shared_xaxes=True, 
                                vertical_spacing=0.05, 
                                row_heights=[0.5, 0.2, 0.3])
        else:
            fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                                vertical_spacing=0.05, 
                                row_heights=[0.7, 0.3])

        # 2-1. 주가 캔들스틱 차트 (Row 1)
        fig.add_trace(go.Candlestick(
            x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
            name="주가 (Candle)"
        ), row=1, col=1)

        # 이동평균선 추가
        if show_ma:
            fig.add_trace(go.Scatter(x=df.index, y=df['MA_Short'], name=f'{ma_window1}일 MA', line=dict(width=1.5)), row=1, col=1)
            fig.add_trace(go.Scatter(x=df.index, y=df['MA_Long'], name=f'{ma_window2}일 MA', line=dict(width=1.5)), row=1, col=1)

        # 2-2. 거래량 차트 (Row 2)
        fig.add_trace(go.Bar(
            x=df.index, y=df['Volume'], name="거래량", marker_color='orange'
        ), row=2, col=1)

        # 2-3. RSI 차트 (Row 3 - 선택 시)
        if show_rsi:
            fig.add_trace(go.Scatter(x=df.index, y=df['RSI'], name="RSI", line=dict(color='purple')), row=3, col=1)
            # RSI 과매수/과매도 기준선 추가
            fig.add_hline(y=70, line_dash="dash", line_color="red", row=3, col=1)
            fig.add_hline(y=30, line_dash="dash", line_color="green", row=3, col=1)

        # 차트 레이아웃 스타일 업데이트
        fig.update_layout(
            height=700,
            xaxis_rangeslider_visible=False,  # 캔들스틱 하단 기본 슬라이더 숨김
            hovermode='x unified',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        # 차트 출력
        st.plotly_chart(fig, use_container_width=True)

        # --- 3. 데이터 테이블 보기 ---
        with st.expander("📊 원본 데이터 테이블 확인"):
            st.dataframe(df.sort_index(ascending=False))

except Exception as e:
    st.error(f"에러가 발생했습니다: {e}")