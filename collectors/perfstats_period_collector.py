# perfstats_period_collector.py

import requests
import pandas as pd
import xmltodict
import os
from dotenv import load_dotenv

load_dotenv()  # .env 에서 SERVICE_KEY 로드
SERVICE_KEY = os.getenv("SERVICE_KEY")

def collect_prfsts_total(ststype, stdate, eddate, service_key=SERVICE_KEY):
    """
    11. 기간별 통계 목록 조회 (prfstsTotalService)
    - ststype: 'day', 'dayWeek', 'month' 등
    - stdate, eddate: YYYYMMDD (최대 31일)
    - service_key: API 서비스 키 (.env 사용 시 기본값으로 전달)
    """
    endpoint = "http://www.kopis.or.kr/openApi/restful/prfstsTotal"
    params = {
        "service": service_key,
        "ststype": ststype,
        "stdate": stdate,
        "eddate": eddate
    }

    response = requests.get(endpoint, params=params)
    response.raise_for_status()

    data_dict = xmltodict.parse(response.text)

    # 루트 태그: <prfSts>, 반복 요소: <prfSt>
    items = data_dict.get("prfsts", {}).get("prfst", [])
    if isinstance(items, dict):
        items = [items]

    records = []
    for item in items:
        record = {
            "prfdt": item.get("prfdt"),          # 날짜 or 요일
            "prfprocnt": item.get("prfprocnt"),  # 개막편수
            "prfdtcnt": item.get("prfdtcnt"),    # 상연횟수
            "amount": item.get("amount"),        # 매출액
            "nmrs": item.get("nmrs"),            # 총관객수(티켓판매수)
            "prfcnt": item.get("prfcnt"),        # 공연건수
            "ntssnmrs": item.get("ntssnmrs"),    # 판매수
            "cancelnmrs": item.get("cancelnmrs") # 취소수
        }
        records.append(record)

    df = pd.DataFrame(records)
    rename_dict = {
        "prfdt": "날짜/요일",
        "prfprocnt": "개막편수",
        "prfdtcnt": "상연횟수",
        "amount": "매출액",
        "nmrs": "총관객수",
        "prfcnt": "공연건수",
        "ntssnmrs": "판매수",
        "cancelnmrs": "취소수"
    }
    df = df.rename(columns=rename_dict)

    return df
