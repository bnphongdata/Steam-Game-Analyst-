# SO TAY THONG TIN CHI TIET BO DU LIEU STEAM GAMES

Tai lieu nay ghi lai toan bo thong tin ve bo du lieu Steam: nguon du lieu, danh sach cac bang, so luong dong, tung cot luu cai gi va kieu du lieu la gi.

---

## 1. NGUON GOC VA QUY MO TONG THE

- Nguon du lieu goc: Tai tu Kaggle (artermiloff/steam-games-dataset), gom toan bo game tren cua hang Steam tu truoc den thang 3/2025.
- Tong so tua game hop le: 89,618 game.
- Doanh thu uoc tinh toan san: Khoang 130.83 ty USD.
- Gia game trung binh: 7.31 USD (khoang 180.000 VND).
- Game mien phi: 14,160 game (chiem 15.8%).
- Game tra phi: 75,458 game (chiem 84.2%).
- Game co tieng Viet: 3,553 game (chiem gan 4%).

---

## 2. NOI LUU TRU DU LIEU TREN O DIA

Toan bo du lieu nam trong thu muc `D:\Steam-Game-Analyst-\data\`:

1. Du lieu tho ban dau (Raw):
   File: `data\raw\games_march2025_cleaned.csv` (Nang 446.9 MB, 47 cot, 89,618 dong).
2. Kho du lieu hoan chinh (Data Warehouse SQLite):
   File: `data\processed\steam_dw.db` (Nang 162.3 MB, gom 13 bang co danh chi muc khoa chinh, khoa ngoai).
3. Cac file CSV xuat ra de mo bang Excel / Power BI / Tableau:
   Thu muc: `data\processed\csv\`
   Gom 13 bang rieng le va 1 bang gop san ten la `flat_steam_games_bi.csv` (nang 63.6 MB).
4. Cac file Parquet nen hieu nang cao:
   Thu muc: `data\processed\parquet\` (doc bang Python, Pandas, PySpark rat nhanh).

---

## 3. DANH SACH TAT CA CAC BANG VA SO DONG

Kho du lieu duoc chia theo mo hinh hinh sao (Star Schema) gom 3 nhom bang:

| Ten bang | Loai bang | So dong | So cot | Y nghia tom tat |
| :--- | :---: | :---: | :---: | :--- |
| `fact_game_metrics` | Bang chinh (Fact) | 89,618 | 27 | Chua tat ca so lieu do luong: tien, luot danh gia, gio choi, nguoi choi. |
| `dim_games` | Bang mo ta (Dim) | 89,618 | 23 | Ten game, phan khuc gia, co Win/Mac/Linux, link anh, mo ta. |
| `dim_date` | Bang mo ta (Dim) | 4,459 | 12 | Ngay phat hanh, nam, quy, thang, thu trong tuan. |
| `dim_genres` | Bang mo ta (Dim) | 33 | 2 | Danh sach 33 the loai game (Hanh dong, Nhap vai, Chien thuat...). |
| `dim_categories` | Bang mo ta (Dim) | 40 | 2 | 40 tinh nang (Choi don, Nhieu nguoi, Co-op, Tay cam, VR...). |
| `dim_developers` | Bang mo ta (Dim) | 60,096 | 2 | Ten cac studio / nguoi lam game. |
| `dim_publishers` | Bang mo ta (Dim) | 49,839 | 2 | Ten cac cong ty phat hanh game. |
| `dim_tags` | Bang mo ta (Dim) | 452 | 2 | 452 the tag do nguoi choi binh chon (Ban sung, The gioi mo...). |
| `bridge_game_genres` | Cau noi (Bridge) | 258,024 | 2 | Noi Game voi The loai (vi 1 game co nhieu the loai). |
| `bridge_game_categories` | Cau noi (Bridge) | 376,084 | 2 | Noi Game voi Tinh nang. |
| `bridge_game_developers` | Cau noi (Bridge) | 97,833 | 2 | Noi Game voi Nha phat trien. |
| `bridge_game_publishers` | Cau noi (Bridge) | 92,473 | 2 | Noi Game voi Nha phat hanh. |
| `bridge_game_tags` | Cau noi (Bridge) | 1,008,987 | 3 | Noi Game voi Tag va so phieu bau cua nguoi choi. |
| `flat_steam_games_bi` | Bang gop (BI View) | 89,618 | 53 | Noi san Fact + Dim Game + Dim Date de mo bang Power BI keo tha ngay. |

---

## 4. CHI TIET TUNG BANG VA TUNG COT DU LIEU SACH

### BANG 1: `fact_game_metrics` (Bang so lieu chinh)
- So dong: 89,618 dong (moi dong tuong ung voi dung 1 tua game).
- Muc dich: Luu toan bo cac con so dung de tinh tong, tinh trung binh, ve bieu do.

| Ten cot | Kieu du lieu | Khoa | Y nghia va cach tinh | Vi du |
| :--- | :---: | :---: | :--- | :--- |
| `fact_id` | INTEGER | PK | So thu tu tu tang cua bang | 1 |
| `appid` | INTEGER | FK | Ma ID cua game tren Steam (noi sang `dim_games`) | 730 |
| `release_date_id` | INTEGER | FK | Ma ngay phat hanh (dang YYYYMMDD, noi sang `dim_date`) | 20120821 |
| `price_usd` | REAL | | Gia ban tinh bang do la My | 0.0 hoac 19.99 |
| `discount_pct` | INTEGER | | Ty le giam gia hien tai (%) | 0 hoac 50 |
| `dlc_count` | INTEGER | | So luong ban mo rong DLC cua game | 1 |
| `achievements` | INTEGER | | So luong thanh tuu dat duoc trong game | 167 |
| `positive_reviews` | INTEGER | | So luot danh gia tich cuc (khen) | 7480813 |
| `negative_reviews` | INTEGER | | So luot danh gia tieu cuc (che) | 1135108 |
| `total_reviews` | INTEGER | | Tong so luot danh gia = positive + negative | 8615921 |
| `positive_ratio_pct` | REAL | | Ty le khen (%) = (positive / total) x 100 | 86.82 |
| `review_score_tier` | TEXT | | Xep hang cua Steam (Very Positive, Mixed...) | Very Positive |
| `metacritic_score` | REAL | | Diem cua bao chi cham tren Metacritic (1-100) | 83.0 (neu khong co thi bang 0) |
| `has_metacritic` | INTEGER | | Co diem Metacritic hay khong (1: Co, 0: Khong co) | 1 |
| `recommendations` | INTEGER | | So luot nguoi choi bam nut khuyen nen choi | 4401572 |
| `estimated_owners_min` | INTEGER | | Uoc luong nguoi so huu (muc thap nhat) | 100000000 |
| `estimated_owners_max` | INTEGER | | Uoc luong nguoi so huu (muc cao nhat) | 200000000 |
| `estimated_owners_avg` | INTEGER | | Uoc luong nguoi so huu (trung binh = (min + max) / 2) | 150000000 |
| `owner_bracket` | TEXT | | Dai nguoi so huu dang chu ban dau tu SteamSpy | 100000000 - 200000000 |
| `estimated_revenue_min_usd` | REAL | | Doanh thu toi thieu uoc tinh = owners_min x price | 0.0 |
| `estimated_revenue_max_usd` | REAL | | Doanh thu toi da uoc tinh = owners_max x price | 0.0 |
| `estimated_revenue_avg_usd` | REAL | | Doanh thu trung binh uoc tinh = owners_avg x price | 0.0 |
| `peak_ccu` | INTEGER | | So nguoi cung online choi nhieu nhat tai 1 thoi diem | 1212356 |
| `avg_playtime_forever_hours` | REAL | | Thoi gian choi trung binh tu truoc den nay (doi ra Gio) | 553.15 |
| `median_playtime_forever_hours` | REAL | | Thoi gian choi trung vi tu truoc den nay (Gio) | 86.23 |
| `avg_playtime_2weeks_hours` | REAL | | Thoi gian choi trung binh trong 2 tuan qua (Gio) | 14.65 |
| `median_playtime_2weeks_hours`| REAL | | Thoi gian choi trung vi trong 2 tuan qua (Gio) | 5.83 |

---

### BANG 2: `dim_games` (Bang thong tin game)
- So dong: 89,618 dong.
- Muc dich: Chua ten, phan loai, he dieu hanh, ngon ngu, hinh anh va mo ta cua game.

| Ten cot | Kieu du lieu | Khoa | Y nghia | Vi du |
| :--- | :---: | :---: | :--- | :--- |
| `appid` | INTEGER | PK | ID duy nhat cua game tren Steam | 730 |
| `name` | TEXT | | Ten tua game | Counter-Strike 2 |
| `release_date_id` | INTEGER | FK | Noi sang bang `dim_date` | 20120821 |
| `required_age` | INTEGER | | Do tuoi toi thieu duoc choi (0, 16, 18) | 0 |
| `is_free` | INTEGER | | Game mien phi hay khong (1: Mien phi, 0: Thu phi) | 1 |
| `price_usd` | REAL | | Gia goc bang USD | 0.0 |
| `price_tier` | TEXT | | Nhom gia (Free, Duoi $5, $5-$15, $15-$30, $30-$60, Tren $60) | Free ($0) |
| `windows` | INTEGER | | Chay duoc tren Windows khong (1: Co, 0: Khong) | 1 |
| `mac` | INTEGER | | Chay duoc tren Mac khong (1: Co, 0: Khong) | 0 |
| `linux` | INTEGER | | Chay duoc tren Linux / Steam Deck khong | 1 |
| `platform_support` | TEXT | | Tom tat nen tang chay duoc | Windows & Linux |
| `has_vietnamese` | INTEGER | | Co tieng Viet khong (1: Co, 0: Khong) | 1 |
| `has_english` | INTEGER | | Co tieng Anh khong (1: Co, 0: Khong) | 1 |
| `supported_languages_count`| INTEGER | | Tong so ngon ngu game ho tro | 29 |
| `primary_genre` | TEXT | | The loai chinh dung dau | Action |
| `primary_developer` | TEXT | | Ten studio chinh lam ra game | Valve |
| `primary_publisher` | TEXT | | Ten nha phat hanh chinh | Valve |
| `genres_display` | TEXT | | Chuoi gom cac the loai noi nhau bang dau phay | Action, Free To Play |
| `categories_display` | TEXT | | Chuoi gom cac tinh nang noi nhau bang dau phay | Multi-player, Steam Cloud |
| `top_tags_display` | TEXT | | 5 the tag duoc nhieu nguoi binh chon nhat | FPS, Shooter, Multiplayer |
| `header_image` | TEXT | | Link anh bia ngang tren Steam Store | https://shared.akamai... |
| `website` | TEXT | | Trang web chinh thuc cua game | http://counter-strike.net/ |
| `short_description` | TEXT | | Doan tom tat gioi thieu ngan noi dung game | For over two decades... |

---

### BANG 3: `dim_date` (Bang thoi gian phat hanh)
- So dong: 4,459 dong (moi dong la 1 ngay phat hanh cu the).
- Muc dich: Dung de loc va ve bieu do theo Nam, Quy, Thang.

| Ten cot | Kieu du lieu | Khoa | Y nghia | Vi du |
| :--- | :---: | :---: | :--- | :--- |
| `date_id` | INTEGER | PK | Ma ngay dang YYYYMMDD | 20240315 |
| `full_date` | TEXT | | Ngay day du chuan YYYY-MM-DD | 2024-03-15 |
| `year` | INTEGER | | Nam | 2024 |
| `quarter` | INTEGER | | Quy (1, 2, 3, 4) | 1 |
| `quarter_name` | TEXT | | Ten quy de hien len bieu do | Q1 2024 |
| `month` | INTEGER | | Thang trong nam (1 den 12) | 3 |
| `month_name` | TEXT | | Ten tieng Anh cua thang | March |
| `month_year` | TEXT | | Nam va thang de sap xep timeline | 2024-03 |
| `day_of_month` | INTEGER | | Ngay trong thang (1 den 31) | 15 |
| `day_of_week` | INTEGER | | Thu trong tuan (1 = Thu Hai, 7 = Chu Nhat) | 5 |
| `day_name` | TEXT | | Ten thu bang tieng Anh | Friday |
| `is_weekend` | INTEGER | | Co phai cuoi tuan khong (1: T7/CN, 0: Ngay thuong) | 0 |

---

### BANG 4 DEN 8: CAC BANG DANH MUC KHAC

- `dim_genres` (33 dong):
  `genre_id` (INTEGER, PK): Ma so the loai.
  `genre_name` (TEXT): Ten the loai (Action, Adventure, Casual, Indie, RPG, Simulation, Strategy...).
- `dim_categories` (40 dong):
  `category_id` (INTEGER, PK): Ma so tinh nang.
  `category_name` (TEXT): Ten tinh nang (Single-player, Multi-player, Co-op, Steam Cloud, VR Support...).
- `dim_developers` (60,096 dong):
  `developer_id` (INTEGER, PK): Ma so studio.
  `developer_name` (TEXT): Ten hang lam game (Valve, Capcom, Ubisoft, KRAFTON...).
- `dim_publishers` (49,839 dong):
  `publisher_id` (INTEGER, PK): Ma so nha phat hanh.
  `publisher_name` (TEXT): Ten nha phat hanh (Electronic Arts, Sony...).
- `dim_tags` (452 dong):
  `tag_id` (INTEGER, PK): Ma so the tag.
  `tag_name` (TEXT): Ten the tag do cong dong gan (FPS, Souls-like, Open World, 2D Platformer...).

---

### BANG 9 DEN 13: CAC BANG CAU NOI (BRIDGE TABLES)
Vi mot game co the thuoc nhieu the loai, do 2 studio cung lam va co 20 the tag. Neu viet chung vao 1 bang thi khi tinh tong tien the loai Action roi cong voi Adventure se bi trung tien (tinh tien 1 game 2 lan). Cac bang cau noi sinh ra de tach rieng tung moi lien ket:

- `bridge_game_genres` (258,024 dong): Cot `appid` va `genre_id`.
- `bridge_game_categories` (376,084 dong): Cot `appid` va `category_id`.
- `bridge_game_developers` (97,833 dong): Cot `appid` va `developer_id`.
- `bridge_game_publishers` (92,473 dong): Cot `appid` va `publisher_id`.
- `bridge_game_tags` (1,008,987 dong): Cot `appid`, `tag_id` va `vote_count` (so phieu bau cua game thu cho tag do).

---

### BANG 14: `flat_steam_games_bi` (Bang gop san phuc vu Power BI / Tableau)
- So dong: 89,618 dong.
- So cot: 53 cot.
- File luu: `data\processed\csv\flat_steam_games_bi.csv` (63.6 MB).
- Muc dich: Bang nay da duoc gom san toan bo cot cua Fact (`fact_game_metrics`) + Chieu Game (`dim_games`) + Chieu Thoi gian (`dim_date`).
- Cach dung: Danh cho ai khong muon tao moi quan he day nho phuc tap trong Power BI. Ban chi can nap dung 1 file nay vao Power BI hoac Tableau la co san tat ca cot de keo tha lam bieu do ngay.

---

## 5. BANG DU LIEU GOC BAN DAU (FILE CSV THO TU KAGGLE)

Tep goc la `data\raw\games_march2025_cleaned.csv` gom 47 cot truoc khi duoc chuan hoa:

| Nhom cot | Cac cot goc | Van de cua du lieu goc |
| :--- | :--- | :--- |
| Dinh danh & Gia | appid, name, release_date, required_age, price, discount, dlc_count | release_date la chu lon xon, khong sap xep timeline duoc. |
| Mo ta & Media | detailed_description, about_the_game, short_description, reviews, notes, header_image, screenshots, movies | Chua nhieu the HTML, link anh, chiem hang tram MB dung luong. |
| He dieu hanh | windows, mac, linux | Dang True/False roi rac. |
| Ngon ngu | supported_languages, full_audio_languages | Bi luu dang chuoi gia lap danh sach: ['English', 'French']. |
| Phan loai nhieu-nhieu | genres, categories, developers, publishers, tags | Bi nhoi nhet dang chuoi list ['Action'] va tu dien {'FPS': 90857}, khong the GROUP BY trong SQL. |
| Danh gia | positive, negative, num_reviews_total, pct_pos_total, num_reviews_recent, pct_pos_recent, metacritic_score, metacritic_url, user_score, score_rank | Cot score_rank trong 99.9%, metacritic_score trong hon 67%. |
| Nguoi choi & Gio choi | estimated_owners, peak_ccu, achievements, recommendations, average_playtime_forever, average_playtime_2weeks, median_playtime_forever, median_playtime_2weeks | estimated_owners la chu 20000 - 50000 khong tinh tong duoc; thoi gian choi de bang phut thay vi gio. |
| Thong tin ho tro | website, support_url, support_email, packages | Nhieu link rong hoac khong dung den trong phan tich kinh doanh. |
