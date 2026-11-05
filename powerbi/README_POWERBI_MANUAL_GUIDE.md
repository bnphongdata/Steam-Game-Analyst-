# HƯỚNG DẪN TỰ XÂY DỰNG DASHBOARD POWER BI THỦ CÔNG

Dự Án: Phân Tích Toàn Diện Thị Trường Game Steam (Steam Games Analytics)
Tác giả: Đội ngũ Phân tích Dữ liệu
Mô hình dữ liệu: Star Schema

---

## 1. Lưu Tệp ".pbix" Từ Cửa Sổ Đang Mở

Trong cửa sổ Power BI Desktop đang mở của bạn (nơi đã có sẵn toàn bộ bảng dữ liệu và thước đo DAX ở thanh Data bên phải):
1. Nhấn tổ hợp phím Ctrl + S (hoặc chọn File -> Save As).
2. Chọn thư mục lưu: D:\Steam-Game-Analyst-\powerbi\
3. Đặt tên tệp: "Steam_Analytics.pbix"
4. Nhấn Save.

Toàn bộ mô hình dữ liệu, quan hệ Star Schema và 14 thước đo DAX đã được tích hợp sẵn vĩnh viễn trong tệp ".pbix" này. Lần sau bạn chỉ cần nhấp đúp vào "Steam_Analytics.pbix" để tiếp tục làm việc.

---

## 2. Danh Mục 14 Thước Đo DAX Đã Nạp Sẵn Trong Bảng "_Key Measures"

Tất cả các thước đo dưới đây đã được tính toán và định dạng sẵn (tiền tệ USD, phân cách hàng nghìn, phần trăm %), bạn chỉ cần kéo vào Canvas:

| STT | Tên Thước Đo (Measure) | Định Dạng | Mô Tả Ý Nghĩa Nghiệp Vụ |
| :---: | :--- | :---: | :--- |
| 1 | "Total Games" | #,##0 | Tổng số lượng tựa game hợp lệ trên Steam (89,618 games). |
| 2 | "Total Free Games" | #,##0 | Số lượng game miễn phí (Free-to-Play). |
| 3 | "Total Paid Games" | #,##0 | Số lượng game trả phí (Paid Games). |
| 4 | "Free Games Ratio" | 0.0% | Tỷ lệ game miễn phí trên toàn sàn Steam. |
| 5 | "Vietnamese Supported Games" | #,##0 | Số tựa game có hỗ trợ Tiếng Việt (3,553 games). |
| 6 | "Total Estimated Revenue" | $#,##0 | Tổng doanh thu ước tính toàn thị trường (Khoảng 130.83 Tỷ USD). |
| 7 | "Avg Game Price" | $#,##0.00 | Giá niêm yết trung bình của một tựa game (7.31 USD). |
| 8 | "Total Estimated Owners" | #,##0 | Tổng lượt tải hoặc sở hữu game ước tính. |
| 9 | "Total Positive Reviews" | #,##0 | Tổng số đánh giá tích cực của game thủ. |
| 10 | "Total Negative Reviews" | #,##0 | Tổng số đánh giá tiêu cực. |
| 11 | "Total Reviews" | #,##0 | Tổng số đánh giá toàn sàn Steam. |
| 12 | "Platform Satisfaction Rate" | 0.0% | Tỷ lệ hài lòng chung của game thủ (Positive Ratio khoảng 82.9%). |
| 13 | "Peak Concurrent Players (CCU)"| #,##0 | Kỷ lục số người chơi đồng thời cao nhất. |
| 14 | "Avg Playtime (Hours)" | #,##0.0 | Thời gian chơi trung bình trọn đời của người chơi (Giờ). |

---

## 3. Công Thức Kéo Thả Xây Dựng 5 Biểu Đồ Khuyên Dùng

### Biểu đồ 1: Thẻ Chỉ Số Tổng Quan (Cards)
- Loại visual: Card (hoặc New Card)
- Trường dữ liệu: Kéo thả lần lượt các chỉ số từ bảng "_Key Measures":
  - Thẻ 1: "Total Games"
  - Thẻ 2: "Total Estimated Revenue"
  - Thẻ 3: "Avg Game Price"
  - Thẻ 4: "Platform Satisfaction Rate"
  - Thẻ 5: "Vietnamese Supported Games"

### Biểu đồ 2: Top Thể Loại Game Có Doanh Thu Cao Nhất
- Loại visual: Clustered Bar Chart (Biểu đồ thanh ngang)
- Trục tung (Y-axis): "dim_genres[genre_name]"
- Trục hoành (X-axis): "_Key Measures[Total Estimated Revenue]"
- Bộ lọc (Filter): Lọc Top 10 thể loại có doanh thu cao nhất.

### Biểu đồ 3: Xu Hướng Số Game Phát Hành Qua Từng Năm
- Loại visual: Clustered Column Chart hoặc Area Chart
- Trục hoành (X-axis): "dim_date[year]"
- Trục tung (Y-axis): "_Key Measures[Total Games]"

### Biểu đồ 4: Cơ Cấu Phân Khúc Giá (Price Tiers)
- Loại visual: Donut Chart (Biểu đồ tròn)
- Chú giải (Legend): "dim_games[price_tier]"
- Giá trị (Values): "_Key Measures[Total Games]"

### Biểu đồ 5: Phân Bổ Tầng Đánh Giá Của Người Chơi (Review Score Tiers)
- Loại visual: Clustered Bar Chart (Biểu đồ thanh)
- Trục tung: "fact_game_metrics[review_score_tier]"
- Trục hoành: "_Key Measures[Total Games]"

### Biểu đồ 6: Bộ Lọc Tương Tác Nền Tảng (Slicer)
- Loại visual: Slicer
- Trường dữ liệu: "dim_games[platform_support]" (để lọc xem riêng theo Win, Mac, Linux hoặc đa nền tảng).
