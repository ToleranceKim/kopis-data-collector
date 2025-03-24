# main.py

import pprint

# 1
from performance_list_collector import collect_pblprfr_list
# 2
from performance_detail_collector import collect_pblprfr_detail
# 3
from venue_list_collector import collect_prfplc_list
# 4
from venue_detail_collector import collect_prfplc_detail
# 5
from production_company_list_collector import collect_mnfct_list
# 6
from boxoffice_status_collector import collect_boxoffice
# 7
from ticketstats_period_collector import collect_boxstats
# 8
from ticketstats_genre_collector import collect_boxstats_cate
# 9
from ticketstats_time_collector import collect_boxstats_time
# 10
from ticketstats_price_collector import collect_boxstats_price
# 11
from perfstats_period_collector import collect_prfsts_total
# 12
from perfstats_area_collector import collect_prfsts_area
# 13
from perfstats_genre_collector import collect_prfsts_cate
# 14
from perfstats_byperformance_collector import collect_prfsts_prfby
# 15
from perfstats_byvenue_collector import collect_prfsts_prfbyfct
# 16
from perfstats_price_collector import collect_prfsts_price
# 17
from awards_list_collector import collect_prfawad_list
# 18
from festival_list_collector import collect_prffest_list
# 19
from playwright_list_collector import collect_prfer_list


def main():
    # 1) 공연목록 조회
    df1 = collect_pblprfr_list(stdate="20230101", eddate="20230107")
    print("1) 공연목록 조회:", df1.shape)
    pprint.pprint(df1.head().to_dict())

    # 2) 공연 상세 조회 (예: PF132236)
    df2 = collect_pblprfr_detail("PF132236")
    print("\n2) 공연 상세 조회:", df2.shape)
    pprint.pprint(df2.head().to_dict())

    # 3) 공연시설 목록 조회
    df3 = collect_prfplc_list(cpage=1, rows=5)
    print("\n3) 공연시설 목록 조회:", df3.shape)
    pprint.pprint(df3.head().to_dict())

    # 4) 공연시설 상세 조회 (예: FC001247)
    df4 = collect_prfplc_detail("FC001247")
    print("\n4) 공연시설 상세 조회:", df4.shape)
    pprint.pprint(df4.head().to_dict())

    # 5) 기획/제작사 목록 조회
    df5 = collect_mnfct_list()
    print("\n5) 기획/제작사 목록 조회:", df5.shape)
    pprint.pprint(df5.head().to_dict())

    # 6) 예매상황판 조회
    df6 = collect_boxoffice(stdate="20230601", eddate="20230601")
    print("\n6) 예매상황판 조회:", df6.shape)
    pprint.pprint(df6.head().to_dict())

    # 7) 예매통계 기간별 조회
    df7 = collect_boxstats(ststype="day", stdate="20230101", eddate="20230107")
    print("\n7) 예매통계 기간별 조회:", df7.shape)
    pprint.pprint(df7.head().to_dict())

    # 8) 예매통계 장르별 조회
    df8 = collect_boxstats_cate(stdate="20230101", eddate="20230107", catecode="AAAA")
    print("\n8) 예매통계 장르별 조회:", df8.shape)
    pprint.pprint(df8.head().to_dict())

    # 9) 예매통계 시간대별 조회
    df9 = collect_boxstats_time(stdate="20230101", eddate="20230107")
    print("\n9) 예매통계 시간대별 조회:", df9.shape)
    pprint.pprint(df9.head().to_dict())

    # 10) 예매통계 가격대별 조회
    df10 = collect_boxstats_price(stdate="20230101", eddate="20230107")
    print("\n10) 예매통계 가격대별 조회:", df10.shape)
    pprint.pprint(df10.head().to_dict())

    # 11) 기간별 통계 목록 조회
    df11 = collect_prfsts_total(ststype="day", stdate="20230101", eddate="20230107")
    print("\n11) 기간별 통계 목록 조회:", df11.shape)
    pprint.pprint(df11.head().to_dict())

    # 12) 지역별 통계 목록 조회
    df12 = collect_prfsts_area(stdate="20230101", eddate="20230107")
    print("\n12) 지역별 통계 목록 조회:", df12.shape)
    pprint.pprint(df12.head().to_dict())

    # 13) 장르별 통계 목록 조회
    df13 = collect_prfsts_cate(stdate="20230101", eddate="20230107")
    print("\n13) 장르별 통계 목록 조회:", df13.shape)
    pprint.pprint(df13.head().to_dict())

    # 14) 공연별 통계 목록 조회
    df14 = collect_prfsts_prfby(stdate="20230101", eddate="20230107")
    print("\n14) 공연별 통계 목록 조회:", df14.shape)
    pprint.pprint(df14.head().to_dict())

    # 15) 공연시설별 통계 목록 조회
    df15 = collect_prfsts_prfbyfct(stdate="20230101", eddate="20230107")
    print("\n15) 공연시설별 통계 목록 조회:", df15.shape)
    pprint.pprint(df15.head().to_dict())

    # 16) 가격대별 통계 목록 조회
    df16 = collect_prfsts_price(stdate="20230101", eddate="20230107", shcate="AAAA")
    print("\n16) 가격대별 통계 목록 조회:", df16.shape)
    pprint.pprint(df16.head().to_dict())

    # 17) 수상작 목록 조회
    df17 = collect_prfawad_list(stdate="20230101", eddate="20230107")
    print("\n17) 수상작 목록 조회:", df17.shape)
    pprint.pprint(df17.head().to_dict())

    # 18) 축제 목록 조회
    df18 = collect_prffest_list(stdate="20230101", eddate="20230107")
    print("\n18) 축제 목록 조회:", df18.shape)
    pprint.pprint(df18.head().to_dict())

    # 19) 극작가 목록 조회
    df19 = collect_prfer_list(stdate="20230101", eddate="20230107")
    print("\n19) 극작가 목록 조회:", df19.shape)
    pprint.pprint(df19.head().to_dict())


if __name__ == "__main__":
    main()
