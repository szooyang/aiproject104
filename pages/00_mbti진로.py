
import streamlit as st

st.set_page_config(
    page_title="MBTI 진로 탐험소",
    page_icon="🧭",
    layout="wide"
)

# -------------------------------
# 🎨 화면 꾸미기
# -------------------------------
st.markdown("""
<style>
    .main-title {
        font-size: 38px;
        font-weight: bold;
        text-align: center;
        color: #5B5BD6;
    }
    .sub-title {
        text-align: center;
        font-size: 17px;
        color: #666666;
    }
    .career-card {
        background-color: #F3F4FF;
        padding: 22px;
        border-radius: 18px;
        border: 1px solid #E0E0FF;
        margin-bottom: 12px;
    }
    .career-name {
        font-size: 23px;
        font-weight: bold;
        color: #4444AA;
    }
    .career-info {
        font-size: 16px;
        line-height: 1.8;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------
# 🧭 MBTI별 진로 자료
# 연봉은 세전 기준의 대략적인 참고 범위
# -------------------------------
careers = {
    "ISTJ": {
        "intro": "꼼꼼하고 책임감이 강한 현실적인 계획가!",
        "jobs": [
            {
                "name": "회계사",
                "emoji": "📊",
                "major": "회계학과, 경영학과, 세무회계과",
                "personality": "숫자를 정확하게 다루고 규칙을 지키며 꾸준히 공부하는 사람",
                "salary": "약 5,000만~8,000만 원"
            },
            {
                "name": "정보보안 전문가",
                "emoji": "🔐",
                "major": "정보보호학과, 컴퓨터공학과, 정보통신과",
                "personality": "논리적으로 문제를 분석하고 세부 사항을 꼼꼼하게 확인하는 사람",
                "salary": "약 3,500만~6,000만 원"
            }
        ]
    },
    "ISFJ": {
        "intro": "세심하게 주변을 살피고 다른 사람을 잘 챙기는 따뜻한 조력자!",
        "jobs": [
            {
                "name": "간호사",
                "emoji": "🩺",
                "major": "간호학과",
                "personality": "책임감이 있고 세심하며 다른 사람을 배려하는 사람",
                "salary": "약 3,500만~5,000만 원"
            },
            {
                "name": "초등학교 교사",
                "emoji": "🍎",
                "major": "초등교육과",
                "personality": "인내심이 있고 학생의 성장을 꾸준히 돕는 사람",
                "salary": "약 3,500만~6,000만 원"
            }
        ]
    },
    "INFJ": {
        "intro": "사람의 마음을 이해하고 의미 있는 변화를 꿈꾸는 이상주의자!",
        "jobs": [
            {
                "name": "상담심리 전문가",
                "emoji": "💬",
                "major": "심리학과, 상담심리학과",
                "personality": "공감 능력이 좋고 다른 사람의 이야기를 차분하게 듣는 사람",
                "salary": "약 3,000만~4,500만 원"
            },
            {
                "name": "작가",
                "emoji": "✍️",
                "major": "국어국문학과, 문예창작과, 미디어문학과",
                "personality": "관찰력이 좋고 생각과 감정을 글로 표현하는 것을 좋아하는 사람",
                "salary": "약 2,500만~4,500만 원"
            }
        ]
    },
    "INTJ": {
        "intro": "큰 그림을 보고 전략적으로 문제를 해결하는 설계자!",
        "jobs": [
            {
                "name": "데이터 분석가",
                "emoji": "📈",
                "major": "통계학과, 데이터사이언스학과, 컴퓨터공학과",
                "personality": "자료에서 규칙을 찾고 논리적으로 결론을 내리는 사람",
                "salary": "약 3,500만~6,000만 원"
            },
            {
                "name": "소프트웨어 개발자",
                "emoji": "💻",
                "major": "컴퓨터공학과, 소프트웨어학과, 정보통신과",
                "personality": "복잡한 문제를 분석하고 새로운 해결 방법을 찾는 사람",
                "salary": "약 3,500만~6,500만 원"
            }
        ]
    },
    "ISTP": {
        "intro": "직접 만지고 실험하면서 해결책을 찾는 실전형 탐험가!",
        "jobs": [
            {
                "name": "자동차 정비 기술자",
                "emoji": "🚗",
                "major": "자동차공학과, 자동차과, 미래자동차과",
                "personality": "기계의 작동 원리를 이해하고 문제를 직접 해결하는 사람",
                "salary": "약 3,000만~4,500만 원"
            },
            {
                "name": "로봇 엔지니어",
                "emoji": "🤖",
                "major": "로봇공학과, 기계공학과, 전기전자공학과",
                "personality": "기계와 기술에 관심이 많고 실험과 개선을 즐기는 사람",
                "salary": "약 3,500만~6,000만 원"
            }
        ]
    },
    "ISFP": {
        "intro": "감각이 뛰어나고 자신만의 방식으로 아름다움을 표현하는 예술가!",
        "jobs": [
            {
                "name": "시각디자이너",
                "emoji": "🎨",
                "major": "시각디자인과, 산업디자인과, 디자인학과",
                "personality": "색과 형태에 관심이 많고 시각적으로 아이디어를 표현하는 사람",
                "salary": "약 2,800만~4,500만 원"
            },
            {
                "name": "조리사",
                "emoji": "👨‍🍳",
                "major": "조리과, 호텔조리과, 외식조리학과",
                "personality": "손으로 직접 만들기를 좋아하고 맛과 모양을 세심하게 살피는 사람",
                "salary": "약 2,800만~4,000만 원"
            }
        ]
    },
    "INFP": {
        "intro": "상상력이 풍부하고 자신만의 가치와 이야기를 소중히 여기는 꿈꾸는 사람!",
        "jobs": [
            {
                "name": "웹툰 작가",
                "emoji": "🖌️",
                "major": "웹툰과, 만화애니메이션학과, 콘텐츠창작과",
                "personality": "상상력이 풍부하고 이야기를 그림으로 표현하는 것을 좋아하는 사람",
                "salary": "약 2,500만~4,500만 원"
            },
            {
                "name": "콘텐츠 기획자",
                "emoji": "🎬",
                "major": "미디어학과, 광고홍보학과, 문화콘텐츠학과",
                "personality": "새로운 아이디어를 떠올리고 사람들에게 의미 있는 내용을 전달하는 사람",
                "salary": "약 3,000만~4,500만 원"
            }
        ]
    },
    "INTP": {
        "intro": "궁금한 것을 끝까지 파고들며 원리를 탐구하는 아이디어 연구자!",
        "jobs": [
            {
                "name": "AI 개발자",
                "emoji": "🧠",
                "major": "인공지능학과, 컴퓨터공학과, 소프트웨어학과",
                "personality": "논리적 사고를 즐기고 새로운 기술의 원리를 탐구하는 사람",
                "salary": "약 4,000만~7,000만 원"
            },
            {
                "name": "연구원",
                "emoji": "🔬",
                "major": "자연과학 계열 학과, 공학 계열 학과",
                "personality": "호기심이 많고 자료를 분석하며 깊이 있게 탐구하는 사람",
                "salary": "약 3,500만~6,000만 원"
            }
        ]
    },
    "ESTP": {
        "intro": "행동력이 뛰어나고 새로운 도전을 즐기는 에너지 넘치는 해결사!",
        "jobs": [
            {
                "name": "마케팅 전문가",
                "emoji": "📣",
                "major": "경영학과, 광고홍보학과, 마케팅학과",
                "personality": "빠르게 상황을 파악하고 사람들의 관심을 끄는 아이디어를 내는 사람",
                "salary": "약 3,200만~5,500만 원"
            },
            {
                "name": "행사 기획자",
                "emoji": "🎉",
                "major": "이벤트학과, 관광경영학과, 문화콘텐츠학과",
                "personality": "현장에서 빠르게 판단하고 여러 사람과 협력하는 사람",
                "salary": "약 2,800만~4,500만 원"
            }
        ]
    },
    "ESFP": {
        "intro": "밝은 에너지와 친화력으로 사람들에게 즐거움을 주는 분위기 메이커!",
        "jobs": [
            {
                "name": "호텔리어",
                "emoji": "🏨",
                "major": "호텔경영학과, 호텔관광과, 관광경영학과",
                "personality": "친절하고 사교적이며 다양한 사람을 만나는 것을 좋아하는 사람",
                "salary": "약 2,800만~4,500만 원"
            },
            {
                "name": "영상 크리에이터",
                "emoji": "📹",
                "major": "영상학과, 방송영상과, 미디어콘텐츠학과",
                "personality": "표현력이 좋고 새로운 콘텐츠를 만들며 사람들과 소통하는 사람",
                "salary": "약 2,500만~4,500만 원"
            }
        ]
    },
    "ENFP": {
        "intro": "톡톡 튀는 아이디어와 열정으로 새로운 가능성을 발견하는 아이디어 뱅크!",
        "jobs": [
            {
                "name": "광고 기획자",
                "emoji": "💡",
                "major": "광고홍보학과, 미디어학과, 경영학과",
                "personality": "창의적이고 사람들의 관심과 요구를 파악하는 것을 좋아하는 사람",
                "salary": "약 3,000만~5,000만 원"
            },
            {
                "name": "진로 상담 전문가",
                "emoji": "🧭",
                "major": "교육학과, 상담심리학과, 청소년학과",
                "personality": "다른 사람의 가능성을 발견하고 다양한 선택지를 함께 탐색하는 사람",
                "salary": "약 2,800만~4,500만 원"
            }
        ]
    },
    "ENTP": {
        "intro": "기존의 틀에 질문을 던지고 새로운 방법을 찾아내는 발명가!",
        "jobs": [
            {
                "name": "창업가",
                "emoji": "🚀",
                "major": "경영학과, 창업학과, 산업공학과",
                "personality": "새로운 기회를 찾고 아이디어를 실행하며 도전을 즐기는 사람",
                "salary": "수입 편차가 커서 일률적인 평균 연봉 제시가 어려움"
            },
            {
                "name": "서비스 기획자",
                "emoji": "🧩",
                "major": "산업공학과, 경영학과, 컴퓨터공학과",
                "personality": "다양한 관점에서 문제를 바라보고 더 나은 서비스를 설계하는 사람",
                "salary": "약 3,500만~6,000만 원"
            }
        ]
    },
    "ESTJ": {
        "intro": "목표를 세우고 사람들과 함께 일을 체계적으로 추진하는 리더!",
        "jobs": [
            {
                "name": "프로젝트 관리자",
                "emoji": "📋",
                "major": "경영학과, 산업공학과, 프로젝트 관련 전공",
                "personality": "계획을 세우고 일정을 관리하며 목표 달성을 이끄는 사람",
                "salary": "약 4,000만~7,000만 원"
            },
            {
                "name": "물류 관리자",
                "emoji": "📦",
                "major": "물류학과, 유통학과, 산업공학과",
                "personality": "일의 순서를 정하고 자원과 시간을 효율적으로 관리하는 사람",
                "salary": "약 3,500만~5,500만 원"
            }
        ]
    },
    "ESFJ": {
        "intro": "주변 사람들과 잘 어울리며 함께하는 분위기를 만드는 협력가!",
        "jobs": [
            {
                "name": "인사 담당자",
                "emoji": "🤝",
                "major": "경영학과, 행정학과, 심리학과",
                "personality": "사람들과 원활하게 소통하고 협력과 조직 관리를 중요하게 생각하는 사람",
                "salary": "약 3,200만~5,500만 원"
            },
            {
                "name": "사회복지사",
                "emoji": "💗",
                "major": "사회복지학과, 사회복지과",
                "personality": "공감 능력이 좋고 도움이 필요한 사람을 지원하는 데 보람을 느끼는 사람",
                "salary": "약 2,800만~4,000만 원"
            }
        ]
    },
    "ENFJ": {
        "intro": "사람들의 장점을 발견하고 함께 성장하도록 이끄는 따뜻한 리더!",
        "jobs": [
            {
                "name": "교사",
                "emoji": "📚",
                "major": "교육학과 또는 교과별 사범대학·교직 과정",
                "personality": "설명하는 것을 좋아하고 학생의 성장과 소통에 관심이 많은 사람",
                "salary": "약 3,500만~6,000만 원"
            },
            {
                "name": "인재 교육 담당자",
                "emoji": "🌱",
                "major": "교육학과, 경영학과, 심리학과",
                "personality": "다른 사람의 성장을 돕고 교육 프로그램을 계획하는 것을 좋아하는 사람",
                "salary": "약 3,200만~5,500만 원"
            }
        ]
    },
    "ENTJ": {
        "intro": "목표를 향해 과감하게 나아가며 큰 그림을 그리는 전략가!",
        "jobs": [
            {
                "name": "경영 컨설턴트",
                "emoji": "📊",
                "major": "경영학과, 경제학과, 산업공학과",
                "personality": "복잡한 문제를 분석하고 전략을 세워 개선하는 것을 좋아하는 사람",
                "salary": "약 4,000만~8,000만 원"
            },
            {
                "name": "사업 개발 담당자",
                "emoji": "🌐",
                "major": "경영학과, 경제학과, 국제통상학과",
                "personality": "목표 지향적이고 협상과 새로운 사업 기회 발굴에 관심이 많은 사람",
                "salary": "약 3,500만~6,500만 원"
            }
        ]
    }
}

# -------------------------------
# 🏠 첫 화면
# -------------------------------
st.markdown(
    '<div class="main-title">🧭 MBTI 진로 탐험소</div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="sub-title">'
    '나의 성향을 알아보고, 어울릴 만한 미래 직업을 탐험해 보자! 🚀'
    '</div>',
    unsafe_allow_html=True
)

st.write("")
st.info(
    "✨ MBTI는 진로를 결정하는 정답지가 아니야! "
    "재미있는 자기 이해 도구로 활용하고, 다양한 직업을 탐색해 보자."
)

st.subheader("🔍 너의 MBTI는 무엇이야?")

mbti_groups = {
    "에너지 방향": ["E - 외향형", "I - 내향형"],
    "정보를 받아들이는 방식": ["S - 감각형", "N - 직관형"],
    "판단 기준": ["T - 사고형", "F - 감정형"],
    "생활 방식": ["J - 판단형", "P - 인식형"]
}

mbti_letters = []

col1, col2 = st.columns(2)

with col1:
    energy = st.radio(
        "① 에너지를 얻는 방식",
        ["E - 외향형", "I - 내향형"],
        horizontal=True
    )
    information = st.radio(
        "② 정보를 받아들이는 방식",
        ["S - 감각형", "N - 직관형"],
        horizontal=True
    )

with col2:
    decision = st.radio(
        "③ 판단할 때 더 중요하게 보는 것",
        ["T - 사고형", "F - 감정형"],
        horizontal=True
    )
    lifestyle = st.radio(
        "④ 생활 방식",
        ["J - 판단형", "P - 인식형"],
        horizontal=True
    )

mbti = (
    energy[0]
    + information[0]
    + decision[0]
    + lifestyle[0]
)

st.markdown("---")

# -------------------------------
# 💼 진로 추천 결과
# -------------------------------
profile = careers[mbti]

st.markdown(
    f"<h2 style='text-align:center;'>🎉 너의 MBTI는 {mbti}!</h2>",
    unsafe_allow_html=True
)
st.markdown(
    f"<h4 style='text-align:center;'>{profile['intro']}</h4>",
    unsafe_allow_html=True
)

st.write("")
st.subheader("💼 너에게 추천하는 진로 TOP 2")

col1, col2 = st.columns(2)

for index, job in enumerate(profile["jobs"]):
    target_col = col1 if index == 0 else col2

    with target_col:
        st.markdown(
            f"""
            <div class="career-card">
                <div class="career-name">
                    {job['emoji']} {job['name']}
                </div>
                <div class="career-info">
                    <b>🎓 관련 학과</b><br>
                    {job['major']}<br><br>
                    <b>🌟 이런 성향이라면 잘 맞을 수 있어!</b><br>
                    {job['personality']}<br><br>
                    <b>💰 참고 연봉</b><br>
                    {job['salary']}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

st.markdown("---")

# -------------------------------
# 🌱 나만의 진로 탐색
# -------------------------------
st.subheader("🌱 나의 진로 탐색 노트")

st.write("추천 결과를 보고 아래 질문에 답해 보자!")

interest = st.text_area(
    "💖 두 가지 직업 중 더 관심이 가는 직업은? 그 이유는?",
    placeholder="예: AI 개발자. 인공지능으로 새로운 문제를 해결하는 것이 재미있을 것 같아서!"
)

strength = st.text_area(
    "💪 내가 그 직업에 활용할 수 있는 장점은?",
    placeholder="예: 궁금한 것이 생기면 끝까지 찾아보는 편이다."
)

challenge = st.text_area(
    "🚀 그 직업을 위해 앞으로 키우고 싶은 능력은?",
    placeholder="예: 파이썬 프로그래밍을 더 연습하고 싶다."
)

if st.button("📝 나의 진로 탐색 결과 확인하기", use_container_width=True):
    st.success("진로 탐색 기록을 완성했어! 👏")

    st.markdown("### 📌 나의 진로 탐색 결과")
    st.write(f"**나의 MBTI:** {mbti}")
    st.write(f"**추천 진로 1:** {profile['jobs'][0]['name']}")
    st.write(f"**추천 진로 2:** {profile['jobs'][1]['name']}")
    st.write(f"**관심 직업과 이유:** {interest or '아직 생각 중!'}")
    st.write(f"**나의 장점:** {strength or '앞으로 찾아보기!'}")
    st.write(f"**키우고 싶은 능력:** {challenge or '앞으로 찾아보기!'}")

st.caption(
    "📌 연봉은 직업 탐색을 위한 대략적인 예시 범위이며, "
    "공식 통계의 동일 연도·동일 기준 평균값이 아닐 수 있어. "
    "실제 연봉은 경력, 직무, 근무처 등에 따라 달라져. "
    "최신 직업별 임금은 임금직업포털 워크피디아에서 확인해 보자."
)

st.markdown(
    "[🔎 임금직업포털 워크피디아 바로가기](https://www.wagework.go.kr/pt/index.do)"
)
