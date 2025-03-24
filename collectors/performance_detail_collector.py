# 2. 공연 상세 조회 (pblprfrService)
import requests
import pandas as pd
import xmltodict
import os
from dotenv import load_dotenv

load_dotenv()
SERVICE_KEY = os.getenv("SERVICE_KEY")

def collect_pblprfr_detail(mt20id, service_key=SERVICE_KEY):
    """
    2. 공연 상세 조회(pblprfrService)

    - mt20id: 공연ID (예: 'PF132236')
    - service_key: API 서비스 키
    """
    # 공연 상세 조회: /openApi/restful/pblprfr/{공연아이디}?service={SERVICE_KEY}
    endpoint = f"http://www.kopis.or.kr/openApi/restful/pblprfr/{mt20id}"
    params = {"service": service_key}

    response = requests.get(endpoint, params=params)
    response.raise_for_status()

    data_dict = xmltodict.parse(response.text)
    item = data_dict.get("dbs", {}).get("db", {})

    record = {
        "mt20id": item.get("mt20id"),
        "mt10id": item.get("mt10id"),
        "prfnm": item.get("prfnm"),
        "prfpdfrom": item.get("prfpdfrom"),
        "prfpdto": item.get("prfpdto"),
        "fcltynm": item.get("fcltynm"),
        "prfcast": item.get("prfcast"),
        "prfcrew": item.get("prfcrew"),
        "prfruntime": item.get("prfruntime"),
        "prfage": item.get("prfage"),
        "entrpsnmP": item.get("entrpsnmP"),
        "entrpsnmA": item.get("entrpsnmA"),
        "entrpsnmH": item.get("entrpsnmH"),
        "entrpsnmS": item.get("entrpsnmS"),
        "pcseguidance": item.get("pcseguidance"),
        "poster": item.get("poster"),
        "sty": item.get("sty"),
        "genrenm": item.get("genrenm"),
        "prfstate": item.get("prfstate"),
        "openrun": item.get("openrun"),
        "visit": item.get("visit"),
        "child": item.get("child"),
        "daehakro": item.get("daehakro"),
        "festival": item.get("festival"),
        "musicallicense": item.get("musicallicense"),
        "musicalcreate": item.get("musicalcreate"),
        "updatedate": item.get("updatedate"),
        "dtguidance": item.get("dtguidance")
    }

    df = pd.DataFrame([record])
    rename_dict = {
        "mt20id": "공연ID",
        "mt10id": "공연시설ID",
        "prfnm": "공연명",
        "prfpdfrom": "공연시작일",
        "prfpdto": "공연종료일",
        "fcltynm": "공연시설명",
        "prfcast": "공연출연진",
        "prfcrew": "공연제작진",
        "prfruntime": "공연런타임",
        "prfage": "관람연령",
        "entrpsnmP": "제작사",
        "entrpsnmA": "기획사",
        "entrpsnmH": "주최",
        "entrpsnmS": "주관",
        "pcseguidance": "티켓가격",
        "poster": "포스터경로",
        "sty": "줄거리",
        "genrenm": "공연장르",
        "prfstate": "공연상태",
        "openrun": "오픈런여부",
        "visit": "내한여부",
        "child": "아동공연여부",
        "daehakro": "대학로여부",
        "festival": "축제여부",
        "musicallicense": "뮤지컬라이센스",
        "musicalcreate": "뮤지컬창작",
        "updatedate": "최종수정일",
        "dtguidance": "공연시간"
    }
    df = df.rename(columns=rename_dict)

    return df
