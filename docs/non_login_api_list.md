# 네이버 오픈API 종류 (비로그인 방식) 상세 가이드

비로그인 방식 오픈 API는 번거로운 사용자 인증(OAuth 2.0) 과정 없이, 발급받은 '클라이언트 아이디'와 '클라이언트 시크릿'만 사용하여 바로 호출할 수 있는 API들입니다.

## 1. 개요 및 인증 방식
- **인증 방식**: HTTP 헤더에 아래 값을 포함하여 GET 또는 POST 요청을 보냅니다.
    - `X-Naver-Client-Id`: {발급받은 Client ID}
    - `X-Naver-Client-Secret`: {발급받은 Client Secret}
- **특징**: 네이버 로그인을 통한 액세스 토큰 획득 과정이 필요 없습니다.

## 2. 비로그인 방식 API 목록 및 엔드포인트

### 2.1. 검색 API (Search API)
가장 많이 사용되는 비로그인 방식 API입니다.
- **블로그 검색**: `https://openapi.naver.com/v1/search/blog.json`
- **뉴스 검색**: `https://openapi.naver.com/v1/search/news.json`
- **쇼핑 검색**: `https://openapi.naver.com/v1/search/shop.json`
- **웹 문서 검색**: `https://openapi.naver.com/v1/search/webkr.json`
- **지식iN 검색**: `https://openapi.naver.com/v1/search/kin.json`
- **도서 검색**: `https://openapi.naver.com/v1/search/book.json`
- **카페글 검색**: `https://openapi.naver.com/v1/search/cafearticle.json`
- **지역 검색**: `https://openapi.naver.com/v1/search/local.json`
- **성인 검색어 판별**: `https://openapi.naver.com/v1/search/adult.json`
- **오타 변환**: `https://openapi.naver.com/v1/search/errata.json`

### 2.2. 데이터랩 API (DataLab API)
네이버 대용량 데이터를 통계적으로 조회합니다.
- **검색어 트렌드**: `https://openapi.naver.com/v1/datalab/search`
- **쇼핑인사이트 (카테고리)**: `https://openapi.naver.com/v1/datalab/shopping/categories`
- **쇼핑인사이트 (키워드)**: `https://openapi.naver.com/v1/datalab/shopping/category/keywords`

### 2.3. 기타 기능 API
- **이미지 캡차**: `https://openapi.naver.com/v1/captcha/nkey` (키 발급)
- **음성 캡차**: `https://openapi.naver.com/v1/captcha/skey` (키 발급)
- **Clova Face Recognition (얼굴인식)**: `https://openapi.naver.com/v1/vision/face`
- **Clova Face Recognition (유명인 인식)**: `https://openapi.naver.com/v1/vision/celebrity`
- **단축 URL**: `https://openapi.naver.com/v1/util/shorturl`

## 3. 호출 한도 (Quota)
- 각 API마다 하루 호출 한도가 정해져 있으며, 대개 하루 **25,000회**입니다.
- 호출 한도는 매일 오전 0시(KST)를 기준으로 초기화됩니다.
- 자세한 한도는 네이버 개발자 센터 `내 애플리케이션 > 통계` 탭에서 실시간으로 확인할 수 있습니다.

[원문 링크](https://developers.naver.com/docs/common/openapiguide/apilist.md)
