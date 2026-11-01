-- =============================================================================
-- Steam Games Analytics Data Warehouse - Schema DDL
-- Kiến trúc: Star Schema (Ralph Kimball Methodology)
-- Hệ quản trị cơ sở dữ liệu: SQLite / PostgreSQL / MySQL / DuckDB
-- Tác giả: Data Analyst Team
-- Ngày tạo: 2026-11-01
-- =============================================================================

-- Kích hoạt kiểm tra toàn vẹn khóa ngoại (Foreign Key Enforcement)
PRAGMA foreign_keys = ON;

-- -----------------------------------------------------------------------------
-- 1. BẢNG CHIỀU THỜI GIAN: dim_date
-- Hạt dữ liệu (Grain): 1 dòng biểu diễn 1 ngày lịch duy nhất
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS dim_date (
    date_id         INTEGER PRIMARY KEY, -- Khóa chính dạng YYYYMMDD (ví dụ: 20240315)
    full_date       TEXT NOT NULL,       -- Chuỗi ngày chuẩn ISO (YYYY-MM-DD)
    year            INTEGER NOT NULL,    -- Năm phát hành (ví dụ: 2024)
    quarter         INTEGER NOT NULL,    -- Quý trong năm (1 - 4)
    quarter_name    TEXT NOT NULL,       -- Tên quý hiển thị (ví dụ: 'Q1 2024')
    month           INTEGER NOT NULL,    -- Tháng trong năm (1 - 12)
    month_name      TEXT NOT NULL,       -- Tên tháng (ví dụ: 'March')
    month_year      TEXT NOT NULL,       -- Chuỗi Năm-Tháng (ví dụ: '2024-03')
    day_of_month    INTEGER NOT NULL,    -- Ngày trong tháng (1 - 31)
    day_of_week     INTEGER NOT NULL,    -- Thứ trong tuần (1: Thứ Hai, 7: Chủ Nhật)
    day_name        TEXT NOT NULL,       -- Tên thứ (ví dụ: 'Monday')
    is_weekend      INTEGER NOT NULL     -- Cờ cuối tuần (1: Thứ Bảy/Chủ Nhật, 0: Ngày thường)
);

-- -----------------------------------------------------------------------------
-- 2. BẢNG CHIỀU THỂ LOẠI: dim_genres
-- Hạt dữ liệu (Grain): 1 dòng cho mỗi thể loại game duy nhất
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS dim_genres (
    genre_id        INTEGER PRIMARY KEY,
    genre_name      TEXT NOT NULL UNIQUE
);

-- -----------------------------------------------------------------------------
-- 3. BẢNG CHIỀU TÍNH NĂNG / HẠNG MỤC: dim_categories
-- Hạt dữ liệu (Grain): 1 dòng cho mỗi tính năng duy nhất (Single-player, Co-op,...)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS dim_categories (
    category_id     INTEGER PRIMARY KEY,
    category_name   TEXT NOT NULL UNIQUE
);

-- -----------------------------------------------------------------------------
-- 4. BẢNG CHIỀU NHÀ PHÁT TRIỂN: dim_developers
-- Hạt dữ liệu (Grain): 1 dòng cho mỗi nhà làm game (Developer)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS dim_developers (
    developer_id    INTEGER PRIMARY KEY,
    developer_name  TEXT NOT NULL UNIQUE
);

-- -----------------------------------------------------------------------------
-- 5. BẢNG CHIỀU NHÀ PHÁT HÀNH: dim_publishers
-- Hạt dữ liệu (Grain): 1 dòng cho mỗi nhà phát hành (Publisher)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS dim_publishers (
    publisher_id    INTEGER PRIMARY KEY,
    publisher_name  TEXT NOT NULL UNIQUE
);

-- -----------------------------------------------------------------------------
-- 6. BẢNG CHIỀU THẺ CỘNG ĐỒNG: dim_tags
-- Hạt dữ liệu (Grain): 1 dòng cho mỗi tag do cộng đồng người chơi gán
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS dim_tags (
    tag_id          INTEGER PRIMARY KEY,
    tag_name        TEXT NOT NULL UNIQUE
);

-- -----------------------------------------------------------------------------
-- 7. BẢNG CHIỀU THÔNG TIN TRÒ CHƠI: dim_games
-- Hạt dữ liệu (Grain): 1 dòng cho 1 tựa game Steam duy nhất (appid)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS dim_games (
    appid                       INTEGER PRIMARY KEY,
    name                        TEXT NOT NULL,
    release_date_id             INTEGER REFERENCES dim_date(date_id),
    required_age                INTEGER DEFAULT 0,
    is_free                     INTEGER DEFAULT 0,
    price_usd                   REAL DEFAULT 0.0,
    price_tier                  TEXT,
    windows                     INTEGER DEFAULT 1,
    mac                         INTEGER DEFAULT 0,
    linux                       INTEGER DEFAULT 0,
    platform_support            TEXT,
    has_vietnamese              INTEGER DEFAULT 0,
    has_english                 INTEGER DEFAULT 1,
    supported_languages_count   INTEGER DEFAULT 1,
    primary_genre               TEXT,
    primary_developer           TEXT,
    primary_publisher           TEXT,
    genres_display              TEXT,
    categories_display          TEXT,
    top_tags_display            TEXT,
    header_image                TEXT,
    website                     TEXT,
    short_description           TEXT
);

-- -----------------------------------------------------------------------------
-- 8. CÁC BẢNG CẦU NỐI NHIỀU-NHIỀU (Bridge Tables for Many-to-Many Relationships)
-- -----------------------------------------------------------------------------

-- Kết nối Game - Thể loại
CREATE TABLE IF NOT EXISTS bridge_game_genres (
    appid       INTEGER NOT NULL REFERENCES dim_games(appid),
    genre_id    INTEGER NOT NULL REFERENCES dim_genres(genre_id),
    PRIMARY KEY (appid, genre_id)
);

-- Kết nối Game - Tính năng
CREATE TABLE IF NOT EXISTS bridge_game_categories (
    appid       INTEGER NOT NULL REFERENCES dim_games(appid),
    category_id INTEGER NOT NULL REFERENCES dim_categories(category_id),
    PRIMARY KEY (appid, category_id)
);

-- Kết nối Game - Nhà phát triển
CREATE TABLE IF NOT EXISTS bridge_game_developers (
    appid           INTEGER NOT NULL REFERENCES dim_games(appid),
    developer_id    INTEGER NOT NULL REFERENCES dim_developers(developer_id),
    PRIMARY KEY (appid, developer_id)
);

-- Kết nối Game - Nhà phát hành
CREATE TABLE IF NOT EXISTS bridge_game_publishers (
    appid           INTEGER NOT NULL REFERENCES dim_games(appid),
    publisher_id    INTEGER NOT NULL REFERENCES dim_publishers(publisher_id),
    PRIMARY KEY (appid, publisher_id)
);

-- Kết nối Game - Thẻ cộng đồng (kèm số phiếu vote)
CREATE TABLE IF NOT EXISTS bridge_game_tags (
    appid       INTEGER NOT NULL REFERENCES dim_games(appid),
    tag_id      INTEGER NOT NULL REFERENCES dim_tags(tag_id),
    vote_count  INTEGER DEFAULT 0,
    PRIMARY KEY (appid, tag_id)
);

-- -----------------------------------------------------------------------------
-- 9. BẢNG SỰ KIỆN: fact_game_metrics
-- Hạt dữ liệu (Grain): 1 dòng cho mỗi tựa game Steam, lưu trữ các chỉ số đo lường
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS fact_game_metrics (
    fact_id                     INTEGER PRIMARY KEY,
    appid                       INTEGER NOT NULL REFERENCES dim_games(appid),
    release_date_id             INTEGER NOT NULL REFERENCES dim_date(date_id),
    price_usd                   REAL NOT NULL,
    discount_pct                INTEGER DEFAULT 0,
    dlc_count                   INTEGER DEFAULT 0,
    achievements                INTEGER DEFAULT 0,
    positive_reviews            INTEGER DEFAULT 0,
    negative_reviews            INTEGER DEFAULT 0,
    total_reviews               INTEGER DEFAULT 0,
    positive_ratio_pct          REAL DEFAULT 0.0,
    review_score_tier           TEXT NOT NULL,
    metacritic_score            REAL,
    has_metacritic              INTEGER DEFAULT 0,
    recommendations             INTEGER DEFAULT 0,
    estimated_owners_min        INTEGER DEFAULT 0,
    estimated_owners_max        INTEGER DEFAULT 0,
    estimated_owners_avg        INTEGER DEFAULT 0,
    owner_bracket               TEXT NOT NULL,
    estimated_revenue_min_usd   REAL DEFAULT 0.0,
    estimated_revenue_max_usd   REAL DEFAULT 0.0,
    estimated_revenue_avg_usd   REAL DEFAULT 0.0,
    peak_ccu                    INTEGER DEFAULT 0,
    avg_playtime_forever_hours  REAL DEFAULT 0.0,
    median_playtime_forever_hours REAL DEFAULT 0.0,
    avg_playtime_2weeks_hours   REAL DEFAULT 0.0,
    median_playtime_2weeks_hours REAL DEFAULT 0.0
);

-- -----------------------------------------------------------------------------
-- 10. CHỈ MỤC TỐI ƯU HÓA HIỆU NĂNG TRUY VẤN (Indexes for High-Performance Queries)
-- -----------------------------------------------------------------------------
CREATE INDEX IF NOT EXISTS idx_fact_appid ON fact_game_metrics(appid);
CREATE INDEX IF NOT EXISTS idx_fact_date ON fact_game_metrics(release_date_id);
CREATE INDEX IF NOT EXISTS idx_fact_price ON fact_game_metrics(price_usd);
CREATE INDEX IF NOT EXISTS idx_fact_revenue ON fact_game_metrics(estimated_revenue_avg_usd);
CREATE INDEX IF NOT EXISTS idx_fact_reviews ON fact_game_metrics(total_reviews);

CREATE INDEX IF NOT EXISTS idx_games_release_date ON dim_games(release_date_id);
CREATE INDEX IF NOT EXISTS idx_games_price_tier ON dim_games(price_tier);
CREATE INDEX IF NOT EXISTS idx_games_primary_genre ON dim_games(primary_genre);
CREATE INDEX IF NOT EXISTS idx_games_platform ON dim_games(platform_support);

CREATE INDEX IF NOT EXISTS idx_bridge_genres_genre ON bridge_game_genres(genre_id);
CREATE INDEX IF NOT EXISTS idx_bridge_cats_cat ON bridge_game_categories(category_id);
CREATE INDEX IF NOT EXISTS idx_bridge_devs_dev ON bridge_game_developers(developer_id);
CREATE INDEX IF NOT EXISTS idx_bridge_pubs_pub ON bridge_game_publishers(publisher_id);
CREATE INDEX IF NOT EXISTS idx_bridge_tags_tag ON bridge_game_tags(tag_id);
