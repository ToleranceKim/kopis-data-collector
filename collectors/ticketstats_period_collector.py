# 7. 예매통계 기간별 조회 (boxStatsService)
import requests
import pandas as pd
import xmltodict
import os
from dotenv import load_dotenv

load_dotenv()
SERVICE_KEY = os.getenv("SERVICE_KEY")

def collect_boxstats(
    ststype,
    stdate,
    eddate,
    service_key=SERVICE_KEY
):
    """
    7. 예매통계 기간별 조회(boxStatsService)

    - ststype: 요청형태(day, dayWeek)
    - stdate, eddate: YYYYMMDD (최대 31일)
    - service_key: API 서비스 키
    """
    endpoint = "http://www.kopis.or.kr/openApi/restful/boxStats"
    params = {
        "service": service_key,
        "ststype": ststype,
        "stdate": stdate,
        "eddate": eddate
    }

    response = requests.get(endpoint, params=params)
    response.raise_for_status()

    data_dict = xmltodict.parse(response.text)
    items = data_dict.get("box-statsofs", {}).get("boxStatsof", [])
    if isinstance(items, dict):
        items = [items]

    records = []
    for item in items:
        record = {
            "prfdt": item.get("prfdt"),
            "prfcnt": item.get("prfcnt"),
            "prfdtcnt": item.get("prfdtcnt"),
            "ntssnmrssm": item.get("ntssnmrssm"),
            "cancelnmrssm": item.get("cancelnmrssm"),
            "totnmrssm": item.get("totnmrssm"),
            "ntssamountsm": item.get("ntssamountsm")
        }
        records.append(record)

    df = pd.DataFrame(records)
    rename_dict = {
        "prfdt": "날짜",
        "prfcnt": "공연건수",
        "prfdtcnt": "상연횟수",
        "ntssnmrssm": "예매수",
        "cancelnmrssm": "취소수",
        "totnmrssm": "총티켓판매수",
        "ntssamountsm": "총티켓판매액"
    }
    df = df.rename(columns=rename_dict)

    return df
