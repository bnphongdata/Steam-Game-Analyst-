# Huong Dan Tu Xay Dung Dashboard Power BI Thu Cong

Du An: Phan Tich Toan Dien Thi Truong Game Steam (Steam Games Analytics)
Tac gia: Data Analyst Team
Mo hinh du lieu: Star Schema

---

## 1. Luu Tep `.pbix` Tu Cua So Dang Mo

Trong cua so Power BI Desktop dang mo cua ban (noi da co san toan bo bang du lieu va thuoc do DAX o thanh Data ben phai):
1. Nhan to hop phim Ctrl + S (hoac chon File -> Save As).
2. Chon thu muc luu: `D:\Steam-Game-Analyst-\powerbi\`.
3. Dat ten tep: `Steam_Analytics.pbix`.
4. Nhan Save.

Toan bo mo hinh du lieu, quan he Star Schema va 14 thuoc do DAX da duoc tich hop san vinh vien trong file `.pbix` nay. Lan sau ban chi can nhap dup vao `Steam_Analytics.pbix` de lam viec tiep.

---

## 2. Danh Muc 14 Thuoc Do DAX Da Nap San Trong Bang `_Key Measures`

Tat ca cac thuoc do duoi day da duoc tinh toan va dinh dang san (tien te USD, phan cach hang nghin, phan tram %), ban chi can keo vao Canvas:

| STT | Ten Thuoc Do (Measure) | Dinh Dang | Mo Ta Y Nghia Nghiep Vu |
| :---: | :--- | :---: | :--- |
| 1 | `Total Games` | #,##0 | Tong so luong tua game hop le tren Steam (89,618 games). |
| 2 | `Total Free Games` | #,##0 | So luong game mien phi (Free-to-Play). |
| 3 | `Total Paid Games` | #,##0 | So luong game tra phi (Paid Games). |
| 4 | `Free Games Ratio` | 0.0% | Ty le game mien phi tren toan san Steam. |
| 5 | `Vietnamese Supported Games` | #,##0 | So tua game co ho tro Tieng Viet (3,553 games). |
| 6 | `Total Estimated Revenue` | $#,##0 | Tong doanh thu uoc tinh toan thi truong (Khoang 130.83 Ty USD). |
| 7 | `Avg Game Price` | $#,##0.00 | Gia niem yet trung binh cua mot tua game (7.31 USD). |
| 8 | `Total Estimated Owners` | #,##0 | Tong luot tai hoac so huu game uoc tinh. |
| 9 | `Total Positive Reviews` | #,##0 | Tong so danh gia tich cuc cua game thu. |
| 10 | `Total Negative Reviews` | #,##0 | Tong so danh gia tieu cuc. |
| 11 | `Total Reviews` | #,##0 | Tong so danh gia toan san Steam. |
| 12 | `Platform Satisfaction Rate` | 0.0% | Ty le hai long chung cua game thu (Positive Ratio khoang 82.9%). |
| 13 | `Peak Concurrent Players (CCU)`| #,##0 | Ky luc so nguoi choi dong thoi cao nhat. |
| 14 | `Avg Playtime (Hours)` | #,##0.0 | Thoi gian choi trung binh tron doi cua nguoi choi (Gio). |

---

## 3. Cong Thuc Keo Tha Xay Dung 5 Bieu Do Khuyen Dung

### Visual 1: The Chi So Tong Quan (Cards)
- Loai visual: Card (hoac New Card)
- Truong du lieu: Keo tha lan luot cac chi so tu bang `_Key Measures`:
  - Card 1: `Total Games`
  - Card 2: `Total Estimated Revenue`
  - Card 3: `Avg Game Price`
  - Card 4: `Platform Satisfaction Rate`
  - Card 5: `Vietnamese Supported Games`

### Visual 2: Top The Loai Game Co Doanh Thu Khung Nhat
- Loai visual: Clustered Bar Chart (Bieu do thanh ngang)
- Y-axis (Truc tung): `dim_genres[genre_name]`
- X-axis (Truc hoanh): `_Key Measures[Total Estimated Revenue]`
- Bo loc (Filter): Loc Top 10 the loai co doanh thu cao nhat.

### Visual 3: Xu Huong So Game Phat Hanh Qua Tung Nam
- Loai visual: Clustered Column Chart hoac Area Chart
- X-axis (Truc hoanh): `dim_date[year]`
- Y-axis (Truc tung): `_Key Measures[Total Games]`

### Visual 4: Co Cau Phan Khuc Gia (Price Tiers)
- Loai visual: Donut Chart (Bieu do tron)
- Legend (Chu giai): `dim_games[price_tier]`
- Values (Gia tri): `_Key Measures[Total Games]`

### Visual 5: Phan Bo Tang Danh Gia Cua Nguoi Choi (Review Score Tiers)
- Loai visual: Clustered Bar Chart (Bieu do thanh)
- Y-axis: `fact_game_metrics[review_score_tier]`
- X-axis: `_Key Measures[Total Games]`

### Visual 6: Bo Loc Tuong Tac Nen Tang (Slicer)
- Loai visual: Slicer
- Field: `dim_games[platform_support]` (de loc xem rieng theo Win, Mac, Linux hoac da nen tang).
