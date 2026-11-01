"""
=============================================================================
Module: 03_clean_and_transform.py
Mục đích: Pipeline làm sạch, chuẩn hóa kiểu dữ liệu và kỹ thuật tính năng (Feature Engineering)
Tác giả: Data Analyst Team
Ngày tạo: 2026-11-01
=============================================================================
Nhiệm vụ chính:
1. Xử lý các giá trị Null và làm sạch chuỗi (String Trimming, URL cleaning).
2. Chuẩn hóa ngày phát hành (release_date) sang chuẩn YYYY-MM-DD và tạo khóa Date Key (YYYYMMDD).
3. Tách khoảng người sở hữu ước tính (estimated_owners) thành 3 chỉ số số học:
   - estimated_owners_min (Tối thiểu)
   - estimated_owners_max (Tối đa)
   - estimated_owners_avg (Trung bình điểm giữa)
4. Tính toán doanh thu gộp ước tính (Estimated Gross Revenue = owners_avg * price).
5. Chuẩn hóa thời gian chơi từ phút (Minutes) sang giờ (Hours).
6. Tính toán tỷ lệ đánh giá tích cực (%) và phân tầng độ uy tín (Review Score Tier).
7. Phân khúc giá bán (Price Tier) và phân loại hệ điều hành (Platform Support).
8. Trích xuất cờ ngôn ngữ (Hỗ trợ tiếng Việt, tiếng Anh) và số lượng ngôn ngữ.
9. Parse cấu trúc danh sách genres, categories, developers, publishers, tags.
10. Lưu kết quả chuẩn hóa trung gian vào: `data/staging/games_transformed.parquet`.
=============================================================================
"""

import os
import ast
import time
import pandas as pd
import numpy as np


def parse_literal_list(val) -> list:
    """Chuyển đổi chuỗi biểu diễn mảng Python '[...]' thành danh sách list an toàn."""
    if not isinstance(val, str) or not val.startswith("["):
        return []
    try:
        res = ast.literal_eval(val)
        return [str(x).strip() for x in res if str(x).strip()] if isinstance(res, list) else []
    except Exception:
        return []


def parse_literal_dict(val) -> dict:
    """Chuyển đổi chuỗi dictionary '{...}' của Steam tags thành Python dict."""
    if not isinstance(val, str) or not val.startswith("{"):
        return {}
    try:
        res = ast.literal_eval(val)
        return res if isinstance(res, dict) else {}
    except Exception:
        return {}


def parse_estimated_owners(val):
    """
    Tách chuỗi 'A - B' thành tuple (min_val, max_val, avg_val).
    Ví dụ: '100000 - 200000' -> (100000, 200000, 150000)
    """
    if pd.isna(val) or val == "0 - 0":
        return 0, 0, 0
    parts = str(val).split(" - ")
    if len(parts) == 2:
        try:
            low = int(parts[0].strip())
            high = int(parts[1].strip())
            return low, high, int((low + high) / 2)
        except ValueError:
            return 0, 0, 0
    return 0, 0, 0


def classify_price_tier(price: float) -> str:
    """Phân khúc giá game cho báo cáo trực quan hóa."""
    if price == 0.0:
        return "Free ($0)"
    elif price < 5.0:
        return "Budget (< $5)"
    elif price < 15.0:
        return "Standard ($5 - $14.99)"
    elif price < 30.0:
        return "Mid-Tier ($15 - $29.99)"
    elif price < 60.0:
        return "Premium ($30 - $59.99)"
    else:
        return "AAA / High-End ($60+)"


def classify_review_tier(positive: int, total: int) -> str:
    """
    Phân loại đánh giá Steam theo chuẩn chính thức của Valve:
    - Overwhelmingly Positive: >= 95% positive & total >= 500
    - Very Positive: >= 80% positive & total >= 50
    - Positive: >= 80% positive & total < 50
    - Mostly Positive: >= 70% positive
    - Mixed: 40% - 69% positive
    - Mostly Negative: 20% - 39% positive
    - Negative: < 20% positive
    - No Reviews: total == 0
    """
    if total == 0:
        return "No Reviews"
    pct = (positive / total) * 100
    if pct >= 95 and total >= 500:
        return "Overwhelmingly Positive"
    elif pct >= 80 and total >= 50:
        return "Very Positive"
    elif pct >= 80:
        return "Positive"
    elif pct >= 70:
        return "Mostly Positive"
    elif pct >= 40:
        return "Mixed"
    elif pct >= 20:
        return "Mostly Negative"
    else:
        return "Negative"


def classify_platform_support(win: bool, mac: bool, linux: bool) -> str:
    """Phân nhóm tương thích nền tảng OS."""
    if win and mac and linux:
        return "Cross-Platform (Win/Mac/Linux)"
    elif win and mac:
        return "Windows & Mac"
    elif win and linux:
        return "Windows & Linux"
    elif win:
        return "Windows Only"
    elif mac:
        return "Mac Only"
    elif linux:
        return "Linux Only"
    else:
        return "Other"


def clean_and_transform_pipeline(
    input_csv: str = "data/raw/games_march2025_cleaned.csv",
    output_parquet: str = "data/staging/games_transformed.parquet"
) -> pd.DataFrame:
    """
    Thực thi quy trình làm sạch và làm giàu dữ liệu.
    """
    print("=" * 80)
    print("BẮT ĐẦU: Quy trình Làm sạch và Chuẩn hóa Dữ liệu (Clean & Transform ETL)")
    print("=" * 80)
    start_time = time.time()

    if not os.path.exists(input_csv):
        raise FileNotFoundError(f"Tệp nguồn không tồn tại: {input_csv}")

    print(f"-> 1. Đang đọc dữ liệu thô: {input_csv}...")
    df = pd.read_csv(input_csv)
    initial_rows = len(df)
    print(f"   + Số dòng dữ liệu đầu vào: {initial_rows:,}")

    # 1. Làm sạch Tên game và xử lý khoảng trắng
    print("-> 2. Chuẩn hóa tên game và các trường văn bản cơ bản...")
    df["name"] = df["name"].fillna("Unknown Title").astype(str).str.strip()

    # 2. Xử lý Ngày phát hành (release_date)
    print("-> 3. Chuẩn hóa Ngày phát hành và tạo Date Key...")
    df["release_date"] = pd.to_datetime(df["release_date"], format="%Y-%m-%d", errors="coerce")
    # Thay thế các ngày lỗi bằng mốc mặc định nếu có
    df["release_date"] = df["release_date"].fillna(pd.Timestamp("2000-01-01"))
    df["release_date_str"] = df["release_date"].dt.strftime("%Y-%m-%d")
    df["release_date_id"] = df["release_date"].dt.strftime("%Y%m%d").astype(int)

    # 3. Xử lý Giá (Price) và Phân khúc giá
    print("-> 4. Phân tích giá và phân khúc sản phẩm (Price Tiers)...")
    df["price_usd"] = df["price"].fillna(0.0).astype(float).round(2)
    df["is_free"] = (df["price_usd"] == 0.0).astype(int)
    df["discount_pct"] = df["discount"].fillna(0).astype(int)
    df["price_tier"] = df["price_usd"].apply(classify_price_tier)

    # 4. Xử lý Người sở hữu ước tính (Estimated Owners)
    print("-> 5. Trích xuất số lượng người sở hữu ước tính (Min, Max, Avg) và Doanh thu...")
    parsed_owners = [parse_estimated_owners(x) for x in df["estimated_owners"]]
    df["estimated_owners_min"] = [x[0] for x in parsed_owners]
    df["estimated_owners_max"] = [x[1] for x in parsed_owners]
    df["estimated_owners_avg"] = [x[2] for x in parsed_owners]
    df["owner_bracket"] = df["estimated_owners"].fillna("0 - 0").astype(str)

    # Doanh thu ước tính (Gross Revenue = Avg Owners * Price)
    df["estimated_revenue_avg_usd"] = (df["estimated_owners_avg"] * df["price_usd"]).round(2)
    df["estimated_revenue_min_usd"] = (df["estimated_owners_min"] * df["price_usd"]).round(2)
    df["estimated_revenue_max_usd"] = (df["estimated_owners_max"] * df["price_usd"]).round(2)

    # 5. Xử lý Đánh giá người dùng (Reviews & Ratings)
    print("-> 6. Tính toán chỉ số đánh giá (Total Reviews, Positive Ratio, Review Tiers)...")
    df["positive_reviews"] = df["positive"].fillna(0).astype(int)
    df["negative_reviews"] = df["negative"].fillna(0).astype(int)
    df["total_reviews"] = df["positive_reviews"] + df["negative_reviews"]
    
    # Tỷ lệ % đánh giá tích cực
    pos_mask = df["total_reviews"] > 0
    df["positive_ratio_pct"] = 0.0
    df.loc[pos_mask, "positive_ratio_pct"] = (
        (df.loc[pos_mask, "positive_reviews"] / df.loc[pos_mask, "total_reviews"]) * 100
    ).round(2)

    # Phân tầng đánh giá Steam
    df["review_score_tier"] = [
        classify_review_tier(pos, tot) for pos, tot in zip(df["positive_reviews"], df["total_reviews"])
    ]

    # Metacritic score (0 nghĩa là chưa có điểm -> chuyển thành None để tính trung bình chuẩn)
    df["metacritic_score"] = df["metacritic_score"].replace(0, np.nan)
    df["has_metacritic"] = df["metacritic_score"].notnull().astype(int)

    # 6. Chuẩn hóa Thời gian chơi (Playtime in Hours)
    print("-> 7. Chuyển đổi đơn vị thời gian chơi sang Giờ (Hours)...")
    df["avg_playtime_forever_hours"] = (df["average_playtime_forever"].fillna(0) / 60.0).round(2)
    df["median_playtime_forever_hours"] = (df["median_playtime_forever"].fillna(0) / 60.0).round(2)
    df["avg_playtime_2weeks_hours"] = (df["average_playtime_2weeks"].fillna(0) / 60.0).round(2)
    df["median_playtime_2weeks_hours"] = (df["median_playtime_2weeks"].fillna(0) / 60.0).round(2)
    df["peak_ccu"] = df["peak_ccu"].fillna(0).astype(int)

    # 7. Phân loại Hệ điều hành (Platforms)
    print("-> 8. Phân loại khả năng tương thích Hệ điều hành...")
    df["windows"] = df["windows"].fillna(False).astype(bool)
    df["mac"] = df["mac"].fillna(False).astype(bool)
    df["linux"] = df["linux"].fillna(False).astype(bool)
    df["platform_support"] = [
        classify_platform_support(w, m, l) for w, m, l in zip(df["windows"], df["mac"], df["linux"])
    ]

    # 8. Parse Danh sách Genres, Categories, Developers, Publishers, Tags
    print("-> 9. Phân tích các trường mảng (Genres, Categories, Devs, Pubs, Tags)...")
    genres_list = [parse_literal_list(x) for x in df["genres"]]
    categories_list = [parse_literal_list(x) for x in df["categories"]]
    devs_list = [parse_literal_list(x) for x in df["developers"]]
    pubs_list = [parse_literal_list(x) for x in df["publishers"]]
    langs_list = [parse_literal_list(x) for x in df["supported_languages"]]
    tags_dict_list = [parse_literal_dict(x) for x in df["tags"]]

    # Gán vào DataFrame dạng đối tượng
    df["genres_parsed"] = genres_list
    df["categories_parsed"] = categories_list
    df["developers_parsed"] = devs_list
    df["publishers_parsed"] = pubs_list
    df["supported_languages_parsed"] = langs_list
    df["tags_parsed"] = tags_dict_list

    # Trích xuất thuộc tính đại diện chính (Primary Attributes) & chuỗi hiển thị
    df["primary_genre"] = [g[0] if len(g) > 0 else "Uncategorized" for g in genres_list]
    df["primary_developer"] = [d[0] if len(d) > 0 else "Unknown Developer" for d in devs_list]
    df["primary_publisher"] = [p[0] if len(p) > 0 else "Unknown Publisher" for p in pubs_list]
    
    df["genres_display"] = [", ".join(g) if len(g) > 0 else "Uncategorized" for g in genres_list]
    df["categories_display"] = [", ".join(c) if len(c) > 0 else "None" for c in categories_list]
    df["top_tags_display"] = [", ".join(list(t.keys())[:5]) if len(t) > 0 else "None" for t in tags_dict_list]

    # Ngôn ngữ
    df["supported_languages_count"] = [len(l) for l in langs_list]
    df["has_vietnamese"] = [1 if "Vietnamese" in l else 0 for l in langs_list]
    df["has_english"] = [1 if "English" in l else 0 for l in langs_list]

    # 9. Lưu dữ liệu đã biến đổi ra Staging Parquet
    os.makedirs(os.path.dirname(output_parquet), exist_ok=True)
    print(f"-> 10. Đang lưu tệp Staging Parquet: {output_parquet}...")
    
    # Loại bỏ các cột không còn cần thiết trước khi lưu staging
    cols_to_drop = ["reviews", "packages", "movies", "score_rank", "notes"]
    staging_df = df.drop(columns=[c for c in cols_to_drop if c in df.columns])
    
    # Ghi ra tệp Parquet
    staging_df.to_parquet(output_parquet, index=False, engine="pyarrow")

    elapsed = time.time() - start_time
    file_size_mb = os.path.getsize(output_parquet) / (1024 * 1024)
    print(f"-> Đã lưu Staging Parquet thành công: {file_size_mb:.2f} MB trong {elapsed:.2f} giây.")
    print("=" * 80)
    print("HOÀN TẤT BƯỚC 3: Dữ liệu đã được làm sạch và chuẩn hóa toàn diện.")
    print("=" * 80)

    return staging_df


if __name__ == "__main__":
    clean_and_transform_pipeline()
