# THÔNG TIN VÀ CẨM NANG BỘ DỮ LIỆU STEAM GAMES

Thư mục này chứa toàn bộ tài liệu giải thích chi tiết về bộ dữ liệu Steam Games, được viết bằng tiếng Việt thông thường, rõ ràng, dễ hiểu, không sử dụng các ký tự đặc biệt như dấu sao hay dấu phẩy chéo ngược:

- Đọc tài liệu chi tiết tại tệp: SO_TAY_DU_LIEU.md

---

## TÓM TẮT NHANH CÁC BẢNG TRONG KHO DỮ LIỆU

1. Bảng số liệu chính (Fact):
   - "fact_game_metrics": 89,618 dòng và 27 cột (Doanh thu ước tính, giá bán, lượt đánh giá, giờ chơi, kỷ lục người chơi cùng lúc).

2. Các bảng mô tả (Dimensions):
   - "dim_games": 89,618 dòng và 23 cột (Tên game, phân khúc giá, cờ Win/Mac/Linux, cờ tiếng Việt, link ảnh, mô tả ngắn).
   - "dim_date": 4,459 dòng và 12 cột (Năm, Quý, Tháng, Thứ, cờ cuối tuần).
   - "dim_genres": 33 dòng và 2 cột (Thể loại game).
   - "dim_categories": 40 dòng và 2 cột (Tính năng game).
   - "dim_developers": 60,096 dòng và 2 cột (Hãng làm game).
   - "dim_publishers": 49,839 dòng và 2 cột (Nhà phát hành).
   - "dim_tags": 452 dòng và 2 cột (Thẻ tag do cộng đồng người chơi bình chọn).

3. Các bảng cầu nối (Bridges):
   - "bridge_game_genres": 258,024 dòng (Nối Game với Thể loại).
   - "bridge_game_categories": 376,084 dòng (Nối Game với Tính năng).
   - "bridge_game_developers": 97,833 dòng (Nối Game với Nhà phát triển).
   - "bridge_game_publishers": 92,473 dòng (Nối Game với Nhà phát hành).
   - "bridge_game_tags": 1,008,987 dòng (Nối Game với Thẻ tag kèm số phiếu bình chọn).

4. Bảng gộp sẵn (BI View):
   - "flat_steam_games_bi": 89,618 dòng và 53 cột (Dùng kéo thả trực tiếp trong Power BI hoặc Tableau).
