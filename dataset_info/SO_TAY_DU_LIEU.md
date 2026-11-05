# SỔ TAY THÔNG TIN CHI TIẾT BỘ DỮ LIỆU STEAM GAMES

Tài liệu này ghi lại toàn bộ thông tin về bộ dữ liệu Steam: nguồn gốc, danh sách các bảng, số lượng dòng, từng cột dùng để làm gì và kiểu dữ liệu là gì.

---

## 1. NGUỒN GỐC VÀ CÁC CON SỐ THỰC TẾ

- Nguồn dữ liệu: Tải từ Kaggle (artermiloff/steam-games-dataset), gồm toàn bộ trò chơi trên cửa hàng Steam từ trước đến tháng 3 năm 2025.
- Tổng số tựa game hợp lệ sau khi lọc sạch: 89,618 game.
- Tổng doanh thu ước tính toàn sàn: Khoảng 130.83 tỷ USD.
- Giá game trung bình: 7.31 USD (khoảng 180.000 đồng Việt Nam).
- Game miễn phí: 14,160 game (chiếm 15.8%).
- Game trả phí: 75,458 game (chiếm 84.2%).
- Game có hỗ trợ tiếng Việt: 3,553 game (chiếm gần 4%).

---

## 2. NƠI LƯU TRỮ DỮ LIỆU TRÊN MÁY TÍNH

Toàn bộ dữ liệu nằm trong thư mục D:\Steam-Game-Analyst-\data\:

1. Dữ liệu thô ban đầu (Raw):
   Tệp tin: data\raw\games_march2025_cleaned.csv (Nặng 446.9 MB, gồm 47 cột và 89,618 dòng).
2. Kho dữ liệu hoàn chỉnh (Data Warehouse SQLite):
   Tệp tin: data\processed\steam_dw.db (Nặng 162.3 MB, gồm 13 bảng có khóa chính và khóa ngoại).
3. Các tệp CSV xuất ra để mở bằng Excel, Power BI hoặc Tableau:
   Thư mục: data\processed\csv\
   Gồm 13 bảng riêng lẻ và 1 bảng gộp sẵn tên là "flat_steam_games_bi.csv" (nặng 63.6 MB).
4. Các tệp Parquet nén tốc độ cao:
   Thư mục: data\processed\parquet\ (dùng cho lập trình Python, Pandas hoặc Spark).

---

## 3. DANH SÁCH TẤT CẢ CÁC BẢNG VÀ SỐ DÒNG

Kho dữ liệu được chia theo mô hình hình sao (Star Schema) gồm 3 nhóm bảng:

| Tên bảng | Loại bảng | Số dòng | Số cột | Ý nghĩa tóm tắt |
| :--- | :---: | :---: | :---: | :--- |
| "fact_game_metrics" | Bảng số liệu chính (Fact) | 89,618 | 27 | Chứa tất cả số liệu đo lường: tiền doanh thu, lượt đánh giá, giờ chơi, người chơi. |
| "dim_games" | Bảng mô tả game (Dim) | 89,618 | 23 | Tên game, phân khúc giá, cờ Win/Mac/Linux, cờ tiếng Việt, link ảnh, mô tả ngắn. |
| "dim_date" | Bảng thời gian (Dim) | 4,459 | 12 | Ngày phát hành, năm, quý, tháng, thứ trong tuần. |
| "dim_genres" | Bảng thể loại (Dim) | 33 | 2 | Danh sách 33 thể loại game (Hành động, Nhập vai, Chiến thuật...). |
| "dim_categories" | Bảng tính năng (Dim) | 40 | 2 | Danh sách 40 tính năng (Chơi đơn, Nhiều người, Co-op, Tay cầm, VR...). |
| "dim_developers" | Bảng studio (Dim) | 60,096 | 2 | Tên các studio và đội ngũ lập trình làm ra game. |
| "dim_publishers" | Bảng nhà phát hành (Dim) | 49,839 | 2 | Tên các công ty phát hành game thương mại. |
| "dim_tags" | Bảng thẻ tag (Dim) | 452 | 2 | Danh mục 452 thẻ tag do cộng đồng người chơi bình chọn. |
| "bridge_game_genres" | Bảng cầu nối (Bridge) | 258,024 | 2 | Nối Game với Thể loại (vì 1 game có nhiều thể loại). |
| "bridge_game_categories" | Bảng cầu nối (Bridge) | 376,084 | 2 | Nối Game với Tính năng nền tảng. |
| "bridge_game_developers" | Bảng cầu nối (Bridge) | 97,833 | 2 | Nối Game với Studio làm game. |
| "bridge_game_publishers" | Bảng cầu nối (Bridge) | 92,473 | 2 | Nối Game với Nhà phát hành. |
| "bridge_game_tags" | Bảng cầu nối (Bridge) | 1,008,987 | 3 | Nối Game với Thẻ tag kèm số lượt bình chọn. |
| "flat_steam_games_bi" | Bảng gộp sẵn (BI View) | 89,618 | 53 | Nối sẵn Fact + Dim Game + Dim Date để mở bằng Power BI kéo thả ngay. |

---

## 4. CHI TIẾT TỪNG BẢNG VÀ TỪNG CỘT DỮ LIỆU SẠCH

### BẢNG 1: "fact_game_metrics" (Bảng số liệu đo lường chính)
- Số dòng: 89,618 dòng (mỗi dòng tương ứng với đúng 1 tựa game).
- Mục đích: Lưu toàn bộ các con số dùng để tính tổng doanh thu, tính trung bình, vẽ biểu đồ.

| Tên cột | Kiểu dữ liệu | Vai trò khóa | Ý nghĩa nghiệp vụ và cách tính | Ví dụ thực tế |
| :--- | :---: | :---: | :--- | :--- |
| "fact_id" | INTEGER (Số nguyên) | Khóa chính (PK) | Số thứ tự tự tăng của từng dòng | 1 |
| "appid" | INTEGER (Số nguyên) | Khóa ngoại (FK) | Mã ID của game trên Steam, dùng để nối sang bảng "dim_games" | 730 (Counter-Strike 2) |
| "release_date_id" | INTEGER (Số nguyên) | Khóa ngoại (FK) | Mã ngày phát hành dạng số YYYYMMDD, nối sang bảng "dim_date" | 20120821 |
| "price_usd" | REAL (Số thực) | | Giá bán tính bằng đô la Mỹ | 0.0 (miễn phí) hoặc 19.99 |
| "discount_pct" | INTEGER (Số nguyên) | | Tỷ lệ giảm giá hiện tại theo phần trăm (0 là không giảm, 50 là giảm nửa giá) | 0 |
| "dlc_count" | INTEGER (Số nguyên) | | Số lượng bản mở rộng nội dung (DLC) của trò chơi | 1 |
| "achievements" | INTEGER (Số nguyên) | | Số lượng thành tựu người chơi có thể mở khóa trong game | 167 |
| "positive_reviews" | INTEGER (Số nguyên) | | Số lượt người chơi đánh giá tích cực (khen) | 7480813 |
| "negative_reviews" | INTEGER (Số nguyên) | | Số lượt người chơi đánh giá tiêu cực (chê) | 1135108 |
| "total_reviews" | INTEGER (Số nguyên) | | Tổng số lượt đánh giá = số lượt khen cộng số lượt chê | 8615921 |
| "positive_ratio_pct" | REAL (Số thực) | | Tỷ lệ khen (%) = (lượt khen chia cho tổng lượt đánh giá) nhân 100 | 86.82 |
| "review_score_tier" | TEXT (Chữ) | | Xếp hạng của Steam (Very Positive, Positive, Mixed, Negative...) | Very Positive |
| "metacritic_score" | REAL (Số thực) | | Điểm số của giới báo chí chấm trên Metacritic thang điểm 1-100 | 83.0 (nếu không có thì bằng 0) |
| "has_metacritic" | INTEGER (Số nguyên) | | Có điểm đánh giá của báo chí hay không (1: Có, 0: Không có) | 1 |
| "recommendations" | INTEGER (Số nguyên) | | Số lượt người chơi nhấn nút khuyên người khác nên mua game này | 4401572 |
| "estimated_owners_min" | INTEGER (Số nguyên) | | Ước lượng số người sở hữu game ở mức tối thiểu | 100000000 |
| "estimated_owners_max" | INTEGER (Số nguyên) | | Ước lượng số người sở hữu game ở mức tối đa | 200000000 |
| "estimated_owners_avg" | INTEGER (Số nguyên) | | Ước lượng số người sở hữu trung bình = (tối thiểu + tối đa) chia đôi | 150000000 |
| "owner_bracket" | TEXT (Chữ) | | Dải người sở hữu dạng văn bản ban đầu thu thập từ SteamSpy | "100000000 - 200000000" |
| "estimated_revenue_min_usd" | REAL (Số thực) | | Doanh thu tối thiểu ước tính = số người tối thiểu nhân giá bán | 0.0 |
| "estimated_revenue_max_usd" | REAL (Số thực) | | Doanh thu tối đa ước tính = số người tối đa nhân giá bán | 0.0 |
| "estimated_revenue_avg_usd" | REAL (Số thực) | | Doanh thu trung bình ước tính = số người trung bình nhân giá bán | 0.0 |
| "peak_ccu" | INTEGER (Số nguyên) | | Kỷ lục số người cùng online chơi game tại một thời điểm | 1212356 |
| "avg_playtime_forever_hours" | REAL (Số thực) | | Thời gian chơi trung bình trọn đời của game thủ (đổi ra Giờ) | 553.15 |
| "median_playtime_forever_hours" | REAL (Số thực) | | Thời gian chơi trung vị trọn đời của game thủ (Giờ) | 86.23 |
| "avg_playtime_2weeks_hours" | REAL (Số thực) | | Thời gian chơi trung bình trong 2 tuần gần nhất (Giờ) | 14.65 |
| "median_playtime_2weeks_hours" | REAL (Số thực) | | Thời gian chơi trung vị trong 2 tuần gần nhất (Giờ) | 5.83 |

---

### BẢNG 2: "dim_games" (Bảng thông tin chi tiết tựa game)
- Số dòng: 89,618 dòng.
- Mục đích: Lưu tên, phân khúc giá, hệ điều hành, ngôn ngữ, hình ảnh và mô tả tóm tắt của từng game.

| Tên cột | Kiểu dữ liệu | Vai trò khóa | Ý nghĩa nghiệp vụ | Ví dụ thực tế |
| :--- | :---: | :---: | :--- | :--- |
| "appid" | INTEGER (Số nguyên) | Khóa chính (PK) | Mã định danh duy nhất của trò chơi trên Steam | 730 |
| "name" | TEXT (Chữ) | | Tên chính thức của tựa game | Counter-Strike 2 |
| "release_date_id" | INTEGER (Số nguyên) | Khóa ngoại (FK) | Nối sang bảng "dim_date" để biết ngày phát hành | 20120821 |
| "required_age" | INTEGER (Số nguyên) | | Độ tuổi tối thiểu được phép chơi (0, 16, 18) | 0 |
| "is_free" | INTEGER (Số nguyên) | | Game miễn phí hay không (1: Miễn phí, 0: Trả phí) | 1 |
| "price_usd" | REAL (Số thực) | | Giá niêm yết bằng đô la Mỹ | 0.0 |
| "price_tier" | TEXT (Chữ) | | Nhóm phân khúc giá (Free, Dưới $5, $5-$15, $15-$30, $30-$60, Trên $60) | "Free ($0)" |
| "windows" | INTEGER (Số nguyên) | | Chạy được trên hệ điều hành Windows không (1: Có, 0: Không) | 1 |
| "mac" | INTEGER (Số nguyên) | | Chạy được trên macOS không (1: Có, 0: Không) | 0 |
| "linux" | INTEGER (Số nguyên) | | Chạy được trên Linux hoặc máy Steam Deck không (1: Có, 0: Không) | 1 |
| "platform_support" | TEXT (Chữ) | | Tóm tắt các hệ điều hành hỗ trợ | "Windows & Linux" |
| "has_vietnamese" | INTEGER (Số nguyên) | | Có hỗ trợ tiếng Việt không (1: Có, 0: Không) | 1 |
| "has_english" | INTEGER (Số nguyên) | | Có hỗ trợ tiếng Anh không (1: Có, 0: Không) | 1 |
| "supported_languages_count" | INTEGER (Số nguyên) | | Tổng số lượng ngôn ngữ mà game hỗ trợ | 29 |
| "primary_genre" | TEXT (Chữ) | | Thể loại chính đầu tiên của trò chơi | "Action" |
| "primary_developer" | TEXT (Chữ) | | Tên studio chính lập trình ra game | "Valve" |
| "primary_publisher" | TEXT (Chữ) | | Tên công ty phát hành chính | "Valve" |
| "genres_display" | TEXT (Chữ) | | Danh sách tất cả thể loại nối nhau bằng dấu phẩy | "Action, Free To Play" |
| "categories_display" | TEXT (Chữ) | | Danh sách tất cả tính năng nối nhau bằng dấu phẩy | "Multi-player, Steam Cloud" |
| "top_tags_display" | TEXT (Chữ) | | 5 thẻ tag được game thủ bình chọn nhiều nhất | "FPS, Shooter, Multiplayer" |
| "header_image" | TEXT (Chữ) | | Đường dẫn ảnh bìa ngang trên Steam Store | https://shared.akamai... |
| "website" | TEXT (Chữ) | | Trang web chính thức của trò chơi | http://counter-strike.net/ |
| "short_description" | TEXT (Chữ) | | Đoạn văn tóm tắt ngắn giới thiệu nội dung trò chơi | "For over two decades..." |

---

### BẢNG 3: "dim_date" (Bảng thời gian phát hành)
- Số dòng: 4,459 dòng (mỗi dòng tương ứng với 1 ngày lịch phát hành).
- Mục đích: Dùng để lọc dữ liệu và vẽ biểu đồ theo Năm, Quý, Tháng, Thứ trong tuần.

| Tên cột | Kiểu dữ liệu | Vai trò khóa | Ý nghĩa nghiệp vụ | Ví dụ thực tế |
| :--- | :---: | :---: | :--- | :--- |
| "date_id" | INTEGER (Số nguyên) | Khóa chính (PK) | Mã ngày dạng số YYYYMMDD | 20240315 |
| "full_date" | TEXT (Chữ) | | Ngày đầy đủ dạng chuẩn YYYY-MM-DD | "2024-03-15" |
| "year" | INTEGER (Số nguyên) | | Năm phát hành | 2024 |
| "quarter" | INTEGER (Số nguyên) | | Quý trong năm (từ 1 đến 4) | 1 |
| "quarter_name" | TEXT (Chữ) | | Nhãn quý hiển thị trên biểu đồ | "Q1 2024" |
| "month" | INTEGER (Số nguyên) | | Tháng trong năm (từ 1 đến 12) | 3 |
| "month_name" | TEXT (Chữ) | | Tên tháng bằng tiếng Anh | "March" |
| "month_year" | TEXT (Chữ) | | Chuỗi Năm-Tháng dùng để sắp xếp dòng thời gian | "2024-03" |
| "day_of_month" | INTEGER (Số nguyên) | | Ngày trong tháng (từ 1 đến 31) | 15 |
| "day_of_week" | INTEGER (Số nguyên) | | Thứ trong tuần (1 là Thứ Hai, 7 là Chủ Nhật) | 5 |
| "day_name" | TEXT (Chữ) | | Tên thứ trong tuần bằng tiếng Anh | "Friday" |
| "is_weekend" | INTEGER (Số nguyên) | | Cờ cuối tuần (1: Thứ Bảy hoặc Chủ Nhật, 0: Ngày thường) | 0 |

---

### BẢNG 4 ĐẾN BẢNG 8: CÁC BẢNG DANH MỤC THUỘC TÍNH

- Bảng "dim_genres" (gồm 33 dòng):
  "genre_id" (INTEGER, Khóa chính): Mã số thể loại.
  "genre_name" (TEXT): Tên thể loại (Hành động, Phiêu lưu, Nhập vai, Chiến thuật, Mô phỏng, Indie...).
- Bảng "dim_categories" (gồm 40 dòng):
  "category_id" (INTEGER, Khóa chính): Mã số tính năng.
  "category_name" (TEXT): Tên tính năng (Chơi đơn, Nhiều người, Co-op, Lưu đám mây Steam Cloud, Kính thực tế ảo VR...).
- Bảng "dim_developers" (gồm 60,096 dòng):
  "developer_id" (INTEGER, Khóa chính): Mã số studio.
  "developer_name" (TEXT): Tên hãng làm game (Valve, Capcom, Ubisoft, KRAFTON...).
- Bảng "dim_publishers" (gồm 49,839 dòng):
  "publisher_id" (INTEGER, Khóa chính): Mã số nhà phát hành.
  "publisher_name" (TEXT): Tên công ty phát hành thương mại (Electronic Arts, Sony Interactive...).
- Bảng "dim_tags" (gồm 452 dòng):
  "tag_id" (INTEGER, Khóa chính): Mã số thẻ tag.
  "tag_name" (TEXT): Tên thẻ tag do game thủ gán (Bắn súng góc nhìn thứ nhất, Thế giới mở, Đi cảnh 2D...).

---

### BẢNG 9 ĐẾN BẢNG 13: CÁC BẢNG CẦU NỐI (BRIDGE TABLES)
Tại sao bắt buộc phải có các bảng này: Trong thực tế, một trò chơi có thể vừa là Hành động vừa là Nhập vai (nhiều thể loại), do 2 studio cùng hợp tác và có 20 thẻ tag. Nếu viết dồn chung vào một bảng, khi bạn tính tổng tiền thể loại Hành động rồi lại tính tổng tiền thể loại Nhập vai thì doanh thu của game đó sẽ bị cộng 2 lần (lỗi nhân bản tiền). Các bảng cầu nối được tạo ra để tách riêng từng cặp liên kết:

- Bảng "bridge_game_genres" (258,024 dòng): Nối cặp cột "appid" và "genre_id".
- Bảng "bridge_game_categories" (376,084 dòng): Nối cặp cột "appid" và "category_id".
- Bảng "bridge_game_developers" (97,833 dòng): Nối cặp cột "appid" và "developer_id".
- Bảng "bridge_game_publishers" (92,473 dòng): Nối cặp cột "appid" và "publisher_id".
- Bảng "bridge_game_tags" (1,008,987 dòng): Nối cặp cột "appid", "tag_id" và kèm theo cột "vote_count" (số lượt game thủ bình chọn cho tag đó).

---

### BẢNG 14: "flat_steam_games_bi" (Bảng gộp sẵn phục vụ làm báo cáo nhanh)
- Số dòng: 89,618 dòng.
- Số cột: 53 cột.
- Tệp tin lưu trữ: data\processed\csv\flat_steam_games_bi.csv (nặng 63.6 MB).
- Mục đích: Bảng này đã được ghép sẵn toàn bộ thông tin từ bảng số liệu "fact_game_metrics" cộng bảng mô tả game "dim_games" và bảng thời gian "dim_date".
- Cách dùng: Dành cho những ai không muốn tự nối dây quan hệ phức tạp trong Power BI. Bạn chỉ cần nạp duy nhất một tệp tin này vào Power BI hoặc Tableau là có đầy đủ tất cả các cột để kéo thả vẽ biểu đồ ngay lập tức.

---

## 5. BẢNG DỮ LIỆU GỐC BAN ĐẦU (TỆP CSV THÔ TẢI VỀ TỪ KAGGLE)

Tệp gốc là data\raw\games_march2025_cleaned.csv gồm 47 cột trước khi được làm sạch:

| Nhóm cột | Các cột gốc | Vấn đề của dữ liệu gốc |
| :--- | :--- | :--- |
| Định danh và Giá | appid, name, release_date, required_age, price, discount, dlc_count | Cột release_date là chuỗi chữ lộn xộn, không sắp xếp theo ngày tháng năm được. |
| Mô tả và Hình ảnh | detailed_description, about_the_game, short_description, reviews, notes, header_image, screenshots, movies | Chứa nhiều mã HTML và đường link ảnh, làm tệp tin nặng hàng trăm MB. |
| Hệ điều hành | windows, mac, linux | Định dạng True/False rời rạc. |
| Ngôn ngữ | supported_languages, full_audio_languages | Bị lưu dưới dạng chuỗi chữ giả lập danh sách Python như ['English', 'French']. |
| Phân loại nhiều - nhiều | genres, categories, developers, publishers, tags | Bị nhồi nhét dạng chuỗi danh sách ['Action'] và từ điển {'FPS': 90857}, không thể dùng lệnh nhóm GROUP BY trong SQL. |
| Đánh giá | positive, negative, num_reviews_total, pct_pos_total, num_reviews_recent, pct_pos_recent, metacritic_score, metacritic_url, user_score, score_rank | Cột score_rank bị trống 99.9%, cột metacritic_score bị trống hơn 67%. |
| Người chơi và Giờ chơi | estimated_owners, peak_ccu, achievements, recommendations, average_playtime_forever, average_playtime_2weeks, median_playtime_forever, median_playtime_2weeks | Cột estimated_owners là chữ "20000 - 50000" không thể bấm tính tổng doanh thu; thời gian chơi ghi bằng phút rất khó nhìn. |
| Thông tin hỗ trợ | website, support_url, support_email, packages | Nhiều đường dẫn rỗng hoặc không dùng đến trong phân tích kinh doanh. |
