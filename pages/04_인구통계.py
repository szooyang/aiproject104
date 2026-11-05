
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
import re

# -----------------------------------------
# 1. 기본 페이지 설정
# -----------------------------------------
st.set_page_config(
    page_title="서울 인구 연령별 분석",
    page_icon="🌸",
    layout="wide"
)

# -----------------------------------------
# 2. 화면 제목 및 디자인
# -----------------------------------------
st.title("🌸 서울시 연령별 인구 분석")
st.markdown(
    "행정구역, 성별, 연도를 선택하여 "
    "연령대별 인구 분포를 확인해 보세요."
)

st.markdown("""
<style>
    .main {
        background-color: #FFF9FC;
    }
    h1 {
        color: #E91E8C;
    }
    div[data-testid="stSelectbox"] label {
        color: #C21875;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)


# -----------------------------------------
# 3. CSV 파일 불러오기
# -----------------------------------------
@st.cache_data
def load_data():

    file_path = os.path.join(
        os.path.dirname(__file__),
        "population(4).csv"
    )

    if not os.path.exists(file_path):
        raise FileNotFoundError(
            "population(4).csv 파일을 찾을 수 없습니다."
        )

    # 한글 인코딩 자동 대응
    encodings = ["cp949", "euc-kr", "utf-8-sig", "utf-8"]

    for encoding in encodings:
        try:
            df = pd.read_csv(
                file_path,
                encoding=encoding,
                thousands=","
            )
            return df

        except UnicodeDecodeError:
            continue

    raise ValueError(
        "CSV 파일의 한글 인코딩을 확인해 주세요."
    )


try:
    df = load_data()

except Exception as e:
    st.error(f"데이터를 불러오지 못했습니다: {e}")
    st.stop()


# -----------------------------------------
# 4. 행정구역 이름 정리
# -----------------------------------------
def clean_region(name):

    name = str(name)

    # 행정구역 코드 제거
    name = re.sub(r"\s*\(\d+\)\s*$", "", name)

    # 서울특별시 접두어 제거
    name = re.sub(r"^서울특별시\s*", "", name)

    name = name.strip()

    if name == "":
        return "서울특별시"

    return name


df["행정구역명"] = df["행정구역"].apply(clean_region)


# -----------------------------------------
# 5. 선택 항목 설정
# -----------------------------------------
years = list(range(2020, 2026))

genders = {
    "전체": "",
    "남성": "남_",
    "여성": "여_"
}

age_groups = [
    "0~9세",
    "10~19세",
    "20~29세",
    "30~39세",
    "40~49세",
    "50~59세",
    "60~69세",
    "70~79세",
    "80~89세",
    "90~99세",
    "100세 이상"
]


# -----------------------------------------
# 6. 사용자 선택 화면
# -----------------------------------------
st.subheader("🔎 분석 조건 선택")

col1, col2, col3 = st.columns(3)

regions = df["행정구역명"].tolist()

with col1:
    selected_region = st.selectbox(
        "🏙️ 행정구역",
        regions,
        index=0
    )

with col2:
    selected_gender = st.selectbox(
        "👥 성별",
        list(genders.keys()),
        index=0
    )

with col3:
    selected_year = st.selectbox(
        "📅 연도",
        years,
        index=len(years) - 1
    )


# -----------------------------------------
# 7. 선택한 조건에 맞는 데이터 추출
# -----------------------------------------
selected_data = df[
    df["행정구역명"] == selected_region
]

if selected_data.empty:
    st.error("선택한 행정구역의 데이터가 없습니다.")
    st.stop()

# 한 행의 데이터 추출
row = selected_data.iloc[0]

# 선택한 연도와 성별에 맞는 열 이름 생성
gender_prefix = genders[selected_gender]

population_columns = [
    f"{selected_year}년_{gender_prefix}거주자_{age}"
    for age in age_groups
]

# CSV에 실제 해당 열이 있는지 확인
missing_columns = [
    col for col in population_columns
    if col not in df.columns
]

if missing_columns:
    st.error(
        f"데이터 열을 찾을 수 없습니다: {missing_columns}"
    )
    st.stop()

# 연령대별 인구 데이터 추출
population = [
    pd.to_numeric(row[col], errors="coerce")
    for col in population_columns
]

if pd.isna(population).any():
    st.error("인구 데이터에 숫자가 아닌 값이 있습니다.")
    st.stop()

# -----------------------------------------
# 8. 주요 통계 표시
# -----------------------------------------
total_population = int(sum(population))
max_index = population.index(max(population))

st.divider()

st.subheader("📊 인구 통계 요약")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="선택 지역",
        value=selected_region
    )

with col2:
    st.metric(
        label="연령별 인구 합계",
        value=f"{total_population:,}명"
    )

with col3:
    st.metric(
        label="인구가 가장 많은 연령대",
        value=age_groups[max_index]
    )


# -----------------------------------------
# 9. 핫핑크 꺾은선 그래프
# -----------------------------------------
st.divider()

st.subheader("💗 연령대별 인구 분포")

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=age_groups,
        y=population,
        mode="lines+markers",
        name="인구수",
        line=dict(
            color="#FF1493",
            width=4
        ),
        marker=dict(
            color="#FF1493",
            size=10,
            line=dict(
                color="white",
                width=2
            )
        ),
        hovertemplate=
            "<b>%{x}</b><br>" +
            "인구수: %{y:,.0f}명" +
            "<extra></extra>"
    )
)

# 세로축 최대값을 10만 명 단위로 설정
y_max = max(population)

y_axis_max = max(
    100000,
    ((int(y_max) // 100000) + 1) * 100000
)

fig.update_layout(
    title=dict(
        text=(
            f"{selected_region} | "
            f"{selected_year}년 | "
            f"{selected_gender} 인구"
        ),
        x=0.5,
        font=dict(
            size=22,
            color="#E91E8C"
        )
    ),

    xaxis=dict(
        title="연령대",
        type="category",
        categoryorder="array",
        categoryarray=age_groups,
        showgrid=True,
        gridcolor="#F5C6DD",
        gridwidth=1,
        tickfont=dict(size=12)
    ),

    yaxis=dict(
        title="인구수 (명)",
        range=[0, y_axis_max],
        dtick=100000,
        tickformat=",",
        showgrid=True,
        gridcolor="#E5E5E5",
        gridwidth=1,
        zeroline=True,
        zerolinecolor="#AAAAAA"
    ),

    height=550,

    plot_bgcolor="white",
    paper_bgcolor="white",

    font=dict(
        family="Malgun Gothic, AppleGothic, NanumGothic, sans-serif",
        size=13,
        color="#333333"
    ),

    hovermode="x unified",

    margin=dict(
        l=70,
        r=30,
        t=80,
        b=70
    )
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# -----------------------------------------
# 10. 연령대별 인구 데이터 표
# -----------------------------------------
with st.expander("📋 연령대별 상세 인구수 확인"):

    result_df = pd.DataFrame({
        "연령대": age_groups,
        "인구수": [int(x) for x in population]
    })

    result_df["인구수"] = result_df["인구수"].map(
        lambda x: f"{x:,}명"
    )

    st.dataframe(
        result_df,
        use_container_width=True,
        hide_index=True
    )


# -----------------------------------------
# 11. 데이터 출처
# -----------------------------------------
st.divider()

st.caption(
    "📌 데이터 출처: 업로드한 서울시 인구 통계 CSV 파일"
)

st.caption(
    "💗 그래프 색상: 핫핑크 (#FF1493)"
)

st.caption(
    "※ 세로축 격자 간격은 100,000명입니다."
)
