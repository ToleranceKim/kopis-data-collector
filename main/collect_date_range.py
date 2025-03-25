import time
from datetime import datetime, timedelta
import pandas as pd
import os

# (1) 공연목록 조회
from collectors.performance_list_collector import collect_pblprfr_list

# (6) 예매상황판
from collectors.boxoffice_status_collector import collect_boxoffice

# (7) 예매통계 기간별 조회
from collectors.ticketstats_period_collector import collect_boxstats

# (8) 예매통계 장르별 조회
from collectors.ticketstats_genre_collector import collect_boxstats_cate

# (9) 예매통계 시간대별 조회
from collectors.ticketstats_time_collector import collect_boxstats_time

# (10) 예매통계 가격대별 조회
from collectors.ticketstats_price_collector import collect_boxstats_price

# (11) 기간별 통계 목록
from collectors.perfstats_period_collector import collect_prfsts_total

# (12) 지역별 통계 목록
from collectors.perfstats_area_collector import collect_prfsts_area

# (13) 장르별 통계 목록
from collectors.perfstats_genre_collector import collect_prfsts_cate

# (14) 공연별 통계 목록
from collectors.perfstats_byperformance_collector import collect_prfsts_prfby

# (15) 공연시설별 통계 목록
from collectors.perfstats_byvenue_collector import collect_prfsts_prfbyfct

# (16) 가격대별 통계 목록
from collectors.perfstats_price_collector import collect_prfsts_price

# (17) 수상작 목록 조회
from collectors.awards_list_collector import collect_prfawad_list

# (18) 축제 목록 조회
from collectors.festival_list_collector import collect_prffest_list

# (19) 극작가 목록 조회
from collectors.playwright_list_collector import collect_prfer_list

# config 설정 값 (날짜 범위)
from config import START_DATE, END_DATE

def main():
    """
    날짜 파라미터가 필요한 (혹은 권장되는) 거의 모든 서비스를
    31일 간격으로 반복 호출해, CSV를 생성하는 예시 코드입니다.
    """
    os.makedirs("./data_date_range", exist_ok=True)

    # 전체 수집 기간 설정 (예: 20240101 ~ 20241231)
    start_date_str = START_DATE
    end_date_str = END_DATE

    current = datetime.strptime(start_date_str, "%Y%m%d")
    end_date = datetime.strptime(end_date_str, "%Y%m%d")

    # 각 서비스별로 결과를 저장할 리스트(또는 dict) 준비
    dfs_pblprfr_list = []       # (1) 공연목록
    dfs_boxoffice = []          # (6) 예매상황판
    dfs_boxstats_period = []    # (7) 예매통계 기간별
    dfs_boxstats_cate = []      # (8) 예매통계 장르별
    dfs_boxstats_time = []      # (9) 예매통계 시간대별
    dfs_boxstats_price = []     # (10) 예매통계 가격대별
    dfs_perf_total = []         # (11) 기간별 통계
    dfs_perf_area = []          # (12) 지역별 통계
    dfs_perf_cate = []          # (13) 장르별 통계
    dfs_perf_by = []            # (14) 공연별 통계
    dfs_perf_byfct = []         # (15) 공연시설별 통계
    dfs_perf_price = []         # (16) 가격대별 통계
    dfs_awards = []             # (17) 수상작 목록
    dfs_fest = []               # (18) 축제 목록
    dfs_playwright = []         # (19) 극작가 목록

    while current <= end_date:
        period_end = current + timedelta(days=30)  # 31일 간격 (필요에 따라 조정 가능)
        if period_end > end_date:
            period_end = end_date

        seg_start_str = current.strftime("%Y%m%d")
        seg_end_str = period_end.strftime("%Y%m%d")
        print(f"\n=== 수집 구간: {seg_start_str} ~ {seg_end_str} ===")

        # (1) 공연목록
        df_1 = collect_pblprfr_list(stdate=seg_start_str, eddate=seg_end_str, cpage=1, rows=100)
        if df_1 is not None and not df_1.empty:
            dfs_pblprfr_list.append(df_1)
            print(f"(1) 공연목록: {len(df_1)}건")
        else:
            print("(1) 공연목록 결과 없음")

        # (6) 예매상황판
        df_6 = collect_boxoffice(stdate=seg_start_str, eddate=seg_end_str)
        if df_6 is not None and not df_6.empty:
            dfs_boxoffice.append(df_6)
            print(f"(6) 예매상황판: {len(df_6)}건")
        else:
            print("(6) 예매상황판 결과 없음")

        # (7) 예매통계 기간별
        df_7 = collect_boxstats(ststype="day", stdate=seg_start_str, eddate=seg_end_str)
        if df_7 is not None and not df_7.empty:
            dfs_boxstats_period.append(df_7)
            print(f"(7) 예매통계(기간별): {len(df_7)}건")
        else:
            print("(7) 예매통계(기간별) 결과 없음")

        # (8) 예매통계 장르별
        df_8 = collect_boxstats_cate(stdate=seg_start_str, eddate=seg_end_str, catecode="AAAA")
        if df_8 is not None and not df_8.empty:
            dfs_boxstats_cate.append(df_8)
            print(f"(8) 예매통계(장르별): {len(df_8)}건")
        else:
            print("(8) 예매통계(장르별) 결과 없음")

        # (9) 예매통계 시간대별
        df_9 = collect_boxstats_time(stdate=seg_start_str, eddate=seg_end_str)
        if df_9 is not None and not df_9.empty:
            dfs_boxstats_time.append(df_9)
            print(f"(9) 예매통계(시간대별): {len(df_9)}건")
        else:
            print("(9) 예매통계(시간대별) 결과 없음")

        # (10) 예매통계 가격대별
        df_10 = collect_boxstats_price(stdate=seg_start_str, eddate=seg_end_str)
        if df_10 is not None and not df_10.empty:
            dfs_boxstats_price.append(df_10)
            print(f"(10) 예매통계(가격대별): {len(df_10)}건")
        else:
            print("(10) 예매통계(가격대별) 결과 없음")

        # (11) 기간별 통계
        df_11 = collect_prfsts_total(ststype="day", stdate=seg_start_str, eddate=seg_end_str)
        if df_11 is not None and not df_11.empty:
            dfs_perf_total.append(df_11)
            print(f"(11) 기간별 통계: {len(df_11)}건")
        else:
            print("(11) 기간별 통계 결과 없음")

        # (12) 지역별 통계
        df_12 = collect_prfsts_area(stdate=seg_start_str, eddate=seg_end_str)
        if df_12 is not None and not df_12.empty:
            dfs_perf_area.append(df_12)
            print(f"(12) 지역별 통계: {len(df_12)}건")
        else:
            print("(12) 지역별 통계 결과 없음")

        # (13) 장르별 통계
        df_13 = collect_prfsts_cate(stdate=seg_start_str, eddate=seg_end_str)
        if df_13 is not None and not df_13.empty:
            dfs_perf_cate.append(df_13)
            print(f"(13) 장르별 통계: {len(df_13)}건")
        else:
            print("(13) 장르별 통계 결과 없음")

        # (14) 공연별 통계
        df_14 = collect_prfsts_prfby(stdate=seg_start_str, eddate=seg_end_str, shcate="AAAA")
        if df_14 is not None and not df_14.empty:
            dfs_perf_by.append(df_14)
            print(f"(14) 공연별 통계: {len(df_14)}건")
        else:
            print("(14) 공연별 통계 결과 없음")

        # (15) 공연시설별 통계
        df_15 = collect_prfsts_prfbyfct(stdate=seg_start_str, eddate=seg_end_str)
        if df_15 is not None and not df_15.empty:
            dfs_perf_byfct.append(df_15)
            print(f"(15) 공연시설별 통계: {len(df_15)}건")
        else:
            print("(15) 공연시설별 통계 결과 없음")

        # (16) 가격대별 통계
        df_16 = collect_prfsts_price(stdate=seg_start_str, eddate=seg_end_str, shcate="AAAA")
        if df_16 is not None and not df_16.empty:
            dfs_perf_price.append(df_16)
            print(f"(16) 가격대별 통계: {len(df_16)}건")
        else:
            print("(16) 가격대별 통계 결과 없음")

        # (17) 수상작 목록
        df_17 = collect_prfawad_list(stdate=seg_start_str, eddate=seg_end_str)
        if df_17 is not None and not df_17.empty:
            dfs_awards.append(df_17)
            print(f"(17) 수상작 목록: {len(df_17)}건")
        else:
            print("(17) 수상작 목록 결과 없음")

        # (18) 축제 목록
        df_18 = collect_prffest_list(stdate=seg_start_str, eddate=seg_end_str)
        if df_18 is not None and not df_18.empty:
            dfs_fest.append(df_18)
            print(f"(18) 축제 목록: {len(df_18)}건")
        else:
            print("(18) 축제 목록 결과 없음")

        # (19) 극작가 목록
        df_19 = collect_prfer_list(stdate=seg_start_str, eddate=seg_end_str)
        if df_19 is not None and not df_19.empty:
            dfs_playwright.append(df_19)
            print(f"(19) 극작가 목록: {len(df_19)}건")
        else:
            print("(19) 극작가 목록 결과 없음")

        # API 과도 호출 방지
        time.sleep(1)

        # 다음 구간으로
        current = period_end + timedelta(days=1)

    # 반복문 끝난 후, 각각 병합 & 저장
    save_path = "./data_date_range"
    
    if dfs_pblprfr_list:
        merged_1 = pd.concat(dfs_pblprfr_list, ignore_index=True)
        merged_1.to_csv(f"{save_path}/공연목록_{start_date_str}~{end_date_str}.csv", index=False, encoding="utf-8-sig")
        print(f"\n(1) 공연목록 CSV 저장: {len(merged_1)} 건")

    if dfs_boxoffice:
        merged_6 = pd.concat(dfs_boxoffice, ignore_index=True)
        merged_6.to_csv(f"{save_path}/예매상황판_{start_date_str}~{end_date_str}.csv", index=False, encoding="utf-8-sig")
        print(f"(6) 예매상황판 CSV 저장: {len(merged_6)} 건")

    if dfs_boxstats_period:
        merged_7 = pd.concat(dfs_boxstats_period, ignore_index=True)
        merged_7.to_csv(f"{save_path}/예매통계(기간별)_{start_date_str}~{end_date_str}.csv", index=False, encoding="utf-8-sig")
        print(f"(7) 예매통계(기간별) CSV 저장: {len(merged_7)} 건")

    if dfs_boxstats_cate:
        merged_8 = pd.concat(dfs_boxstats_cate, ignore_index=True)
        merged_8.to_csv(f"{save_path}/예매통계(장르별)_{start_date_str}~{end_date_str}.csv", index=False, encoding="utf-8-sig")
        print(f"(8) 예매통계(장르별) CSV 저장: {len(merged_8)} 건")

    if dfs_boxstats_time:
        merged_9 = pd.concat(dfs_boxstats_time, ignore_index=True)
        merged_9.to_csv(f"{save_path}/예매통계(시간대별)_{start_date_str}~{end_date_str}.csv", index=False, encoding="utf-8-sig")
        print(f"(9) 예매통계(시간대별) CSV 저장: {len(merged_9)} 건")

    if dfs_boxstats_price:
        merged_10 = pd.concat(dfs_boxstats_price, ignore_index=True)
        merged_10.to_csv(f"{save_path}/예매통계(가격대별)_{start_date_str}~{end_date_str}.csv", index=False, encoding="utf-8-sig")
        print(f"(10) 예매통계(가격대별) CSV 저장: {len(merged_10)} 건")

    if dfs_perf_total:
        merged_11 = pd.concat(dfs_perf_total, ignore_index=True)
        merged_11.to_csv(f"{save_path}/기간별 통계_{start_date_str}~{end_date_str}.csv", index=False, encoding="utf-8-sig")
        print(f"(11) 기간별 통계 CSV 저장: {len(merged_11)} 건")

    if dfs_perf_area:
        merged_12 = pd.concat(dfs_perf_area, ignore_index=True)
        merged_12.to_csv(f"{save_path}/지역별 통계_{start_date_str}~{end_date_str}.csv", index=False, encoding="utf-8-sig")
        print(f"(12) 지역별 통계 CSV 저장: {len(merged_12)} 건")

    if dfs_perf_cate:
        merged_13 = pd.concat(dfs_perf_cate, ignore_index=True)
        merged_13.to_csv(f"{save_path}/장르별 통계_{start_date_str}~{end_date_str}.csv", index=False, encoding="utf-8-sig")
        print(f"(13) 장르별 통계 CSV 저장: {len(merged_13)} 건")

    if dfs_perf_by:
        merged_14 = pd.concat(dfs_perf_by, ignore_index=True)
        merged_14.to_csv(f"{save_path}/공연별 통계_{start_date_str}~{end_date_str}.csv", index=False, encoding="utf-8-sig")
        print(f"(14) 공연별 통계 CSV 저장: {len(merged_14)} 건")

    if dfs_perf_byfct:
        merged_15 = pd.concat(dfs_perf_byfct, ignore_index=True)
        merged_15.to_csv(f"{save_path}/공연시설별 통계_{start_date_str}~{end_date_str}.csv", index=False, encoding="utf-8-sig")
        print(f"(15) 공연시설별 통계 CSV 저장: {len(merged_15)} 건")

    if dfs_perf_price:
        merged_16 = pd.concat(dfs_perf_price, ignore_index=True)
        merged_16.to_csv(f"{save_path}/가격대별 통계_{start_date_str}~{end_date_str}.csv", index=False, encoding="utf-8-sig")
        print(f"(16) 가격대별 통계 CSV 저장: {len(merged_16)} 건")

    if dfs_awards:
        merged_17 = pd.concat(dfs_awards, ignore_index=True)
        merged_17.to_csv(f"{save_path}/수상작 목록_{start_date_str}~{end_date_str}.csv", index=False, encoding="utf-8-sig")
        print(f"(17) 수상작 목록 CSV 저장: {len(merged_17)} 건")

    if dfs_fest:
        merged_18 = pd.concat(dfs_fest, ignore_index=True)
        merged_18.to_csv(f"{save_path}/축제 목록_{start_date_str}~{end_date_str}.csv", index=False, encoding="utf-8-sig")
        print(f"(18) 축제 목록 CSV 저장: {len(merged_18)} 건")

    if dfs_playwright:
        merged_19 = pd.concat(dfs_playwright, ignore_index=True)
        merged_19.to_csv(f"{save_path}/극작가 목록_{start_date_str}~{end_date_str}.csv", index=False, encoding="utf-8-sig")
        print(f"(19) 극작가 목록 CSV 저장: {len(merged_19)} 건")

if __name__ == "__main__":
    main()
