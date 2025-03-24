# 10. 예매통계 가격대별 조회 (boxStatsPriceService)
import requests
import pandas as pd
import xmltodict
import os
from dotenv import load_dotenv

load_dotenv()
SERVICE_KEY = os.getenv("SERVICE_KEY")

def collect_boxstats_price(
    stdate,
    eddate,
    service_key=SERVICE_KEY
):
    """
    10. 예매통계 가격대별 조회(boxStatsPriceService)

    - stdate, eddate: YYYYMMDD (최대 31일)
    - service_key: API 서비스 키
    """
    endpoint = "http://www.kopis.or.kr/openApi/restful/boxStatsPrice"
    params = {
        "service": service_key,
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
            "catenm": item.get("catenm"),
            "price": item.get("price"),
            "ntssnmrssm": item.get("ntssnmrssm"),
            "cancelnmrssm": item.get("cancelnmrssm"),
            "totnmrssm": item.get("totnmrssm"),
            "pertotnmrssm": item.get("pertotnmrssm"),
            "ntssamountsm": item.get("ntssamountsm")
        }
        records.append(record)

    df = pd.DataFrame(records)
    rename_dict = {
        "catenm": "장르명",
        "price": "가격대",
        "ntssnmrssm": "예매수",
        "cancelnmrssm": "취소수",
        "totnmrssm": "총티켓판매수",
        "pertotnmrssm": "총티켓판매수_장르비중",
        "ntssamountsm": "총티켓판매액"
    }
    df = df.rename(columns=rename_dict)

    return df
