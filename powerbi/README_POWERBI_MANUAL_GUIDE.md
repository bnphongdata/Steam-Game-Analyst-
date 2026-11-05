# CẨM NANG THIẾT KẾ TOÀN BỘ 5 SHEET DASHBOARD POWER BI

Dự án: Phân tích thị trường game Steam
Tác giả: Đội ngũ Phân tích Dữ liệu
Mục tiêu: Cung cấp đầy đủ hướng dẫn tạo 5 sheet báo cáo chuyên sâu. Mỗi sheet đều có ít nhất 5 đến 6 biểu đồ, đi kèm các thẻ số đo lường nhanh và bộ lọc tương tác.

QUY TẮC CHUNG KHI THIẾT KẾ:
1. Mỗi sheet nên có từ 4 đến 5 thẻ số Card đặt ở mép trên cùng để người xem nắm bắt ngay các số liệu chính.
2. Góc trên bên trái đặt từ 1 đến 2 bộ lọc Slicer để lọc nhanh theo Năm hoặc theo Nhóm phân loại.
3. Phần diện tích còn lại chia đều cho 5 đến 6 biểu đồ, khoảng cách giữa các khối từ 10 đến 15 pixel.
4. Bấm Format visual trên từng biểu đồ để đổi tiêu đề tiếng Việt và bật Data labels hiển thị số liệu trực tiếp.


SHEET 1: TỔNG QUAN THỊ TRƯỜNG VÀ KINH DOANH (EXECUTIVE OVERVIEW)

Mục tiêu: Dành cho lãnh đạo và nhà đầu tư xem nhanh quy mô toàn sàn Steam, doanh thu và các tựa game dẫn đầu.

1. Dải 5 thẻ số nhanh (Card visuals):
- Thẻ 1: Chỉ số "Total Games" từ bảng "_Key Measures" (89,618 game).
- Thẻ 2: Chỉ số "Total Estimated Revenue" từ bảng "_Key Measures" (Khoảng 130.83 tỷ USD).
- Thẻ 3: Chỉ số "Avg Game Price" từ bảng "_Key Measures" (7.31 USD).
- Thẻ 4: Chỉ số "Platform Satisfaction Rate" từ bảng "_Key Measures" (82.9%).
- Thẻ 5: Chỉ số "Vietnamese Supported Games" từ bảng "_Key Measures" (3,553 game).

2. Hai bộ lọc tương tác (Slicers):
- Bộ lọc 1: Cột "year" từ bảng "dim_date" (Lọc theo khoảng năm phát hành).
- Bộ lọc 2: Cột "platform_support" từ bảng "dim_games" (Lọc theo hệ điều hành Windows, Mac, Linux).

3. Sáu biểu đồ chính trên Sheet 1:
- Biểu đồ 1: Clustered bar chart (Biểu đồ thanh ngang) - Top 10 thể loại game có doanh thu cao nhất.
  Trục tung (Y-axis): Cột "primary_genre" từ bảng "dim_games" (Lưu ý: Dùng cột "primary_genre" để mỗi game tính đúng 1 thể loại chính, số liệu chuẩn xác 100% không bị trùng lặp).
  Trục hoành (X-axis): Cột "estimated_revenue_avg_usd" từ bảng "fact_game_metrics" (hoặc chỉ số "Total Estimated Revenue" từ bảng "_Key Measures").
  Bộ lọc Filters: Chọn Top 10 theo doanh thu.

- Biểu đồ 2: Clustered column chart (Biểu đồ cột đứng) - Xu hướng phát hành game qua từng năm.
  Trục hoành (X-axis): Cột "year" từ bảng "dim_date".
  Trục tung (Y-axis): Chỉ số "Total Games" từ bảng "_Key Measures".

- Biểu đồ 3: Donut chart (Biểu đồ tròn khuyết) - Cơ cấu phân khúc giá bán game.
  Chú giải (Legend): Cột "price_tier" từ bảng "dim_games".
  Giá trị (Values): Chỉ số "Total Games" từ bảng "_Key Measures".

- Biểu đồ 4: Clustered column chart (Biểu đồ cột đứng) - Phân bổ mức độ đánh giá người chơi.
  Trục hoành (X-axis): Cột "review_score_tier" từ bảng "fact_game_metrics".
  Trục tung (Y-axis): Chỉ số "Total Games" từ bảng "_Key Measures".

- Biểu đồ 5: Treemap (Biểu đồ hình khối) hoặc Clustered bar chart - Top 10 nhà phát hành có doanh thu lớn nhất.
  Nhóm phân loại (Category): Cột "publisher_name" từ bảng "dim_publishers".
  Giá trị (Values): Chỉ số "Total Estimated Revenue" từ bảng "_Key Measures".
  Bộ lọc Filters: Chọn Top 10 theo doanh thu.

- Biểu đồ 6: Table (Bảng danh sách) - Top 10 tựa game bom tấn dẫn đầu thị trường.
  Kéo các cột: Cột "name", "primary_genre", "price_usd" từ bảng "dim_games", cột "estimated_owners_avg" từ "fact_game_metrics", chỉ số "Total Estimated Revenue" và cột "review_score_tier".
  Sắp xếp giảm dần theo cột Doanh thu.


SHEET 2: THỂ LOẠI, TAG VÀ TÍNH NĂNG TRÒ CHƠI (CONTENT & TAXONOMY)

Mục tiêu: Dành cho studio và nhà làm game tìm kiếm thể loại tiềm năng và tính năng game thủ ưa chuộng.

1. Dải 4 thẻ số nhanh:
- Thẻ 1: Tổng số thể loại: 33 thể loại (Card - Đếm DISTINCTCOUNT cột "genre_name").
- Thẻ 2: Thể loại doanh thu số 1: Hành động (Action - 86.58 tỷ USD).
- Thẻ 3: Thể loại nhiều game nhất: Indie (63,189 game).
- Thẻ 4: Tổng số thẻ tag cộng đồng: 452 tags.

2. Hai bộ lọc tương tác:
- Bộ lọc 1: Cột "genre_name" từ bảng "dim_genres" (Chọn xem riêng từng thể loại).
- Bộ lọc 2: Cột "year" từ bảng "dim_date" (Lọc theo năm).

3. Sáu biểu đồ chính trên Sheet 2:
- Biểu đồ 1: Clustered bar chart - Top 15 thể loại có doanh thu cao nhất toàn sàn.
  Trục tung: Cột "primary_genre" từ bảng "dim_games" (Hoặc cột "genre_name" từ bảng "dim_genres" nếu bạn đã bật lọc 2 chiều Both giữa bảng "dim_games" và "bridge_game_genres").
  Trục hoành: Cột "estimated_revenue_avg_usd" từ bảng "fact_game_metrics" (hoặc chỉ số "Total Estimated Revenue").
  Bộ lọc: Top 15 theo doanh thu.

- Biểu đồ 2: Clustered column chart - Số lượng tựa game theo từng thể loại.
  Trục hoành: Cột "genre_name" từ bảng "dim_genres".
  Trục tung: Chỉ số "Total Games" từ bảng "_Key Measures".

- Biểu đồ 3: Treemap (Khối chữ nhật) - Top 20 thẻ tag cộng đồng được bình chọn nhiều nhất.
  Nhóm phân loại: Cột "tag_name" từ bảng "dim_tags".
  Giá trị: Cột "vote_count" từ bảng "bridge_game_tags" (chọn phép tính SUM).

- Biểu đồ 4: Clustered bar chart - Top 10 tính năng phổ biến nhất trên Steam.
  Trục tung: Cột "category_name" từ bảng "dim_categories".
  Trục hoành: Chỉ số "Total Games" từ bảng "_Key Measures".
  Ý nghĩa: Thể hiện độ phổ biến của các tính năng Chơi đơn, Nhiều người, Co-op, Lưu đám mây, Tay cầm.

- Biểu đồ 5: Scatter plot (Biểu đồ phân tán) - Ma trận định vị thể loại game.
  Trục hoành (X-axis): Chỉ số "Total Games" (Độ cạnh tranh thể loại).
  Trục tung (Y-axis): Chỉ số "Total Estimated Revenue" (Quy mô tiền tệ).
  Chi tiết (Details): Cột "genre_name" từ bảng "dim_genres".
  Ý nghĩa: Phát hiện các thể loại ít cạnh tranh nhưng doanh thu trên từng tựa game lại rất cao.

- Biểu đồ 6: Donut chart - Cơ cấu game Chơi đơn (Single-player) so với game Nhiều người (Multiplayer/Co-op).
  Chú giải: Cột "category_name" từ bảng "dim_categories" (lọc lấy Single-player và Multi-player).
  Giá trị: Chỉ số "Total Games".


SHEET 3: CHIẾN LƯỢC ĐỊNH GIÁ VÀ DOANH THU (PRICING & MONETIZATION)

Mục tiêu: Dành cho bộ phận kinh doanh và định giá tìm ra mức giá bán tối ưu cho sản phẩm.

1. Dải 4 thẻ số nhanh:
- Thẻ 1: Giá niêm yết trung bình: 7.31 USD (Chỉ số "Avg Game Price").
- Thẻ 2: Phân khúc tạo ra nhiều tiền nhất: Premium $30 - $59.99 (Đạt 58.97 tỷ USD, chiếm 45.1% doanh thu).
- Thẻ 3: Phân khúc có nhiều tựa game nhất: Budget dưới $5 (39,388 game, chiếm 44% thị trường).
- Thẻ 4: Tỷ lệ game miễn phí: 15.8% (Chỉ số "Free Games Ratio").

2. Hai bộ lọc tương tác:
- Bộ lọc 1: Cột "price_tier" từ bảng "dim_games" (Lọc phân khúc giá).
- Bộ lọc 2: Cột "is_free" từ bảng "dim_games" (Lọc xem game miễn phí hay trả phí).

3. Sáu biểu đồ chính trên Sheet 3:
- Biểu đồ 1: 100% Stacked column chart (Cột chồng 100%) - Nghịch lý giữa số lượng game và doanh thu theo phân khúc giá.
  Trục hoành: Cột "price_tier" từ bảng "dim_games".
  Cột so sánh: Kéo đồng thời chỉ số "Total Games" và chỉ số "Total Estimated Revenue".
  Ý nghĩa: Minh họa trực quan việc phân khúc dưới $5 chiếm gần nửa thị trường nhưng doanh thu chỉ chiếm 3.4%, trong khi phân khúc $30-$60 chỉ chiếm 1.5% số game nhưng mang về tới 45.1% doanh thu.

- Biểu đồ 2: Clustered column chart - Doanh thu theo từng phân khúc giá bán.
  Trục hoành: Cột "price_tier" từ bảng "dim_games".
  Trục tung: Chỉ số "Total Estimated Revenue" từ bảng "_Key Measures".

- Biểu đồ 3: Clustered bar chart - Giá bán trung bình của từng thể loại game.
  Trục tung: Cột "genre_name" từ bảng "dim_genres".
  Trục hoành: Chỉ số "Avg Game Price" từ bảng "_Key Measures".
  Ý nghĩa: Giúp nhà phát triển biết từng thể loại game (như Mô phỏng hay Đua xe) thì game thủ sẵn sàng trả giá bao nhiêu.

- Biểu đồ 4: Clustered column chart - Phân bổ mức độ giảm giá (% Discount).
  Trục hoành: Cột "discount_pct" từ bảng "fact_game_metrics".
  Trục tung: Chỉ số "Total Games".
  Ý nghĩa: Cho thấy các mức sale phổ biến nhất trên Steam là 0%, 20%, 50% và 75%.

- Biểu đồ 5: Line chart (Biểu đồ đường) - Xu hướng giá game trung bình qua từng năm phát hành.
  Trục hoành: Cột "year" từ bảng "dim_date".
  Trục tung: Chỉ số "Avg Game Price" từ bảng "_Key Measures".
  Ý nghĩa: Phân tích xem giá game trên thị trường đang có xu hướng tăng hay giảm theo thời gian.

- Biểu đồ 6: Donut chart - Tỷ lệ doanh thu giữa Game trả phí và Game miễn phí.
  Chú giải: Cột "is_free" từ bảng "dim_games".
  Giá trị: Chỉ số "Total Estimated Revenue".


SHEET 4: TRẢI NGHIỆM NGƯỜI CHƠI VÀ ĐÁNH GIÁ (ENGAGEMENT & SENTIMENT)

Mục tiêu: Đánh giá thời gian gắn bó của game thủ và mức độ hài lòng đối với các sản phẩm trên Steam.

1. Dải 4 thẻ số nhanh:
- Thẻ 1: Thời gian chơi trung bình: 1.92 giờ (Chỉ số "Avg Playtime (Hours)").
- Thẻ 2: Tỷ lệ đánh giá tích cực toàn sàn: 82.9% (Chỉ số "Platform Satisfaction Rate").
- Thẻ 3: Tổng lượt đánh giá của game thủ: Hơn 100 triệu lượt (Chỉ số "Total Reviews").
- Thẻ 4: Kỷ lục số người chơi cùng lúc: 1.21 triệu CCU (Chỉ số "Peak Concurrent Players (CCU)").

2. Hai bộ lọc tương tác:
- Bộ lọc 1: Cột "review_score_tier" từ bảng "fact_game_metrics" (Lọc theo mức độ khen chê).
- Bộ lọc 2: Cột "has_metacritic" từ bảng "fact_game_metrics" (Lọc xem game có điểm báo chí hay không).

3. Sáu biểu đồ chính trên Sheet 4:
- Biểu đồ 1: Clustered column chart - Số lượng game theo từng tầng đánh giá của Steam.
  Trục hoành: Cột "review_score_tier" từ bảng "fact_game_metrics".
  Trục tung: Chỉ số "Total Games" từ bảng "_Key Measures".

- Biểu đồ 2: Clustered bar chart - Top 10 thể loại có thời gian chơi trung bình lâu nhất.
  Trục tung: Cột "genre_name" từ bảng "dim_genres".
  Trục hoành: Chỉ số "Avg Playtime (Hours)" từ bảng "_Key Measures".
  Ý nghĩa: Thể loại Nhập vai (RPG) và Chiến thuật (Strategy) luôn giữ chân game thủ lâu nhất.

- Biểu đồ 3: Scatter plot (Biểu đồ phân tán) - Mối quan hệ giữa Thời gian chơi và Tỷ lệ hài lòng.
  Trục hoành (X-axis): Cột "avg_playtime_forever_hours" từ bảng "fact_game_metrics".
  Trục tung (Y-axis): Cột "positive_ratio_pct" từ bảng "fact_game_metrics".
  Ý nghĩa: Khảo sát xem game thủ chơi càng lâu thì có đánh giá tích cực hơn hay không.

- Biểu đồ 4: Donut chart - Thị phần khả năng hỗ trợ hệ điều hành.
  Chú giải: Cột "platform_support" từ bảng "dim_games".
  Giá trị: Chỉ số "Total Games".
  Ý nghĩa: Thể hiện tỷ lệ game chỉ chạy Windows (76.9%) so với game hỗ trợ cả Mac và Linux/Steam Deck.

- Biểu đồ 5: Clustered bar chart - Top 10 game có số người chơi cùng lúc (Peak CCU) cao nhất.
  Trục tung: Cột "name" từ bảng "dim_games".
  Trục hoành: Chỉ số "Peak Concurrent Players (CCU)" từ bảng "_Key Measures".
  Bộ lọc: Top 10 theo Peak CCU (Các tựa game như Counter-Strike 2, Dota 2, PUBG, Cyberpunk 2077...).

- Biểu đồ 6: Line chart - Tương quan giữa điểm đánh giá của Báo chí (Metacritic) và Đánh giá của Game thủ.
  Trục hoành: Cột "genre_name" từ bảng "dim_genres".
  Trục tung 1: Điểm Metacritic trung bình.
  Trục tung 2: Tỷ lệ khen trung bình của game thủ.


SHEET 5: THỊ TRƯỜNG VIỆT NAM VÀ BẢN ĐỊA HÓA (VIETNAM FOCUS)

Mục tiêu: Đánh giá tiềm năng, quy mô và cơ hội cho các tựa game có hỗ trợ Tiếng Việt.

1. Dải 4 thẻ số nhanh:
- Thẻ 1: Số tựa game có tiếng Việt: 3,553 game (Chỉ số "Vietnamese Supported Games").
- Thẻ 2: Tỷ lệ game có tiếng Việt trên toàn sàn: 3.96%.
- Thẻ 3: Tổng doanh thu ước tính từ các game có tiếng Việt: Khoảng 18.5 tỷ USD.
- Thẻ 4: Tỷ lệ đánh giá tích cực bình quân của game có tiếng Việt: 85.2%.

2. Hai bộ lọc tương tác:
- Bộ lọc 1: Cột "year" từ bảng "dim_date" (Lọc theo năm phát hành).
- Bộ lọc 2: Cột "price_tier" từ bảng "dim_games" (Lọc theo phân khúc giá).

3. Năm biểu đồ chính trên Sheet 5:
- Biểu đồ 1: Clustered column chart - Tốc độ tăng trưởng số lượng game hỗ trợ tiếng Việt qua các năm.
  Trục hoành: Cột "year" từ bảng "dim_date".
  Trục tung: Chỉ số "Vietnamese Supported Games" từ bảng "_Key Measures".
  Ý nghĩa: Cho thấy các nhà phát triển quốc tế ngày càng chú trọng bổ sung tiếng Việt từ năm 2020 trở lại đây.

- Biểu đồ 2: Clustered bar chart - Top 10 thể loại game có tiếng Việt nhiều nhất.
  Trục tung: Cột "genre_name" từ bảng "dim_genres".
  Trục hoành: Chỉ số "Vietnamese Supported Games" từ bảng "_Key Measures".

- Biểu đồ 3: Donut chart - Cơ cấu phân khúc giá của các tựa game có tiếng Việt.
  Chú giải: Cột "price_tier" từ bảng "dim_games".
  Giá trị: Chỉ số "Vietnamese Supported Games".
  Bộ lọc: Đặt điều kiện cột "has_vietnamese" bằng 1.

- Biểu đồ 4: Clustered bar chart - Top 10 nhà phát hành có nhiều tựa game hỗ trợ tiếng Việt nhất.
  Trục tung: Cột "publisher_name" từ bảng "dim_publishers".
  Trục hoành: Chỉ số "Vietnamese Supported Games".

- Biểu đồ 5: Table - Danh sách các tựa game bom tấn nổi tiếng nhất có hỗ trợ Tiếng Việt.
  Kéo các cột: Cột "name", "primary_genre", "price_usd", "estimated_owners_avg", "positive_ratio_pct" và chỉ số "Total Estimated Revenue".
  Bộ lọc Filters: Đặt điều kiện cột "has_vietnamese" bằng 1 và sắp xếp theo doanh thu giảm dần (như Cyberpunk 2077, Black Myth Wukong, Dota 2, Counter-Strike 2...).
