import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import json
from datetime import datetime, timedelta
import os

# 1. Page Configuration
st.set_page_config(page_title="네이버 통합 트렌드 분석 대시보드", layout="wide")

# 2. Credential Loading
def load_credentials():
    env_path = ".env.local"
    creds = {"client_id": None, "client_secret": None}
    
    # Try loading from .env.local if it exists
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                if "=" in line:
                    parts = line.strip().split("=", 1)
                    if len(parts) == 2:
                        k, v = parts
                        if k.upper() in ["CLIENT_ID", "CLIENT_SECRET", "CLIENT_ID", "CLIENT_SECRET"]:
                            creds[k.lower().replace("client_id", "client_id").replace("client_secret", "client_secret")] = v
    
    # Try loading from streamlit secrets (for cloud deployment)
    if not creds["client_id"] or not creds["client_secret"]:
        try:
            creds["client_id"] = st.secrets.get("CLIENT_ID") or st.secrets.get("client_id")
            creds["client_secret"] = st.secrets.get("CLIENT_SECRET") or st.secrets.get("client_secret")
        except:
            pass
            
    return creds

creds = load_credentials()

# 3. Sidebar Configuration
st.sidebar.title("🔍 검색 설정")
if not creds["client_id"] or not creds["client_secret"]:
    st.sidebar.error("API 인증 정보가 없습니다 (.env.local 확인)")
else:
    st.sidebar.success("API 인증 완료")

keywords_input = st.sidebar.text_input("비교 키워드 (쉼표 구분)", "선풍기, 핫팩")
target_keywords = [k.strip() for k in keywords_input.split(",") if k.strip()]

date_range = st.sidebar.number_input("조회 기간 (일)", min_value=30, max_value=365, value=365)
end_date = datetime.now()
start_date = end_date - timedelta(days=int(date_range))

# 4. API Request Functions
def get_shopping_insight(keywords, start_date, end_date):
    url = "https://openapi.naver.com/v1/datalab/shopping/category/keywords"
    headers = {
        "X-Naver-Client-Id": creds["client_id"],
        "X-Naver-Client-Secret": creds["client_secret"],
        "Content-Type": "application/json"
    }
    
    # We use a broad category (Sports/Leisure as it covers Hotpack well, or Appliance for Fan)
    # For a cross-category comparison, we might need multiple calls, but here we try keywords in one.
    # We'll use Category 50000000 (Fashion) as a default if not specified, 
    # but based on previous EDA, let's use 50000000 for keyword general search if possible.
    results = []
    
    for kw in keywords:
        # Determine category ID based on keyword (simple logic for demo)
        cat_id = "50000007" if kw == "핫팩" else "50000003"
        body = {
            "startDate": start_date.strftime('%Y-%m-%d'),
            "endDate": end_date.strftime('%Y-%m-%d'),
            "timeUnit": "date",
            "category": cat_id,
            "keyword": [{"name": kw, "param": [kw]}]
        }
        res = requests.post(url, headers=headers, json=body)
        if res.status_code == 200:
            data = res.json()
            for row in data['results'][0]['data']:
                results.append({
                    "date": row['period'],
                    "keyword": kw,
                    "ratio": row['ratio']
                })
    return pd.DataFrame(results)

def search_naver(query, category="blog", start=1, display=10):
    url_map = {
        "blog": "https://openapi.naver.com/v1/search/blog.json",
        "news": "https://openapi.naver.com/v1/search/news.json",
        "shop": "https://openapi.naver.com/v1/search/shop.json",
        "cafe": "https://openapi.naver.com/v1/search/cafearticle.json"
    }
    headers = {
        "X-Naver-Client-Id": creds["client_id"],
        "X-Naver-Client-Secret": creds["client_secret"]
    }
    params = {"query": query, "display": display, "start": start}
    res = requests.get(url_map[category], headers=headers, params=params)
    if res.status_code == 200:
        return res.json()
    return None

# 5. Main UI
st.title("📊 네이버 쇼핑 트렌드 통합 대시보드")
st.markdown("---")

tab1, tab2, tab3 = st.tabs(["📉 트렌드 분석", "📑 심층 EDA 리포트", "🔗 통합 콘텐츠 검색"])

if target_keywords:
    with st.spinner('데이터 수집 중...'):
        df = get_shopping_insight(target_keywords, start_date, end_date)
        df['date'] = pd.to_datetime(df['date'])

    # --- TAB 1: Trend Analysis ---
    with tab1:
        st.subheader("실시간 키워드 트렌드 비교")
        if not df.empty:
            fig = px.line(df, x='date', y='ratio', color='keyword', title="일자별 클릭 비율 트렌드")
            fig.update_layout(hovermode="x unified")
            st.plotly_chart(fig, use_container_width=True)
            
            # Monthly Pivot
            df['month'] = df['date'].dt.strftime('%Y-%m')
            pivot_df = df.pivot_table(index='month', columns='keyword', values='ratio', aggfunc='mean')
            st.write("📅 **월별 평균 클릭 지수 피봇 데이터**")
            st.dataframe(pivot_df.style.highlight_max(axis=0))
        else:
            st.warning("데이터가 없습니다. 키워드나 기간을 확인해 주세요.")

    # --- TAB 2: Deep EDA ---
    with tab2:
        st.subheader("데이터 심층 분석 (EDA)")
        if not df.empty:
            col1, col2 = st.columns(2)
            
            with col1:
                # 1. Box plot
                fig_box = px.box(df, x='keyword', y='ratio', color='keyword', points="all", title="키워드별 클릭 비율 분포 및 변동성")
                st.plotly_chart(fig_box, use_container_width=True)
                
                # 2. Histogram
                fig_hist = px.histogram(df, x='ratio', color='keyword', barmode='overlay', title="클릭 비율 히스토그램")
                st.plotly_chart(fig_hist, use_container_width=True)

            with col2:
                # 3. Heatmap (Month vs Keyword)
                heatmap_data = df.pivot_table(index=df['date'].dt.month, columns='keyword', values='ratio', aggfunc='mean')
                fig_heat = px.imshow(heatmap_data, labels=dict(x="키워드", y="월", color="평균 비율"), title="월별 키워드 수요 강도 (Heatmap)")
                st.plotly_chart(fig_heat, use_container_width=True)
                
                # 4. Bar chart (Quarterly)
                df['quarter'] = df['date'].dt.quarter
                q_avg = df.groupby(['quarter', 'keyword'])['ratio'].mean().reset_index()
                fig_bar = px.bar(q_avg, x='quarter', y='ratio', color='keyword', barmode='group', title="분기별 평균 수요 비중")
                st.plotly_chart(fig_bar, use_container_width=True)
            
            # 5. Descriptive Statistics Table
            st.write("📊 **키워드별 기술 통계량 (Descriptive Statistics)**")
            stats_df = df.groupby('keyword')['ratio'].describe().T
            st.table(stats_df)
            
            # 6. Correlations (if multiple keywords)
            if len(target_keywords) > 1:
                st.write("🔗 **키워드 간 상관관계 분석**")
                corr_pivot = df.pivot_table(index='date', columns='keyword', values='ratio').corr()
                st.write(corr_pivot)

    # --- TAB 3: Search Results ---
    with tab3:
        st.subheader("통합 콘텐츠 검색 결과")
        search_kw = st.selectbox("검색할 키워드 선택", target_keywords)
        ch_col1, ch_col2 = st.columns([1, 4])
        
        with ch_col1:
            channel = st.radio("채널", ["blog", "news", "shop", "cafe"])
            page_size = 10
            if 'start_idx' not in st.session_state:
                st.session_state.start_idx = 1
            
            btn_prev, btn_next = st.columns(2)
            if btn_prev.button("이전"):
                st.session_state.start_idx = max(1, st.session_state.start_idx - page_size)
            if btn_next.button("다음"):
                st.session_state.start_idx += page_size

        with ch_col2:
            results = search_naver(search_kw, category=channel, start=st.session_state.start_idx, display=page_size)
            if results and 'items' in results:
                st.write(f"Displaying {st.session_state.start_idx} ~ {st.session_state.start_idx + page_size - 1}")
                for item in results['items']:
                    title = item.get('title', '').replace('<b>', '').replace('</b>', '')
                    link = item.get('link') or item.get('originallink')
                    desc = item.get('description', '').replace('<b>', '').replace('</b>', '')
                    
                    st.markdown(f"### [{title}]({link})")
                    if channel == 'shop':
                        st.write(f"가격: {item.get('lprice')}원 / 몰: {item.get('mallName')}")
                    st.write(desc)
                    st.markdown("---")
            else:
                st.error("검색 결과를 가져오지 못했습니다.")
else:
    st.info("사이드바에서 키워드를 입력해 주세요.")
