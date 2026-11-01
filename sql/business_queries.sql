-- =============================================================================
-- Steam Games Market Analytics - Business Analysis Queries
-- Mục đích: Bộ câu truy vấn SQL mẫu giải quyết các bài toán kinh doanh cốt lõi
-- Đối tượng phục vụ: Dashboard Power BI / Tableau / Báo cáo phân tích thị trường
-- Tác giả: Data Analyst Team
-- Ngày tạo: 2026-11-01
-- =============================================================================

-- =============================================================================
-- 1. BÁO CÁO TỔNG QUAN TOÀN NỀN TẢNG STEAM (Executive Summary KPI)
-- Mục đích: Đo lường quy mô nền tảng, cơ cấu sản phẩm và dung lượng thị trường
-- =============================================================================
SELECT 
    COUNT(f.appid) AS total_games,
    SUM(CASE WHEN g.is_free = 1 THEN 1 ELSE 0 END) AS total_free_games,
    SUM(CASE WHEN g.is_free = 0 THEN 1 ELSE 0 END) AS total_paid_games,
    ROUND(AVG(g.price_usd), 2) AS avg_game_price_usd,
    ROUND(SUM(f.estimated_revenue_avg_usd) / 1000000000.0, 2) AS total_market_est_revenue_billion_usd,
    SUM(f.positive_reviews) AS total_positive_reviews,
    SUM(f.negative_reviews) AS total_negative_reviews,
    ROUND(SUM(f.positive_reviews) * 100.0 / (SUM(f.positive_reviews) + SUM(f.negative_reviews)), 2) AS platform_satisfaction_rate_pct,
    MAX(f.peak_ccu) AS highest_concurrent_players
FROM fact_game_metrics f
JOIN dim_games g ON f.appid = g.appid;


-- =============================================================================
-- 2. TOP 10 TỰA GAME DOANH THU ƯỚC TÍNH CAO NHẤT (Top 10 Revenue Blockbusters)
-- Mục đích: Nhận diện các tựa game dẫn đầu về mặt thương mại
-- =============================================================================
SELECT 
    g.name AS game_title,
    g.primary_genre,
    g.primary_developer,
    g.primary_publisher,
    d.year AS release_year,
    g.price_usd,
    f.estimated_owners_avg,
    ROUND(f.estimated_revenue_avg_usd / 1000000.0, 2) AS est_revenue_million_usd,
    f.positive_ratio_pct,
    f.review_score_tier
FROM fact_game_metrics f
JOIN dim_games g ON f.appid = g.appid
LEFT JOIN dim_date d ON f.release_date_id = d.date_id
ORDER BY f.estimated_revenue_avg_usd DESC
LIMIT 10;


-- =============================================================================
-- 3. PHÂN TÍCH THỊ PHẦN VÀ HIỆU QUẢ THEO THỂ LOẠI (Genre Market Share Analysis)
-- Mục đích: Đánh giá thể loại nào đem lại doanh thu cao nhất và độ cạnh tranh
-- =============================================================================
SELECT 
    gen.genre_name,
    COUNT(DISTINCT bg.appid) AS total_games_count,
    ROUND(SUM(f.estimated_revenue_avg_usd) / 1000000.0, 2) AS total_est_revenue_million_usd,
    ROUND(AVG(f.estimated_revenue_avg_usd), 2) AS avg_revenue_per_game_usd,
    ROUND(AVG(g.price_usd), 2) AS avg_genre_price_usd,
    ROUND(AVG(f.positive_ratio_pct), 2) AS avg_satisfaction_pct,
    ROUND(SUM(f.estimated_revenue_avg_usd) * 100.0 / (SELECT SUM(estimated_revenue_avg_usd) FROM fact_game_metrics), 2) AS revenue_market_share_pct
FROM bridge_game_genres bg
JOIN dim_genres gen ON bg.genre_id = gen.genre_id
JOIN fact_game_metrics f ON bg.appid = f.appid
JOIN dim_games g ON bg.appid = g.appid
GROUP BY gen.genre_id, gen.genre_name
ORDER BY total_est_revenue_million_usd DESC;


-- =============================================================================
-- 4. HIỆU QUẢ CỦA CÁC PHÂN KHÚC GIÁ (Pricing Strategy & Price Tiers)
-- Mục đích: Tìm ra "điểm ngọt" (Sweet Spot) về giá bán tối ưu hóa doanh thu
-- =============================================================================
SELECT 
    g.price_tier,
    COUNT(g.appid) AS total_games,
    ROUND(COUNT(g.appid) * 100.0 / (SELECT COUNT(*) FROM dim_games), 2) AS pct_of_catalog,
    ROUND(AVG(f.estimated_owners_avg), 0) AS avg_owners_per_game,
    ROUND(AVG(f.estimated_revenue_avg_usd), 2) AS avg_revenue_per_game_usd,
    ROUND(SUM(f.estimated_revenue_avg_usd) / 1000000.0, 2) AS total_revenue_million_usd,
    ROUND(AVG(f.positive_ratio_pct), 2) AS avg_positive_ratio_pct,
    ROUND(AVG(f.avg_playtime_forever_hours), 2) AS avg_playtime_hours
FROM dim_games g
JOIN fact_game_metrics f ON g.appid = f.appid
GROUP BY g.price_tier
ORDER BY total_revenue_million_usd DESC;


-- =============================================================================
-- 5. XU HƯỚNG PHÁT TRIỂN CỦA NỀN TẢNG THEO NĂM (Yearly Growth & Release Trends)
-- Mục đích: Thể hiện tốc độ tăng trưởng số lượng game phát hành qua từng năm
-- =============================================================================
SELECT 
    d.year AS release_year,
    COUNT(f.appid) AS games_released_count,
    ROUND(SUM(f.estimated_revenue_avg_usd) / 1000000.0, 2) AS total_revenue_million_usd,
    ROUND(AVG(f.positive_ratio_pct), 2) AS avg_positive_ratio_pct,
    ROUND(AVG(g.price_usd), 2) AS avg_launch_price_usd,
    SUM(f.peak_ccu) AS total_peak_ccu
FROM fact_game_metrics f
JOIN dim_games g ON f.appid = g.appid
JOIN dim_date d ON f.release_date_id = d.date_id
WHERE d.year >= 2005
GROUP BY d.year
ORDER BY d.year ASC;


-- =============================================================================
-- 6. TOP 10 NHÀ PHÁT HÀNH (PUBLISHERS) THÀNH CÔNG NHẤT
-- Mục đích: Xác định các Publisher có thị phần áp đảo trên Steam
-- =============================================================================
SELECT 
    p.publisher_name,
    COUNT(DISTINCT bp.appid) AS games_published_count,
    ROUND(SUM(f.estimated_revenue_avg_usd) / 1000000.0, 2) AS total_revenue_million_usd,
    ROUND(AVG(f.estimated_revenue_avg_usd), 2) AS avg_revenue_per_game_usd,
    ROUND(AVG(f.positive_ratio_pct), 2) AS avg_rating_pct,
    SUM(f.peak_ccu) AS total_peak_ccu
FROM bridge_game_publishers bp
JOIN dim_publishers p ON bp.publisher_id = p.publisher_id
JOIN fact_game_metrics f ON bp.appid = f.appid
GROUP BY p.publisher_id, p.publisher_name
HAVING games_published_count >= 3
ORDER BY total_revenue_million_usd DESC
LIMIT 10;


-- =============================================================================
-- 7. CƠ HỘI THỊ TRƯỜNG: GAME CÓ HỖ TRỢ TIẾNG VIỆT (Vietnamese Language Market)
-- Mục đích: Đánh giá tiềm năng và mức độ thành công của các game có bản địa hóa Tiếng Việt
-- =============================================================================
SELECT 
    CASE WHEN g.has_vietnamese = 1 THEN 'Có hỗ trợ Tiếng Việt' ELSE 'Không hỗ trợ Tiếng Việt' END AS vietnamese_support_status,
    COUNT(g.appid) AS total_games,
    ROUND(COUNT(g.appid) * 100.0 / (SELECT COUNT(*) FROM dim_games), 2) AS pct_of_catalog,
    ROUND(AVG(f.estimated_owners_avg), 0) AS avg_owners,
    ROUND(AVG(f.estimated_revenue_avg_usd), 2) AS avg_revenue_usd,
    ROUND(AVG(f.positive_ratio_pct), 2) AS avg_satisfaction_pct,
    ROUND(AVG(f.avg_playtime_forever_hours), 2) AS avg_playtime_hours
FROM dim_games g
JOIN fact_game_metrics f ON g.appid = f.appid
GROUP BY g.has_vietnamese;


-- =============================================================================
-- 8. SO SÁNH GIỮA ĐIỂM METACRITIC VÀ ĐÁNH GIÁ NGƯỜI CHƠI (Metacritic vs Steam Sentiment)
-- Mục đích: Kiểm tra xem các game được giới phê bình khen ngợi có được lòng game thủ không
-- =============================================================================
SELECT 
    CASE 
        WHEN f.metacritic_score >= 90 THEN '90 - 100 (Masterpiece)'
        WHEN f.metacritic_score >= 80 THEN '80 - 89 (Great)'
        WHEN f.metacritic_score >= 70 THEN '70 - 79 (Good)'
        WHEN f.metacritic_score >= 50 THEN '50 - 69 (Average)'
        ELSE '< 50 (Poor)'
    END AS metacritic_tier,
    COUNT(f.appid) AS game_count,
    ROUND(AVG(f.metacritic_score), 1) AS avg_meta_score,
    ROUND(AVG(f.positive_ratio_pct), 2) AS avg_user_satisfaction_pct,
    ROUND(AVG(f.estimated_revenue_avg_usd) / 1000000.0, 2) AS avg_revenue_million_usd
FROM fact_game_metrics f
WHERE f.has_metacritic = 1
GROUP BY metacritic_tier
ORDER BY avg_meta_score DESC;


-- =============================================================================
-- 9. PHÂN TÍCH TƯƠNG THÍCH ĐA NỀN TẢNG (Multi-Platform Support Value)
-- Mục đích: Đo lường lợi ích kinh tế khi phát hành game trên cả Mac/Linux ngoài Windows
-- =============================================================================
SELECT 
    g.platform_support,
    COUNT(g.appid) AS game_count,
    ROUND(AVG(f.estimated_revenue_avg_usd), 2) AS avg_revenue_usd,
    ROUND(AVG(f.estimated_owners_avg), 0) AS avg_owners,
    ROUND(AVG(f.positive_ratio_pct), 2) AS avg_positive_ratio_pct
FROM dim_games g
JOIN fact_game_metrics f ON g.appid = f.appid
GROUP BY g.platform_support
ORDER BY avg_revenue_usd DESC;


-- =============================================================================
-- 10. TOP 15 THẺ CỘNG ĐỒNG (TAGS) ĐƯỢC BÌNH CHỌN VÀ YÊU THÍCH NHẤT
-- Mục đích: Phân tích xu hướng gameplay mà cộng đồng game thủ quan tâm nhất
-- =============================================================================
SELECT 
    t.tag_name,
    COUNT(DISTINCT bt.appid) AS associated_games_count,
    SUM(bt.vote_count) AS total_community_votes,
    ROUND(AVG(f.positive_ratio_pct), 2) AS avg_game_satisfaction_pct,
    ROUND(SUM(f.estimated_revenue_avg_usd) / 1000000.0, 2) AS total_revenue_million_usd
FROM bridge_game_tags bt
JOIN dim_tags t ON bt.tag_id = t.tag_id
JOIN fact_game_metrics f ON bt.appid = f.appid
GROUP BY t.tag_id, t.tag_name
ORDER BY total_community_votes DESC
LIMIT 15;
