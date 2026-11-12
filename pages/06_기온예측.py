
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from pathlib import Path

# ---------------------------------
# 1. 페이지 설정
# ---------------------------------
st.set_page_config(
    page_title="월별 평균기온 예측",
    page_icon="🌡️",
    layout="wide"
)

st.title("🌡️ 월별 평균기온 예측 프로그램")
st.write("선형회귀 알고리즘을 이용하여 미래의 평균기온을 예측해 봅시다.")

st.divider()

# ---------------------------------
# 2. CSV 파일 불러오기
# ---------------------------------
# 현재 파일은 pages 폴더에 있고
# CSV 파일은 프로젝트 상위 폴더에 있음

BASE_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = BASE_DIR / "temperature.csv"

try:
    df = pd.read_csv(CSV_PATH, encoding="cp949")

except FileNotFoundError:
    st.error("temperature.csv 파일을 찾을 수 없습니다.")
    st.info("GitHub 저장소의 최상위 폴더에 temperature.csv 파일을 업로드해 주세요.")
    st.stop()

except Exception as e:
    st.error(f"CSV 파일을 읽는 중 오류가 발생했습니다: {e}")
    st.stop()

# ---------------------------------
# 3. 데이터 전처리
# ---------------------------------

# 날짜를 날짜 형식으로 변환
df["날짜"] = pd.to_datetime(
    df["일시"],
    format="%b-%y",
    errors="coerce"
)

# 연도와 월 추출
df["연도"] = df["날짜"].dt.year
df["월"] = df["날짜"].dt.month

# 평균기온 숫자 변환
df["평균기온(℃)"] = pd.to_numeric(
    df["평균기온(℃)"],
    errors="coerce"
)

# 필요한 데이터만 추출하고 결측치 제거
df = df.dropna(
    subset=["연도", "월", "평균기온(℃)"]
)

df["연도"] = df["연도"].astype(int)
df["월"] = df["월"].astype(int)

# ---------------------------------
# 4. 사용자 입력
# ---------------------------------

st.subheader("📌 예측 조건 선택")

col1, col2 = st.columns(2)

with col1:
    selected_month = st.selectbox(
        "예측할 월을 선택하세요.",
        list(range(1, 13)),
        index=0,
        format_func=lambda x: f"{x}월"
    )

with col2:
    min_year = int(df["연도"].min())
    max_year = int(df["연도"].max())

    predict_year = st.number_input(
        "예측할 연도를 입력하세요.",
        min_value=min_year,
        max_value=2100,
        value=max(max_year + 4, 2030),
        step=1
    )

# ---------------------------------
# 5. 선택한 월의 데이터 추출
# ---------------------------------

month_data = df[
    df["월"] == selected_month
].copy()

month_data = month_data.sort_values("연도")

if len(month_data) < 2:
    st.error("선형회귀를 계산하기 위한 데이터가 부족합니다.")
    st.stop()

# 독립변수 X : 연도
# 종속변수 y : 평균기온

X = month_data["연도"].values
y = month_data["평균기온(℃)"].values

# ---------------------------------
# 6. 선형회귀 알고리즘
# ---------------------------------

# 1차 다항식의 계수 계산
# 기울기와 절편을 구함

slope, intercept = np.polyfit(X, y, 1)

# 예측 기온 계산
predicted_temp = slope * predict_year + intercept

# 기존 데이터의 회귀선 예측값
regression_values = slope * X + intercept

# 결정계수 R² 계산
ss_total = np.sum((y - np.mean(y)) ** 2)
ss_residual = np.sum((y - regression_values) ** 2)

if ss_total == 0:
    r2 = 0
else:
    r2 = 1 - (ss_residual / ss_total)

# ---------------------------------
# 7. 예측 결과 표시
# ---------------------------------

st.divider()
st.subheader(f"📊 {selected_month}월 평균기온 분석 및 예측")

result1, result2, result3 = st.columns(3)

result1.metric(
    "예측 연도",
    f"{predict_year}년"
)

result2.metric(
    "예측 평균기온",
    f"{predicted_temp:.1f} ℃"
)

result3.metric(
    "결정계수 (R²)",
    f"{r2:.3f}"
)

st.caption(
    f"{selected_month}월의 {min_year}년부터 {max_year}년까지의 "
    f"실제 평균기온 {len(month_data)}개를 학습에 사용했습니다."
)

# ---------------------------------
# 8. 그래프 작성
# ---------------------------------

fig = go.Figure()

# 실제 관측 데이터
fig.add_trace(
    go.Scatter(
        x=X,
        y=y,
        mode="markers",
        name="실제 평균기온",
        marker=dict(
            color="royalblue",
            size=10,
            line=dict(width=1, color="white")
        ),
        hovertemplate=
        "%{x}년<br>실제 평균기온: %{y:.1f}℃<extra></extra>"
    )
)

# 회귀선의 시작과 끝
line_start = min(min_year, predict_year)
line_end = max(max_year, predict_year)

line_x = np.linspace(line_start, line_end, 200)
line_y = slope * line_x + intercept

# 선형회귀 추세선
fig.add_trace(
    go.Scatter(
        x=line_x,
        y=line_y,
        mode="lines",
        name="선형회귀 추세선",
        line=dict(
            color="red",
            width=3
        ),
        hovertemplate=
        "연도: %{x:.1f}<br>회귀 예측값: %{y:.2f}℃<extra></extra>"
    )
)

# 예측 기온
fig.add_trace(
    go.Scatter(
        x=[predict_year],
        y=[predicted_temp],
        mode="markers+text",
        name="미래 예측 기온",
        marker=dict(
            color="green",
            size=18,
            symbol="star"
        ),
        text=[f"{predicted_temp:.1f}℃"],
        textposition="top center",
        textfont=dict(
            size=14,
            color="green"
        ),
        hovertemplate=
        "%{x}년<br>예측 평균기온: %{y:.1f}℃<extra></extra>"
    )
)

# 예측연도 위치 표시
fig.add_vline(
    x=predict_year,
    line_dash="dash",
    line_color="green",
    opacity=0.6
)

fig.update_layout(
    title=dict(
        text=f"{selected_month}월 평균기온 선형회귀 예측",
        x=0.5
    ),
    xaxis_title="연도",
    yaxis_title="평균기온 (℃)",
    hovermode="x unified",
    template="plotly_white",
    height=550,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="center",
        x=0.5
    )
)

fig.update_xaxes(
    dtick=2,
    showgrid=True
)

fig.update_yaxes(
    showgrid=True,
    ticksuffix="℃"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ---------------------------------
# 9. 선형회귀 알고리즘 설명
# ---------------------------------

st.divider()

st.subheader("🧠 선형회귀 알고리즘이란?")

st.write("""
선형회귀는 여러 데이터 사이의 관계를 분석하여
가장 적합한 직선을 찾고, 그 직선을 이용해 새로운 값을 예측하는 알고리즘입니다.
""")

st.markdown("#### ① 실제 데이터 수집")

st.write("""
파란색 점은 temperature.csv에 기록된 실제 평균기온입니다.

예를 들어 1월을 선택하면 여러 해의 1월 평균기온이
각각 하나의 점으로 그래프에 표시됩니다.
""")

st.markdown("#### ② 가장 적합한 직선 찾기")

st.write("""
빨간색 직선은 선형회귀 알고리즘이 계산한 추세선입니다.

알고리즘은 실제 데이터 점과 직선 사이의 세로 방향 차이(오차)를
제곱하여 모두 더한 값이 가장 작아지도록 기울기와 절편을 계산합니다.

즉, 실제 데이터의 전체적인 흐름을 가장 잘 설명하는 직선을 찾습니다.
""")

st.markdown("#### ③ 미래 기온 예측하기")

st.write("""
사용자가 입력한 예측연도를 빨간색 직선에 대입하면
그 위치에 해당하는 기온을 계산할 수 있습니다.

그래프의 초록색 별표가 바로 선형회귀 알고리즘이 예측한 기온입니다.
""")

st.markdown("#### ④ 선형회귀의 수학적 원리")

st.latex(r"y = ax + b")

st.write("""
- x : 연도
- y : 예측 평균기온
- a : 기울기 (연도에 따라 기온이 얼마나 변하는지)
- b : 절편 (직선이 세로축과 만나는 값)

기울기가 양수이면 시간이 지날수록 기온이 상승하는 경향이고,
음수이면 하락하는 경향입니다.
""")

st.markdown("#### ⑤ 이번 프로그램의 실제 계산식")

st.latex(
    rf"y = {slope:.4f}x + ({intercept:.2f})"
)

st.write(
    f"위 계산식에 {predict_year}을 대입하면 "
    f"예측 평균기온은 **{predicted_temp:.2f}℃**입니다."
)

st.info(
    "주의: 선형회귀는 과거 데이터의 추세가 미래에도 이어진다고 가정합니다. "
    "실제 기온은 기후변화, 기상 현상 등 다양한 요인의 영향을 받으므로 "
    "이 결과는 실제 기온을 보장하는 예보가 아니라 통계적 예측값입니다."
)

# ---------------------------------
# 10. 실제 데이터 확인
# ---------------------------------

with st.expander("📋 학습에 사용된 실제 데이터 확인하기"):
    display_df = month_data[["연도", "평균기온(℃)"]].copy()
    st.dataframe(
        display_df.sort_values("연도"),
        use_container_width=True,
        hide_index=True
    )
