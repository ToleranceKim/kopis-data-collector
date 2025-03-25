# main_detail.py
import pandas as pd
import os

from collectors.performance_detail_collector import collect_pblprfr_detail
from collectors.venue_detail_collector import collect_prfplc_detail

# config 설정 값 (공연 코드, 공연장 코드)
from config import PERFORMANCE_CODE, VENUE_CODE

def main():
    os.makedirs("./data_detail", exist_ok=True)

    # 공연 상세
    df_perf_detail = collect_pblprfr_detail(PERFORMANCE_CODE)
    if df_perf_detail is not None and not df_perf_detail.empty:
        df_perf_detail.to_csv("./data_detail/공연상세_PF132236.csv", index=False, encoding="utf-8-sig")
        print("[공연 상세] PF132236 CSV 저장 완료")

    # 공연시설 상세
    df_venue_detail = collect_prfplc_detail(VENUE_CODE)
    if df_venue_detail is not None and not df_venue_detail.empty:
        df_venue_detail.to_csv("./data_detail/공연시설상세_FC001247.csv", index=False, encoding="utf-8-sig")
        print("[공연시설 상세] FC001247 CSV 저장 완료")

if __name__ == "__main__":
    main()
