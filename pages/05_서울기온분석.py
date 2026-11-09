
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

# --------------------------------------------------
# 1. 페이지 설정
# --------------------------------------------------

st.set_page_config(
    page_title="월별 기온분석",
    page_icon="🌡️",
    layout="wide"
)

st.title("🌡️ 월별 기온분석")
st.write("월을 선택하면 연도별 최고기온과 최저기온을 비교합니다.")

# --------------------------------------------------
# 2. CSV 파일 경로 설정
# --------------------------------------------------

# 현재 파일은 pages 폴더에 있으므로
# 상위 폴더에서 CSV 파일을 찾습니다.

csv_path = Path(__file__).resolve().parent.parent / "temperature.csv"

if not csv_path.exists():
    csv_path = Path.cwd() / "temperature.csv"

# --------------------------------------------------
# 3. CSV 파일 읽기
# --------------------------------------------------

try:
    df = pd.read_csv(
        csv_path,
        encoding="cp949"
    )

except FileNotFoundError:
    st.error("temperature.csv 파일을 찾을 수 없습니다.")
    st.stop()

except Exception as e:
    st.error(f"CSV 파일을 읽는 중 오류가 발생했습니다: {e}")
    st.stop()

# --------------------------------------------------
# 4. 필요한 열 확인
# --------------------------------------------------

required_columns = [
    "일시",
    "최고기온(℃)",
    "최저기온(℃)"
]

if not all(col in df.columns for col in required_columns):
    st.error("CSV 파일의 열 이름을 확인해 주세요.")
    st.stop()

# --------------------------------------------------
# 5. 날짜 데이터에서 연도와 월 추출
# --------------------------------------------------

# 날짜 형식 예시: Oct-07, Jan-08

month_dict = {
    "Jan": 1,
    "Feb": 2,
    "Mar": 3,
    "Apr": 4,
    "May": 5,
    "Jun": 6,
    "Jul": 7,
    "Aug": 8,
    "Sep": 9,
    "Oct": 10,
    "Nov": 11,
    "Dec": 12
}

date_parts = (
    df["일시"]
    .astype(str)
    .str.strip()
    .str.extract(r"^([A-Za-z]{3})-(\d{2,4})$")
)

df["월"] = date_parts[0].map(month_dict)

year_values = pd.to_numeric(
    date_parts[1],
    errors="coerce"
)

# 이 파일의 두 자리 연도는 2000년대로 처리
df["연도"] = year_values.apply(
    lambda x: 2000 + x if pd.notna(x) and x < 100
    else x
)

# 연도와 월이 없는 행 제거
df = df.dropna(
    subset=["연도", "월"]
).copy()

df["연도"] = df["연도"].astype(int)
df["월"] = df["월"].astype(int)

# --------------------------------------------------
# 6. 기온 데이터 숫자로 변환
# --------------------------------------------------

df["최고기온(℃)"] = pd.to_numeric(
    df["최고기온(℃)"],
    errors="coerce"
)

df["최저기온(℃)"] = pd.to_numeric(
    df["최저기온(℃)"],
    errors="coerce"
)

# --------------------------------------------------
# 7. 월 선택 메뉴
# --------------------------------------------------

month_names = [
    "1월", "2월", "3월", "4월",
    "5월", "6월", "7월", "8월",
    "9월", "10월", "11월", "12월"
]

selected_month = st.selectbox(
    "분석할 월을 선택하세요.",
    range(1, 13),
    format_func=lambda x: month_names[x - 1]
)

# --------------------------------------------------
# 8. 선택한 월의 데이터 추출
# --------------------------------------------------

month_df = df[df["월"] == selected_month].copy()

# 같은 연도와 월에 여러 데이터가 있는 경우
# 기온의 평균값으로 하나의 값으로 정리합니다.

result = (
    month_df
    .groupby("연도", as_index=False)
    .agg({
        "최고기온(℃)": "mean",
        "최저기온(℃)": "mean"
    })
    .sort_values("연도")
)

if result.empty:
    st.warning("선택한 월의 데이터가 없습니다.")
    st.stop()

# --------------------------------------------------
# 9. 그래프 그리기
# --------------------------------------------------

fig = go.Figure()

# 최고기온 그래프 - 핫핑크

fig.add_trace(
    go.Scatter(
        x=result["연도"].astype(str),
        y=result["최고기온(℃)"],
        mode="lines+markers",
        name="최고기온",
        line=dict(
            color="#FF1493",
            width=3
        ),
        marker=dict(
            size=7
        )
    )
)

# 최저기온 그래프 - 파란색

fig.add_trace(
    go.Scatter(
        x=result["연도"].astype(str),
        y=result["최저기온(℃)"],
        mode="lines+markers",
        name="최저기온",
        line=dict(
            color="#1E90FF",
            width=3
        ),
        marker=dict(
            size=7
        )
    )
)

# --------------------------------------------------
# 10. 그래프 제목과 축 설정
# --------------------------------------------------

fig.update_layout(
    title={
        "text": "월별 기온분석",
        "x": 0.5,
        "xanchor": "center"
    },

    xaxis_title="연도",
    yaxis_title="온도 (℃)",

    legend=dict(
        title="범례",
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="center",
        x=0.5
    ),

    hovermode="x unified",

    template="plotly_white",

    height=550
)

fig.update_xaxes(
    title_text="연도",
    type="category"
)

fig.update_yaxes(
    title_text="온도 (℃)",
    showgrid=True,
    zeroline=True
)

# --------------------------------------------------
# 11. Streamlit 화면에 그래프 출력
# --------------------------------------------------

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# 12. 분석 데이터 표 출력
# --------------------------------------------------

with st.expander("📊 분석 데이터 확인하기"):

    display_df = result.rename(
        columns={
            "연도": "연도",
            "최고기온(℃)": "최고기온(℃)",
            "최저기온(℃)": "최저기온(℃)"
        }
    )

    st.dataframe(
        display_df.round(1),
        use_container_width=True,
        hide_index=True
    )

# --------------------------------------------------
# 13. 데이터 분석 안내
# --------------------------------------------------

duplicate_count = (
    month_df.groupby(["연도", "월"])
    .size()
    .gt(1)
    .sum()
)

if duplicate_count > 0:
    st.info(
        f"선택한 월에 중복된 연도 데이터가 "
        f"{duplicate_count}개 있습니다. "
        "중복 데이터는 평균값으로 통합하여 표시했습니다."
    )

st.caption(
    "데이터 출처: temperature.csv | "
    "최고기온과 최저기온은 해당 월의 관측값입니다."
)
