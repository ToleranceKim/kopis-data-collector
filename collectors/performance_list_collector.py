# performance_list_collector.py

import requests
import pandas as pd
import xmltodict
import os
from dotenv import load_dotenv

load_dotenv()
SERVICE_KEY = os.getenv("SERVICE_KEY")

def collect_pblprfr_list(
    stdate,
    eddate,
    cpage=1,
    rows=10,
    max_pages=999,
    shcate=None,
    shprfnm=None,
    shprfnmfct=None,
    prfplccd=None,
    signgucode=None,
    signgucodesub=None,
    kidstate=None,
    prfstate=None,
    openrun=None,
    afterdate=None,
    service_key=SERVICE_KEY,
    sleep_sec=0
):
    """
    (1) 공연목록 조회(pblprfrService) - 페이지를 모두 순회하여 한 번에 DataFrame으로 반환

    - stdate, eddate: YYYYMMDD (최대 31일)
    - rows: 페이지당 건수(최대 100)
    - max_pages: 안전장치(최대 페이지)
    - 기타 파라미터(장르코드, 공연명 등)도 필요시 인자로 받음
    - sleep_sec: 페이지 호출 간격(과도 호출 방지용)
    """

    # 결과 누적용
    all_dfs = []

    for cpage in range(1, max_pages + 1):
        # 파라미터 구성
        params = {
            "service": service_key,
            "stdate": stdate,
            "eddate": eddate,
            "cpage": cpage,
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
        if openrun:
            params["openrun"] = openrun
        if afterdate:
            params["afterdate"] = afterdate

        # 1) 요청
        response = requests.get("http://www.kopis.or.kr/openApi/restful/pblprfr", params=params)
        if response.status_code != 200:
            print(f"[collect_pblprfr_list_all] HTTP Error {response.status_code}")
            break  # HTTP 에러 시 중단 (또는 계속 시도할지 선택)

        # 2) XML 파싱
        try:
            data_dict = xmltodict.parse(response.text)
        except Exception as e:
            print(f"[collect_pblprfr_list_all] XML 파싱 오류: {e}")
            break

        # OpenAPI 오류 메시지 여부(예: <OpenAPI_ServiceResponse>...)
        if "OpenAPI_ServiceResponse" in data_dict:
            print("[collect_pblprfr_list_all] OpenAPI Error:", data_dict)
            break

        # 3) 실제 데이터 추출
        dbs = data_dict.get("dbs")
        if not dbs:
            # 더 이상 데이터 없거나 오류
            print(f"[collect_pblprfr_list_all] 'dbs' 태그 없음 -> 수집 종료 (page={cpage})")
            break

        items = dbs.get("db")
        if not items:
            print(f"[collect_pblprfr_list_all] 'db' 태그가 비었음 -> 수집 종료 (page={cpage})")
            break

        # 단일 객체 dict -> 리스트 변환
        if isinstance(items, dict):
            items = [items]

        # 4) records -> DataFrame
        records = []
        for item in items:
            records.append({
                "mt20id":     item.get("mt20id"),
                "prfnm":      item.get("prfnm"),
                "genrenm":    item.get("genrenm"),
                "prfstate":   item.get("prfstate"),
                "prfpdfrom":  item.get("prfpdfrom"),
                "prfpdto":    item.get("prfpdto"),
                "poster":     item.get("poster"),
                "fcltynm":    item.get("fcltynm"),
                "openrun":    item.get("openrun"),
                "area":       item.get("area")
            })
        df_page = pd.DataFrame(records)

        # 만약 실제 데이터가 0건이면 종료
        if df_page.empty:
            print(f"[collect_pblprfr_list_all] 페이지 {cpage} - 데이터 0건 -> 종료")
            break

        all_dfs.append(df_page)

        # 페이지 호출 간격
        if sleep_sec > 0:
            time.sleep(sleep_sec)

        # rows보다 실제 수가 적게 왔으면 마지막 페이지로 판단 -> 종료
        if len(df_page) < rows:
            print(f"[collect_pblprfr_list_all] (page={cpage}) 마지막 페이지로 판단, 수집 종료.")
            break

    # 5) 전체 병합
    if not all_dfs:
        return pd.DataFrame()

    df_merged = pd.concat(all_dfs, ignore_index=True)

    # 컬럼 rename
    rename_dict = {
        "mt20id": "공연ID",
        "prfnm": "공연명",
        "genrenm": "공연장르",
        "prfstate": "공연상태",
        "prfpdfrom": "공연시작일",
        "prfpdto": "공연종료일",
        "poster": "포스터경로",
        "fcltynm": "공연시설명",
        "openrun": "오픈런여부",
        "area": "공연지역"
    }
    df_merged = df_merged.rename(columns=rename_dict)

    return df_merged
