# THÔNG TIN VÀ CẨM NANG BỘ DỮ LIỆU STEAM GAMES (DATASET INFO)

Thư mục này chứa toàn bộ tài liệu giải thích chi tiết về bộ dữ liệu Steam Games, được viết bằng ngôn ngữ thông thường, rõ ràng, dễ hiểu:

* 👉 [**SO_TAY_DU_LIEU.md**](file:///D:/Steam-Game-Analyst-/dataset_info/SO_TAY_DU_LIEU.md): Toàn bộ thông tin chi tiết về từng bảng, số dòng, từng cột, kiểu dữ liệu và ý nghĩa thực tế.

---

### TÓM TẮT NHANH CÁC BẢNG TRONG KHO DỮ LIỆU:

1. **Bảng số liệu chính (Fact)**:
   * `fact_game_metrics`: **89,618** dòng | **27** cột (Doanh thu ước tính, giá bán, lượt đánh giá, giờ chơi, người chơi cùng lúc).
2. **Các bảng mô tả (Dimensions)**:
   * `dim_games`: **89,618** dòng | **23** cột (Tên game, phân khúc giá, cờ Win/Mac/Linux, tiếng Việt, link ảnh, mô tả).
   * `dim_date`: **4,459** dòng | **12** cột (Năm, Quý, Tháng, Thứ, cờ cuối tuần).
   * `dim_genres`: **33** dòng | **2** cột (Thể loại game).
   * `dim_categories`: **40** dòng | **2** cột (Tính năng game).
   * `dim_developers`: **60,096** dòng | **2** cột (Hãng làm game).
   * `dim_publishers`: **49,839** dòng | **2** cột (Nhà phát hành).
   * `dim_tags`: **452** dòng | **2** cột (Thẻ tag cộng đồng vote).
3. **Các bảng cầu nối (Bridges)**:
   * `bridge_game_genres`: **258,024** dòng (Nối Game - Thể loại).
   * `bridge_game_categories`: **376,084** dòng (Nối Game - Tính năng).
   * `bridge_game_developers`: **97,833** dòng (Nối Game - Nhà phát triển).
   * `bridge_game_publishers`: **92,473** dòng (Nối Game - Nhà phát hành).
   * `bridge_game_tags`: **1,008,987** dòng (Nối Game - Thẻ tag kèm số phiếu vote).
4. **Bảng gộp sẵn (BI View)**:
   * `flat_steam_games_bi`: **89,618** dòng | **53** cột (Dùng kéo thả trực tiếp trong Power BI / Tableau).
