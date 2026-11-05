# SỔ TAY THÔNG TIN CHI TIẾT BỘ DỮ LIỆU STEAM GAMES

Tài liệu này ghi lại toàn bộ thông tin về bộ dữ liệu Steam: nguồn dữ liệu, danh sách các bảng, số lượng dòng, từng cột lưu cái gì và kiểu dữ liệu là gì.

---

## 1. NGUỒN GỐC VÀ QUY MÔ TỔNG THỂ

* **Nguồn dữ liệu gốc**: Tải từ Kaggle (`artermiloff/steam-games-dataset`), gồm toàn bộ game trên cửa hàng Steam từ trước đến tháng 3/2025.
* **Tổng số tựa game hợp lệ**: **89,618** game.
* **Doanh thu ước tính toàn sàn**: Khoảng **130.83 tỷ USD**.
* **Giá game trung bình**: **7.31 USD** (khoảng 180.000 VNĐ).
* **Game miễn phí**: 14,160 game (chiếm 15.8%).
* **Game trả phí**: 75,458 game (chiếm 84.2%).
* **Game có tiếng Việt**: 3,553 game (chiếm gần 4%).

---

## 2. NƠI LƯU TRỮ DỮ LIỆU TRÊN Ổ ĐĨA

Toàn bộ dữ liệu nằm trong thư mục `D:\Steam-Game-Analyst-\data\`:

1. **Dữ liệu thô ban đầu (Raw)**:
   * File: `data\raw\games_march2025_cleaned.csv` (Nặng 446.9 MB, 47 cột, 89,618 dòng).
2. **Kho dữ liệu hoàn chỉnh (Data Warehouse SQLite)**:
   * File: `data\processed\steam_dw.db` (Nặng 162.3 MB, gồm 13 bảng có đánh chỉ mục khóa chính, khóa ngoại).
3. **Các file CSV xuất ra để mở bằng Excel / Power BI / Tableau**:
   * Thư mục: `data\processed\csv\`
   * Gồm 13 bảng riêng lẻ và 1 bảng gộp sẵn tên là `flat_steam_games_bi.csv` (nặng 63.6 MB).
4. **Các file Parquet nén hiệu năng cao**:
   * Thư mục: `data\processed\parquet\` (đọc bằng Python, Pandas, PySpark rất nhanh).

---

## 3. DANH SÁCH TẤT CẢ CÁC BẢNG VÀ SỐ DÒNG

Kho dữ liệu được chia theo mô hình hình sao (Star Schema) gồm 3 nhóm bảng:

| Tên bảng | Loại bảng | Số dòng | Số cột | Ý nghĩa tóm tắt |
| :--- | :---: | :---: | :---: | :--- |
| **`fact_game_metrics`** | Bảng chính (Fact) | **89,618** | 27 | Chứa tất cả số liệu đo lường: tiền, lượt đánh giá, giờ chơi, người chơi. |
| **`dim_games`** | Bảng mô tả (Dim) | **89,618** | 23 | Tên game, phân khúc giá, cờ Win/Mac/Linux, link ảnh, mô tả. |
| **`dim_date`** | Bảng mô tả (Dim) | **4,459** | 12 | Ngày phát hành, năm, quý, tháng, thứ trong tuần. |
| **`dim_genres`** | Bảng mô tả (Dim) | **33** | 2 | Danh sách 33 thể loại game (Hành động, Nhập vai, Chiến thuật...). |
| **`dim_categories`** | Bảng mô tả (Dim) | **40** | 2 | 40 tính năng (Chơi đơn, Nhiều người, Co-op, Tay cầm, VR...). |
| **`dim_developers`** | Bảng mô tả (Dim) | **60,096** | 2 | Tên các studio / người làm game. |
| **`dim_publishers`** | Bảng mô tả (Dim) | **49,839** | 2 | Tên các công ty phát hành game. |
| **`dim_tags`** | Bảng mô tả (Dim) | **452** | 2 | 452 thẻ tag do người chơi bình chọn (Bắn súng, Thế giới mở...). |
| **`bridge_game_genres`** | Cầu nối (Bridge) | **258,024** | 2 | Nối Game với Thể loại (vì 1 game có nhiều thể loại). |
| **`bridge_game_categories`** | Cầu nối (Bridge) | **376,084** | 2 | Nối Game với Tính năng. |
| **`bridge_game_developers`** | Cầu nối (Bridge) | **97,833** | 2 | Nối Game với Nhà phát triển. |
| **`bridge_game_publishers`** | Cầu nối (Bridge) | **92,473** | 2 | Nối Game với Nhà phát hành. |
| **`bridge_game_tags`** | Cầu nối (Bridge) | **1,008,987** | 3 | Nối Game với Tag và số phiếu bầu của người chơi. |
| **`flat_steam_games_bi`** | Bảng gộp (BI View) | **89,618** | 53 | Nối sẵn Fact + Dim Game + Dim Date để mở bằng Power BI kéo thả ngay. |

---

## 4. CHI TIẾT TỪNG BẢNG VÀ TỪNG CỘT DỮ LIỆU SẠCH

---

### BẢNG 1: `fact_game_metrics` (Bảng số liệu chính)
* **Số dòng**: 89,618 dòng (mỗi dòng tương ứng với đúng 1 tựa game).
* **Mục đích**: Lưu toàn bộ các con số dùng để tính tổng, tính trung bình, vẽ biểu đồ.

| Tên cột | Kiểu dữ liệu | Khóa | Ý nghĩa và cách tính | Ví dụ |
| :--- | :---: | :---: | :--- | :--- |
| `fact_id` | INTEGER | PK | Số thứ tự tự tăng của bảng | `1` |
| `appid` | INTEGER | FK | Mã ID của game trên Steam (nối sang `dim_games`) | `730` |
| `release_date_id` | INTEGER | FK | Mã ngày phát hành (dạng YYYYMMDD, nối sang `dim_date`) | `20120821` |
| `price_usd` | REAL | | Giá bán tính bằng đô la Mỹ | `0.0` hoặc `19.99` |
| `discount_pct` | INTEGER | | Tỷ lệ giảm giá hiện tại (%) | `0` hoặc `50` |
| `dlc_count` | INTEGER | | Số lượng bản mở rộng DLC của game | `1` |
| `achievements` | INTEGER | | Số lượng thành tựu đạt được trong game | `167` |
| `positive_reviews` | INTEGER | | Số lượt đánh giá tích cực (khen) | `7480813` |
| `negative_reviews` | INTEGER | | Số lượt đánh giá tiêu cực (chê) | `1135108` |
| `total_reviews` | INTEGER | | Tổng số lượt đánh giá = khen + chê | `8615921` |
| `positive_ratio_pct` | REAL | | Tỷ lệ khen (%) = positive / total * 100 | `86.82` |
| `review_score_tier` | TEXT | | Xếp hạng của Steam (Cực kỳ tích cực, Trái chiều...) | `Very Positive` |
| `metacritic_score` | REAL | | Điểm của báo chí chấm trên Metacritic (1-100) | `83.0` (nếu không có thì để 0) |
| `has_metacritic` | INTEGER | | Có điểm Metacritic hay không (1: Có, 0: Không có) | `1` |
| `recommendations` | INTEGER | | Số lượt người chơi bấm nút khuyên người khác nên chơi | `4401572` |
| `estimated_owners_min` | INTEGER | | Ước lượng người sở hữu (mức thấp nhất) | `100000000` |
| `estimated_owners_max` | INTEGER | | Ước lượng người sở hữu (mức cao nhất) | `200000000` |
| `estimated_owners_avg` | INTEGER | | Ước lượng người sở hữu (trung bình = (min + max) / 2) | `150000000` |
| `owner_bracket` | TEXT | | Dải người sở hữu dạng chữ ban đầu từ SteamSpy | `100000000 - 200000000` |
| `estimated_revenue_min_usd` | REAL | | Doanh thu tối thiểu ước tính = owners_min * price | `0.0` |
| `estimated_revenue_max_usd` | REAL | | Doanh thu tối đa ước tính = owners_max * price | `0.0` |
| `estimated_revenue_avg_usd` | REAL | | Doanh thu trung bình ước tính = owners_avg * price | `0.0` |
| `peak_ccu` | INTEGER | | Số người cùng online chơi nhiều nhất tại 1 thời điểm | `1212356` |
| `avg_playtime_forever_hours` | REAL | | Thời gian chơi trung bình từ trước đến nay (đổi ra Giờ) | `553.15` |
| `median_playtime_forever_hours` | REAL | | Thời gian chơi trung vị từ trước đến nay (Giờ) | `86.23` |
| `avg_playtime_2weeks_hours` | REAL | | Thời gian chơi trung bình trong 2 tuần qua (Giờ) | `14.65` |
| `median_playtime_2weeks_hours`| REAL | | Thời gian chơi trung vị trong 2 tuần qua (Giờ) | `5.83` |

---

### BẢNG 2: `dim_games` (Bảng thông tin game)
* **Số dòng**: 89,618 dòng.
* **Mục đích**: Chứa tên, phân loại, hệ điều hành, ngôn ngữ, hình ảnh và mô tả của game.

| Tên cột | Kiểu dữ liệu | Khóa | Ý nghĩa | Ví dụ |
| :--- | :---: | :---: | :--- | :--- |
| `appid` | INTEGER | PK | ID duy nhất của game | `730` |
| `name` | TEXT | | Tên tựa game | `Counter-Strike 2` |
| `release_date_id` | INTEGER | FK | Nối sang bảng `dim_date` | `20120821` |
| `required_age` | INTEGER | | Độ tuổi tối thiểu được chơi (0, 16, 18) | `0` |
| `is_free` | INTEGER | | Game miễn phí hay không (1: Miễn phí, 0: Thu phí) | `1` |
| `price_usd` | REAL | | Giá gốc bằng USD | `0.0` |
| `price_tier` | TEXT | | Nhóm giá (Free, Dưới $5, $5-$15, $15-$30, $30-$60, Trên $60) | `Free ($0)` |
| `windows` | INTEGER | | Chạy được trên Windows không (1: Có, 0: Không) | `1` |
| `mac` | INTEGER | | Chạy được trên Mac không (1: Có, 0: Không) | `0` |
| `linux` | INTEGER | | Chạy được trên Linux / Steam Deck không | `1` |
| `platform_support` | TEXT | | Tóm tắt nền tảng chạy được | `Windows & Linux` |
| `has_vietnamese` | INTEGER | | Có tiếng Việt không (1: Có, 0: Không) | `1` |
| `has_english` | INTEGER | | Có tiếng Anh không (1: Có, 0: Không) | `1` |
| `supported_languages_count`| INTEGER | | Tổng số ngôn ngữ game hỗ trợ | `29` |
| `primary_genre` | TEXT | | Thể loại chính đứng đầu | `Action` |
| `primary_developer` | TEXT | | Tên studio chính làm ra game | `Valve` |
| `primary_publisher` | TEXT | | Tên nhà phát hành chính | `Valve` |
| `genres_display` | TEXT | | Chuỗi gom các thể loại nối nhau bằng dấu phẩy | `Action, Free To Play` |
| `categories_display` | TEXT | | Chuỗi gom các tính năng nối nhau bằng dấu phẩy | `Multi-player, Steam Cloud` |
| `top_tags_display` | TEXT | | 5 thẻ tag được nhiều người bình chọn nhất | `FPS, Shooter, Multiplayer` |
| `header_image` | TEXT | | Link ảnh bìa ngang trên Steam Store | `https://shared.akamai...` |
| `website` | TEXT | | Trang web chính thức của game | `http://counter-strike.net/` |
| `short_description` | TEXT | | Đoạn tóm tắt giới thiệu ngắn nội dung game | `For over two decades...` |

---

### BẢNG 3: `dim_date` (Bảng thời gian phát hành)
* **Số dòng**: 4,459 dòng (mỗi dòng là 1 ngày phát hành cụ thể).
* **Mục đích**: Dùng để lọc và vẽ biểu đồ theo Năm, Quý, Tháng.

| Tên cột | Kiểu dữ liệu | Khóa | Ý nghĩa | Ví dụ |
| :--- | :---: | :---: | :--- | :--- |
| `date_id` | INTEGER | PK | Mã ngày dạng YYYYMMDD | `20240315` |
| `full_date` | TEXT | | Ngày đầy đủ chuẩn YYYY-MM-DD | `2024-03-15` |
| `year` | INTEGER | | Năm | `2024` |
| `quarter` | INTEGER | | Quý (1, 2, 3, 4) | `1` |
| `quarter_name` | TEXT | | Tên quý để hiện lên biểu đồ | `Q1 2024` |
| `month` | INTEGER | | Tháng trong năm (1 đến 12) | `3` |
| `month_name` | TEXT | | Tên tiếng Anh của tháng | `March` |
| `month_year` | TEXT | | Năm và tháng để sắp xếp timeline | `2024-03` |
| `day_of_month` | INTEGER | | Ngày trong tháng (1 đến 31) | `15` |
| `day_of_week` | INTEGER | | Thứ trong tuần (1 = Thứ Hai, 7 = Chủ Nhật) | `5` |
| `day_name` | TEXT | | Tên thứ trong tuần | `Friday` |
| `is_weekend` | INTEGER | | Có phải cuối tuần không (1: T7/CN, 0: Ngày thường) | `0` |

---

### BẢNG 4, 5, 6, 7, 8: CÁC BẢNG DANH MỤC KHÁC

* **`dim_genres` (33 dòng)**:
  * `genre_id` (INTEGER, PK): Mã số thể loại.
  * `genre_name` (TEXT): Tên thể loại (Action, Adventure, Casual, Indie, RPG, Simulation, Strategy...).
* **`dim_categories` (40 dòng)**:
  * `category_id` (INTEGER, PK): Mã số tính năng.
  * `category_name` (TEXT): Tên tính năng (Single-player, Multi-player, Co-op, Steam Cloud, VR Support...).
* **`dim_developers` (60,096 dòng)**:
  * `developer_id` (INTEGER, PK): Mã số studio.
  * `developer_name` (TEXT): Tên hãng làm game (Valve, Capcom, Ubisoft, KRAFTON...).
* **`dim_publishers` (49,839 dòng)**:
  * `publisher_id` (INTEGER, PK): Mã số nhà phát hành.
  * `publisher_name` (TEXT): Tên nhà phát hành (Electronic Arts, Sony Interactive...).
* **`dim_tags` (452 dòng)**:
  * `tag_id` (INTEGER, PK): Mã số thẻ tag.
  * `tag_name` (TEXT): Tên thẻ tag do cộng đồng gán (FPS, Souls-like, Open World, 2D Platformer...).

---

### BẢNG 9 ĐẾN 13: CÁC BẢNG CẦU NỐI (BRIDGE TABLES)
> **Tại sao cần các bảng này?** Vì một game có thể vừa là Action, vừa là Adventure (Nhiều Thể loại). Nếu viết chung vào 1 bảng thì khi tính tổng tiền của thể loại Action rồi cộng với Adventure sẽ bị trùng tiền (tính tiền 1 game 2 lần). Các bảng cầu nối sinh ra để tách riêng từng mối liên kết:

* **`bridge_game_genres` (258,024 dòng)**: Cột `appid` và `genre_id`.
* **`bridge_game_categories` (376,084 dòng)**: Cột `appid` và `category_id`.
* **`bridge_game_developers` (97,833 dòng)**: Cột `appid` và `developer_id`.
* **`bridge_game_publishers` (92,473 dòng)**: Cột `appid` và `publisher_id`.
* **`bridge_game_tags` (1,008,987 dòng)**: Cột `appid`, `tag_id` và `vote_count` (số phiếu bầu của game thủ cho tag đó).

---

### BẢNG 14: `flat_steam_games_bi` (Bảng gộp sẵn phục vụ Power BI / Tableau)
* **Số dòng**: 89,618 dòng.
* **Số cột**: 53 cột.
* **File lưu**: `data\processed\csv\flat_steam_games_bi.csv` (63.6 MB).
* **Mục đích**: Bảng này đã được gom sẵn toàn bộ cột của Fact (`fact_game_metrics`) + Chiều Game (`dim_games`) + Chiều Thời gian (`dim_date`).
* **Cách dùng**: Dành cho ai không muốn tạo mối quan hệ dây nhợ phức tạp trong Power BI. Bạn chỉ cần nạp đúng 1 file này vào Power BI hoặc Tableau là có sẵn tất cả cột để kéo thả làm biểu đồ ngay.

---

## 5. BẢNG DỮ LIỆU GỐC BAN ĐẦU (FILE CSV THÔ TỪ KAGGLE)

Tệp gốc là `data\raw\games_march2025_cleaned.csv` gồm **47 cột** trước khi được chuẩn hóa:

| Nhóm cột | Các cột gốc | Vấn đề của dữ liệu gốc |
| :--- | :--- | :--- |
| **Định danh & Giá** | `appid`, `name`, `release_date`, `required_age`, `price`, `discount`, `dlc_count` | `release_date` là chữ lộn xộn, không sắp xếp timeline được. |
| **Mô tả & Media** | `detailed_description`, `about_the_game`, `short_description`, `reviews`, `notes`, `header_image`, `screenshots`, `movies` | Chứa nhiều thẻ HTML, link ảnh, chiếm hàng trăm MB dung lượng. |
| **Hệ điều hành** | `windows`, `mac`, `linux` | Dạng True/False rời rạc. |
| **Ngôn ngữ** | `supported_languages`, `full_audio_languages` | Bị lưu dạng chuỗi giả lập danh sách: `['English', 'French']`. |
| **Phân loại nhiều-nhiều** | `genres`, `categories`, `developers`, `publishers`, `tags` | Bị nhồi nhét dạng chuỗi list `['Action']` và từ điển `{'FPS': 90857}`, không thể GROUP BY trong SQL. |
| **Đánh giá** | `positive`, `negative`, `num_reviews_total`, `pct_pos_total`, `num_reviews_recent`, `pct_pos_recent`, `metacritic_score`, `metacritic_url`, `user_score`, `score_rank` | Cột `score_rank` trống 99.9%, `metacritic_score` trống >67%. |
| **Người chơi & Giờ chơi** | `estimated_owners`, `peak_ccu`, `achievements`, `recommendations`, `average_playtime_forever`, `average_playtime_2weeks`, `median_playtime_forever`, `median_playtime_2weeks` | `estimated_owners` là chữ `"20000 - 50000"` không tính tổng được; thời gian chơi để bằng phút thay vì giờ. |
| **Thông tin hỗ trợ** | `website`, `support_url`, `support_email`, `packages` | Nhiều link rỗng hoặc không dùng đến trong phân tích kinh doanh. |
