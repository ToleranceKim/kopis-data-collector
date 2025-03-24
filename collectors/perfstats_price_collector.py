# 16. 가격대별 통계 목록 조회 (prfstsPriceService)
import requests
import pandas as pd
import xmltodict
import os
from dotenv import load_dotenv

load_dotenv()
SERVICE_KEY = os.getenv("SERVICE_KEY")

def collect_prfsts_price(
    stdate,
    eddate,
    shcate,
    service_key=SERVICE_KEY
):
    """
    16. 가격대별 통계 목록 조회(prfstsPriceService)

    - stdate, eddate: YYYYMMDD (최대 31일)
    - shcate: 장르코드 (예: AAAA=연극)
    - service_key: API 서비스 키
    """
    endpoint = "http://www.kopis.or.kr/openApi/restful/prfstsPrice"
    params = {
        "service": service_key,
        "stdate": stdate,
        "eddate": eddate,
        "shcate": shcate
    }

    response = requests.get(endpoint, params=params)
    response.raise_for_status()

    data_dict = xmltodict.parse(response.text)
    items = data_dict.get("prfsts", {}).get("prfst", [])
    if isinstance(items, dict):
        items = [items]

    records = []
    for item in items:
        record = {
            "nmrs": item.get("nmrs"),
            "amount": item.get("amount"),
            "nmrcancl": item.get("nmrcancl"),
            "cate": item.get("cate"),
            "price": item.get("price"),
            "amountsmratio": item.get("amountsmratio"),
            "totnmrs": item.get("totnmrs")
        }
        records.append(record)

    df = pd.DataFrame(records)
    rename_dict = {
        "nmrs": "예매수",
        "amount": "예매액",
        "nmrcancl": "취소수",
        "cate": "장르",
        "price": "가격대",
        "amountsmratio": "예매액비중",
        "totnmrs": "총티켓판매수"
    }
    df = df.rename(columns=rename_dict)

    return df
