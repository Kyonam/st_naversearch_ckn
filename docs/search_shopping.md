# 네이버 검색 > 쇼핑 API 구현 가이드

네이버 검색의 쇼핑 검색 결과를 XML 형식 또는 JSON 형식으로 반환하는 RESTful API입니다.

## 1. 개요
쇼핑 검색 API는 비로그인 방식 오픈 API로, 네이버 쇼핑의 상품 정보와 가격 정보를 실시간으로 조회할 수 있습니다.

- **프로토콜**: HTTPS
- **HTTP 메서드**: GET
- **하루 호출 한도**: 25,000회

## 2. 요청 URL
| 형식 | URL |
| :--- | :--- |
| JSON | `https://openapi.naver.com/v1/search/shop.json` |
| XML | `https://openapi.naver.com/v1/search/shop.xml` |

## 3. 요청 파라미터
| 파라미터 | 타입 | 필수 여부 | 설명 |
| :--- | :--- | :--- | :--- |
| `query` | String (UTF-8) | Y | 검색어. UTF-8로 인코딩되어야 합니다. |
| `display` | Integer | N | 한 번에 표시할 검색 결과 개수 (기본값: 10, 최댓값: 100) |
| `start` | Integer | N | 검색 시작 위치 (기본값: 1, 최댓값: 1000) |
| `sort` | String | N | 정렬 옵션: `sim` (유사도순), `date` (날짜순), `asc` (가격 오름차순), `dsc` (가격 내림차순) |
| `filter` | String | N | 필터 옵션: `naverpay` (네이버페이 상품만 검색) |
| `exclude` | String | N | 제외 옵션: `used` (중고 제외), `rental` (렌탈 제외), `cbshop` (해외직구 제외) |

## 4. 응답 필드
### 4.1. 공통 필드
| 필드 | 타입 | 설명 |
| :--- | :--- | :--- |
| `lastBuildDate` | datetime | 검색 결과가 생성된 시간 |
| `total` | Integer | 총 검색 결과 개수 |
| `start` | Integer | 검색 시작 위치 |
| `display` | Integer | 한 번에 표시된 검색 결과 개수 |
| `items` | Array | 개별 검색 결과 목록 |

### 4.2. 개별 아이템 필드 (`items`)
| 필드 | 타입 | 설명 |
| :--- | :--- | :--- |
| `title` | String | 상품의 명칭. 검색어와 일치하는 부분은 `<b>` 태그로 감싸져 있습니다. |
| `link` | String | 상품의 URL (네이버 쇼핑 결과 페이지로 이동) |
| `image` | String | 상품의 이미지 URL |
| `lprice` | Integer | 상품의 최저가 정보 |
| `hprice` | Integer | 상품의 최고가 정보 (정보가 없으면 0) |
| `mallName` | String | 상품을 판매하는 몰의 이름 |
| `productId` | Long | 상품의 고유 ID |
| `productType` | Integer | 상품군 타입: 1(일반상품), 2(중고상품), 3(단종상품) 등 |
| `brand` | String | 브랜드 이름 |
| `maker` | String | 제조사 이름 |
| `category1~4` | String | 상품의 카테고리 정보 (대분류, 중분류, 소분류, 세분류) |

## 5. 구현 예제 (Python)
```python
import os
import sys
import urllib.request

client_id = "YOUR_CLIENT_ID"
client_secret = "YOUR_CLIENT_SECRET"
encText = urllib.parse.quote("노트북")
url = "https://openapi.naver.com/v1/search/shop.json?query=" + encText + "&display=10&sort=sim"

request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id", client_id)
request.add_header("X-Naver-Client-Secret", client_secret)

try:
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if(rescode == 200):
        response_body = response.read()
        print(response_body.decode('utf-8'))
    else:
        print("Error Code: " + str(rescode))
except Exception as e:
    print(e)
```

## 6. 오류 코드
주요 오류 코드는 블로그 검색 API와 동일하며, `display`/`start`/`sort` 파라미터 오류 시 주로 발생합니다.

[원문 링크](https://developers.naver.com/docs/serviceapi/search/shopping/shopping.md)
