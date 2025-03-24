# perfstats_area_collector.py

import requests
import pandas as pd
import xmltodict
import os
from dotenv import load_dotenv

load_dotenv()  # .env 로드
SERVICE_KEY = os.getenv("SERVICE_KEY")

def collect_prfsts_area(stdate, eddate, service_key=SERVICE_KEY):
    """
    12. 지역별 통계 목록 조회 (prfstsAreaService)
    - stdate, eddate: YYYYMMDD (최대 31일)
    - service_key: API 키
    """
    endpoint = "http://www.kopis.or.kr/openApi/restful/prfstsArea"
    params = {
        "service": service_key,
        "stdate": stdate,
        "eddate": eddate
    }

    response = requests.get(endpoint, params=params)
    response.raise_for_status()

    data_dict = xmltodict.parse(response.text)

    # 루트: <Prfsts>, 반복: <prfst>
    items = data_dict.get("prfsts", {}).get("prfst", [])
    if isinstance(items, dict):
        items = [items]

    records = []
    for item in items:
        record = {
            "area": item.get("area"),           # 지역명
            "fcltycnt": item.get("fcltycnt"),   # 공연시설수
            "prfplccnt": item.get("prfplccnt"), # 공연장수
            "seatcnt": item.get("seatcnt"),     # 총좌석수
            "prfcnt": item.get("prfcnt"),       # 공연건수
            "prfprcnt": item.get("prfprcnt"),   # 개막편수
            "prfdtcnt": item.get("prfdtcnt"),   # 상연횟수
            "nmrs": item.get("nmrs"),           # 판매수
            "nmrcancl": item.get("nmrcancl"),   # 취소수
            "totnmrs": item.get("totnmrs"),     # 총티켓판매수
            "amount": item.get("amount")        # 총티켓판매액
        }
        records.append(record)

    df = pd.DataFrame(records)
    rename_dict = {
        "area": "지역명",
        "fcltycnt": "공연시설수",
        "prfplccnt": "공연장수",
        "seatcnt": "총좌석수",
        "prfcnt": "공연건수",
        "prfprcnt": "개막편수",
        "prfdtcnt": "상연횟수",
        "nmrs": "판매수",
        "nmrcancl": "취소수",
        "totnmrs": "총티켓판매수",
        "amount": "총티켓판매액"
    }
    df = df.rename(columns=rename_dict)

    return df
