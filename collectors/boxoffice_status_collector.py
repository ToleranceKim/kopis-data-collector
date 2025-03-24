# 6. 예매상황판 조회 (boxofficeService)
import requests
import pandas as pd
import xmltodict
import os
from dotenv import load_dotenv

load_dotenv()
SERVICE_KEY = os.getenv("SERVICE_KEY")

def collect_boxoffice(
    stdate,
    eddate,
    date=None,
    catecode=None,
    area=None,
    srchseatscale=None,
    service_key=SERVICE_KEY
):
    """
    6. 예매상황판 조회(boxofficeService)

    - stdate, eddate: YYYYMMDD (최대 31일)
    - date: 날짜(YYYYMMDD)
    - catecode: 장르구분코드
    - area: 지역코드
    - srchseatscale: 좌석수(0,100,300,500,1000,5000,10000)
    - service_key: API 서비스 키
    """
    endpoint = "http://www.kopis.or.kr/openApi/restful/boxoffice"
    params = {
        "service": service_key,
        "stdate": stdate,
        "eddate": eddate
    }
    if date:
        params["date"] = date
    if catecode:
        params["catecode"] = catecode
    if area:
        params["area"] = area
    if srchseatscale:
        params["srchseatscale"] = srchseatscale

    response = requests.get(endpoint, params=params)
    response.raise_for_status()

    data_dict = xmltodict.parse(response.text)
    boxofs = data_dict.get("boxofs", {})
    # basedate = boxofs.get("basedate") # 필요하면 추출

    items = boxofs.get("boxof", [])
    if isinstance(items, dict):
        items = [items]

    records = []
    for item in items:
        record = {
            "cate": item.get("cate"),
            "rnum": item.get("rnum"),
            "prfnm": item.get("prfnm"),
            "prfpd": item.get("prfpd"),
            "prfplcnm": item.get("prfplcnm"),
            "seatcnt": item.get("seatcnt"),
            "prfdtcnt": item.get("prfdtcnt"),
            "area": item.get("area"),
            "poster": item.get("poster"),
            "mt20id": item.get("mt20id")
        }
        records.append(record)

    df = pd.DataFrame(records)
    rename_dict = {
        "cate": "장르",
        "rnum": "순위",
        "prfnm": "공연명",
        "prfpd": "공연기간",
        "prfplcnm": "공연장소",
        "seatcnt": "좌석수",
        "prfdtcnt": "상연횟수",
        "area": "지역",
        "poster": "포스터경로",
        "mt20id": "공연ID"
    }
    df = df.rename(columns=rename_dict)

    return df
