# THONG TIN VA CAM NANG BO DU LIEU STEAM GAMES (DATASET INFO)

Thu muc nay chua toan bo tai lieu giai thich chi tiet ve bo du lieu Steam Games, duoc viet bang ngon ngu thong thuong, ro rang, de hieu, khong dung ky tu sao:

- Doc tai lieu chi tiet tai: SO_TAY_DU_LIEU.md

---

## TOM TAT NHANH CAC BANG TRONG KHO DU LIEU

1. Bang so lieu chinh (Fact):
   - fact_game_metrics: 89,618 dong va 27 cot (Doanh thu uoc tinh, gia ban, luot danh gia, gio choi, nguoi choi cung luc).

2. Cac bang mo ta (Dimensions):
   - dim_games: 89,618 dong va 23 cot (Ten game, phan khuc gia, co Win/Mac/Linux, tieng Viet, link anh, mo ta).
   - dim_date: 4,459 dong va 12 cot (Nam, Quy, Thang, Thu, co cuoi tuan).
   - dim_genres: 33 dong va 2 cot (The loai game).
   - dim_categories: 40 dong va 2 cot (Tinh nang game).
   - dim_developers: 60,096 dong va 2 cot (Hang lam game).
   - dim_publishers: 49,839 dong va 2 cot (Nha phat hanh).
   - dim_tags: 452 dong va 2 cot (The tag cong dong vote).

3. Cac bang cau noi (Bridges):
   - bridge_game_genres: 258,024 dong (Noi Game voi The loai).
   - bridge_game_categories: 376,084 dong (Noi Game voi Tinh nang).
   - bridge_game_developers: 97,833 dong (Noi Game voi Nha phat trien).
   - bridge_game_publishers: 92,473 dong (Noi Game voi Nha phat hanh).
   - bridge_game_tags: 1,008,987 dong (Noi Game voi The tag kem so phieu vote).

4. Bang gop san (BI View):
   - flat_steam_games_bi: 89,618 dong va 53 cot (Dung keo tha truc tiep trong Power BI hoac Tableau).
