"""
=============================================================================
Module: 02_eda_profiling.py
Mục đích: Khám phá, đánh giá chất lượng và hồ sơ dữ liệu (Data Quality & Profiling)
Tác giả: Data Analyst Team
Ngày tạo: 2026-11-01
=============================================================================
Nội dung kiểm tra:
1. Kích thước tập dữ liệu (Shape, Memory Usage).
2. Kiểm tra tính duy nhất (Uniqueness) của appid (Primary Key).
3. Đánh giá tỷ lệ dữ liệu bị thiếu (Missing / Null Analysis).
4. Phân phối các chỉ số định lượng chính: giá (Price), đánh giá tích cực/tiêu cực,
   lượng người chơi đồng thời (Peak CCU), thời gian chơi (Playtime).
5. Phân phối các thuộc tính phân loại: Hệ điều hành (OS), Tỷ lệ Game miễn phí (Free vs Paid).
=============================================================================
"""

import os
import pandas as pd
import numpy as np


def run_data_profiling(raw_csv_path: str = "data/raw/games_march2025_cleaned.csv") -> dict:
    """
    Thực hiện kiểm tra chất lượng và thống kê dữ liệu đầu vào.
    
    Parameters:
    -----------
    raw_csv_path : str
        Đường dẫn tệp CSV dữ liệu thô.
        
    Returns:
    --------
    dict : Báo cáo tóm tắt các chỉ số chất lượng dữ liệu.
    """
    print("=" * 80)
    print("BẮT ĐẦU: Khám phá và Kiểm tra chất lượng dữ liệu Steam Games (Data Profiling)")
    print("=" * 80)

    if not os.path.exists(raw_csv_path):
        raise FileNotFoundError(f"Không tìm thấy tệp dữ liệu thô tại: {raw_csv_path}")

    # 1. Đọc dữ liệu
    print(f"-> Đang tải tệp: {raw_csv_path}...")
    df = pd.read_csv(raw_csv_path)
    total_rows, total_cols = df.shape
    memory_mb = df.memory_usage(deep=True).sum() / (1024 * 1024)

    print(f"   + Tổng số dòng (Records): {total_rows:,}")
    print(f"   + Tổng số cột (Features): {total_cols}")
    print(f"   + Dung lượng bộ nhớ: {memory_mb:.2f} MB\n")

    # 2. Kiểm tra tính toàn vẹn của Khóa chính (Primary Key - appid)
    unique_appids = df["appid"].nunique()
    appid_nulls = df["appid"].isnull().sum()
    print("--- 1. KIỂM TRA KHÓA CHÍNH (appid) ---")
    print(f"   + Số lượng appid duy nhất: {unique_appids:,} / {total_rows:,}")
    print(f"   + Số lượng appid bị rỗng (Null): {appid_nulls}")
    assert unique_appids == total_rows, "Lỗi: appid không phải là khóa duy nhất!"
    print("   -> ĐÁNH GIÁ: 'appid' đạt chuẩn 100% làm Khóa chính (Primary Key).\n")

    # 3. Phân tích giá trị bị thiếu (Missing Values)
    print("--- 2. CÁC CỘT CÓ TỶ LỆ DỮ LIỆU BỊ THIẾU CAO (Missing Rate > 10%) ---")
    null_counts = df.isnull().sum()
    null_pct = (null_counts / total_rows) * 100
    missing_df = pd.DataFrame({"Missing_Count": null_counts, "Missing_Pct": null_pct})
    high_missing = missing_df[missing_df["Missing_Pct"] > 10].sort_values(by="Missing_Pct", ascending=False)
    for col, row in high_missing.iterrows():
        print(f"   - {col:25s}: {row['Missing_Count']:,} dòng ({row['Missing_Pct']:.2f}%)")

    # 4. Phân tích phân khúc Giá (Price Analysis)
    print("\n--- 3. PHÂN PHỐI GIÁ VÀ TỶ LỆ GAME MIỄN PHÍ ---")
    free_games = (df["price"] == 0).sum()
    free_pct = (free_games / total_rows) * 100
    paid_games = total_rows - free_games
    print(f"   + Game miễn phí (Free-to-Play, $0): {free_games:,} ({free_pct:.2f}%)")
    print(f"   + Game trả phí (Paid Games): {paid_games:,} ({100 - free_pct:.2f}%)")
    print(f"   + Giá bán trung bình (Mean Price): ${df['price'].mean():.2f}")
    print(f"   + Giá bán trung vị (Median Price): ${df['price'].median():.2f}")
    print(f"   + Giá cao nhất (Max Price): ${df['price'].max():.2f}")

    # 5. Phân tích đánh giá (Reviews & User Sentiment)
    print("\n--- 4. TỔNG QUAN ĐÁNH GIÁ NGƯỜI DÙNG (Reviews & Sentiment) ---")
    total_positive = df["positive"].sum()
    total_negative = df["negative"].sum()
    overall_ratio = (total_positive / (total_positive + total_negative)) * 100 if (total_positive + total_negative) > 0 else 0
    print(f"   + Tổng lượt đánh giá Tích cực (Positive): {total_positive:,}")
    print(f"   + Tổng lượt đánh giá Tiêu cực (Negative): {total_negative:,}")
    print(f"   + Tỷ lệ hài lòng chung toàn nền tảng: {overall_ratio:.2f}%")

    # 6. Hỗ trợ hệ điều hành (Platform Support)
    print("\n--- 5. TỶ LỆ HỖ TRỢ CÁC HỆ ĐIỀU HÀNH ---")
    win_support = df["windows"].sum()
    mac_support = df["mac"].sum()
    linux_support = df["linux"].sum()
    print(f"   + Windows: {win_support:,} ({win_support / total_rows * 100:.2f}%)")
    print(f"   + Mac: {mac_support:,} ({mac_support / total_rows * 100:.2f}%)")
    print(f"   + Linux: {linux_support:,} ({linux_support / total_rows * 100:.2f}%)")

    print("\n" + "=" * 80)
    print("HOÀN TẤT: Dữ liệu đủ điều kiện để chuyển sang bước Làm sạch & Chuẩn hóa (ETL).")
    print("=" * 80)

    return {
        "total_rows": total_rows,
        "total_cols": total_cols,
        "free_pct": free_pct,
        "overall_positive_ratio": overall_ratio
    }


if __name__ == "__main__":
    run_data_profiling()
