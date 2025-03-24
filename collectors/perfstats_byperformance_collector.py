# 14. 공연별 통계 목록 조회 (prfstsPrfByService) - 페이지 반복 수집 예시
import requests
import pandas as pd
import xmltodict
import os
import time
from dotenv import load_dotenv

load_dotenv()
SERVICE_KEY = os.getenv("SERVICE_KEY")

def collect_prfsts_prfby(
    stdate,
    eddate,
    rows=100,
    max_pages=999,
    shcate=None,
    shprfnm=None,
    service_key=SERVICE_KEY,
    sleep_sec=0.0
):
    """
    14. 공연별 통계 목록 조회(prfstsPrfByService), 모든 페이지(cpage) 반복하여 하나의 DataFrame으로 병합
    
    [파라미터]
    - stdate, eddate: YYYYMMDD 형식 (최대 31일)
    - rows: 페이지당 목록 수(최대 100)
    - max_pages: 최대 페이지(안전장치)
    - shcate: 장르코드 (예: AAAA=연극, BBBC=무용 등)
    - shprfnm: 공연명 (URL 인코딩 주의)
    - service_key: API 인증키(.env 에서 로드)
    - sleep_sec: 페이지 호출 간격(과도호출 방지용, 기본 0초)
    
    [출력]
    - 모든 페이지를 합친 pandas DataFrame
    """
    endpoint = "http://www.kopis.or.kr/openApi/restful/prfstsPrfBy"
    all_pages = []

    for page in range(1, max_pages + 1):
        # 1) 파라미터 구성
        params = {
            "service": service_key,
            "stdate": stdate,
            "eddate": eddate,
            "cpage": page,
            "rows": rows
        }
        if shcate:
            params["shcate"] = shcate
        if shprfnm:
            params["shprfnm"] = shprfnm

        # 2) 요청
        response = requests.get(endpoint, params=params)
        if response.status_code != 200:
            print(f"[collect_prfsts_prfby_all] HTTP Error {response.status_code}, page={page}")
            break  # 필요 시 재시도 로직을 넣어도 됨

        # 3) XML -> dict 파싱
        try:
            data_dict = xmltodict.parse(response.text)
        except Exception as e:
            print(f"[collect_prfsts_prfby_all] XML 파싱 오류: {e}")
            break

        # OpenAPI 에러 태그 검사(예: <OpenAPI_ServiceResponse>..)
        if "OpenAPI_ServiceResponse" in data_dict:
            print("[collect_prfsts_prfby_all] OpenAPI Error 응답:", data_dict)
            break

        # 4) 실제 목록 추출
        prfsts = data_dict.get("prfsts")
        if not prfsts:
            print(f"[collect_prfsts_prfby_all] 'prfsts' 태그 없음 -> 종료(page={page})")
            break

        items = prfsts.get("prfst")
        if not items:
            print(f"[collect_prfsts_prfby_all] 'prfst' 태그가 비었음 -> 종료(page={page})")
            break

        if isinstance(items, dict):
            items = [items]

        # 5) dict -> records -> DataFrame
        page_records = []
        for item in items:
            page_records.append({
                "prfnm":      item.get("prfnm"),      # 공연명
                "cate":       item.get("cate"),       # 장르
                "mt20id":     item.get("mt20id"),     # 공연ID
                "fcltynm":    item.get("fcltynm"),    # 공연시설명
                "entrpsnm":   item.get("entrpsnm"),   # 기획/제작사
                "prfpdfrom":  item.get("prfpdfrom"),  # 공연시작일
                "prfpdto":    item.get("prfpdto"),    # 공연종료일
                "prfdtcnt":   item.get("prfdtcnt")    # 상연횟수
            })

        df_page = pd.DataFrame(page_records)
        if df_page.empty:
            print(f"[collect_prfsts_prfby_all] 페이지 {page} 결과 0건 -> 종료")
            break

        all_pages.append(df_page)

        # 페이지 호출 간격
        if sleep_sec > 0:
            time.sleep(sleep_sec)

        # rows보다 실제 건수가 적다면 마지막 페이지로 간주 -> 종료
        if len(df_page) < rows:
            print(f"[collect_prfsts_prfby_all] (page={page}) 마지막 페이지로 판단 -> 종료")
            break

    # 전체 병합
    if not all_pages:
        return pd.DataFrame()

    df_merged = pd.concat(all_pages, ignore_index=True)

    # 컬럼명 변경
    rename_dict = {
        "prfnm": "공연명",
        "cate": "장르",
        "mt20id": "공연ID",
        "fcltynm": "공연시설명",
        "entrpsnm": "기획/제작사",
        "prfpdfrom": "공연시작일",
        "prfpdto": "공연종료일",
        "prfdtcnt": "상연횟수"
    }
    df_merged = df_merged.rename(columns=rename_dict)

    return df_merged
