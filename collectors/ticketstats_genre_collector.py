# 8. 예매통계 장르별 조회 (boxStatsCateService)
import requests
import pandas as pd
import xmltodict
import os
from dotenv import load_dotenv

load_dotenv()
SERVICE_KEY = os.getenv("SERVICE_KEY")

def collect_boxstats_cate(
    stdate,
    eddate,
    catecode,
    service_key=SERVICE_KEY
):
    """
    8. 예매통계 장르별 조회(boxStatsCateService)

    - stdate, eddate: YYYYMMDD (최대 31일)
    - catecode: 장르 구분 코드 (예: 'AAAA|BBBB|CCCA')
    - service_key: API 서비스 키
    """
    endpoint = "http://www.kopis.or.kr/openApi/restful/boxStatsCate"
    params = {
        "service": service_key,
        "stdate": stdate,
        "eddate": eddate,
        "catecode": catecode
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
        "catenm": "장르명",
        "prfcnt": "공연건수",
        "prfdtcnt": "상연횟수",
        "ntssnmrssm": "예매수",
        "cancelnmrssm": "취소수",
        "totnmrssm": "총티켓판매수",
        "ntssamountsm": "총티켓판매액"
    }
    df = df.rename(columns=rename_dict)

    return df
