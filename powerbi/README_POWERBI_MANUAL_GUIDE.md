# HƯỚNG DẪN TẠO DASHBOARD TRÊN MỘT SHEET DUY NHẤT

Dự án: Phân tích thị trường game Steam
Mục tiêu: Thiết kế 1 trang báo cáo tổng thể gồm 5 thẻ số KPI, 2 bộ lọc và 6 biểu đồ trực quan.

I. LƯU TỆP BÁO CÁO

Trong cửa sổ Power BI Desktop đang mở có sẵn dữ liệu ở thanh bên phải:
1. Bấm tổ hợp phím Ctrl + S hoặc vào menu File chọn Save As.
2. Chọn thư mục lưu: D:\Steam-Game-Analyst-\powerbi\
3. Đặt tên tệp: "Steam_Analytics.pbix" rồi bấm Save.

II. BỐ CỤC TỔNG THỂ TRÊN 1 SHEET DASHBOARD

Một trang báo cáo chuyên nghiệp được chia thành 4 khu vực:

1. Hàng trên cùng: 5 thẻ số đo lường nhanh (Card visuals).
2. Góc trên bên trái: 2 bộ lọc (Slicers) để chọn Năm và chọn Hệ điều hành.
3. Khu vực giữa: 3 biểu đồ chính về Doanh thu thể loại, Xu hướng năm và Phân khúc giá.
4. Khu vực dưới cùng: 3 biểu đồ về Đánh giá người chơi, Nhà phát hành lớn và Bảng xếp hạng game bom tấn.

III. CHI TIẾT CÁCH TẠO CÁC BIỂU ĐỒ TRÊN CÙNG 1 SHEET

KHU VỰC 1: 5 THẺ CHỈ SỐ NHANH (CARDS)
Đặt nằm ngang ở sát mép trên cùng của trang:

Thẻ 1: Tổng số game
- Chọn biểu tượng Card (biểu tượng thẻ số 123) trong khung Visualizations.
- Kéo chỉ số "Total Games" từ bảng "_Key Measures" vào ô Fields.
- Kết quả hiện số: 89,618 game.

Thẻ 2: Tổng doanh thu ước tính
- Chọn biểu tượng Card.
- Kéo chỉ số "Total Estimated Revenue" từ bảng "_Key Measures" vào ô Fields.
- Kết quả hiện: Khoảng 130.83 tỷ USD.

Thẻ 3: Giá bán trung bình
- Chọn biểu tượng Card.
- Kéo chỉ số "Avg Game Price" từ bảng "_Key Measures" vào ô Fields.
- Kết quả hiện: 7.31 USD.

Thẻ 4: Tỷ lệ hài lòng chung
- Chọn biểu tượng Card.
- Kéo chỉ số "Platform Satisfaction Rate" từ bảng "_Key Measures" vào ô Fields.
- Kết quả hiện: 82.9%.

Thẻ 5: Game có tiếng Việt
- Chọn biểu tượng Card.
- Kéo chỉ số "Vietnamese Supported Games" từ bảng "_Key Measures" vào ô Fields.
- Kết quả hiện: 3,553 game.


KHU VỰC 2: 2 BỘ LỌC TƯƠNG TÁC (SLICERS)
Đặt ở góc bên trái, ngay dưới hàng thẻ số:

Bộ lọc 1: Lọc theo năm phát hành
- Chọn biểu tượng Slicer (hình cái phễu lọc).
- Kéo cột "year" từ bảng "dim_date" vào ô Field.
- Chuyển kiểu hiển thị sang dạng thanh trượt (Between) hoặc danh sách chọn.

Bộ lọc 2: Lọc theo hệ điều hành
- Chọn biểu tượng Slicer.
- Kéo cột "platform_support" từ bảng "dim_games" vào ô Field.
- Giúp người xem lọc nhanh các game chạy riêng Windows, Mac hoặc cả 3 hệ điều hành.


KHU VỰC 3: 6 BIỂU ĐỒ CHÍNH (ĐÁP ỨNG YÊU CẦU ÍT NHẤT 5 BIỂU ĐỒ)

Biểu đồ 1: Top 10 thể loại game có doanh thu cao nhất
- Loại biểu đồ: Clustered bar chart (biểu đồ thanh nằm ngang).
- Trục tung (Y-axis): Kéo cột "genre_name" từ bảng "dim_genres".
- Trục hoành (X-axis): Kéo chỉ số "Total Estimated Revenue" từ bảng "_Key Measures".
- Cách lọc lấy Top 10: Nhìn vào ô Filters bên cạnh, mở mục "genre_name", đổi từ Basic filtering sang Top N, gõ số 10, kéo chỉ số "Total Estimated Revenue" vào ô By value rồi bấm Apply filter.
- Ý nghĩa: Cho thấy các thể loại Hành động, Nhập vai, Phiêu lưu chiếm phần lớn tiền trên Steam.

Biểu đồ 2: Xu hướng số lượng game phát hành qua từng năm
- Loại biểu đồ: Clustered column chart (biểu đồ cột đứng).
- Trục hoành (X-axis): Kéo cột "year" từ bảng "dim_date".
- Trục tung (Y-axis): Kéo chỉ số "Total Games" từ bảng "_Key Measures".
- Ý nghĩa: Cho thấy tốc độ tăng trưởng số lượng game bùng nổ mạnh mẽ từ năm 2014 đến 2024.

Biểu đồ 3: Cơ cấu phân khúc giá bán game
- Loại biểu đồ: Donut chart (biểu đồ hình tròn khuyết).
- Chú giải (Legend): Kéo cột "price_tier" từ bảng "dim_games".
- Giá trị (Values): Kéo chỉ số "Total Games" từ bảng "_Key Measures".
- Ý nghĩa: Thể hiện tỷ lệ game miễn phí, game giá rẻ dưới 5 USD và game giá cao trên 60 USD.

Biểu đồ 4: Phân bổ mức độ đánh giá của người chơi
- Loại biểu đồ: Clustered column chart hoặc Clustered bar chart.
- Trục phân loại: Kéo cột "review_score_tier" từ bảng "fact_game_metrics".
- Trục đo lường: Kéo chỉ số "Total Games" từ bảng "_Key Measures".
- Ý nghĩa: Thống kê số lượng game đạt các mức đánh giá như Cực kỳ tích cực, Tích cực, Trái chiều hoặc Tiêu cực.

Biểu đồ 5: Top 10 nhà phát hành có doanh thu lớn nhất
- Loại biểu đồ: Treemap (biểu đồ hình khối cây chữ nhật) hoặc Clustered bar chart.
- Nhóm phân loại (Category): Kéo cột "publisher_name" từ bảng "dim_publishers".
- Giá trị (Values): Kéo chỉ số "Total Estimated Revenue" từ bảng "_Key Measures".
- Cách lọc: Lọc Top 10 theo doanh thu trong ô Filters.
- Ý nghĩa: Điểm mặt các ông lớn phát hành game đứng đầu thị trường như Valve, Electronic Arts, Capcom, Ubisoft...

Biểu đồ 6: Bảng chi tiết Top game bom tấn dẫn đầu thị trường
- Loại biểu đồ: Table (biểu tượng bảng biểu).
- Kéo lần lượt các cột vào ô Columns:
  1. Cột "name" từ bảng "dim_games" (Tên game).
  2. Cột "primary_genre" từ bảng "dim_games" (Thể loại chính).
  3. Cột "price_usd" từ bảng "dim_games" (Giá tiền).
  4. Cột "estimated_owners_avg" từ bảng "fact_game_metrics" (Số người tải).
  5. Chỉ số "Total Estimated Revenue" từ bảng "_Key Measures" (Doanh thu).
  6. Cột "review_score_tier" từ bảng "fact_game_metrics" (Xếp hạng đánh giá).
- Cách sắp xếp: Bấm chuột vào tiêu đề cột Doanh thu trên bảng để sắp xếp giảm dần từ trên xuống dưới.

IV. NGUYÊN TẮC TRÌNH BÀY ĐẸP VÀ DỄ NHÌN

- Sắp xếp ngay ngắn: Giữ khoảng cách giữa các biểu đồ đều nhau từ 10 đến 15 pixel.
- Tiêu đề ngắn gọn: Bấm vào từng biểu đồ, vào mục Format visual, sửa Title thành tên tiếng Việt dễ hiểu như: Top 10 thể loại doanh thu, Doanh thu theo nhà phát hành, Cơ cấu giá bán.
- Bật nhãn dữ liệu: Với các biểu đồ cột và biểu đồ thanh, vào mục Format visual, bật Data labels để hiện con số cụ thể ngay trên đầu mỗi cột.
