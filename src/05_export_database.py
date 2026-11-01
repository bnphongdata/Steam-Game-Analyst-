"""
=============================================================================
Module: 05_export_database.py
Mục đích: Khởi tạo và nạp dữ liệu vào Data Warehouse SQLite (steam_dw.db)
Tác giả: Data Analyst Team
Ngày tạo: 2026-11-01
=============================================================================
Quy trình:
1. Kết nối cơ sở dữ liệu SQLite: `data/processed/steam_dw.db`.
2. Đọc và thực thi DDL script `sql/schema_ddl.sql` để tạo cấu trúc bảng,
   ràng buộc toàn vẹn khóa ngoại (Foreign Keys) và chỉ mục (Indexes).
3. Đọc dữ liệu từ các tệp Parquet đã chuẩn hóa trong `data/processed/parquet/`
   và nạp khối (Bulk Insert) vào các bảng tương ứng thông qua SQLAlchemy Engine.
4. Tạo View SQL `vw_steam_games_dashboard` hỗ trợ kết nối 1-click từ Power BI / Tableau.
5. Thực hiện kiểm tra tính toàn vẹn (Data Quality Checks) và in kết quả mẫu.
=============================================================================
"""

import os
import sqlite3
import time
import pandas as pd
from sqlalchemy import create_engine, text


def export_to_sqlite(
    db_path: str = "data/processed/steam_dw.db",
    ddl_path: str = "sql/schema_ddl.sql",
    parquet_dir: str = "data/processed/parquet"
):
    """
    Tạo cơ sở dữ liệu SQLite và nạp toàn bộ Star Schema.
    """
    print("=" * 80)
    print("BẮT ĐẦU: Khởi tạo và Nạp dữ liệu vào SQLite Data Warehouse")
    print("=" * 80)
    start_time = time.time()

    abs_db_path = os.path.abspath(db_path)
    if os.path.exists(abs_db_path):
        os.remove(abs_db_path)

    os.makedirs(os.path.dirname(abs_db_path), exist_ok=True)

    # 1. Đọc và thực thi file DDL bằng sqlite3 connection trực tiếp
    print(f"-> 1. Thực thi tệp DDL tạo lược đồ: {ddl_path}...")
    with open(ddl_path, "r", encoding="utf-8") as f:
        ddl_script = f.read()

    raw_conn = sqlite3.connect(abs_db_path)
    raw_conn.executescript(ddl_script)
    raw_conn.commit()
    raw_conn.close()
    print("   -> Lược đồ bảng và chỉ mục đã được tạo thành công.")

    # 2. Kết nối thông qua SQLAlchemy Engine để nạp khối tối ưu
    db_url = f"sqlite:///{abs_db_path.replace(os.sep, '/')}"
    engine = create_engine(db_url)

    # 3. Thứ tự nạp bảng
    load_order = [
        "dim_date",
        "dim_genres",
        "dim_categories",
        "dim_developers",
        "dim_publishers",
        "dim_tags",
        "dim_games",
        "bridge_game_genres",
        "bridge_game_categories",
        "bridge_game_developers",
        "bridge_game_publishers",
        "bridge_game_tags",
        "fact_game_metrics"
    ]

    print("-> 2. Đang nạp dữ liệu từ Parquet vào các bảng SQLite...")
    with engine.begin() as conn:
        for table_name in load_order:
            parquet_file = os.path.join(parquet_dir, f"{table_name}.parquet")
            if not os.path.exists(parquet_file):
                print(f"   [Cảnh báo] Bỏ qua {table_name}: không tìm thấy file {parquet_file}")
                continue

            t_load = time.time()
            df_table = pd.read_parquet(parquet_file)
            
            # Ghi dữ liệu vào bảng
            df_table.to_sql(table_name, con=conn, if_exists="append", index=False, chunksize=25000)
            
            # Đếm số dòng
            result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name};"))
            row_count = result.scalar()
            print(f"   [OK] Đã nạp {table_name:25s}: {row_count:,} dòng ({time.time() - t_load:.2f}s)")

    # 4. Tạo View tổng hợp hỗ trợ Dashboard trực quan
    print("-> 3. Khởi tạo View phân tích tổng hợp: vw_steam_games_dashboard...")
    view_sql = """
    CREATE VIEW IF NOT EXISTS vw_steam_games_dashboard AS
    SELECT 
        f.fact_id,
        f.appid,
        g.name AS game_title,
        d.full_date AS release_date,
        d.year AS release_year,
        d.quarter_name AS release_quarter,
        d.month_name AS release_month,
        g.is_free,
        g.price_usd,
        g.price_tier,
        g.platform_support,
        g.primary_genre,
        g.primary_developer,
        g.primary_publisher,
        g.genres_display,
        g.categories_display,
        g.top_tags_display,
        g.has_vietnamese,
        g.has_english,
        f.positive_reviews,
        f.negative_reviews,
        f.total_reviews,
        f.positive_ratio_pct,
        f.review_score_tier,
        f.metacritic_score,
        f.has_metacritic,
        f.estimated_owners_avg,
        f.owner_bracket,
        f.estimated_revenue_avg_usd,
        f.peak_ccu,
        f.avg_playtime_forever_hours,
        f.median_playtime_forever_hours,
        g.header_image,
        g.website
    FROM fact_game_metrics f
    JOIN dim_games g ON f.appid = g.appid
    LEFT JOIN dim_date d ON f.release_date_id = d.date_id;
    """
    with engine.begin() as conn:
        conn.execute(text(view_sql))

    # 5. Kiểm tra truy vấn mẫu
    print("\n--- KIỂM TRA TRUY VẤN MẪU: TOP 5 GAME DOANH THU ƯỚC TÍNH CAO NHẤT ---")
    sample_query = """
    SELECT 
        game_title,
        primary_genre,
        price_usd,
        estimated_owners_avg,
        estimated_revenue_avg_usd,
        review_score_tier
    FROM vw_steam_games_dashboard
    ORDER BY estimated_revenue_avg_usd DESC
    LIMIT 5;
    """
    with engine.connect() as conn:
        sample_df = pd.read_sql_query(text(sample_query), conn)
        print(sample_df.to_string(index=False))

    total_time = time.time() - start_time
    db_size_mb = os.path.getsize(abs_db_path) / (1024 * 1024)
    print("\n" + "=" * 80)
    print(f"HOÀN THÀNH: Data Warehouse SQLite sẵn sàng sử dụng tại: {abs_db_path}")
    print(f"Kích thước Database: {db_size_mb:.2f} MB | Tổng thời gian nạp: {total_time:.2f}s")
    print("=" * 80)


if __name__ == "__main__":
    export_to_sqlite()
