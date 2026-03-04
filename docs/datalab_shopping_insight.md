# 데이터랩 > 쇼핑인사이트 API 구현 가이드

네이버 쇼핑 영역에서의 검색 클릭 추이를 분야별로 조회할 수 있는 API입니다.

## 1. 개요
쇼핑인사이트 API는 비로그인 방식 오픈 API로, 상품 카테고리별 클릭 추이와 인기도를 다양한 조건(기기, 성별, 연령)으로 분석할 수 있습니다.

- **프로토콜**: HTTPS
- **HTTP 메서드**: POST
- **콘텐츠 타입**: `application/json`

## 2. 주요 요청 엔드포인트
- **분야별 트렌드**: `https://openapi.naver.com/v1/datalab/shopping/categories`
- **기기별 트렌드**: `https://openapi.naver.com/v1/datalab/shopping/category/device`
- **성별 트렌드**: `https://openapi.naver.com/v1/datalab/shopping/category/gender`
- **연령별 트렌드**: `https://openapi.naver.com/v1/datalab/shopping/category/age`

## 3. 주요 요청 파라미터 (분야별 트렌드 기준)
| 파라미터 | 타입 | 필수 | 설명 |
| :--- | :--- | :--- | :--- |
| `startDate` | String | Y | 시작 날짜 (YYYY-MM-DD) |
| `endDate` | String | Y | 종료 날짜 (YYYY-MM-DD) |
| `timeUnit` | String | Y | 구간 단위: `date`, `week`, `month` |
| `category` | Array | Y | 조회할 카테고리 정보 (최대 5개) |
| `category.name` | String | Y | 카테고리 명칭 |
| `category.param` | Array | Y | 카테고리 ID (8자리 코드) |
| `device` | String | N | `pc`, `mo` |
| `gender` | String | N | `m`, `f` |
| `ages` | Array | N | `10` (10~19세) ~ `60` (60세 이상) |

## 4. 응답 구조 예시
```json
{
  "startDate": "2023-08-01",
  "endDate": "2023-09-30",
  "timeUnit": "month",
  "results": [
    {
      "title": "패션의류",
      "category": ["50000000"],
      "data": [
        {"period": "2023-08-01", "ratio": 81.12},
        {"period": "2023-09-01", "ratio": 100.0}
      ]
    }
  ]
}
```

## 5. 구현 예제 (cURL)
```bash
curl "https://openapi.naver.com/v1/datalab/shopping/categories" \
  -H "X-Naver-Client-Id: {YOUR_CLIENT_ID}" \
  -H "X-Naver-Client-Secret: {YOUR_CLIENT_SECRET}" \
  -H "Content-Type: application/json" \
  -d '{
    "startDate": "2023-08-01",
    "endDate": "2023-09-30",
    "timeUnit": "month",
    "category": [{"name": "패션의류", "param": ["50000000"]}],
    "device": "pc",
    "gender": "f",
    "ages": ["20", "30"]
  }'
```

## 6. 참고 사항
- **카테고리 ID**: 네이버 쇼핑 카테고리 분류 가이드를 참조하여 8자리 코드를 사용해야 합니다.
- **비율(Ratio)**: 조회 기간 내 검색 클릭이 가장 많이 발생한 시점을 100으로 잡고 나머지 지점을 상대적으로 계산한 값입니다.

[원문 링크](https://developers.naver.com/docs/serviceapi/datalab/shopping/shopping.md)
