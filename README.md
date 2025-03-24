# 1. 사용 가이드

KOPIS Open API는 여러 **서비스 단위의 데이터를 제공**합니다.  
본 데이터 수집기는 총 **19개 서비스**를 **3가지 유형**으로 분류하여 기능을 구성하였습니다.

- **기간을 설정값으로 받는 데이터**
  - 수집 기간 기준으로 수집
- **개별 상세 조회 데이터**
  - 공연, 공연시설을 지정하여 상세 조회
- **일괄 수집 데이터**
  - 일괄 수집 가능한 정적 데이터(전국 공연시설 목록 등)

### 1. **KOPIS Open API 키 발급 신청**

- 아래 URL에서 신청 -> 이메일로 발급
- https://www.kopis.or.kr/por/cs/openapi/openApiUseSend.do?menuId=MNU_00074

### 2. **필요 라이브러리 설치**

- 터미널에서 입력
- 실행 경로는 프로젝트 루트(README.md가 있는 폴더, .\kopis_data_collector )

```
pip install -r requirements.txt
```

- 위 코드로 설치 혹은 아래 라이브러리 개별 설치 (수업에서 사용하지 라이브러리입니다.)
  - xmltodict
  - python-dotenv

### 3. **.env 파일을 생성하여 SERVICE_KEY 변수에 키 설정**

```python
SERVICE_KEY=<api키>
```

### 4. **config.py** 수집 설정값 입력

```python
# 수집 기간 설정 (수집 기간을 설정값으로 받는 데이터의 설정값)
START_DATE = "20230101"
END_DATE = "20230228"

# 상세조회 할 공연과 공연시설 코드 설정 (상세 조회 데이터의 설정값)
PERFORMANCE_CODE = "PF200099" # 예시) 이프덴[뮤지컬]
VENUE_CODE = "FC000001" # 예시) 예술의전당
```

### 5. **기간을 설정값으로 받는 데이터 수집**

- 터미널에서 입력
- 실행 경로는 프로젝트 루트(README.md가 있는 폴더, .\kopis_data_collector )

```
python -m main.collect_date_range
```

- **수집 대상**
  - 1. 공연목록 조회 (pblprfrService)
  - 6. 예매상황판 조회 (boxofficeService)
  - 7. 예매통계 기간별 조회 (boxStatsService)
  - 8. 예매통계 장르별 조회 (boxStatsCateService)
  - 9. 예매통계 시간대별 조회 (boxStatsTimeService)
  - 10. 예매통계 가격대별 조회 (boxStatsPriceService)
  - 11. 공연통계 기간별 통계 목록 조회 (prfstsTotalService)
  - 12. 지역별 통계 목록 조회 (prfstsAreaService)
  - 13. 장르별 통계 목록 조회 (prfstsCateService)
  - 14. 공연별 통계 목록 조회 (prfstsPrfByService)
  - 15. 공연시설별 통계 목록 조회 (prfstsPrfByFctService)
  - 16. 가격대별 통계 목록 조회 (prfstsPriceService)
  - 17. 수상작 목록 조회 (prfawadService)
  - 18. 축제 목록 조회 (prffestService)
  - 19. 극작가 목록 조회 (prferService)
- 위치 : data_date_range

### 5. **개별 상세 조회 데이터 수집**

- 터미널에서 입력
- 실행 경로는 프로젝트 루트(README.md가 있는 폴더, .\kopis_data_collector )

```
python -m main.collect_detail
```

- **수집 대상**
  - 2. 공연 상세 조회 (pblprfrService)
  - 4. 공연시설 상세 조회 (pblprfrService)
- 위치 : data_detail

### 6. **일괄 수집 데이터 수집**

- 터미널에서 입력
- 실행 경로는 프로젝트 루트(README.md가 있는 폴더, .\kopis_data_collector )

```
python -m main.collect_facility
```

- **수집 대상**
  - 3. 공연시설 목록 조회 (prfplcService)
  - 5. 기획/제작사 목록 조회 (mnfctService)
- 위치 : data_facility

</br>

---

</br>

# 2. 서비스 목록

### 1. **공연목록 조회 서비스**

- **기능:** 지정한 기간 내의 공연 목록 조회
- **주요 파라미터:**
  - 공연 시작일 (stdate)
  - 종료일 (eddate)
  - 페이지 정보 등
- **반환 데이터:**
  - 공연 ID, 공연명, 장르, 공연 상태, 공연 기간
  - 포스터 경로, 공연시설명, 지역 등
- **특징:** 날짜, 장르, 지역 등의 필터 적용 가능

### 2. **공연 상세 조회 서비스**

- **기능:** 특정 공연의 상세 정보 조회
- **주요 파라미터:**
  - 공연 ID (mt20id)
- **반환 데이터:**
  - 공연명, 시작/종료일, 출연진, 제작진, 런타임, 관람 연령
  - 포스터 및 소개 이미지 등
- **특징:** 공연 목록 조회 결과에서 선택한 공연의 자세한 정보 제공

### 3. **공연시설 목록 조회 서비스**

- **기능:** 공연이 진행되는 시설(공연장, 예술의전당 등) 목록 조회
- **주요 파라미터:**
  - 시설명 (필터)
  - 지역 코드 (시도, 구군)
  - 페이지 정보 등
- **반환 데이터:**
  - 공연시설 ID, 시설명, 공연장 수, 지역 정보, 개관연도 등
- **특징:** 지역별 또는 시설명 필터로 검색 가능

### 4. **공연시설 상세 조회 서비스**

- **기능:** 선택한 공연시설의 상세 정보 조회
- **주요 파라미터:**
  - 공연시설 ID
- **반환 데이터:**
  - 시설명, 개관연도, 좌석 수, 전화번호, 주소
  - 부대시설(레스토랑, 카페, 주차지 등) 정보
- **특징:** 공연시설의 구체적인 정보와 편의시설 정보 제공

### 5. **기획/제작사 목록 조회 서비스**

- **기능:** 공연 기획 및 제작에 참여한 업체 목록 조회
- **주요 파라미터:**
  - 업체명 (필터)
  - 페이지 정보 등
- **반환 데이터:**
  - 기획/제작사 ID, 업체명, 장르, 연락처, 홈페이지 등
- **특징:** 기획 및 제작 업체 정보를 한눈에 확인 가능

### 6. **예매상황판 조회 서비스**

- **기능:** 특정 기간 또는 실시간 예매 상황 조회
- **주요 파라미터:**
  - 시작/종료날짜
  - 특정 날짜
  - 장르 구분 코드, 지역 코드, 좌석 규모 등
- **반환 데이터:**
  - 순위, 공연명, 공연 기간, 공연장명
  - 좌석 수, 상연 횟수, 포스터 경로 등
- **특징:** 예매 현황을 통해 공연별 티켓 판매 동향 분석 가능

### 7. **예매통계 기간별 조회 서비스**

- **기능:** 일별 또는 주별 예매 통계 조회
- **주요 파라미터:**
  - 날짜 코드 (ststype: day, week)
  - 시작일, 종료일
- **반환 데이터:**
  - 날짜별 공연 건수, 상연 횟수, 예매 수, 취소 수
  - 총 티켓 판매 수, 판매액 등
- **특징:** 시간에 따른 티켓 판매 추이 파악 가능

### 8. **예매통계 장르별 조회 서비스**

- **기능:** 공연 장르별 예매 통계 집계
- **주요 파라미터:**
  - 시작일, 종료일
  - 장르 구분 코드 (예: AAAA: 연극, GGGA: 뮤지컬 등)
- **반환 데이터:**
  - 장르명, 공연 건수, 상연 횟수, 예매 수, 취소 수, 총 판매액 등
- **특징:** 장르별 관객 동향 및 매출 비중 분석 가능

### 9. **예매통계 시간대별 조회 서비스**

- **기능:** 공연 예매가 이루어진 시간대별 통계 제공
- **주요 파라미터:**
  - 시작일, 종료일
- **반환 데이터:**
  - 각 시간대별 공연 건수, 예매 수, 취소 수, 판매액 등
- **특징:** 예매 활동 집중 시간대 분석 및 마케팅 전략 수립에 활용 가능

### 10. **예매통계 가격대별 조회 서비스**

- **기능:** 티켓 가격대별 예매 통계 조회
- **주요 파라미터:**
  - 시작일, 종료일
- **반환 데이터:**
  - 가격대, 예매 수, 취소 수, 총 판매액, 가격대별 비중 등
- **특징:** 티켓 가격 분포와 매출 구조 분석 가능

### 11. **공연통계 기간별 통계 목록 조회 서비스**

- **기능:** 전체 공연에 대한 기간별(일별, 주별, 월별) 통계 정보 제공
- **주요 파라미터:**
  - 날짜 코드 (ststype: day, week, month)
  - 시작일, 종료일
- **반환 데이터:**
  - 공연 건수, 개막편수, 상연 횟수, 매출액, 총 티켓 판매 수 등
- **특징:** 공연 전반의 성과를 시간에 따라 분석 가능

### 12. **지역별 통계 목록 조회 서비스**

- **기능:** 지역별 공연 및 시설 관련 통계 데이터 제공
- **주요 파라미터:**
  - 시작일, 종료일
- **반환 데이터:**
  - 지역명, 공연시설 수, 공연장 수, 총 좌석 수
  - 공연 건수, 판매 수, 매출액 등
- **특징:** 지역별 문화 인프라와 공연 시장 규모 파악 가능

### 13. **장르별 통계 목록 조회 서비스**

- **기능:** 공연 장르에 따른 통계 데이터 집계
- **주요 파라미터:**
  - 시작일, 종료일
- **반환 데이터:**
  - 장르명, 개막편수, 상연 횟수, 매출액, 관객 수, 점유율 등
- **특징:** 특정 장르의 성과 및 시장 점유율 분석 가능

### 14. **공연별 통계 목록 조회 서비스**

- **기능:** 개별 공연의 상세 통계 데이터 제공
- **주요 파라미터:**
  - 공연명, 장르 코드, 기간, 페이지 정보 등
- **반환 데이터:**
  - 공연명, 공연 ID, 장르, 공연시설명, 기획/제작사, 상연 횟수 등
- **특징:** 개별 공연 단위의 성과를 심도 있게 분석할 때 사용

### 15. **공연시설별 통계 목록 조회 서비스**

- **기능:** 공연시설(공연장) 단위의 통계 조회
- **주요 파라미터:**
  - 시설명 (필터), 지역 코드, 시작일, 종료일
- **반환 데이터:**
  - 시설명, 공연장명, 좌석 수, 공연 건수, 상연 횟수, 총 티켓 판매 수 등
- **특징:** 각 시설의 운영 성과와 활용도를 비교 분석 가능

### 16. **가격대별 통계 목록 조회 서비스**

- **기능:** 티켓 가격대별 공연 통계 데이터 제공
- **주요 파라미터:**
  - 시작일, 종료일
- **반환 데이터:**
  - 가격대, 예매 수, 취소 수, 총 판매액, 가격대별 비중 등
- **특징:** 티켓 가격 정책 및 매출 구조 분석에 활용

### 17. **수상작 목록 조회 서비스**

- **기능:** 수상 경력이 있는 공연 목록 조회
- **주요 파라미터:**
  - 공연 시작일, 종료일, 페이지 정보
  - 필터 조건 (공연명, 시설 등)
- **반환 데이터:**
  - 공연 ID, 공연명, 수상 내역, 포스터, 장르, 공연 상태 등
- **특징:** 수상 경력을 통해 작품의 예술적 가치 평가 가능

### 18. **축제 목록 조회 서비스**

- **기능:** 공연예술 관련 축제 정보 조회
- **주요 파라미터:**
  - 공연 시작일, 종료일, 페이지 정보
  - 필터 조건 등
- **반환 데이터:**
  - 공연 ID, 공연명, 축제 여부, 장르, 시설 정보 등
- **특징:** 축제 성격의 공연 및 이벤트 정보 파악 가능

### 19. **극작가 목록 조회 서비스**

- **기능:** 극작가 관련 정보 조회
- **주요 파라미터:**
  - 공연명 등 필요에 따른 필터
- **반환 데이터:**
  - 극작가 이름, 관련 공연 정보 등
- **특징:** 극작가의 활동 내역과 작품 정보를 분석하는 데 활용

</br>

---

# 3. collector 파일 = 서비스명 대조표

</br>

| **File Name**                            | **Service**                                           | **Description**                                                                                                                |
| ---------------------------------------- | ----------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| **performance_list_collector.py**        | 1. 공연목록 조회 (pblprfrService)                     | 기간(최대 31일) 내 공연목록(공연ID, 공연명, 장르, 공연상태 등) 조회                                                            |
| **performance_detail_collector.py**      | 2. 공연 상세 조회 (pblprfrService)                    | 특정 공연ID의 상세 정보(출연진, 제작진, 런타임, 관람연령 등)                                                                   |
| **venue_list_collector.py**              | 3. 공연시설 목록 조회 (prfplcService)                 | 공연시설 목록(시설ID, 시설명, 지역, 공연장수, 개관연도 등) 조회                                                                |
| **venue_detail_collector.py**            | 4. 공연시설 상세 조회 (pblprfrService)                | 특정 공연시설ID의 상세 정보(좌석수, 편의시설, 전화번호, 주소 등), <br> 개발가이드 오류 - 엔드포인트 끝 pblprfr이 아닌 prfplc임 |
| **production_company_list_collector.py** | 5. 기획/제작사 목록 조회 (mnfctService)               | 기획/제작사 목록(기획사명, 장르, 전화번호, 최신작품 등) 조회                                                                   |
| **boxoffice_status_collector.py**        | 6. 예매상황판 조회 (boxofficeService)                 | 예매상황판(일자별/구간별 공연 순위, 공연명, 기간, 좌석수 등) 조회                                                              |
| **ticketstats_period_collector.py**      | 7. 예매통계 기간별 조회 (boxStatsService)             | 예매통계(일/주별) 예매수, 취소수, 총티켓판매수, 총티켓판매액 등 조회                                                           |
| **ticketstats_genre_collector.py**       | 8. 예매통계 장르별 조회 (boxStatsCateService)         | 장르별 예매통계(공연건수, 상연횟수, 예매수, 매출액 등) 조회                                                                    |
| **ticketstats_time_collector.py**        | 9. 예매통계 시간대별 조회 (boxStatsTimeService)       | 시간대별 예매통계(구간별 공연건수, 예매수, 판매액 등) 조회                                                                     |
| **ticketstats_price_collector.py**       | 10. 예매통계 가격대별 조회 (boxStatsPriceService)     | 가격대별 예매통계(예매수, 취소수, 총판매수, 매출액 등) 조회                                                                    |
| **perfstats_period_collector.py**        | 11. 기간별 통계 목록 조회 (prfstsTotalService)        | 공연통계(일/요일별) 개막편수, 상연횟수, 매출액, 관객수 등 조회                                                                 |
| **perfstats_area_collector.py**          | 12. 지역별 통계 목록 조회 (prfstsAreaService)         | 지역별 공연통계(공연시설수, 공연장수, 판매수, 매출액 등) 조회                                                                  |
| **perfstats_genre_collector.py**         | 13. 장르별 통계 목록 조회 (prfstsCateService)         | 장르별 공연통계(개막편수, 상연횟수, 매출액, 관객수 등) 조회                                                                    |
| **perfstats_byperformance_collector.py** | 14. 공연별 통계 목록 조회 (prfstsPrfByService)        | 공연별 통계(공연명, 공연시설명, 상연횟수, 기획/제작사 등) 조회                                                                 |
| **perfstats_byvenue_collector.py**       | 15. 공연시설별 통계 목록 조회 (prfstsPrfByFctService) | 공연시설별 통계(좌석수, 공연건수, 상연횟수, 총티켓판매수 등) 조회                                                              |
| **perfstats_price_collector.py**         | 16. 가격대별 통계 목록 조회 (prfstsPriceService)      | 가격대별 공연통계(예매수, 예매액, 취소수 등) 조회                                                                              |
| **awards_list_collector.py**             | 17. 수상작 목록 조회 (prfawadService)                 | 수상작 목록(공연ID, 공연명, 시설명, 수상실적 등) 조회                                                                          |
| **festival_list_collector.py**           | 18. 축제 목록 조회 (prffestService)                   | 축제 목록(공연ID, 공연명, 기간, 시설명, 축제여부 등) 조회                                                                      |
| **playwright_list_collector.py**         | 19. 극작가 목록 조회 (prferService)                   | 극작가 목록(공연명, 원작자·창작자, 공연장르, 공연상태 등) 조회                                                                 |

---

### cpage & rows 지원 서비스 목록

- (1번) 공연목록 조회   (pblprfrService)
- (3번) 공연시설 목록 조회   (prfplcService)
- (5번) 기획/제작사 목록 조회   (mnfctService)
- (14번) 공연별 통계 목록 조회   (prfstsPrfByService)
- (15번) 공연시설별 통계 목록 조회   (prfstsPrfByFctService
- (17번) 수상작 목록 조회   (prfawadService)
- (18번) 축제 목록 조회   (prffestService)
- (19번) 극작가 목록 조회   (prferService)
