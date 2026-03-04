# Naver Search Trend Analysis Dashboard

네이버 쇼핑 및 검색 API를 활용한 통합 트렌드 분석 도구입니다.

## 주요 기능
- **데이터 수집**: 네이버 쇼핑 인사이트 API를 통한 1년치 트렌드 자동 수집 (`collect_trend_csv.py`)
- **EDA 분석**: 수집된 데이터를 바탕으로 한 심층 탐색적 데이터 분석 (`eda_process.py`)
- **슬라이드 리포트**: Marp 기반의 분석 프리젠테이션 생성 (`presentation.md`)
- **실시간 대시보드**: Streamlit과 Plotly를 활용한 인터랙티브 분석 환경 (`app.py`)

## 사용 방법
1. `.env.local` 파일에 네이버 API Client ID 및 Secret 설정
2. `pip install -r requirements.txt` 명령어로 필요한 라이브러리 설치
3. `streamlit run app.py` 실행

## Streamlit Cloud 배포 설정
Streamlit Cloud에 배포할 때는 보안을 위해 `.env.local` 파일을 업로드하지 않습니다. 대신 아래 설정을 완료해 주세요:
1. Streamlit Cloud의 대시보드에서 해당 앱의 **Settings > Secrets** 탭으로 이동합니다.
2. 아래 형식으로 API 키를 입력하고 저장합니다:
   ```toml
   CLIENT_ID = "YOUR_NAVER_CLIENT_ID"
   CLIENT_SECRET = "YOUR_NAVER_CLIENT_SECRET"
   ```
- Python 3.x
- Streamlit
- Plotly
- Pandas
- Naver Developers API
