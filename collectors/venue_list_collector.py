# 3. 공연시설 목록 조회 (prfplcService) - 페이지 반복 수집 예시
import requests
import pandas as pd
import xmltodict
import os
import time
from dotenv import load_dotenv

load_dotenv()
SERVICE_KEY = os.getenv("SERVICE_KEY")

def collect_prfplc_list(
    rows=100,
    max_pages=999,
    shprfnmfct=None,
    fcltychartr=None,
    signgucode=None,
    signgucodesub=None,
    afterdate=None,
    service_key=SERVICE_KEY,
    sleep_sec=0.0
):
    """
    3. 공연시설 목록 조회(prfplcService) - cpage 반복 로직 적용

    [파라미터]
    - rows: 페이지당 목록 수 (최대 100)
    - max_pages: 최대 페이지 (안전장치)
    - shprfnmfct: 공연시설명
    - fcltychartr: 공연시설특성코드
    - signgucode: 시도코드
    - signgucodesub: 구군코드
    - afterdate: 해당일자 이후 등록/수정된 항목만 (YYYYMMDD)
    - service_key: API 서비스 키 (.env에서 로드)
    - sleep_sec: 페이지 호출 간격(초)

    [출력]
    - 1페이지부터 max_pages까지 반복 수집한 공연시설 목록을 합친 pandas DataFrame
    """
    endpoint = "http://www.kopis.or.kr/openApi/restful/prfplc"
    all_pages = []  # 페이지별 결과 누적

    for page in range(1, max_pages + 1):
        # 1) 요청 파라미터
        params = {
            "service": service_key,
            "cpage": page,
            "rows": rows
        }
        if shprfnmfct:
            params["shprfnmfct"] = shprfnmfct
        if fcltychartr:
            params["fcltychartr"] = fcltychartr
        if signgucode:
            params["signgucode"] = signgucode
        if signgucodesub:
            params["signgucodesub"] = signgucodesub
        if afterdate:
            params["afterdate"] = afterdate

        # 2) 요청
        response = requests.get(endpoint, params=params)
        if response.status_code != 200:
            print(f"[collect_prfplc_list] HTTP Error {response.status_code}, page={page}")
            break

        # 3) XML -> dict 파싱
        try:
            data_dict = xmltodict.parse(response.text)
        except Exception as e:
            print(f"[collect_prfplc_list] XML 파싱 오류: {e}")
            break

        # OpenAPI 오류 태그 검사 (예: <OpenAPI_ServiceResponse>..)
        if "OpenAPI_ServiceResponse" in data_dict:
            print("[collect_prfplc_list] OpenAPI Error 응답:", data_dict)
            break

        # 4) 실제 목록 추출
        dbs = data_dict.get("dbs")
        if not dbs:
            print(f"[collect_prfplc_list] 'dbs' 태그 없음 -> 종료(page={page})")
            break

        items = dbs.get("db")
        if not items:
            print(f"[collect_prfplc_list] 'db' 태그 비었음 -> 종료(page={page})")
            break

        if isinstance(items, dict):
            items = [items]

        # 5) dict -> records -> DataFrame
        page_records = []
        for item in items:
            page_records.append({
                "mt10id":        item.get("mt10id"),        # 공연시설 ID
                "fcltynm":       item.get("fcltynm"),       # 공연시설명
                "mt13cnt":       item.get("mt13cnt"),       # 공연장 수
                "fcltychartr":   item.get("fcltychartr"),   # 시설특성코드
                "sidonm":        item.get("sidonm"),        # 시도명
                "gugunnm":       item.get("gugunnm"),       # 구군명
                "opende":        item.get("opende")         # 개관연도
            })

        df_page = pd.DataFrame(page_records)
        if df_page.empty:
            print(f"[collect_prfplc_list] 페이지 {page} 결과 0건 -> 종료")
            break

        all_pages.append(df_page)

        # 페이지 호출 간격
        if sleep_sec > 0:
            time.sleep(sleep_sec)

        # rows보다 적게 왔으면 마지막 페이지로 간주 -> 종료
        if len(df_page) < rows:
            print(f"[collect_prfplc_list] (page={page}) 마지막 페이지로 판단 -> 종료")
            break

    # 6) 전체 병합
    if not all_pages:
        return pd.DataFrame()

    df_merged = pd.concat(all_pages, ignore_index=True)

    # 컬럼명 변경
    rename_dict = {
        "mt10id":      "공연시설ID",
        "fcltynm":     "공연시설명",
        "mt13cnt":     "공연장수",
        "fcltychartr": "시설특성코드",
        "sidonm":      "시도명",
        "gugunnm":     "구군명",
        "opende":      "개관연도"
    }
    df_merged = df_merged.rename(columns=rename_dict)

    return df_merged
