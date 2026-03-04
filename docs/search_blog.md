# 네이버 검색 > 블로그 API 구현 가이드

네이버 검색의 블로그 검색 결과를 XML 형식 또는 JSON 형식으로 반환하는 RESTful API입니다.

## 1. 개요
블로그 검색 API는 비로그인 방식 오픈 API입니다. HTTP 요청 헤더에 클라이언트 아이디와 클라이언트 시크릿 값만 전송하여 사용할 수 있습니다.

- **프로토콜**: HTTPS
- **HTTP 메서드**: GET
- **하루 호출 한도**: 25,000회

## 2. 요청 URL
| 형식 | URL |
| :--- | :--- |
| JSON | `https://openapi.naver.com/v1/search/blog.json` |
| XML | `https://openapi.naver.com/v1/search/blog.xml` |

## 3. 요청 파라미터
| 파라미터 | 타입 | 필수 여부 | 설명 |
| :--- | :--- | :--- | :--- |
| `query` | String (UTF-8) | Y | 검색어. UTF-8로 인코딩되어야 합니다. |
| `display` | Integer | N | 한 번에 표시할 검색 결과 개수 (기본값: 10, 최댓값: 100) |
| `start` | Integer | N | 검색 시작 위치 (기본값: 1, 최댓값: 1000) |
| `sort` | String | N | 정렬 옵션: `sim` (유사도순), `date` (날짜순) |

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
| `title` | String | 블로그 포스트의 제목. 검색어와 일치하는 부분은 `<b>` 태그로 감싸져 있습니다. |
| `link` | String | 블로그 포스트의 URL |
| `description` | String | 블로그 포스트의 본문 요약 내용 |
| `bloggername` | String | 블로그의 이름 |
| `bloggerlink` | String | 블로그의 주소 |
| `postdate` | String | 블로그 포스트가 작성된 날짜 (YYYYMMDD 형식) |

## 5. 구현 예제
### 5.1. cURL
```bash
curl "https://openapi.naver.com/v1/search/blog.json?query=%EB%A6%AC%EB%B7%B0&display=10&start=1&sort=sim" \
    -H "X-Naver-Client-Id: {YOUR_CLIENT_ID}" \
    -H "X-Naver-Client-Secret: {YOUR_CLIENT_SECRET}" -v
```

### 5.2. Python
```python
import os
import sys
import urllib.request
client_id = "YOUR_CLIENT_ID"
client_secret = "YOUR_CLIENT_SECRET"
encText = urllib.parse.quote("리뷰")
url = "https://openapi.naver.com/v1/search/blog?query=" + encText # JSON 결과
# url = "https://openapi.naver.com/v1/search/blog.xml?query=" + encText # XML 결과
request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id",client_id)
request.add_header("X-Naver-Client-Secret",client_secret)
response = urllib.request.urlopen(request)
rescode = response.getcode()
if(rescode==200):
    response_body = response.read()
    print(response_body.decode('utf-8'))
else:
    print("Error Code:" + rescode)
```

## 6. 오류 코드
| 코드 | 메시지 | 설명 |
| :--- | :--- | :--- |
| 400 | Bad Request | 요청 파라미터가 잘못되었습니다. |
| 401 | Unauthorized | 인증에 실패했습니다. (Client ID/Secret 확인) |
| 403 | Forbidden | API 권한이 없거나 호출 한도를 초과했습니다. |
| 404 | Not Found | 요청 경로가 잘못되었습니다. |
| 500 | Internal Server Error | 서버 내부 오류가 발생했습니다. |

[원문 링크](https://developers.naver.com/docs/serviceapi/search/blog/blog.md)
