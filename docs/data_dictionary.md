# Từ Điển Dữ Liệu - Steam Games Analytics Data Warehouse (Data Dictionary)

Tài liệu này định nghĩa chi tiết cấu trúc bảng, kiểu dữ liệu, ràng buộc khóa và ý nghĩa nghiệp vụ của tất cả các thực thể trong Data Warehouse `steam_dw.db` theo mô hình Star Schema.

---

## 1. Bảng Chiều (Dimension Tables)

### 1.1. `dim_date` (Chiều Thời Gian Phát Hành)
*Hạt dữ liệu (Grain):* 1 dòng biểu diễn 1 ngày lịch duy nhất.

| Tên Cột | Kiểu Dữ Liệu | Khóa | Cho phép Null | Mô Tả & Ý Nghĩa Nghiệp Vụ | Giá Trị Mẫu |
| :--- | :--- | :---: | :---: | :--- | :--- |
| `date_id` | INTEGER | **PK** | Không | Mã định danh ngày dạng YYYYMMDD | `20240315` |
| `full_date` | TEXT | | Không | Ngày chuẩn ISO 8601 (YYYY-MM-DD) | `2024-03-15` |
| `year` | INTEGER | | Không | Năm phát hành | `2024` |
| `quarter` | INTEGER | | Không | Quý trong năm (1 đến 4) | `1` |
| `quarter_name` | TEXT | | Không | Nhãn quý hiển thị trên biểu đồ | `Q1 2024` |
| `month` | INTEGER | | Không | Tháng trong năm (1 đến 12) | `3` |
| `month_name` | TEXT | | Không | Tên tiếng Anh của tháng | `March` |
| `month_year` | TEXT | | Không | Chuỗi Năm-Tháng dùng để sort timeline | `2024-03` |
| `day_of_month` | INTEGER | | Không | Ngày trong tháng (1 đến 31) | `15` |
| `day_of_week` | INTEGER | | Không | Thứ trong tuần (1: Thứ Hai, 7: Chủ Nhật) | `5` |
| `day_name` | TEXT | | Không | Tên thứ trong tuần | `Friday` |
| `is_weekend` | INTEGER | | Không | Cờ cuối tuần (1: Thứ Bảy/CN, 0: Ngày thường) | `0` |

---

### 1.2. `dim_games` (Chiều Thông Tin Trò Chơi)
*Hạt dữ liệu (Grain):* 1 dòng cho 1 tựa game Steam duy nhất.

| Tên Cột | Kiểu Dữ Liệu | Khóa | Cho phép Null | Mô Tả & Ý Nghĩa Nghiệp Vụ | Giá Trị Mẫu |
| :--- | :--- | :---: | :---: | :--- | :--- |
| `appid` | INTEGER | **PK** | Không | Mã định danh game chính thức trên Steam | `730` |
| `name` | TEXT | | Không | Tên chính thức của tựa game | `Counter-Strike 2` |
| `release_date_id` | INTEGER | **FK** | Có | Khóa ngoại liên kết `dim_date.date_id` | `20120821` |
| `required_age` | INTEGER | | Không | Độ tuổi tối thiểu quy định (0, 18...) | `0` |
| `is_free` | INTEGER | | Không | Cờ game miễn phí (1: Free-to-play, 0: Trả phí) | `1` |
| `price_usd` | REAL | | Không | Giá niêm yết hiện tại (USD) | `0.0` |
| `price_tier` | TEXT | | Không | Phân khúc giá (Free, Budget, Standard, AAA...) | `Free ($0)` |
| `windows` | INTEGER | | Không | Hỗ trợ hệ điều hành Windows (1/0) | `1` |
| `mac` | INTEGER | | Không | Hỗ trợ hệ điều hành macOS (1/0) | `0` |
| `linux` | INTEGER | | Không | Hỗ trợ hệ điều hành Linux/SteamOS (1/0) | `1` |
| `platform_support` | TEXT | | Không | Phân loại tương thích nền tảng | `Windows & Linux` |
| `has_vietnamese` | INTEGER | | Không | Cờ có hỗ trợ giao diện/phụ đề Tiếng Việt | `1` |
| `has_english` | INTEGER | | Không | Cờ có hỗ trợ Tiếng Anh | `1` |
| `supported_languages_count` | INTEGER | | Không | Tổng số lượng ngôn ngữ được game hỗ trợ | `29` |
| `primary_genre` | TEXT | | Không | Thể loại chính của game | `Action` |
| `primary_developer` | TEXT | | Không | Nhà phát triển chính | `Valve` |
| `primary_publisher` | TEXT | | Không | Nhà phát hành chính | `Valve` |
| `genres_display` | TEXT | | Có | Chuỗi tổng hợp thể loại phân cách bằng dấu phẩy | `Action, Free To Play` |
| `categories_display` | TEXT | | Có | Chuỗi tổng hợp tính năng phân cách bằng phẩy | `Multi-player, Steam Trading Cards` |
| `top_tags_display` | TEXT | | Có | Top 5 tag cộng đồng được vote nhiều nhất | `FPS, Shooter, Multiplayer` |
| `header_image` | TEXT | | Có | Đường dẫn ảnh banner chính thức trên Steam Store | `https://shared.akamai...` |
| `website` | TEXT | | Có | Website chính thức của trò chơi | `http://counter-strike.net/` |
| `short_description` | TEXT | | Có | Đoạn tóm tắt giới thiệu ngắn (300 ký tự) | `For over two decades...` |

---

### 1.3. `dim_genres` (Chiều Thể Loại)
| Tên Cột | Kiểu Dữ Liệu | Khóa | Cho phép Null | Mô Tả | Giá Trị Mẫu |
| :--- | :--- | :---: | :---: | :--- | :--- |
| `genre_id` | INTEGER | **PK** | Không | Mã định danh thể loại | `1` |
| `genre_name` | TEXT | **UK** | Không | Tên thể loại (Action, Strategy, RPG, Indie...) | `Action` |

### 1.4. `dim_categories` (Chiều Tính Năng Nền Tảng)
| Tên Cột | Kiểu Dữ Liệu | Khóa | Cho phép Null | Mô Tả | Giá Trị Mẫu |
| :--- | :--- | :---: | :---: | :--- | :--- |
| `category_id` | INTEGER | **PK** | Không | Mã định danh tính năng | `1` |
| `category_name` | TEXT | **UK** | Không | Tên tính năng (Single-player, Co-op, Steam Cloud...) | `Single-player` |

### 1.5. `dim_developers` (Chiều Nhà Phát Triển)
| Tên Cột | Kiểu Dữ Liệu | Khóa | Cho phép Null | Mô Tả | Giá Trị Mẫu |
| :--- | :--- | :---: | :---: | :--- | :--- |
| `developer_id` | INTEGER | **PK** | Không | Mã định danh nhà phát triển | `1` |
| `developer_name` | TEXT | **UK** | Không | Tên hãng phát triển phần mềm trò chơi | `Valve` |

### 1.6. `dim_publishers` (Chiều Nhà Phát Hành)
| Tên Cột | Kiểu Dữ Liệu | Khóa | Cho phép Null | Mô Tả | Giá Trị Mẫu |
| :--- | :--- | :---: | :---: | :--- | :--- |
| `publisher_id` | INTEGER | **PK** | Không | Mã định danh nhà phát hành thương mại | `1` |
| `publisher_name` | TEXT | **UK** | Không | Tên hãng phát hành (Publisher) | `Valve` |

### 1.7. `dim_tags` (Chiều Thẻ Người Dùng Bình Chọn)
| Tên Cột | Kiểu Dữ Liệu | Khóa | Cho phép Null | Mô Tả | Giá Trị Mẫu |
| :--- | :--- | :---: | :---: | :--- | :--- |
| `tag_id` | INTEGER | **PK** | Không | Mã định danh tag cộng đồng | `1` |
| `tag_name` | TEXT | **UK** | Không | Tên tag (FPS, Souls-like, Story Rich...) | `FPS` |

---

## 2. Bảng Cầu Nối (Bridge Tables)

Giải quyết mối quan hệ Nhiều - Nhiều (Many-to-Many) giữa Game và các thuộc tính đa trị:

- **`bridge_game_genres`**: `appid` (FK) + `genre_id` (FK)
- **`bridge_game_categories`**: `appid` (FK) + `category_id` (FK)
- **`bridge_game_developers`**: `appid` (FK) + `developer_id` (FK)
- **`bridge_game_publishers`**: `appid` (FK) + `publisher_id` (FK)
- **`bridge_game_tags`**: `appid` (FK) + `tag_id` (FK) + `vote_count` (Số lượt bình chọn của game thủ)

---

## 3. Bảng Sự Kiện (Fact Table): `fact_game_metrics`

*Hạt dữ liệu (Grain):* 1 dòng cho mỗi tựa game Steam, lưu trữ tất cả các thước đo định lượng có thể cộng dồn (Additive) hoặc bán cộng dồn (Semi-additive).

| Tên Cột | Kiểu Dữ Liệu | Khóa | Cho phép Null | Mô Tả & Công Thức Tính | Giá Trị Mẫu |
| :--- | :--- | :---: | :---: | :--- | :--- |
| `fact_id` | INTEGER | **PK** | Không | Mã sự kiện tăng tự động | `1` |
| `appid` | INTEGER | **FK** | Không | Khóa ngoại liên kết `dim_games.appid` | `730` |
| `release_date_id` | INTEGER | **FK** | Không | Khóa ngoại liên kết `dim_date.date_id` | `20120821` |
| `price_usd` | REAL | | Không | Giá bán hiện tại bằng USD | `0.0` |
| `discount_pct` | INTEGER | | Không | Tỷ lệ giảm giá hiện tại (%) | `0` |
| `dlc_count` | INTEGER | | Không | Số lượng gói nội dung mở rộng (DLC) | `1` |
| `achievements` | INTEGER | | Không | Số lượng thành tựu trong trò chơi | `1` |
| `positive_reviews` | INTEGER | | Không | Tổng số đánh giá tích cực | `7480813` |
| `negative_reviews` | INTEGER | | Không | Tổng số đánh giá tiêu cực | `1135108` |
| `total_reviews` | INTEGER | | Không | Tổng số đánh giá = positive + negative | `8615921` |
| `positive_ratio_pct` | REAL | | Không | Tỷ lệ hài lòng = positive / total * 100 | `86.82` |
| `review_score_tier` | TEXT | | Không | Phân cấp đánh giá Steam (Overwhelmingly Positive, Mixed...) | `Very Positive` |
| `metacritic_score` | REAL | | Có | Điểm chấm của giới chuyên môn Metacritic (1-100) | `83.0` |
| `has_metacritic` | INTEGER | | Không | Cờ có điểm Metacritic (1/0) | `1` |
| `recommendations` | INTEGER | | Không | Số lượt khuyến nghị từ người chơi | `4401572` |
| `estimated_owners_min` | INTEGER | | Không | Cận dưới số lượng người sở hữu game | `100000000` |
| `estimated_owners_max` | INTEGER | | Không | Cận trên số lượng người sở hữu game | `200000000` |
| `estimated_owners_avg` | INTEGER | | Không | Điểm giữa người sở hữu = (min + max) / 2 | `150000000` |
| `owner_bracket` | TEXT | | Không | Khoảng sở hữu dạng văn bản ban đầu | `100000000 - 200000000` |
| `estimated_revenue_min_usd` | REAL | | Không | Doanh thu tối thiểu ước tính = owners_min * price | `0.0` |
| `estimated_revenue_max_usd` | REAL | | Không | Doanh thu tối đa ước tính = owners_max * price | `0.0` |
| `estimated_revenue_avg_usd` | REAL | | Không | Doanh thu trung bình ước tính = owners_avg * price | `0.0` |
| `peak_ccu` | INTEGER | | Không | Số người chơi đồng thời cao nhất (Peak CCU) | `1212356` |
| `avg_playtime_forever_hours` | REAL | | Không | Thời gian chơi trung bình toàn thời gian (Giờ) | `553.15` |
| `median_playtime_forever_hours` | REAL | | Không | Thời gian chơi trung vị toàn thời gian (Giờ) | `86.23` |
| `avg_playtime_2weeks_hours` | REAL | | Không | Thời gian chơi trung bình 2 tuần gần nhất (Giờ) | `14.65` |
| `median_playtime_2weeks_hours` | REAL | | Không | Thời gian chơi trung vị 2 tuần gần nhất (Giờ) | `5.83` |

---

## 4. Bảng Phẳng Báo Cáo: `flat_steam_games_bi`

Bảng tổng hợp đã join sẵn tất cả các trường cốt lõi từ `fact_game_metrics`, `dim_games` và `dim_date`, giúp người dùng chỉ cần kéo thả 1 bảng duy nhất vào Power BI / Tableau / Excel mà không cần tạo quan hệ data model phức tạp.
