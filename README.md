# Steam Games Market Analytics & Data Warehouse 🎮📊

Dự án Phân tích Dữ liệu Toàn diện Thị trường Steam Game được xây dựng theo chuẩn chuyên nghiệp của **Data Analyst / Analytics Engineer**. 

Toàn bộ quy trình từ **Thu thập dữ liệu (Ingestion)**, **Khám phá & Kiểm định chất lượng (EDA & Profiling)**, **Làm sạch & Chuẩn hóa (ETL)**, **Thiết kế Mô hình Đa chiều (Star Schema)** đến **Lưu trữ Data Warehouse** đều được tự động hóa, tài liệu hóa chi tiết và sẵn sàng 100% để kết nối trực tiếp vào các công cụ BI (**Power BI, Tableau, Excel**).

---

## 📌 Điểm Nổi Bật Của Dự Án

- **Dữ liệu chuẩn xác & cập nhật:** Khai thác hơn **89,618 trò chơi** chính thức trên Steam từ bộ dữ liệu `artermiloff/steam-games-dataset` (đã loại bỏ Playtest, bản beta không chính thức).
- **Mô hình hóa dữ liệu chuẩn Ralph Kimball (Star Schema):** Tách bạch rõ ràng giữa **Fact Table** (`fact_game_metrics`) và các **Dimension Tables** (`dim_games`, `dim_date`, `dim_genres`, `dim_categories`, `dim_developers`, `dim_publishers`, `dim_tags`), chuẩn hóa các quan hệ Nhiều - Nhiều (Many-to-Many) qua **Bridge Tables**.
- **Kỹ thuật tính năng kinh doanh (Business Feature Engineering):**
  - Tách khoảng người sở hữu (`estimated_owners`) thành các giá trị số học: `min`, `max`, `avg`.
  - Ước tính doanh thu gộp (`estimated_gross_revenue = owners_avg * price`).
  - Phân khúc giá (`price_tier`) và phân loại đánh giá người dùng theo chuẩn Valve (`review_score_tier`).
  - Chuẩn hóa thời gian chơi từ phút sang giờ (`playtime_hours`).
  - Trích xuất cờ tương thích hệ điều hành (`platform_support`) và hỗ trợ bản địa hóa **Tiếng Việt** (`has_vietnamese`).
- **Đa dạng hình thức lưu trữ (Ready-to-use):**
  - **SQLite Data Warehouse (`steam_dw.db`):** Chứa toàn bộ các bảng, ràng buộc khóa chính/ngoại, chỉ mục tối ưu và View tổng hợp `vw_steam_games_dashboard`.
  - **Parquet Columnar Files:** Định dạng nén hiệu năng cao, tải cực nhanh cho Power BI, Python, DuckDB.
  - **Clean CSV Files:** Sẵn sàng cho người dùng Excel hoặc Power BI kéo thả trực tiếp.
- **Tài liệu & Chú thích 100% Tiếng Việt:** Code Python, kịch bản SQL DDL, truy vấn phân tích kinh doanh và từ điển dữ liệu (Data Dictionary).

---

## 🗂️ Cấu Trúc Thư Mục Dự Án

```
D:\Steam-Game-Analyst-
│
├── .gitignore                   # Cấu hình bỏ qua tệp tạm, cache và dữ liệu thô lớn
├── README.md                    # Tài liệu tổng quan dự án và hướng dẫn sử dụng
├── requirements.txt             # Danh sách thư viện Python phụ thuộc
│
├── data/
│   ├── raw/                     # Dữ liệu thô tải từ KaggleHub (games_march2025_cleaned.csv)
│   ├── staging/                 # Dữ liệu trung gian sau khi làm sạch sơ bộ (.parquet)
│   └── processed/               # DỮ LIỆU SẠCH SẴN SÀNG CHO DASHBOARD
│       ├── steam_dw.db          # Cơ sở dữ liệu SQLite Data Warehouse hoàn chỉnh
│       ├── parquet/             # 14 tệp Parquet chuẩn Star Schema + Bảng phẳng BI
│       └── csv/                 # 14 tệp CSV định dạng UTF-8-BOM cho Excel/Power BI
│
├── src/                         # Mã nguồn ETL Pipeline hoàn chỉnh
│   ├── 01_download_data.py      # Tải dữ liệu tự động qua KaggleHub API
│   ├── 02_eda_profiling.py      # Khám phá và kiểm tra chất lượng dữ liệu đầu vào
│   ├── 03_clean_and_transform.py# Làm sạch, ép kiểu và kỹ thuật tính năng nghiệp vụ
│   ├── 04_build_star_schema.py  # Xây dựng Star Schema (Fact, Dims, Bridges, Flat table)
│   ├── 05_export_database.py    # Nạp dữ liệu vào SQLite và tạo View phân tích
│   └── run_pipeline.py          # Kịch bản chạy toàn bộ End-to-End Pipeline chỉ bằng 1 lệnh
│
├── sql/                         # Kịch bản cơ sở dữ liệu SQL
│   ├── schema_ddl.sql           # DDL khởi tạo bảng, khóa chính, khóa ngoại và chỉ mục (Index)
│   └── business_queries.sql     # 10 câu truy vấn giải quyết các bài toán kinh doanh thực tế
│
├── notebooks/                   # Jupyter Notebook phân tích trực quan
│   └── 01_exploratory_data_analysis.ipynb
│
└── docs/                        # Tài liệu chi tiết
    ├── data_dictionary.md       # Từ điển dữ liệu chi tiết từng cột, kiểu và ý nghĩa
    └── star_schema_erd.md       # Sơ đồ thực thể quan hệ ERD và hướng dẫn mô hình hóa
```

---

## ⚡ Hướng Dẫn Khởi Chạy Nhanh (Quick Start)

### 1. Cài đặt môi trường
Đảm bảo bạn đã cài đặt Python (>= 3.10). Cài đặt các thư viện phụ thuộc:
```bash
pip install -r requirements.txt
```

### 2. Chạy toàn bộ Pipeline chỉ với 1 lệnh duy nhất:
```bash
python src/run_pipeline.py
```
*Pipeline sẽ tự động tải dữ liệu, kiểm tra chất lượng, làm sạch, tạo 14 bảng Star Schema và nạp vào Data Warehouse SQLite trong vòng chưa đầy 1 phút!*

---

## 📊 Hướng Dẫn Kết Nối Dashboard (Power BI / Tableau / Excel)

### Cách 1: Kéo thả 1 bảng phẳng duy nhất (Nhanh nhất - Không cần tạo quan hệ)
1. Mở **Power BI Desktop** -> Chọn **Get Data** -> Chọn **Parquet** (hoặc **Text/CSV**).
2. Trỏ đến tệp: `data/processed/parquet/flat_steam_games_bi.parquet` (hoặc `data/processed/csv/flat_steam_games_bi.csv`).
3. Toàn bộ các thước đo doanh thu, rating, phân khúc giá, ngày phát hành đã được join sẵn. Bạn chỉ cần kéo thả vào biểu đồ!

### Cách 2: Kết nối Data Warehouse SQLite (Mô hình hóa chuyên sâu)
1. Mở **Power BI Desktop** -> Chọn **Get Data** -> Chọn **ODBC** (hoặc SQLite Driver).
2. Trỏ đến tệp cơ sở dữ liệu: `data/processed/steam_dw.db`.
3. Bạn có thể chọn:
   - Toàn bộ các bảng trong **Star Schema** (`fact_game_metrics`, `dim_games`, `dim_date`, `bridge_game_genres`...) và nối quan hệ theo hướng dẫn trong [docs/star_schema_erd.md](file:///D:/Steam-Game-Analyst-/docs/star_schema_erd.md).
   - Hoặc chọn View tổng hợp: `vw_steam_games_dashboard`.

---

## 📈 Tóm Tắt Một Số Chỉ Số Thị Trường Nổi Bật (Executive Highlights)

| Chỉ Số Kinh Doanh | Giá Trị Thực Tế | Ghi Chú |
| :--- | :---: | :--- |
| **Tổng số tựa game phân tích** | **89,618** | Đã loại bỏ playtest/beta |
| **Tỷ lệ game miễn phí (Free-to-Play)** | **15.80%** (14,160 game) | Tỷ lệ game trả phí là 84.20% |
| **Giá bán trung bình toàn nền tảng** | **\$7.31 USD** | Giá trung vị là \$4.99 USD |
| **Tổng doanh thu ước tính toàn thị trường** | **\$130.83 Tỷ USD** | Dựa trên ước tính người sở hữu |
| **Tỷ lệ đánh giá hài lòng chung** | **85.82%** | Dựa trên > 132 triệu lượt review |
| **Số lượng game hỗ trợ Tiếng Việt** | **3,553** (3.96%) | Lượng người sở hữu TB cao gấp 2.5 lần game thông thường |

---

## 🎯 Danh Mục Truy Vấn SQL Mẫu Có Sẵn

Trong tệp [sql/business_queries.sql](file:///D:/Steam-Game-Analyst-/sql/business_queries.sql), bạn có sẵn 10 câu truy vấn tối ưu hóa sẵn:
1. **Báo cáo tổng quan KPI toàn sàn Steam**.
2. **Top 10 tựa game đạt doanh thu ước tính cao nhất mọi thời đại**.
3. **Thị phần doanh thu và giá bán theo Thể loại (Genre Market Share)**.
4. **Phân tích độ co giãn và hiệu quả của các Phân khúc giá (Price Tiers)**.
5. **Xu hướng tăng trưởng số lượng game phát hành qua từng năm (2005 - 2025)**.
6. **Top 10 Nhà phát hành (Publishers) thống trị thị trường**.
7. **Cơ hội thị trường cho Game có bản địa hóa Tiếng Việt**.
8. **So sánh Điểm chuyên môn Metacritic và Đánh giá cộng đồng Steam**.
9. **Giá trị thương mại của việc phát hành Đa nền tảng (Windows / Mac / Linux)**.
10. **Top 15 Thẻ người dùng (Steam Tags) có lượt bình chọn cao nhất**.

---
*Dự án được bảo trì bởi Data Analyst Team.*
