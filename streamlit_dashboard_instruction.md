# 작업 지시서: 네이버 트렌드 통합분석 Streamlit 대시보드 구축

본 문서는 `docs/` 내 네이버 API 가이드를 참조하여, 실시간 트렌드 분석 및 검색 결과 시각화가 가능한 Streamlit 대시보드를 제작하는 절차를 설명합니다.

## 1. 개요 및 요구사항
- **목적**: 키워드 입력 기반의 실시간 트렌드 비교 및 관련 콘텐츠(쇼핑, 블로그 등) 통합 조회.
- **기술 스택**: Streamlit, Plotly (시각화), Pandas (데이터 가공), Naver OpenAPI.
- **핵심 UI**: 사이드바(검색어 입력), 메인 탭(트렌드 분석, EDA 리포트, 콘텐츠 검색).

## 2. 대시보드 구조 및 메뉴 설계
대시보드는 크게 3개의 탭으로 구성합니다.

| 탭 이름 | 주요 내용 |
| :--- | :--- |
| **Trend Comparison** | 키워드 간 데이터랩 쇼핑인사이트/검색량 트렌드 비교 시각화 |
| **Deep EDA** | 수집 데이터 기반 5종 이상의 세부 통계 그래프 및 표 |
| **Content Search** | 쇼핑/블로그/카페/뉴스 검색 결과 목록 (페이징 포함) |

## 3. 세부 구현 가이드

### 3.1. 트렌드 비교 및 EDA (Plotly 활용)
`docs/datalab_search.md` 및 `docs/datalab_shopping_insight.md`를 참조하여 다음 그래프를 구현합니다.

- **필수 그래프 (5가지 이상)**:
  1. **Line Chart**: 일자별 클릭/검색량 비교 트렌드
  2. **Bar Chart**: 월별/분기별 누적 점유율 비교
  3. **Heatmap**: 요일별/시간별 검색 강도 분석
  4. **Boxplot**: 키워드별 클릭 비율의 변동성 및 이상치 확인
  5. **Scatter Plot**: 두 키워드 간의 상관관계 분석 (Correlation)

- **필수 표 (5가지 이상)**:
  - 기술통계 요약표 (Describe), 월별 피봇 테이블, 요일별 평균표, 구간별 성장률 등.

### 3.2. 검색 결과 목록 및 페이징 (Search API)
`docs/search_blog.md` 및 `docs/search_shopping.md`를 활용합니다.

- **페이징 처리**: Streamlit의 `st.empty()` 또는 상태 관리를 통해 10개/20개 단위로 페이지 이동 버튼 구현.
- **하이퍼링크**: 항목 제목 클릭 시 원문 URL로 새 탭에서 이동하도록 HTML 태그 적용.

## 4. 코드 아키텍처 예시 (Python)

```python
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
# (API 연동 모듈은 별도 파일로 분리 권장)

# Sidebar
st.sidebar.title("Search Parameters")
keywords = st.sidebar.text_input("비교할 키워드 (쉼표 구분)", "선풍기, 핫팩")

# Main Tabs
tab1, tab2, tab3 = st.tabs(["트렌드 분석", "심층 EDA", "검색 결과"])

with tab1:
    st.subheader("실시간 트렌드 비교")
    # API 호출 및 Plotly 시연
    # fig = px.line(df, x='date', y='ratio', color='keyword')
    # st.plotly_chart(fig)

with tab2:
    st.subheader("기초 EDA 리포트")
    col1, col2 = st.columns(2)
    # 5종 이상의 그래프를 그리드 형태로 배치
    # col1.plotly_chart(box_fig)
    # col2.write(df.describe())

with tab3:
    st.subheader("통합 콘텐츠 검색")
    category = st.selectbox("채널 선택", ["쇼핑", "블로그", "카페", "뉴스"])
    # 페이징 로직 구현 (st.session_state 사용)
```

## 5. 최종 데이터 검증 및 확인
1. **API 호출 성공 여부**: `app_registration.md`에 설정된 Client ID/Secret 유효성 체크.
2. **반응형 디자인**: 사이드바 입력값 변경 시 Plotly 차트가 즉시 갱신되는지 확인.
3. **링크 연결성**: 생성된 검색 결과 목록의 링크가 정상 작동하는지 확인.
4. **페이징 속도**: 대량의 검색 결과(최대 1000개) 처리 시 페이지 전환의 매끄러움 확인.
