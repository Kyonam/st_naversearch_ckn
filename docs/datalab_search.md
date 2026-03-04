# 데이터랩 > 통합 검색어 트렌드 API 구현 가이드

네이버 통합검색 내에서 검색어의 상대적 트렌드를 조회할 수 있는 API입니다.

## 1. 개요
통합 검색어 트렌드 API는 비로그인 방식 오픈 API로, 사용자가 설정한 기간 동안 특정 검색어의 인기도 추이를 데이터로 반환합니다.

- **프로토콜**: HTTPS
- **HTTP 메서드**: POST
- **콘텐츠 타입**: `application/json`

## 2. 요청 URL
```
https://openapi.naver.com/v1/datalab/search
```

## 3. 요청 파라미터 (JSON Body)
| 파라미터 | 타입 | 필수 | 설명 |
| :--- | :--- | :--- | :--- |
| `startDate` | String | Y | 조회 시작 날짜 (YYYY-MM-DD) |
| `endDate` | String | Y | 조회 종료 날짜 (YYYY-MM-DD) |
| `timeUnit` | String | Y | 구간 단위: `date`, `week`, `month` |
| `keywordGroups` | Array | Y | 검색어 그룹 목록 (최대 5개) |
| `keywordGroups.groupName` | String | Y | 그룹 명칭 |
| `keywordGroups.keywords` | Array | Y | 그룹에 포함될 검색어들 (최대 20개) |
| `device` | String | N | 기기 구분: `pc` (PC), `mo` (모바일) |
| `ages` | Array | N | 연령대 구분: `1` (0~12세) ~ `11` (60세 이상) |
| `gender` | String | N | 성별 구분: `m` (남성), `f` (여성) |

## 4. 응답 필드
| 필드 | 타입 | 설명 |
| :--- | :--- | :--- |
| `startDate` | String | 조회 시작 날짜 |
| `endDate` | String | 조회 종료 날짜 |
| `timeUnit` | String | 구간 단위 |
| `results` | Array | 검색 결과 데이터 |
| `results.title` | String | 검색어 그룹 제목 |
| `results.keywords` | Array | 그룹 내 포함된 검색어들 |
| `results.data` | Array | 구간별 트렌드 데이터 |
| `results.data.period` | String | 구간 시작 날짜 |
| `results.data.ratio` | Double | 해당 구간의 검색 비율 (구간 내 최고 인기 시점을 100으로 기준) |

## 5. 구현 예제 (Python)
```python
import os
import sys
import urllib.request
import json

client_id = "YOUR_CLIENT_ID"
client_secret = "YOUR_CLIENT_SECRET"
url = "https://openapi.naver.com/v1/datalab/search"

body = {
    "startDate": "2023-01-01",
    "endDate": "2023-12-31",
    "timeUnit": "month",
    "keywordGroups": [
        {"groupName": "한글", "keywords": ["한글", "korean"]},
        {"groupName": "영어", "keywords": ["영어", "english"]}
    ],
    "device": "pc",
    "ages": ["1", "2"],
    "gender": "f"
}

request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id", client_id)
request.add_header("X-Naver-Client-Secret", client_secret)
request.add_header("Content-Type", "application/json")

response = urllib.request.urlopen(request, data=json.dumps(body).encode("utf-8"))
rescode = response.getcode()

if(rescode == 200):
    response_body = response.read()
    print(response_body.decode('utf-8'))
else:
    print("Error Code: " + str(rescode))
```

## 6. 응답 예시
```json
{
  "startDate": "2023-01-01",
  "endDate": "2023-12-31",
  "timeUnit": "month",
  "results": [
    {
      "title": "한글",
      "keywords": ["한글", "korean"],
      "data": [
        {"period": "2023-01-01", "ratio": 47.0},
        {"period": "2023-02-01", "ratio": 53.23}
      ]
    }
  ]
}
```

[원문 링크](https://developers.naver.com/docs/serviceapi/datalab/search/search.md)
