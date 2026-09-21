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
# 구역 2. 누적 관객 상위 5편의 일관객 비교
# ─────────────────────────────────────────────
st.header("구역 2. 일관객 합계 상위 5편 비교")

top5_names = (
    df.groupby("영화명")["일관객"].sum().sort_values(ascending=False).head(5).index
)
top5_df = df[df["영화명"].isin(top5_names)].sort_values("날짜")

fig2 = px.line(
    top5_df,
    x="날짜",
    y="일관객",
    color="영화명",
    markers=True,
    title="기간 내 일관객 합계 상위 5편의 날짜별 일관객 수",
    labels={"날짜": "날짜", "일관객": "일관객 수(명)", "영화명": "영화명"},
)
fig2.update_traces(
    hovertemplate="날짜: %{x|%Y-%m-%d}<br>일관객: %{y:,}명<extra>%{fullData.name}</extra>"
)
fig2.update_layout(hovermode="x unified", legend_title_text="영화명 (클릭해서 켜고 끄기)")

st.plotly_chart(fig2, use_container_width=True)

st.text_area(
    "이 그래프로 알 수 있는 것",
    placeholder="예: 상위 5편은 대부분 개봉 첫 주말에 관객이 집중되고 이후 빠르게 줄어든다.",
    key="insight_2",
)

st.divider()

# ─────────────────────────────────────────────
# 구역 3. 날짜별 전체(10위권) 일관객 합계 추이
# ─────────────────────────────────────────────
st.header("구역 3. 날짜별 전체 일관객 합계 (영역 그래프)")

daily_total = df.groupby("날짜")["일관객"].sum().reset_index()
daily_total = daily_total.sort_values("날짜")

top3_days = daily_total.sort_values("일관객", ascending=False).head(3)

fig3 = px.area(
    daily_total,
    x="날짜",
    y="일관객",
    title="날짜별 박스오피스 10위권 일관객 합계",
    labels={"날짜": "날짜", "일관객": "일관객 합계(명)"},
)
fig3.update_traces(
    hovertemplate="날짜: %{x|%Y-%m-%d}<br>합계: %{y:,}명<extra></extra>"
)
fig3.update_layout(hovermode="x unified")

# 합계가 가장 컸던 3일을 점 + 날짜 라벨로 표시
fig3.add_scatter(
    x=top3_days["날짜"],
    y=top3_days["일관객"],
    mode="markers+text",
    text=top3_days["날짜"].dt.strftime("%Y-%m-%d"),
    textposition="top center",
    marker=dict(size=10, color="red"),
    name="상위 3일",
    hovertemplate="날짜: %{x|%Y-%m-%d}<br>합계: %{y:,}명<extra>상위 3일</extra>",
)

st.plotly_chart(fig3, use_container_width=True)

st.text_area(
    "이 그래프로 알 수 있는 것",
    placeholder="예: 주말이나 연휴, 큰 영화 개봉 시점에 전체 관객 합계가 크게 튀어 오른다.",
    key="insight_3",
)

st.divider()

# ─────────────────────────────────────────────
# 구역 4. 일관객 합계 TOP 10 영화 (가로 막대그래프)
# ─────────────────────────────────────────────
st.header("구역 4. 일관객 합계 TOP 10 영화")

movie_summary = (
    df.groupby("영화명")
    .agg(합계일관객=("일관객", "sum"), 순위권진입일수=("날짜", "count"))
    .reset_index()
)

top10_summary = movie_summary.sort_values("합계일관객", ascending=False).head(10)
# 가로 막대그래프에서 위에서부터 큰 값이 오도록, 그리는 순서는 오름차순으로 뒤집어 줌
top10_summary = top10_summary.sort_values("합계일관객", ascending=True)

fig4 = px.bar(
    top10_summary,
    x="합계일관객",
    y="영화명",
    orientation="h",
    custom_data=["순위권진입일수"],
    title="기간 내 일관객 합계 TOP 10 영화",
    labels={"합계일관객": "일관객 합계(명)", "영화명": "영화명"},
)
fig4.update_traces(
    hovertemplate="영화명: %{y}<br>일관객 합계: %{x:,}명"
    "<br>10위권 진입 일수: %{customdata[0]}일<extra></extra>"
)
fig4.update_layout(yaxis=dict(categoryorder="total ascending"))

st.plotly_chart(fig4, use_container_width=True)

st.text_area(
    "이 그래프로 알 수 있는 것",
    placeholder="예: 총관객이 많은 영화라고 해서 꼭 10위권에 오래 머문 것은 아니다.",
    key="insight_4",
)

st.divider()

# ─────────────────────────────────────────────
# 구역 5. 월 × 요일별 일관객 합계 (히트맵)
# ─────────────────────────────────────────────
st.header("구역 5. 월 × 요일별 일관객 합계 히트맵")

weekday_labels = ["월", "화", "수", "목", "금", "토", "일"]

heat_df = df.copy()
heat_df["월"] = heat_df["날짜"].dt.month
heat_df["요일"] = heat_df["날짜"].dt.weekday.map(dict(enumerate(weekday_labels)))

heat_table = (
    heat_df.groupby(["요일", "월"])["일관객"]
    .sum()
    .reset_index()
    .pivot(index="요일", columns="월", values="일관객")
    .reindex(weekday_labels)
    .sort_index(axis=1)
)
heat_table.columns = [f"{m}월" for m in heat_table.columns]

fig5 = px.imshow(
    heat_table,
    color_continuous_scale="Reds",
    aspect="auto",
    labels=dict(x="월", y="요일", color="일관객 합계"),
    title="월 × 요일별 일관객 합계",
)
fig5.update_traces(
    hovertemplate="월: %{x}<br>요일: %{y}<br>일관객 합계: %{z:,}명<extra></extra>"
)
fig5.update_xaxes(side="bottom")

st.plotly_chart(fig5, use_container_width=True)

st.text_area(
    "이 그래프로 알 수 있는 것",
    placeholder="예: 특정 요일(주말)에 특정 달의 관객 합계가 유독 진하게 나타난다.",
    key="insight_5",
)

st.divider()

# ─────────────────────────────────────────────
# 구역 6. (다음 그래프를 위한 자리)
# ─────────────────────────────────────────────
st.header("구역 6. (다음 그래프 추가 예정)")
st.caption("여기에 새로운 그래프를 계속 추가할 예정입니다.")
