# 19. 극작가 목록 조회 (prferService) - 페이지 반복 수집 예시
import requests
import pandas as pd
import xmltodict
import os
import time
from dotenv import load_dotenv

load_dotenv()
SERVICE_KEY = os.getenv("SERVICE_KEY")

def collect_prfer_list(
    stdate,
    eddate,
    rows=100,
    max_pages=999,
    shcate=None,
    shprfnm=None,
    shprfnmfct=None,
    prfplccd=None,
    signgucode=None,
    signgucodesub=None,
    kidstate=None,
    prfstate=None,
    afterdate=None,
    service_key=SERVICE_KEY,
    sleep_sec=0.0
):
    """
    19. 극작가 목록 조회(prferService) - 모든 페이지(cpage)를 반복 수집하여 DataFrame 병합

    [파라미터]
    - stdate, eddate: YYYYMMDD (최대 31일)
    - rows: 페이지당 목록 수 (최대 100)
    - max_pages: 최대 페이지 (안전장치)
    - shcate: 장르코드
    - shprfnm: 공연명
    - shprfnmfct: 공연시설명
    - prfplccd: 공연장코드
    - signgucode: 시도코드
    - signgucodesub: 구군코드
    - kidstate: 아동공연여부 (Y/N)
    - prfstate: 공연상태코드 (01,02,03)
    - afterdate: 해당일자 이후 등록/수정된 항목만 (YYYYMMDD)
    - service_key: .env 파일에서 불러온 API 서비스 키
    - sleep_sec: 페이지 호출 간격(초), 기본 0.0

    [출력]
    - 모든 페이지(cpage) 결과를 합친 pandas DataFrame
    """
    endpoint = "http://www.kopis.or.kr/openApi/restful/prfper"
    all_pages = []

    for page in range(1, max_pages + 1):
        # 1) 요청 파라미터 구성
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
        if shprfnmfct:
            params["shprfnmfct"] = shprfnmfct
        if prfplccd:
            params["prfplccd"] = prfplccd
        if signgucode:
            params["signgucode"] = signgucode
        if signgucodesub:
            params["signgucodesub"] = signgucodesub
        if kidstate:
            params["kidstate"] = kidstate
        if prfstate:
            params["prfstate"] = prfstate
        if afterdate:
            params["afterdate"] = afterdate

        # 2) 요청
        response = requests.get(endpoint, params=params)
        if response.status_code != 200:
            print(f"[collect_prfer_list_all] HTTP Error {response.status_code}, page={page}")
            break  # 필요 시 재시도 로직 추가 가능

        # 3) XML -> dict 파싱
        try:
            data_dict = xmltodict.parse(response.text)
        except Exception as e:
            print(f"[collect_prfer_list_all] XML 파싱 오류: {e}")
            break

        # OpenAPI 오류 태그 검사 (예: <OpenAPI_ServiceResponse>..)
        if "OpenAPI_ServiceResponse" in data_dict:
            print("[collect_prfer_list_all] OpenAPI Error 응답:", data_dict)
            break

        # 4) 실제 목록 추출
        dbs = data_dict.get("dbs")
        if not dbs:
            print(f"[collect_prfer_list_all] 'dbs' 태그 없음 -> 종료(page={page})")
            break

        items = dbs.get("db")
        if not items:
            print(f"[collect_prfer_list_all] 'db' 태그 비었음 -> 종료(page={page})")
            break

        if isinstance(items, dict):
            items = [items]

        # 5) dict -> records -> DataFrame
        page_records = []
        for item in items:
            page_records.append({
                "mt20id":     item.get("mt20id"),     # 공연ID
                "prfnm":      item.get("prfnm"),      # 공연명
                "prfpdfrom":  item.get("prfpdfrom"),  # 공연시작일
                "prfpdto":    item.get("prfpdto"),    # 공연종료일
                "fcltynm":    item.get("fcltynm"),    # 공연시설명
                "poster":     item.get("poster"),     # 포스터경로
                "genrenm":    item.get("genrenm"),    # 공연장르
                "prfstate":   item.get("prfstate"),   # 공연상태
                "author":     item.get("author"),     # 원작자
                "creator":    item.get("creator")     # 창작자
            })

        df_page = pd.DataFrame(page_records)
        if df_page.empty:
            print(f"[collect_prfer_list_all] 페이지 {page} 결과 0건 -> 종료")
            break

        all_pages.append(df_page)

        # 페이지 호출 간격
        if sleep_sec > 0:
            time.sleep(sleep_sec)

        # rows보다 적게 왔다면 마지막 페이지로 간주 -> 종료
        if len(df_page) < rows:
            print(f"[collect_prfer_list_all] (page={page}) 마지막 페이지로 판단 -> 종료")
            break

    # 6) 전체 병합
    if not all_pages:
        return pd.DataFrame()

    df_merged = pd.concat(all_pages, ignore_index=True)

    # 컬럼명 변경
    rename_dict = {
        "mt20id":    "공연ID",
        "prfnm":     "공연명",
        "prfpdfrom": "공연시작일",
        "prfpdto":   "공연종료일",
        "fcltynm":   "공연시설명",
        "poster":    "포스터경로",
        "genrenm":   "공연장르",
        "prfstate":  "공연상태",
        "author":    "원작자",
        "creator":   "창작자"
    }
    df_merged = df_merged.rename(columns=rename_dict)

    return df_merged
