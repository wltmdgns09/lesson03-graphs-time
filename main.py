import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="영화 데이터 그래프 도감 1 - 시간", layout="wide")
st.title("영화 데이터 그래프 도감 1 - 시간")

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)
    # 날짜 열(예: 20230101)을 실제 날짜 타입으로 변환
    df["날짜"] = pd.to_datetime(df["날짜"], format="%Y%m%d")
    return df


df = load_data()

st.divider()

# ─────────────────────────────────────────────
# 구역 1. 영화별 일관객 수 변화 (선 그래프)
# ─────────────────────────────────────────────
st.header("구역 1. 영화별 일관객 수 변화")

movie_list = sorted(df["영화명"].unique())
selected_movie = st.selectbox("영화를 선택하세요", movie_list, key="movie_select_1")

movie_df = df[df["영화명"] == selected_movie].sort_values("날짜")

fig1 = px.line(
    movie_df,
    x="날짜",
    y="일관객",
    markers=True,
    title=f"'{selected_movie}' 날짜별 일관객 수 변화",
    labels={"날짜": "날짜", "일관객": "일관객 수(명)"},
)
fig1.update_traces(
    hovertemplate="날짜: %{x|%Y-%m-%d}<br>일관객: %{y:,}명<extra></extra>"
)
fig1.update_layout(hovermode="x unified")

st.plotly_chart(fig1, use_container_width=True)

st.text_area(
    "이 그래프로 알 수 있는 것",
    placeholder="예: 개봉 초반 관객 수가 급증했다가 이후 점차 감소하는 추세를 보인다.",
    key="insight_1",
)

st.divider()

# ─────────────────────────────────────────────
# 구역 2. (다음 그래프를 위한 자리)
# ─────────────────────────────────────────────
st.header("구역 2. (다음 그래프 추가 예정)")
st.caption("여기에 새로운 그래프를 계속 추가할 예정입니다.")
