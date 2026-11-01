"""
=============================================================================
Module: run_pipeline.py
Mục đích: Tự động hóa toàn diện quy trình End-to-End Data Pipeline
Tác giả: Data Analyst Team
Ngày tạo: 2026-11-01
=============================================================================
Thứ tự các giai đoạn (Stages):
1. Ingestion: Tải dữ liệu thô từ KaggleHub (01_download_data.py)
2. Profiling: Đánh giá chất lượng và hồ sơ dữ liệu (02_eda_profiling.py)
3. Transformation: Làm sạch, chuẩn hóa kiểu dữ liệu (03_clean_and_transform.py)
4. Dimensional Modeling: Xây dựng Star Schema (04_build_star_schema.py)
5. Data Warehouse Load: Nạp dữ liệu vào SQLite & kiểm tra (05_export_database.py)
=============================================================================
"""

import os
import sys
import time
import importlib

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Nạp động các module theo thứ tự pipeline
mod_01 = importlib.import_module("src.01_download_data")
mod_02 = importlib.import_module("src.02_eda_profiling")
mod_03 = importlib.import_module("src.03_clean_and_transform")
mod_04 = importlib.import_module("src.04_build_star_schema")
mod_05 = importlib.import_module("src.05_export_database")


def run_full_pipeline():
    """Chạy toàn bộ pipeline ETL từ đầu đến cuối."""
    print("#" * 80)
    print(" KHỞI CHẠY STEAM GAMES DATA ANALYST END-TO-END PIPELINE")
    print("#" * 80)
    total_start = time.time()

    # Bước 1: Tải dữ liệu
    print("\n>>> GIAI ĐOẠN 1: Thu thập Dữ liệu từ Kaggle (Data Ingestion)")
    raw_path = mod_01.download_steam_dataset()

    # Bước 2: Khám phá & Hồ sơ dữ liệu
    print("\n>>> GIAI ĐOẠN 2: Hồ sơ & Kiểm tra chất lượng Dữ liệu (EDA & Profiling)")
    mod_02.run_data_profiling(raw_path)

    # Bước 3: Làm sạch & Kỹ thuật đặc trưng
    print("\n>>> GIAI ĐOẠN 3: Làm sạch & Chuẩn hóa Dữ liệu (Cleaning & Feature Engineering)")
    mod_03.clean_and_transform_pipeline()

    # Bước 4: Xây dựng Star Schema
    print("\n>>> GIAI ĐOẠN 4: Xây dựng Star Schema & Xuất Parquet/CSV (Dimensional Modeling)")
    mod_04.build_star_schema()

    # Bước 5: Nạp Data Warehouse SQLite
    print("\n>>> GIAI ĐOẠN 5: Khởi tạo Data Warehouse SQLite (Database Loading & Verification)")
    mod_05.export_to_sqlite()

    total_elapsed = time.time() - total_start
    print("\n" + "#" * 80)
    print(f" PIPELINE HOÀN TẤT THÀNH CÔNG TRONG {total_elapsed:.2f} GIÂY!")
    print(" Sẵn sàng kết nối Dashboard Power BI / Tableau / Excel!")
    print("#" * 80)


if __name__ == "__main__":
    run_full_pipeline()
