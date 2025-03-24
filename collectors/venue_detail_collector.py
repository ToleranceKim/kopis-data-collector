# 4. 공연시설 상세 조회 (pblprfrService - 공연시설ID)
import requests
import pandas as pd
import xmltodict
import os
from dotenv import load_dotenv

load_dotenv()
SERVICE_KEY = os.getenv("SERVICE_KEY")

def collect_prfplc_detail(mt10id, service_key=SERVICE_KEY):
    """
    4. 공연시설 상세 조회 (pblprfrService? - {공연시설ID})
    - mt10id: 공연시설 ID (예: 'FC001247')
    - service_key: API 서비스 키
    """
    endpoint = f"http://www.kopis.or.kr/openApi/restful/prfplc/{mt10id}"
    params = {"service": service_key}

    response = requests.get(endpoint, params=params)
    response.raise_for_status()

    data_dict = xmltodict.parse(response.text)
    item = data_dict.get("dbs", {}).get("db", {})

    record = {
        "mt10id": item.get("mt10id"),
        "fcltynm": item.get("fcltynm"),
        "opende": item.get("opende"),
        "fcltychartr": item.get("fcltychartr"),
        "seatscale": item.get("seatscale"),
        "mt13cnt": item.get("mt13cnt"),
        "telno": item.get("telno"),
        "relateurl": item.get("relateurl"),
        "adres": item.get("adres"),
        "la": item.get("la"),
        "lo": item.get("lo"),
        "restaurant": item.get("restaurant"),
        "cafe": item.get("cafe"),
        "store": item.get("store"),
        "nolibang": item.get("nolibang"),
        "suyu": item.get("suyu"),
        "parkbarrier": item.get("parkbarrier"),
        "restbarrier": item.get("restbarrier"),
        "runwbarrier": item.get("runwbarrier"),
        "elevbarrier": item.get("elevbarrier"),
        "parkinglot": item.get("parkinglot")
    }

    df = pd.DataFrame([record])
    rename_dict = {
        "mt10id": "공연시설ID",
        "fcltynm": "공연시설명",
        "opende": "개관연도",
        "fcltychartr": "시설특성",
        "seatscale": "객석수",
        "mt13cnt": "공연장수",
        "telno": "전화번호",
        "relateurl": "홈페이지",
        "adres": "주소",
        "la": "위도",
        "lo": "경도",
        "restaurant": "레스토랑유무",
        "cafe": "카페유무",
        "store": "편의점유무",
        "nolibang": "놀이방유무",
        "suyu": "수유실유무",
        "parkbarrier": "장애시설(주차장)",
        "restbarrier": "장애시설(화장실)",
        "runwbarrier": "장애시설(경사로)",
        "elevbarrier": "장애시설(엘리베이터)",
        "parkinglot": "주차시설"
    }
    df = df.rename(columns=rename_dict)

    return df
