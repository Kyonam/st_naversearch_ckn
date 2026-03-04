import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib
import os

# Create images folder if not exists
if not os.path.exists("images"):
    os.makedirs("images")

def perform_eda(file_path):
    # Load data
    df = pd.read_csv(file_path)
    df['date'] = pd.to_datetime(df['date'])
    
    # 1. Basic Info
    print("--- HEAD 5 ---")
    print(df.head())
    print("\n--- TAIL 5 ---")
    print(df.tail())
    print("\n--- INFO ---")
    df.info()
    print(f"\nShape: {df.shape}")
    print(f"Duplicates: {df.duplicated().sum()}")
    
    # 2. Descriptive Stats
    print("\n--- Numerical Stats ---")
    print(df.describe())
    print("\n--- Categorical Stats ---")
    print(df.describe(include=['object', 'datetime']))

    # Prepare for plots
    df_fan = df[df['keyword_group'] == '선풍기'].copy()
    df_hot = df[df['keyword_group'] == '핫팩'].copy()
    
    # 1. Univariate: Click Ratio Distribution (Fan)
    plt.figure(figsize=(10, 6))
    df_fan['ratio'].hist(bins=30, color='skyblue', edgecolor='black')
    plt.title('선풍기 클릭 비율 분포')
    plt.xlabel('비율 (Ratio)')
    plt.ylabel('빈도')
    plt.savefig('images/01_fan_ratio_dist.png')
    plt.close()

    # 2. Univariate: Click Ratio Distribution (Hotpack)
    plt.figure(figsize=(10, 6))
    df_hot['ratio'].hist(bins=30, color='salmon', edgecolor='black')
    plt.title('핫팩 클릭 비율 분포')
    plt.xlabel('비율 (Ratio)')
    plt.ylabel('빈도')
    plt.savefig('images/02_hotpack_ratio_dist.png')
    plt.close()

    # 3. Univariate: Keyword Group Frequency
    plt.figure(figsize=(10, 6))
    df['keyword_group'].value_counts().plot(kind='bar', color=['skyblue', 'salmon'])
    plt.title('키워드 그룹별 데이터 빈도')
    plt.ylabel('빈도')
    plt.xticks(rotation=0)
    plt.savefig('images/03_group_freq.png')
    plt.close()

    # 4. Bivariate: Trend over Time (Comparison)
    plt.figure(figsize=(12, 6))
    plt.plot(df_fan['date'], df_fan['ratio'], label='선풍기', color='blue')
    plt.plot(df_hot['date'], df_hot['ratio'], label='핫팩', color='red')
    plt.title('지난 1년간 선풍기 vs 핫팩 쇼핑 트렌드')
    plt.xlabel('날짜')
    plt.ylabel('클릭 비율 (Ratio)')
    plt.legend()
    plt.savefig('images/04_time_comparison.png')
    plt.close()

    # 5. Bivariate: Monthly Average Ratio
    df['month'] = df['date'].dt.month
    monthly_avg = df.groupby(['month', 'keyword_group'])['ratio'].mean().unstack()
    monthly_avg.plot(kind='bar', figsize=(10, 6), color=['skyblue', 'salmon'])
    plt.title('월별 평균 클릭 비율')
    plt.ylabel('평균 비율')
    plt.savefig('images/05_monthly_avg.png')
    plt.close()

    # 6. Bivariate: Boxplot by Keyword Group
    plt.figure(figsize=(10, 6))
    df.boxplot(column='ratio', by='keyword_group', grid=False)
    plt.title('키워드 그룹별 클릭 비율 박스플롯')
    plt.suptitle('')
    plt.savefig('images/06_boxplot_ratio.png')
    plt.close()

    # 7. Multivariate: Heatmap of Month vs Keyword Group
    pivot_data = df.pivot_table(index='month', columns='keyword_group', values='ratio', aggfunc='mean')
    plt.figure(figsize=(8, 6))
    plt.imshow(pivot_data, cmap='YlOrRd', aspect='auto')
    plt.colorbar(label='평균 비율')
    plt.xticks(range(len(pivot_data.columns)), pivot_data.columns)
    plt.yticks(range(len(pivot_data.index)), pivot_data.index)
    plt.title('월별/키워드별 클릭 비율 히트맵')
    plt.savefig('images/07_heatmap_month_keyword.png')
    plt.close()

    # 8. Time Component: Day of week analysis
    df['dayofweek'] = df['date'].dt.day_name()
    dow_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    dow_avg = df.groupby(['dayofweek', 'keyword_group'])['ratio'].mean().unstack().reindex(dow_order)
    dow_avg.plot(kind='line', marker='o', figsize=(10, 6))
    plt.title('요일별 평균 클릭 비율 변화')
    plt.ylabel('평균 비율')
    plt.savefig('images/08_dow_trend.png')
    plt.close()

    # 9. Cumulative Trend
    df_fan['cum_ratio'] = df_fan['ratio'].cumsum()
    df_hot['cum_ratio'] = df_hot['ratio'].cumsum()
    plt.figure(figsize=(12, 6))
    plt.fill_between(df_fan['date'], df_fan['cum_ratio'], label='선풍기(누적)', color='blue', alpha=0.3)
    plt.fill_between(df_hot['date'], df_hot['cum_ratio'], label='핫팩(누적)', color='red', alpha=0.3)
    plt.title('누적 클릭 비율 변화')
    plt.legend()
    plt.savefig('images/09_cumulative_ratio.png')
    plt.close()

    # 10. Quarterly Analysis
    df['quarter'] = df['date'].dt.quarter
    quarter_avg = df.groupby(['quarter', 'keyword_group'])['ratio'].mean().unstack()
    quarter_avg.plot(kind='pie', subplots=True, figsize=(15, 7), autopct='%1.1f%%', legend=False)
    plt.savefig('images/10_quarterly_pie.png')
    plt.close()

    # Output tables for the report
    print("\n--- PIVOT TABLE (MONTHLY) ---")
    print(pivot_data)
    print("\n--- DOW TABLE ---")
    print(dow_avg)
    print("\n--- QUARTER TABLE ---")
    print(quarter_avg)

if __name__ == "__main__":
    file_path = "data/shopping_trend_fan_hotpack_20260304.csv"
    perform_eda(file_path)
