# 작업 지시서: 네이버 쇼핑 트렌드 수집 (선풍기 & 핫팩)

본 문서는 `docs/` 폴더 내의 명세서를 참조하여, **선풍기**와 **핫팩**에 대한 지난 1년간의 일자별 쇼핑 클릭 트렌드를 수집하는 절차를 안내합니다.

## 1. 개요
- **목적**: 계절성 상품인 '선풍기'와 '핫팩'의 연간 수요 변화 비교 분석.
- **대상 API**: 쇼핑인사이트 키워드별 트렌드 조회 API (`datalab_shopping_insight.md` 참조)
- **엔드포인트**: `https://openapi.naver.com/v1/datalab/shopping/category/keywords`

## 2. 수집 설정 (Parameters)
키워드 중심의 정밀한 분석을 위해 다음과 같이 파라미터를 설정합니다.

- **카테고리 ID (`category`)**: `50000003` (디지털/가전) 또는 수집 범위에 따라 조정
- **키워드 (`keyword`)**:
  - 그룹 1: `{"name": "선풍기", "param": ["선풍기", "에어컨팬"]}`
  - 그룹 2: `{"name": "핫팩", "param": ["핫팩", "손난로"]}`
- **조회 기간**: 현재부터 과거 1년 (일간 단위 `date`)

## 3. 실행 코드 (Python)

```python
import json
import urllib.request
from datetime import datetime, timedelta

client_id = "YOUR_CLIENT_ID"
client_secret = "YOUR_CLIENT_SECRET"
url = "https://openapi.naver.com/v1/datalab/shopping/category/keywords"

# 날짜 범위 (지난 1년)
end_date = datetime.now()
start_date = end_date - timedelta(days=365)

body = {
    "startDate": start_date.strftime('%Y-%m-%d'),
    "endDate": end_date.strftime('%Y-%m-%d'),
    "timeUnit": "date",
    "category": "50000003",  # 디지털/가전 카테고리 내 키워드 분석
    "keyword": [
        {"name": "선풍기", "param": ["선풍기"]},
        {"name": "핫팩", "param": ["핫팩"]}
    ],
    "device": "", 
    "gender": "",
    "ages": []
}

request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id", client_id)
request.add_header("X-Naver-Client-Secret", client_secret)
request.add_header("Content-Type", "application/json")

try:
    response = urllib.request.urlopen(request, data=json.dumps(body).encode("utf-8"))
    res_data = json.loads(response.read().decode("utf-8"))
    
    # 결과 파일 저장
    with open("fan_hotpack_trend.json", "w", encoding="utf-8") as f:
        json.dump(res_data, f, indent=2, ensure_ascii=False)
    print("데이터 수집 완료: fan_hotpack_trend.json")

except Exception as e:
    print(f"오류 발생: {e}")
```

## 4. 데이터 확인 포인트
1. **계절성 교차점 확인**: 선풍기 클릭이 줄어들고 핫팩 클릭이 급증하는 시점(주로 10월~11월)을 확인합니다.
2. **이상치 분석**: 한여름인데 핫팩 클릭이 발생하거나, 한겨울에 선풍기 클릭이 발생하는 특이 데이터를 점검합니다.
3. **상대 강도**: 두 키워드가 동시에 요청되므로, 한 카테고리 내에서 선풍기와 핫팩 중 어느 쪽이 연간 최대 클릭량이 더 높은지 `ratio: 100` 지점을 통해 비교할 수 있습니다.

## 5. 참고 문서
- [app_registration.md](file:///c:/Users/ckyonam/Downloads/st_naversearch/docs/app_registration.md): Client ID/Secret 확인법
- [datalab_shopping_insight.md](file:///c:/Users/ckyonam/Downloads/st_naversearch/docs/datalab_shopping_insight.md): 키워드 API 상세 명세
