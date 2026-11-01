"""
=============================================================================
Module: 04_build_star_schema.py
Mục đích: Xây dựng Mô hình Dữ liệu Đa chiều (Star Schema Dimensional Model)
Tác giả: Data Analyst Team
Ngày tạo: 2026-11-01
=============================================================================
Mô hình Star Schema theo chuẩn Ralph Kimball:
1. Bảng Chiều (Dimension Tables):
   - dim_date: Chiều thời gian phát hành (Năm, Quý, Tháng, Ngày, Thứ, Cuối tuần).
   - dim_games: Chiều thông tin game (Tiêu đề, phân khúc, hệ điều hành, cờ tiếng Việt...).
   - dim_genres: Chiều thể loại game (Action, Strategy, RPG...).
   - dim_categories: Chiều tính năng game (Single-player, Co-op, Full controller...).
   - dim_developers: Chiều nhà phát triển game (Valve, Ubisoft...).
   - dim_publishers: Chiều nhà phát hành game (Valve, EA, Capcom...).
   - dim_tags: Chiều thẻ người dùng (FPS, Souls-like, Open World...).

2. Bảng Cầu nối (Bridge Tables - Many-to-Many):
   - bridge_game_genres: Kết nối Game - Thể loại.
   - bridge_game_categories: Kết nối Game - Tính năng.
   - bridge_game_developers: Kết nối Game - Nhà phát triển.
   - bridge_game_publishers: Kết nối Game - Nhà phát hành.
   - bridge_game_tags: Kết nối Game - Tag cộng đồng kèm số phiếu bình chọn (vote_count).

3. Bảng Sự kiện (Fact Table):
   - fact_game_metrics: Chứa các thước đo định lượng (Doanh thu ước tính, Lượng người sở hữu,
     Lượt đánh giá tích cực/tiêu cực, Tỷ lệ hài lòng, Thời gian chơi, Đỉnh người chơi CCU).

4. Bảng Phẳng tối ưu Dashboard (Denormalized BI View):
   - flat_steam_games_bi: Bảng tổng hợp đã join sẵn, phục vụ trực tiếp Power BI, Tableau, Excel.
=============================================================================
"""

import os
import time
import pandas as pd
import numpy as np


def build_dim_date(release_dates_series: pd.Series) -> pd.DataFrame:
    """Tạo bảng chiều thời gian dim_date từ chuỗi ngày phát hành."""
    unique_dates = pd.Series(pd.to_datetime(release_dates_series.unique())).sort_values().reset_index(drop=True)
    
    dim_date = pd.DataFrame({
        "date_id": unique_dates.dt.strftime("%Y%m%d").astype(int),
        "full_date": unique_dates.dt.strftime("%Y-%m-%d"),
        "year": unique_dates.dt.year,
        "quarter": unique_dates.dt.quarter,
        "quarter_name": "Q" + unique_dates.dt.quarter.astype(str) + " " + unique_dates.dt.year.astype(str),
        "month": unique_dates.dt.month,
        "month_name": unique_dates.dt.strftime("%B"),
        "month_year": unique_dates.dt.strftime("%Y-%m"),
        "day_of_month": unique_dates.dt.day,
        "day_of_week": unique_dates.dt.dayofweek + 1,  # 1: Thứ 2, 7: Chủ nhật
        "day_name": unique_dates.dt.strftime("%A"),
        "is_weekend": (unique_dates.dt.dayofweek >= 5).astype(int)
    })
    return dim_date


def build_bridge_and_dim(df: pd.DataFrame, list_col: str, id_name: str, val_name: str):
    """Trích xuất Dimension Table và Bridge Table cho các quan hệ nhiều-nhiều (Many-to-Many)."""
    pairs = []
    for appid, items in zip(df["appid"], df[list_col]):
        if items is not None:
            for item in items:
                clean_item = str(item).strip()
                if clean_item:
                    pairs.append((appid, clean_item))
                    
    unique_values = sorted(list(set(p[1] for p in pairs)))
    val_to_id = {val: idx + 1 for idx, val in enumerate(unique_values)}
    
    dim_df = pd.DataFrame({
        id_name: list(val_to_id.values()),
        val_name: list(val_to_id.keys())
    })
    
    bridge_df = pd.DataFrame({
        "appid": [p[0] for p in pairs],
        id_name: [val_to_id[p[1]] for p in pairs]
    }).drop_duplicates()
    
    return dim_df, bridge_df


def build_tags_dim_and_bridge(df: pd.DataFrame):
    """Trích xuất dim_tags và bridge_game_tags kèm số lượng vote (chỉ lấy tag thực sự có vote > 0)."""
    tag_records = []
    for appid, tag_dict in zip(df["appid"], df["tags_parsed"]):
        if isinstance(tag_dict, dict):
            for tag, votes in tag_dict.items():
                if isinstance(votes, (int, float)) and votes > 0:
                    clean_tag = str(tag).strip()
                    if clean_tag:
                        tag_records.append((appid, clean_tag, int(votes)))
                    
    unique_tags = sorted(list(set(r[1] for r in tag_records)))
    tag_to_id = {tag: idx + 1 for idx, tag in enumerate(unique_tags)}
    
    dim_tags = pd.DataFrame({
        "tag_id": list(tag_to_id.values()),
        "tag_name": list(tag_to_id.keys())
    })
    
    bridge_tags = pd.DataFrame({
        "appid": [r[0] for r in tag_records],
        "tag_id": [tag_to_id[r[1]] for r in tag_records],
        "vote_count": [r[2] for r in tag_records]
    }).drop_duplicates(subset=["appid", "tag_id"])
    
    return dim_tags, bridge_tags


def build_star_schema(
    staging_parquet: str = "data/staging/games_transformed.parquet",
    output_dir_parquet: str = "data/processed/parquet",
    output_dir_csv: str = "data/processed/csv"
) -> dict:
    """
    Tạo toàn bộ các bảng trong mô hình Star Schema và xuất ra Parquet & CSV.
    """
    print("=" * 80)
    print("BẮT ĐẦU: Xây dựng Mô hình Dữ liệu Đa chiều (Star Schema ETL)")
    print("=" * 80)
    start_time = time.time()

    os.makedirs(output_dir_parquet, exist_ok=True)
    os.makedirs(output_dir_csv, exist_ok=True)

    print(f"-> 1. Đang nạp dữ liệu từ Staging: {staging_parquet}...")
    df = pd.read_parquet(staging_parquet)
    print(f"   + Nạp thành công {len(df):,} bản ghi.")

    # 1. Bảng dim_date
    print("-> 2. Xây dựng bảng dim_date (Chiều thời gian)...")
    dim_date = build_dim_date(df["release_date"])

    # 2. Bảng dim_genres & bridge_game_genres
    print("-> 3. Xây dựng dim_genres & bridge_game_genres...")
    dim_genres, bridge_game_genres = build_bridge_and_dim(df, "genres_parsed", "genre_id", "genre_name")

    # 3. Bảng dim_categories & bridge_game_categories
    print("-> 4. Xây dựng dim_categories & bridge_game_categories...")
    dim_categories, bridge_game_categories = build_bridge_and_dim(df, "categories_parsed", "category_id", "category_name")

    # 4. Bảng dim_developers & bridge_game_developers
    print("-> 5. Xây dựng dim_developers & bridge_game_developers...")
    dim_developers, bridge_game_developers = build_bridge_and_dim(df, "developers_parsed", "developer_id", "developer_name")

    # 5. Bảng dim_publishers & bridge_game_publishers
    print("-> 6. Xây dựng dim_publishers & bridge_game_publishers...")
    dim_publishers, bridge_game_publishers = build_bridge_and_dim(df, "publishers_parsed", "publisher_id", "publisher_name")

    # 6. Bảng dim_tags & bridge_game_tags
    print("-> 7. Xây dựng dim_tags & bridge_game_tags...")
    dim_tags, bridge_game_tags = build_tags_dim_and_bridge(df)

    # 7. Bảng dim_games
    print("-> 8. Xây dựng bảng dim_games (Chiều thông tin game)...")
    game_dim_cols = [
        "appid", "name", "release_date_id", "required_age", "is_free", "price_usd",
        "price_tier", "windows", "mac", "linux", "platform_support",
        "has_vietnamese", "has_english", "supported_languages_count",
        "primary_genre", "primary_developer", "primary_publisher",
        "genres_display", "categories_display", "top_tags_display",
        "header_image", "website", "short_description"
    ]
    dim_games = df[game_dim_cols].copy()
    dim_games["short_description"] = dim_games["short_description"].fillna("").astype(str).str.slice(0, 300)

    # 8. Bảng fact_game_metrics
    print("-> 9. Xây dựng bảng fact_game_metrics (Bảng sự kiện / Fact Table)...")
    fact_cols = [
        "appid", "release_date_id", "price_usd", "discount_pct", "dlc_count",
        "achievements", "positive_reviews", "negative_reviews", "total_reviews",
        "positive_ratio_pct", "review_score_tier", "metacritic_score", "has_metacritic",
        "recommendations", "estimated_owners_min", "estimated_owners_max", "estimated_owners_avg",
        "owner_bracket", "estimated_revenue_min_usd", "estimated_revenue_max_usd", "estimated_revenue_avg_usd",
        "peak_ccu", "avg_playtime_forever_hours", "median_playtime_forever_hours",
        "avg_playtime_2weeks_hours", "median_playtime_2weeks_hours"
    ]
    fact_game_metrics = df[fact_cols].copy()
    fact_game_metrics.insert(0, "fact_id", range(1, len(fact_game_metrics) + 1))

    # 9. Bảng phẳng tối ưu hóa Dashboard (Flat BI Reporting Table)
    print("-> 10. Tạo bảng tổng hợp phẳng (Flat Table) cho Power BI / Tableau...")
    # Join dim_games + fact_game_metrics + dim_date các cột cốt lõi
    date_sub = dim_date[["date_id", "year", "quarter_name", "month_year", "month_name"]].copy()
    flat_steam_games_bi = fact_game_metrics.merge(
        dim_games.drop(columns=["release_date_id"]),
        on="appid",
        how="inner"
    ).merge(
        date_sub,
        left_on="release_date_id",
        right_on="date_id",
        how="left"
    )

    # Từ điển chứa tất cả các bảng
    tables = {
        "dim_date": dim_date,
        "dim_games": dim_games,
        "dim_genres": dim_genres,
        "dim_categories": dim_categories,
        "dim_developers": dim_developers,
        "dim_publishers": dim_publishers,
        "dim_tags": dim_tags,
        "bridge_game_genres": bridge_game_genres,
        "bridge_game_categories": bridge_game_categories,
        "bridge_game_developers": bridge_game_developers,
        "bridge_game_publishers": bridge_game_publishers,
        "bridge_game_tags": bridge_game_tags,
        "fact_game_metrics": fact_game_metrics,
        "flat_steam_games_bi": flat_steam_games_bi
    }

    # 10. Xuất các bảng ra Parquet và CSV
    print("-> 11. Đang xuất các bảng ra định dạng Parquet & CSV...")
    for table_name, table_df in tables.items():
        parquet_path = os.path.join(output_dir_parquet, f"{table_name}.parquet")
        table_df.to_parquet(parquet_path, index=False, engine="pyarrow")
        
        # Với CSV: xuất các bảng chính (nếu bảng quá lớn như bridge_tags 1.5M dòng thì chỉ xuất parquet hoặc sample)
        csv_path = os.path.join(output_dir_csv, f"{table_name}.csv")
        table_df.to_csv(csv_path, index=False, encoding="utf-8-sig")
        print(f"   [OK] Đã xuất {table_name:25s}: {len(table_df):,} dòng")

    total_time = time.time() - start_time
    print("=" * 80)
    print(f"HOÀN TẤT XÂY DỰNG STAR SCHEMA: 14 bảng dữ liệu sạch được tạo trong {total_time:.2f}s!")
    print("=" * 80)

    return tables


if __name__ == "__main__":
    build_star_schema()
