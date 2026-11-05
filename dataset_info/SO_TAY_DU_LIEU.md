# SỔ TAY DỮ LIỆU STEAM GAMES

Tài liệu giải thích toàn bộ các bảng và các cột trong kho dữ liệu Steam Games. Dữ liệu gồm 89,618 tựa game tính đến tháng 3 năm 2025.

I. TỔNG QUAN VÀ NƠI LƯU TRỮ

1. Các con số chính:
- Tổng số tựa game sau lọc sạch: 89,618 game.
- Doanh thu ước tính toàn thị trường: Khoảng 130.83 tỷ USD.
- Giá game trung bình: 7.31 USD (khoảng 180.000 đồng Việt Nam).
- Game miễn phí: 14,160 game (chiếm 15.8%).
- Game trả phí: 75,458 game (chiếm 84.2%).
- Game có tiếng Việt: 3,553 game (chiếm gần 4%).

2. Thư mục lưu dữ liệu trên máy:
- Dữ liệu thô ban đầu: data\raw\games_march2025_cleaned.csv (file CSV nặng 446.9 MB, gồm 47 cột).
- Database SQLite: data\processed\steam_dw.db (file nặng 162.3 MB, gồm 13 bảng có khóa chính và khóa ngoại).
- File CSV để mở bằng Excel hoặc Power BI: data\processed\csv\ (gồm 13 bảng rời và 1 bảng gộp sẵn flat_steam_games_bi.csv).
- File Parquet nén: data\processed\parquet\ (dùng cho lập trình Python, nén nhỏ và đọc nhanh).

II. DANH SÁCH 13 BẢNG TRONG KHO DỮ LIỆU

Bảng số liệu chính (Fact):
1. fact_game_metrics: 89,618 dòng, 27 cột. Chứa toàn bộ số liệu tính toán về doanh thu, lượt tải, đánh giá, giờ chơi, người chơi cùng lúc.

Bảng thông tin mô tả (Dimensions):
2. dim_games: 89,618 dòng, 23 cột. Chứa tên game, giá tiền, phân khúc giá, cờ Win/Mac/Linux, cờ tiếng Việt, link ảnh, mô tả ngắn.
3. dim_date: 4,459 dòng, 12 cột. Chứa ngày phát hành, năm, quý, tháng, thứ trong tuần.
4. dim_genres: 33 dòng, 2 cột. Danh sách 33 thể loại game như Hành động, Nhập vai, Chiến thuật, Mô phỏng...
5. dim_categories: 40 dòng, 2 cột. Danh sách 40 tính năng như Chơi đơn, Nhiều người, Co-op, Hỗ trợ tay cầm, VR...
6. dim_developers: 60,096 dòng, 2 cột. Tên các hãng và studio lập trình làm ra game.
7. dim_publishers: 49,839 dòng, 2 cột. Tên các công ty phát hành game ra thị trường.
8. dim_tags: 452 dòng, 2 cột. Danh mục 452 thẻ tag chi tiết do người chơi bình chọn.

Bảng cầu nối nhiều - nhiều (Bridges):
9. bridge_game_genres: 258,024 dòng. Nối game với thể loại.
10. bridge_game_categories: 376,084 dòng. Nối game với tính năng.
11. bridge_game_developers: 97,833 dòng. Nối game với studio làm game.
12. bridge_game_publishers: 92,473 dòng. Nối game với nhà phát hành.
13. bridge_game_tags: 1,008,987 dòng. Nối game với thẻ tag và số lượt bình chọn.

Bảng gộp sẵn cho Power BI và Tableau:
14. flat_steam_games_bi: 89,618 dòng, 53 cột. Đã ghép sẵn bảng fact với dim_games và dim_date để người dùng kéo thả vẽ biểu đồ ngay mà không cần nối dây quan hệ.

III. CHI TIẾT TỪNG BẢNG VÀ TỪNG CỘT

1. Bảng fact_game_metrics (89,618 dòng, 27 cột)
Mỗi dòng là một tựa game, lưu toàn bộ các số liệu đo lường.
- fact_id: Kiểu số nguyên, khóa chính tự tăng.
- appid: Kiểu số nguyên, mã ID của game trên Steam, dùng nối sang bảng dim_games. Ví dụ: 730 (Counter-Strike 2).
- release_date_id: Kiểu số nguyên, mã ngày phát hành dạng số YYYYMMDD, nối sang bảng dim_date. Ví dụ: 20120821.
- price_usd: Kiểu số thực, giá bán niêm yết bằng USD. Ví dụ: 0.0 (miễn phí) hoặc 19.99.
- discount_pct: Kiểu số nguyên, phần trăm giảm giá hiện tại (0 là không giảm, 50 là giảm 50%).
- dlc_count: Kiểu số nguyên, số lượng gói mở rộng của game.
- achievements: Kiểu số nguyên, số thành tựu trong game.
- positive_reviews: Kiểu số nguyên, số lượt đánh giá khen. Ví dụ: 7,480,813 lượt.
- negative_reviews: Kiểu số nguyên, số lượt đánh giá chê. Ví dụ: 1,135,108 lượt.
- total_reviews: Kiểu số nguyên, tổng lượt đánh giá bằng khen cộng chê.
- positive_ratio_pct: Kiểu số thực, tỷ lệ khen (%) bằng lượt khen chia tổng lượt đánh giá nhân 100.
- review_score_tier: Kiểu chữ, xếp hạng của Steam như Very Positive, Positive, Mixed, Negative...
- metacritic_score: Kiểu số thực, điểm báo chí chấm trên thang 100 (nếu không có thì bằng 0).
- has_metacritic: Kiểu số nguyên, cờ kiểm tra có điểm báo chí hay không (1 là có, 0 là không).
- recommendations: Kiểu số nguyên, số người chơi khuyên nên mua game này.
- estimated_owners_min: Kiểu số nguyên, số người sở hữu game ở mức tối thiểu.
- estimated_owners_max: Kiểu số nguyên, số người sở hữu game ở mức tối đa.
- estimated_owners_avg: Kiểu số nguyên, số người sở hữu trung bình bằng tối thiểu cộng tối đa chia đôi.
- owner_bracket: Kiểu chữ, khoảng người sở hữu ban đầu dạng chữ. Ví dụ: 100000000 - 200000000.
- estimated_revenue_min_usd: Kiểu số thực, doanh thu tối thiểu bằng số người tối thiểu nhân giá bán.
- estimated_revenue_max_usd: Kiểu số thực, doanh thu tối đa bằng số người tối đa nhân giá bán.
- estimated_revenue_avg_usd: Kiểu số thực, doanh thu trung bình bằng số người trung bình nhân giá bán.
- peak_ccu: Kiểu số nguyên, kỷ lục số người cùng online chơi game tại một thời điểm. Ví dụ: 1,212,356 người.
- avg_playtime_forever_hours: Kiểu số thực, thời gian chơi trung bình từ trước đến nay tính bằng giờ.
- median_playtime_forever_hours: Kiểu số thực, thời gian chơi trung vị từ trước đến nay tính bằng giờ.
- avg_playtime_2weeks_hours: Kiểu số thực, thời gian chơi trung bình 2 tuần gần nhất tính bằng giờ.
- median_playtime_2weeks_hours: Kiểu số thực, thời gian chơi trung vị 2 tuần gần nhất tính bằng giờ.

2. Bảng dim_games (89,618 dòng, 23 cột)
Lưu thông tin định danh, phân khúc và tính tương thích của từng game.
- appid: Kiểu số nguyên, khóa chính, mã ID duy nhất của trò chơi trên Steam.
- name: Kiểu chữ, tên chính thức của trò chơi. Ví dụ: Counter-Strike 2.
- release_date_id: Kiểu số nguyên, khóa ngoại, nối sang bảng dim_date.
- required_age: Kiểu số nguyên, độ tuổi tối thiểu được phép chơi (0, 16, 18).
- is_free: Kiểu số nguyên, game miễn phí hay không (1: Miễn phí, 0: Thu phí).
- price_usd: Kiểu số thực, giá niêm yết bằng USD.
- price_tier: Kiểu chữ, phân khúc giá gồm Free, Dưới $5, $5-$15, $15-$30, $30-$60, Trên $60.
- windows: Kiểu số nguyên, chạy được trên Windows không (1: Có, 0: Không).
- mac: Kiểu số nguyên, chạy được trên Mac không (1: Có, 0: Không).
- linux: Kiểu số nguyên, chạy được trên Linux hoặc máy Steam Deck không (1: Có, 0: Không).
- platform_support: Kiểu chữ, tóm tắt hệ điều hành như Windows Only, Windows & Mac, Windows & Linux, Cross-Platform.
- has_vietnamese: Kiểu số nguyên, có tiếng Việt không (1: Có, 0: Không).
- has_english: Kiểu số nguyên, có tiếng Anh không (1: Có, 0: Không).
- supported_languages_count: Kiểu số nguyên, tổng số lượng ngôn ngữ game hỗ trợ.
- primary_genre: Kiểu chữ, thể loại chính đứng đầu của game.
- primary_developer: Kiểu chữ, tên studio chính làm ra game.
- primary_publisher: Kiểu chữ, tên công ty phát hành chính.
- genres_display: Kiểu chữ, danh sách các thể loại nối nhau bằng dấu phẩy.
- categories_display: Kiểu chữ, danh sách tính năng nối nhau bằng dấu phẩy.
- top_tags_display: Kiểu chữ, 5 thẻ tag được bình chọn nhiều nhất.
- header_image: Kiểu chữ, đường link ảnh bìa trên Steam Store.
- website: Kiểu chữ, trang web chính thức của game.
- short_description: Kiểu chữ, đoạn văn ngắn giới thiệu nội dung game.

3. Bảng dim_date (4,459 dòng, 12 cột)
Lưu thông tin ngày phát hành, dùng để phân tích xu hướng theo thời gian.
- date_id: Kiểu số nguyên, khóa chính, mã ngày dạng YYYYMMDD. Ví dụ: 20240315.
- full_date: Kiểu chữ, ngày đầy đủ dạng YYYY-MM-DD. Ví dụ: 2024-03-15.
- year: Kiểu số nguyên, năm phát hành từ 2006 đến 2025.
- quarter: Kiểu số nguyên, quý trong năm từ 1 đến 4.
- quarter_name: Kiểu chữ, tên quý hiển thị biểu đồ như Q1 2024.
- month: Kiểu số nguyên, tháng trong năm từ 1 đến 12.
- month_name: Kiểu chữ, tên tiếng Anh của tháng như March, April.
- month_year: Kiểu chữ, chuỗi Năm-Tháng dùng sắp xếp như 2024-03.
- day_of_month: Kiểu số nguyên, ngày trong tháng từ 1 đến 31.
- day_of_week: Kiểu số nguyên, thứ trong tuần từ 1 (Thứ Hai) đến 7 (Chủ Nhật).
- day_name: Kiểu chữ, tên thứ như Friday, Saturday.
- is_weekend: Kiểu số nguyên, có phải cuối tuần không (1: Thứ Bảy hoặc Chủ Nhật, 0: Ngày thường).

4. Các bảng danh mục thuộc tính:
- Bảng dim_genres (33 dòng): gồm cột genre_id (mã thể loại) và genre_name (tên thể loại như Action, Adventure, RPG, Strategy, Indie...).
- Bảng dim_categories (40 dòng): gồm cột category_id (mã tính năng) và category_name (tên tính năng như Single-player, Multi-player, Co-op, Steam Cloud, VR...).
- Bảng dim_developers (60,096 dòng): gồm cột developer_id (mã studio) và developer_name (tên hãng làm game như Valve, Capcom, Ubisoft...).
- Bảng dim_publishers (49,839 dòng): gồm cột publisher_id (mã nhà phát hành) và publisher_name (tên công ty phát hành như Electronic Arts, Sony...).
- Bảng dim_tags (452 dòng): gồm cột tag_id (mã tag) và tag_name (tên thẻ cộng đồng như FPS, Open World, Souls-like...).

5. Các bảng cầu nối (Bridge Tables):
Lý do cần có: Một game có nhiều thể loại, do nhiều studio làm và có nhiều tag. Nếu để chung 1 bảng thì khi tính tổng doanh thu theo thể loại sẽ bị cộng tiền 1 game nhiều lần (lỗi trùng lặp). Các bảng cầu nối tách riêng từng cặp liên kết để phép tính luôn chuẩn xác 100%.
- bridge_game_genres (258,024 dòng): Cột appid và genre_id.
- bridge_game_categories (376,084 dòng): Cột appid và category_id.
- bridge_game_developers (97,833 dòng): Cột appid và developer_id.
- bridge_game_publishers (92,473 dòng): Cột appid và publisher_id.
- bridge_game_tags (1,008,987 dòng): Cột appid, tag_id và cột vote_count (số phiếu bầu của người chơi cho tag đó).

6. Bảng gộp flat_steam_games_bi (89,618 dòng, 53 cột)
File lưu: data\processed\csv\flat_steam_games_bi.csv (nặng 63.6 MB).
Mục đích: Bảng này đã được ghép sẵn toàn bộ thông tin từ fact_game_metrics cộng dim_games và dim_date. Dành cho những ai muốn mở nhanh Power BI hoặc Tableau kéo thả vẽ biểu đồ ngay lập tức mà không cần nối bảng.

IV. VẤN ĐỀ CỦA BẢNG DỮ LIỆU GỐC TỪ KAGGLE

Tệp gốc là data\raw\games_march2025_cleaned.csv gồm 47 cột thô, gặp các lỗi sau trước khi được làm sạch:
1. Cột thể loại genres, developers, tags bị lưu dạng chuỗi chữ bọc ngoặc vuông như ['Action', 'Indie'] hoặc từ điển {'FPS': 90857}. Không thể dùng lệnh nhóm GROUP BY trong SQL hay kéo thả vào Power BI được.
2. Cột số người sở hữu estimated_owners bị lưu dạng chữ như 20000 - 50000, không thể bấm cộng tổng doanh thu hay tính trung bình được.
3. Cột thời gian chơi ghi bằng phút (hàng chục nghìn phút) rất khó nhìn, đã được chia cho 60 để đổi sang đơn vị Giờ.
4. Cột ngày phát hành release_date là chuỗi chữ lộn xộn, không sắp xếp theo dòng thời gian được.
5. Cột score_rank bị trống 99.9%, cột metacritic_score bị trống hơn 67%, các cột mô tả chứa nhiều thẻ HTML làm tệp tin nặng hàng trăm MB vô ích.
