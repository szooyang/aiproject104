
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

from pathlib import Path
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor

# -----------------------------------------
# 1. 페이지 설정
# -----------------------------------------
st.set_page_config(
    page_title="월별 평균기온 예측",
    page_icon="🌡️",
    layout="wide"
)

st.title("🌡️ 월별 평균기온 예측 프로그램")
st.write(
    "세 가지 머신러닝 회귀 알고리즘을 이용하여 "
    "미래의 평균기온을 예측하고 결과를 비교해 봅시다."
)

st.divider()

# -----------------------------------------
# 2. CSV 파일 불러오기
# -----------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = BASE_DIR / "temperature.csv"

try:
    df = pd.read_csv(CSV_PATH, encoding="cp949")

except FileNotFoundError:
    st.error("temperature.csv 파일을 찾을 수 없습니다.")
    st.info("GitHub 최상위 폴더에 CSV 파일이 있는지 확인해 주세요.")
    st.stop()

except Exception as e:
    st.error(f"CSV 파일을 읽을 수 없습니다: {e}")
    st.stop()

# -----------------------------------------
# 3. 데이터 전처리
# -----------------------------------------

df["날짜"] = pd.to_datetime(
    df["일시"],
    format="%b-%y",
    errors="coerce"
)

df["연도"] = df["날짜"].dt.year
df["월"] = df["날짜"].dt.month

df["평균기온(℃)"] = pd.to_numeric(
    df["평균기온(℃)"],
    errors="coerce"
)

df = df.dropna(
    subset=["연도", "월", "평균기온(℃)"]
).copy()

df["연도"] = df["연도"].astype(int)
df["월"] = df["월"].astype(int)

# -----------------------------------------
# 4. 사용자 입력
# -----------------------------------------

st.subheader("📌 예측 조건 선택")

col1, col2 = st.columns(2)

with col1:
    selected_month = st.selectbox(
        "예측할 월을 선택하세요.",
        list(range(1, 13)),
        format_func=lambda x: f"{x}월"
    )

with col2:
    max_year = int(df["연도"].max())

    predict_year = st.number_input(
        "예측할 연도를 입력하세요.",
        min_value=max_year + 1,
        max_value=2100,
        value=max(2030, max_year + 4),
        step=1
    )

# -----------------------------------------
# 5. 회귀 알고리즘 선택
# -----------------------------------------

st.subheader("🤖 회귀 알고리즘 선택")

algorithm_options = [
    "선형회귀 (Linear Regression)",
    "의사결정나무 회귀 (Decision Tree)",
    "랜덤 포레스트 회귀 (Random Forest)"
]

selected_algorithm = st.selectbox(
    "사용할 알고리즘을 선택하세요.",
    algorithm_options
)

# -----------------------------------------
# 6. 선택한 월의 데이터 추출
# -----------------------------------------

month_data = df[
    df["월"] == selected_month
].copy()

month_data = month_data.sort_values("연도")

if len(month_data) < 4:
    st.error("학습 데이터가 부족합니다. 최소 4개 이상의 데이터가 필요합니다.")
    st.stop()

# X : 연도
# y : 평균기온

X = month_data[["연도"]].values
y = month_data["평균기온(℃)"].values

# -----------------------------------------
# 7. 세 가지 회귀 모델 생성
# -----------------------------------------

models = {

    "선형회귀 (Linear Regression)": LinearRegression(),

    "의사결정나무 회귀 (Decision Tree)": DecisionTreeRegressor(
        max_depth=3,
        min_samples_leaf=2,
        random_state=42
    ),

    "랜덤 포레스트 회귀 (Random Forest)": RandomForestRegressor(
        n_estimators=300,
        max_depth=3,
        min_samples_leaf=2,
        random_state=42
    )
}

# -----------------------------------------
# 8. 세 가지 모델 학습 및 예측
# -----------------------------------------

results = {}

for name, model in models.items():

    # 모델 학습
    model.fit(X, y)

    # 미래 기온 예측
    prediction = model.predict(
        np.array([[predict_year]])
    )[0]

    # 학습 데이터 결정계수
    r2 = model.score(X, y)

    results[name] = {
        "model": model,
        "prediction": prediction,
        "r2": r2
    }

# 선택한 모델의 결과
selected_result = results[selected_algorithm]

predicted_temp = selected_result["prediction"]
selected_r2 = selected_result["r2"]

# -----------------------------------------
# 9. 예측 결과 표시
# -----------------------------------------

st.divider()

st.subheader(
    f"📊 {selected_month}월 평균기온 예측 결과"
)

st.caption(
    f"{int(month_data['연도'].min())}년부터 "
    f"{max_year}년까지의 실제 데이터를 학습했습니다."
)

col1, col2, col3 = st.columns(3)

col1.metric(
    "선택한 알고리즘",
    selected_algorithm.split(" (")[0]
)

col2.metric(
    "예측 연도",
    f"{predict_year}년"
)

col3.metric(
    "예측 평균기온",
    f"{predicted_temp:.2f} ℃"
)

# -----------------------------------------
# 10. 그래프 데이터 생성
# -----------------------------------------

fig = go.Figure()

# 실제 데이터 표시
fig.add_trace(
    go.Scatter(
        x=month_data["연도"],
        y=month_data["평균기온(℃)"],
        mode="markers",
        name="실제 평균기온",
        marker=dict(
            color="royalblue",
            size=10,
            line=dict(color="white", width=1)
        ),
        hovertemplate=
        "%{x}년<br>실제 기온: %{y:.2f}℃<extra></extra>"
    )
)

# 모든 알고리즘의 예측 곡선 생성
line_start = int(month_data["연도"].min())
line_end = int(predict_year)

year_range = np.arange(
    line_start,
    line_end + 1
).reshape(-1, 1)

# 알고리즘별 그래프 색상
colors = {
    "선형회귀 (Linear Regression)": "red",
    "의사결정나무 회귀 (Decision Tree)": "orange",
    "랜덤 포레스트 회귀 (Random Forest)": "purple"
}

# 알고리즘별 추세선 표시
for name, result in results.items():

    model = result["model"]

    line_predictions = model.predict(year_range)

    is_selected = (name == selected_algorithm)

    fig.add_trace(
        go.Scatter(
            x=year_range.flatten(),
            y=line_predictions,
            mode="lines",
            name=name,
            line=dict(
                color=colors[name],
                width=4 if is_selected else 2,
                dash="solid" if is_selected else "dot"
            ),
            opacity=1 if is_selected else 0.65,
            hovertemplate=
            "연도: %{x}년<br>예측 기온: %{y:.2f}℃<extra></extra>"
        )
    )

    # 미래 예측 지점
    fig.add_trace(
        go.Scatter(
            x=[predict_year],
            y=[result["prediction"]],
            mode="markers+text",
            name=f"{name.split(' (')[0]} 예측값",
            marker=dict(
                color=colors[name],
                size=19 if is_selected else 11,
                symbol="star" if is_selected else "circle"
            ),
            text=[
                f"{result['prediction']:.1f}℃"
                if is_selected else ""
            ],
            textposition="top center",
            showlegend=False,
            hovertemplate=
            f"{name}<br>%{{x}}년<br>예측: %{{y:.2f}}℃<extra></extra>"
        )
    )

# 예측 연도 표시
fig.add_vline(
    x=predict_year,
    line_dash="dash",
    line_color="green",
    opacity=0.7
)

fig.update_layout(
    title=dict(
        text=f"{selected_month}월 평균기온 회귀 알고리즘 비교",
        x=0.5
    ),
    xaxis_title="연도",
    yaxis_title="평균기온 (℃)",
    template="plotly_white",
    hovermode="x unified",
    height=600,
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

# -----------------------------------------
# 11. 알고리즘별 예측 결과 비교
# -----------------------------------------

st.divider()

st.subheader("📋 세 가지 알고리즘 예측 결과 비교")

comparison_data = []

for name, result in results.items():

    comparison_data.append({
        "회귀 알고리즘": name,
        "예측 기온(℃)": round(result["prediction"], 2),
        "학습 데이터 결정계수(R²)": round(result["r2"], 3)
    })

comparison_df = pd.DataFrame(comparison_data)

st.dataframe(
    comparison_df,
    use_container_width=True,
    hide_index=True
)

# 알고리즘별 예측값 차이
temperatures = [
    result["prediction"]
    for result in results.values()
]

temperature_difference = max(temperatures) - min(temperatures)

st.info(
    f"세 알고리즘의 예측 기온 중 가장 높은 값과 "
    f"가장 낮은 값의 차이는 {temperature_difference:.2f}℃입니다."
)

# -----------------------------------------
# 12. 선택한 알고리즘 설명
# -----------------------------------------

st.divider()

st.subheader("🧠 선택한 회귀 알고리즘 알아보기")

if selected_algorithm == "선형회귀 (Linear Regression)":

    st.markdown("### ① 선형회귀 (Linear Regression)")

    st.write("""
    선형회귀는 실제 데이터의 전체적인 경향을 가장 잘 나타내는
    직선을 찾는 알고리즘입니다.

    실제 데이터 점과 직선 사이의 오차 제곱합이
    최소가 되도록 기울기와 절편을 계산합니다.
    """)

    st.latex(r"y = ax + b")

    st.write("""
    - x : 연도
    - y : 예측 평균기온
    - a : 기울기
    - b : 절편

    미래 연도를 직선의 식에 대입하여 기온을 예측합니다.
    """)

    slope = results[selected_algorithm]["model"].coef_[0]
    intercept = results[selected_algorithm]["model"].intercept_

    st.latex(
        rf"y = {slope:.4f}x + ({intercept:.2f})"
    )

    st.success(
        "빨간색 직선의 기울기를 통해 기온의 장기적인 "
        "상승 또는 하락 경향을 확인할 수 있습니다."
    )

elif selected_algorithm == "의사결정나무 회귀 (Decision Tree)":

    st.markdown("### ② 의사결정나무 회귀 (Decision Tree)")

    st.write("""
    의사결정나무는 데이터를 여러 구간으로 나누어
    각 구간의 평균값을 이용해 예측하는 알고리즘입니다.

    마치 질문에 따라 여러 갈래로 나누어지는
    나무 모양의 구조를 생각하면 됩니다.
    """)

    st.write("""
    예를 들어 연도를 기준으로 데이터를 나누고,
    각 구간에 속한 실제 기온의 평균을 계산합니다.

    새로운 연도가 입력되면 해당 연도가 속하는 구간을 찾아
    그 구간의 평균기온을 예측값으로 제시합니다.
    """)

    st.success(
        "주황색 선의 계단식 모양을 관찰해 보세요. "
        "구간에 따라 예측 기온이 달라지는 모습을 확인할 수 있습니다."
    )

elif selected_algorithm == "랜덤 포레스트 회귀 (Random Forest)":

    st.markdown("### ③ 랜덤 포레스트 회귀 (Random Forest)")

    st.write("""
    랜덤 포레스트는 여러 개의 의사결정나무를 만들어
    각각 예측하게 한 다음, 그 예측값들의 평균을 구하는 알고리즘입니다.
    """)

    st.write("""
    하나의 나무만 사용하는 것이 아니라
    여러 나무의 예측 결과를 종합한다는 점이 특징입니다.
    """)

    st.latex(
        r"\text{최종 예측값} = "
        r"\frac{\text{여러 나무의 예측값 합계}}"
        r"{\text{나무의 개수}}"
    )

    st.success(
        "보라색 선은 여러 의사결정나무의 예측 결과를 "
        "평균하여 만든 결과입니다."
    )

# -----------------------------------------
# 13. 결정계수 설명
# -----------------------------------------

st.divider()

st.subheader("📈 결정계수(R²)란?")

st.write("""
결정계수는 모델이 학습에 사용한 실제 데이터의 변동을
얼마나 설명하는지 나타내는 지표입니다.

일반적으로 1에 가까울수록 학습 데이터에 대한 설명력이 높습니다.
""")

st.metric(
    "선택한 알고리즘의 학습 데이터 결정계수",
    f"{selected_r2:.3f}"
)

st.caption("""
주의: 이 값은 학습에 사용한 데이터에 대한 결정계수입니다.
미래 예측의 정확도를 직접 보장하지 않으며,
알고리즘 간 실제 예측 성능 비교에는 별도의 평가용 데이터가 필요합니다.
""")

# -----------------------------------------
# 14. 전체 데이터 확인
# -----------------------------------------

with st.expander("📂 학습에 사용된 실제 데이터 확인하기"):

    st.dataframe(
        month_data[["연도", "평균기온(℃)"]],
        use_container_width=True,
        hide_index=True
    )

# -----------------------------------------
# 15. 주의사항
# -----------------------------------------

st.divider()

st.warning("""
세 알고리즘은 과거 기온 데이터를 학습하여 미래 기온을 예측합니다.

특히 의사결정나무와 랜덤 포레스트는 학습한 연도 범위보다
먼 미래를 예측할 때 마지막 구간의 예측값이 유지될 수 있습니다.

실제 기온은 다양한 기후 요인의 영향을 받으므로
이 결과는 공식적인 기상 예보가 아닌 통계적 예측값입니다.
""")
