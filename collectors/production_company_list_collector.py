# 5. 기획/제작사 목록 조회 (mnfctService) - 모든 페이지 반복 수집
import requests
import pandas as pd
import xmltodict
import os
import time
from dotenv import load_dotenv

load_dotenv()
SERVICE_KEY = os.getenv("SERVICE_KEY")

def collect_mnfct_list(
    rows=100,
    max_pages=999,
    entrpsnm=None,
    shcate=None,
    afterdate=None,
    service_key=SERVICE_KEY,
    sleep_sec=0.0
):
    """
    5. 기획/제작사 목록 조회(mnfctService) - 페이지(cpage)를 자동으로 순회하며 전체 결과를 DataFrame으로 반환

    [파라미터]
    - rows: 페이지당 목록 수 (최대 100)
    - max_pages: 최대 페이지 수(안전장치)
    - entrpsnm: 기획/제작사명 (예: 국악단)
    - shcate: 장르코드 (AAAA=연극, BBBC=무용 등)
    - afterdate: 해당일자 이후 등록/수정된 항목만 (YYYYMMDD)
    - service_key: API 서비스 키(.env에서 로드)
    - sleep_sec: 페이지 호출 간격(초) (기본=0.0)

    [출력]
    - 모든 페이지를 합친 pandas DataFrame
    """

    endpoint = "http://www.kopis.or.kr/openApi/restful/mnfct"
    all_pages = []

    for page in range(1, max_pages + 1):
        # 1) 요청 파라미터
        params = {
            "service": service_key,
            "cpage": page,  # 여기서 페이지 자동 증가
            "rows": rows
        }
        if entrpsnm:
            params["entrpsnm"] = entrpsnm
        if shcate:
            params["shcate"] = shcate
        if afterdate:
            params["afterdate"] = afterdate

        # 2) 요청
        response = requests.get(endpoint, params=params)
        if response.status_code != 200:
            print(f"[collect_mnfct_list] HTTP Error {response.status_code} (page={page})")
            break

        # 3) XML 파싱
        try:
            data_dict = xmltodict.parse(response.text)
        except Exception as e:
            print(f"[collect_mnfct_list] XML 파싱 오류: {e} (page={page})")
            break

        # OpenAPI 오류 태그(<OpenAPI_ServiceResponse> 등) 검사
        if "OpenAPI_ServiceResponse" in data_dict:
            print("[collect_mnfct_list] OpenAPI Error 응답:", data_dict)
            break

        # 4) 실제 데이터 추출
        dbs = data_dict.get("dbs")
        if not dbs:
            print(f"[collect_mnfct_list] 'dbs' 태그 없음 -> 종료 (page={page})")
            break

        items = dbs.get("db")
        if not items:
            print(f"[collect_mnfct_list] 'db' 태그 비었음 -> 종료 (page={page})")
            break

        # 단일 dict -> list 변환
        if isinstance(items, dict):
            items = [items]

        # 5) dict -> record -> DataFrame
        page_records = []
        for item in items:
            page_records.append({
                "mt30id":   item.get("mt30id"),      # 기획/제작사 ID
                "entrpsnm": item.get("entrpsnm"),   # 기획/제작사명
                "genrenm":  item.get("genrenm"),    # 장르
                "telno":    item.get("telno"),      # 전화번호
                "prfnm":    item.get("prfnm"),      # 최신작품
                "relateurl": item.get("relateurl"), # 홈페이지
                "sidonm":   item.get("sidonm")      # 시도명
            })

        df_page = pd.DataFrame(page_records)
        if df_page.empty:
            print(f"[collect_mnfct_list] page={page} => 0건 -> 종료")
            break

        all_pages.append(df_page)

        # 페이지 호출 간격
        if sleep_sec > 0:
            time.sleep(sleep_sec)

        # rows보다 적게 오면 마지막 페이지로 판단 -> 종료
        if len(df_page) < rows:
            print(f"[collect_mnfct_list] page={page} => 마지막 페이지로 판단 -> 종료")
            break

    # 6) 전체 병합
    if not all_pages:
        return pd.DataFrame()

    df_merged = pd.concat(all_pages, ignore_index=True)
    rename_dict = {
        "mt30id":   "기획사ID",
        "entrpsnm": "기획사명",
        "genrenm":  "장르",
        "telno":    "전화번호",
        "prfnm":    "최신작품",
        "relateurl":"홈페이지",
        "sidonm":   "시도명"
    }
    df_merged = df_merged.rename(columns=rename_dict)

    return df_merged
