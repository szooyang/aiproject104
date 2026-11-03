
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

# ==========================================
# 1. 기본 페이지 설정
# ==========================================
st.set_page_config(
    page_title="세계 국가별 MBTI 탐험",
    page_icon="🌏",
    layout="wide"
)

# ==========================================
# 2. 제목
# ==========================================
st.title("🌏 세계 국가별 MBTI 탐험")
st.markdown(
    "158개 국가의 MBTI 분포를 살펴보고 "
    "국가별 성격 유형의 비율을 비교해 보세요! 🔍"
)

st.divider()

# ==========================================
# 3. CSV 파일 불러오기
# ==========================================
@st.cache_data
def load_data():

    file_name = "countriesMBTI_16types(6).csv"

    file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        file_name
    )

    if not os.path.exists(file_path):
        return None

    try:
        data = pd.read_csv(
            file_path,
            encoding="utf-8-sig"
        )
    except UnicodeDecodeError:
        data = pd.read_csv(
            file_path,
            encoding="cp949"
        )

    return data


df = load_data()

if df is None:
    st.error(
        "CSV 파일을 찾을 수 없습니다. "
        "GitHub 저장소에 countriesMBTI_16types(6).csv "
        "파일을 업로드했는지 확인해 주세요."
    )
    st.stop()


# ==========================================
# 4. 데이터 정리
# ==========================================
df.columns = df.columns.str.strip()

if "Country" not in df.columns:
    st.error("CSV 파일에 Country 열이 없습니다.")
    st.stop()

mbti_types = [
    "INFJ", "ISFJ", "INTP", "ISFP",
    "ENTP", "INFP", "ENTJ", "ISTP",
    "INTJ", "ESFP", "ESTJ", "ENFP",
    "ESTP", "ISTJ", "ENFJ", "ESFJ"
]

missing_columns = [
    col for col in mbti_types
    if col not in df.columns
]

if missing_columns:
    st.error(
        f"CSV 파일에 없는 MBTI 열: {missing_columns}"
    )
    st.stop()

for col in mbti_types:
    df[col] = pd.to_numeric(
        df[col],
        errors="coerce"
    )

df = df.dropna(subset=["Country"])

df[mbti_types] = df[mbti_types].fillna(0)

# ==========================================
# 5. 국가 선택
# ==========================================
st.subheader("🗺️ 국가 선택하기")

countries = sorted(
    df["Country"].astype(str).unique()
)

default_index = (
    countries.index("South Korea")
    if "South Korea" in countries
    else 0
)

selected_country = st.selectbox(
    "분석하고 싶은 국가를 선택하세요.",
    countries,
    index=default_index
)

country_data = df[
    df["Country"].astype(str) == selected_country
].iloc[0]


# ==========================================
# 6. MBTI 비율 계산
# ==========================================
result = pd.DataFrame({
    "MBTI": mbti_types,
    "비율": [
        country_data[x]
        for x in mbti_types
    ]
})

# 소수 형태의 비율을 백분율로 변환
if result["비율"].max() <= 1.5:
    result["비율"] = result["비율"] * 100

# 높은 비율 순서대로 정렬
result = result.sort_values(
    "비율",
    ascending=False
).reset_index(drop=True)

result["순위"] = range(1, 17)


# ==========================================
# 7. 최고 및 최저 MBTI 안내
# ==========================================
st.subheader(
    f"📊 {selected_country}의 MBTI 분석"
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "🥇 가장 높은 유형",
        result.iloc[0]["MBTI"],
        f'{result.iloc[0]["비율"]:.2f}%'
    )

with col2:
    st.metric(
        "📉 가장 낮은 유형",
        result.iloc[-1]["MBTI"],
        f'{result.iloc[-1]["비율"]:.2f}%'
    )

with col3:
    st.metric(
        "🌍 분석 국가 수",
        f"{len(countries)}개"
    )

st.divider()


# ==========================================
# 8. 초록색 그라데이션 생성
# ==========================================
def make_gradient(
    start_color,
    end_color,
    steps
):

    colors = []

    start = tuple(
        int(start_color[i:i+2], 16)
        for i in (1, 3, 5)
    )

    end = tuple(
        int(end_color[i:i+2], 16)
        for i in (1, 3, 5)
    )

    for i in range(steps):

        ratio = i / max(steps - 1, 1)

        color = tuple(
            int(
                start[j]
                + (end[j] - start[j]) * ratio
            )
            for j in range(3)
        )

        colors.append(
            "#{:02x}{:02x}{:02x}".format(*color)
        )

    return colors


# 1위는 빨간색
# 2~16위는 진한 초록색에서 연한 초록색
green_colors = make_gradient(
    "#16803C",
    "#DDF5E3",
    15
)

bar_colors = ["#FF3333"] + green_colors


# ==========================================
# 9. MBTI 막대그래프
# ==========================================
st.subheader("🏆 MBTI 유형별 비율 순위")

fig = go.Figure()

fig.add_trace(
    go.Bar(
        x=result["비율"],
        y=result["MBTI"],
        orientation="h",

        marker=dict(
            color=bar_colors,
            line=dict(width=0)
        ),

        text=[
            f"{v:.2f}%"
            for v in result["비율"]
        ],

        textposition="outside",

        textfont=dict(
            size=13
        ),

        hovertemplate=(
            "<b>%{y}</b><br>"
            "비율: %{x:.2f}%"
            "<extra></extra>"
        )
    )
)

fig.update_layout(
    height=650,

    xaxis_title="MBTI 비율 (%)",
    yaxis_title="MBTI 유형",

    yaxis=dict(
        autorange="reversed",
        tickfont=dict(size=13)
    ),

    xaxis=dict(
        rangemode="tozero",
        showgrid=True,
        gridcolor="#E5E5E5"
    ),

    plot_bgcolor="white",
    paper_bgcolor="white",

    margin=dict(
        l=50,
        r=70,
        t=30,
        b=50
    ),

    showlegend=False
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.caption(
    "🔴 1위 유형 | 🟢 2~16위 유형 "
    "(순위가 낮아질수록 연한 초록색)"
)


# ==========================================
# 10. MBTI 순위 상세표
# ==========================================
st.divider()

st.subheader("📋 MBTI 순위 상세 정보")

display_data = result[
    ["순위", "MBTI", "비율"]
].copy()

display_data["비율"] = display_data[
    "비율"
].map(
    lambda x: f"{x:.2f}%"
)

st.dataframe(
    display_data,
    use_container_width=True,
    hide_index=True
)


# ==========================================
# 11. CSV 다운로드
# ==========================================
st.divider()

st.subheader("📥 데이터 다운로드")

csv_data = result.to_csv(
    index=False,
    encoding="utf-8-sig"
)

st.download_button(
    label="📄 선택한 국가의 MBTI 데이터 다운로드",
    data=csv_data,
    file_name=f"{selected_country}_MBTI.csv",
    mime="text/csv"
)


# ==========================================
# 12. 안내 문구
# ==========================================
st.divider()

st.info(
    "💡 이 자료는 국가별 MBTI 분포를 탐색하기 위한 "
    "교육용 데이터입니다. 실제 국민 전체의 성격 분포를 "
    "확정적으로 나타내는 통계는 아닙니다."
)

st.caption(
    "🌏 세계 국가별 MBTI 탐험 | Streamlit"
)
