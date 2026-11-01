"""
=============================================================================
Module: build_powerbi_dashboard.py
Mục đích: Tự động tạo dự án Power BI Project (.pbip) kèm Dashboard hoàn chỉnh
Tác giả: Data Analyst Team
Ngày tạo: 2026-11-01
=============================================================================
"""

import os
import json
import shutil


def create_visual_json(name, x, y, width, height, z, visual_type, query_state, title_text, sort_def=None):
    """Tạo cấu trúc JSON chuẩn cho từng visual trong PBIR format."""
    visual_obj = {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.4.0/schema.json",
        "name": name,
        "position": {
            "x": x,
            "y": y,
            "z": z,
            "height": height,
            "width": width,
            "tabOrder": z
        },
        "visual": {
            "visualType": visual_type,
            "query": {
                "queryState": query_state
            },
            "visualContainerObjects": {
                "border": [
                    {
                        "properties": {
                            "show": {"expr": {"Literal": {"Value": "true"}}},
                            "radius": {"expr": {"Literal": {"Value": "8D"}}},
                            "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#E0E0E0'"}}}}}
                        }
                    }
                ],
                "dropShadow": [
                    {
                        "properties": {
                            "show": {"expr": {"Literal": {"Value": "true"}}},
                            "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#D0D0D0'"}}}}}
                        }
                    }
                ],
                "title": [
                    {
                        "properties": {
                            "show": {"expr": {"Literal": {"Value": "true"}}},
                            "text": {"expr": {"Literal": {"Value": f"'{title_text}'"}}},
                            "fontFamily": {"expr": {"Literal": {"Value": "'Segoe UI'"}}},
                            "bold": {"expr": {"Literal": {"Value": "true"}}}
                        }
                    }
                ]
            },
            "drillFilterOtherVisuals": True
        }
    }
    if sort_def:
        visual_obj["visual"]["query"]["sortDefinition"] = sort_def
    return visual_obj


def build_steam_pbip(target_dir: str = "D:/Steam-Game-Analyst-"):
    """Xây dựng thư mục và các tệp Power BI Project (.pbip)."""
    print("=" * 80)
    print("BẮT ĐẦU: Tạo dự án Power BI Project (.pbip) kèm Dashboard trực quan...")
    print("=" * 80)

    pbip_file = os.path.join(target_dir, "Steam_Analytics.pbip")
    sem_dir = os.path.join(target_dir, "Steam_Analytics.SemanticModel")
    rep_dir = os.path.join(target_dir, "Steam_Analytics.Report")

    # 1. Tạo file .pbip
    pbip_content = {
        "version": "1.0",
        "artifacts": [
            {"report": {"path": "Steam_Analytics.Report"}}
        ],
        "settings": {}
    }
    with open(pbip_file, "w", encoding="utf-8") as f:
        json.dump(pbip_content, f, indent=2)
    print(f"-> [OK] Đã tạo file dự án: {pbip_file}")

    # 2. Tạo Semantic Model (sao chép TMDL definition đã được kiểm thử)
    src_tmdl_dir = os.path.join(target_dir, "powerbi/Steam_Analytics.SemanticModel/definition")
    dst_tmdl_dir = os.path.join(sem_dir, "definition")
    os.makedirs(dst_tmdl_dir, exist_ok=True)
    if os.path.exists(src_tmdl_dir):
        for item in os.listdir(src_tmdl_dir):
            s = os.path.join(src_tmdl_dir, item)
            d = os.path.join(dst_tmdl_dir, item)
            if os.path.isfile(s):
                shutil.copy2(s, d)
    
    with open(os.path.join(sem_dir, "definition.pbism"), "w", encoding="utf-8") as f:
        json.dump({"version": "1.0", "settings": {}}, f, indent=2)
    print(f"-> [OK] Đã thiết lập Semantic Model TMDL tại: {sem_dir}")

    # 3. Tạo Report PBIR
    rep_def_dir = os.path.join(rep_dir, "definition")
    pages_dir = os.path.join(rep_def_dir, "pages")
    page1_dir = os.path.join(pages_dir, "page1")
    visuals_dir = os.path.join(page1_dir, "visuals")
    os.makedirs(visuals_dir, exist_ok=True)

    # definition.pbir
    pbir_content = {
        "version": "1.0",
        "datasetReference": {
            "byPath": {"path": "../Steam_Analytics.SemanticModel"},
            "byConnection": None
        }
    }
    with open(os.path.join(rep_dir, "definition.pbir"), "w", encoding="utf-8") as f:
        json.dump(pbir_content, f, indent=2)

    # version.json
    with open(os.path.join(rep_def_dir, "version.json"), "w", encoding="utf-8") as f:
        json.dump({
            "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/versionMetadata/1.0.0/schema.json",
            "version": "2.0.0"
        }, f, indent=2)

    # report.json
    report_json_content = {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/report/3.0.0/schema.json",
        "themeCollection": {
            "baseTheme": {
                "name": "CY25SU11",
                "reportVersionAtImport": {"visual": "2.4.0", "report": "3.0.0", "page": "2.3.0"},
                "type": "SharedResources"
            }
        },
        "settings": {
            "useStylableVisualContainerHeader": True,
            "defaultDrillFilterOtherVisuals": True
        }
    }
    with open(os.path.join(rep_def_dir, "report.json"), "w", encoding="utf-8") as f:
        json.dump(report_json_content, f, indent=2)

    # pages.json
    pages_json_content = {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/pagesMetadata/1.0.0/schema.json",
        "pageOrder": ["page1"],
        "activePageName": "page1"
    }
    with open(os.path.join(pages_dir, "pages.json"), "w", encoding="utf-8") as f:
        json.dump(pages_json_content, f, indent=2)

    # page1/page.json
    page1_content = {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.0.0/schema.json",
        "name": "page1",
        "displayName": "01. Tổng Quan Thị Trường Steam",
        "displayOption": "FitToPage",
        "height": 720,
        "width": 1280
    }
    with open(os.path.join(page1_dir, "page.json"), "w", encoding="utf-8") as f:
        json.dump(page1_content, f, indent=2)

    # 4. TẠO CÁC VISUAL (Biểu đồ và KPI Cards)
    visuals = []

    # KPI 1: Total Games
    v_kpi1 = create_visual_json(
        name="kpi_total_games", x=15, y=15, width=235, height=100, z=1,
        visual_type="cardVisual",
        query_state={
            "Data": {"projections": [{
                "field": {"Measure": {"Expression": {"SourceRef": {"Entity": "_Key Measures"}}, "Property": "Total Games"}},
                "queryRef": "_Key Measures.Total Games", "nativeQueryRef": "Total Games"
            }]}
        },
        title_text="Tổng Số Tựa Game"
    )
    visuals.append(v_kpi1)

    # KPI 2: Total Revenue
    v_kpi2 = create_visual_json(
        name="kpi_total_revenue", x=265, y=15, width=240, height=100, z=2,
        visual_type="cardVisual",
        query_state={
            "Data": {"projections": [{
                "field": {"Measure": {"Expression": {"SourceRef": {"Entity": "_Key Measures"}}, "Property": "Total Estimated Revenue"}},
                "queryRef": "_Key Measures.Total Estimated Revenue", "nativeQueryRef": "Total Estimated Revenue"
            }]}
        },
        title_text="Tổng Doanh Thu Ước Tính"
    )
    visuals.append(v_kpi2)

    # KPI 3: Avg Game Price
    v_kpi3 = create_visual_json(
        name="kpi_avg_price", x=520, y=15, width=235, height=100, z=3,
        visual_type="cardVisual",
        query_state={
            "Data": {"projections": [{
                "field": {"Measure": {"Expression": {"SourceRef": {"Entity": "_Key Measures"}}, "Property": "Avg Game Price"}},
                "queryRef": "_Key Measures.Avg Game Price", "nativeQueryRef": "Avg Game Price"
            }]}
        },
        title_text="Giá Bán Trung Bình"
    )
    visuals.append(v_kpi3)

    # KPI 4: Satisfaction Rate
    v_kpi4 = create_visual_json(
        name="kpi_satisfaction", x=770, y=15, width=240, height=100, z=4,
        visual_type="cardVisual",
        query_state={
            "Data": {"projections": [{
                "field": {"Measure": {"Expression": {"SourceRef": {"Entity": "_Key Measures"}}, "Property": "Platform Satisfaction Rate"}},
                "queryRef": "_Key Measures.Platform Satisfaction Rate", "nativeQueryRef": "Platform Satisfaction Rate"
            }]}
        },
        title_text="Tỷ Lệ Đánh Giá Hài Lòng"
    )
    visuals.append(v_kpi4)

    # KPI 5: Vietnamese Games
    v_kpi5 = create_visual_json(
        name="kpi_vietnamese", x=1025, y=15, width=240, height=100, z=5,
        visual_type="cardVisual",
        query_state={
            "Data": {"projections": [{
                "field": {"Measure": {"Expression": {"SourceRef": {"Entity": "_Key Measures"}}, "Property": "Vietnamese Supported Games"}},
                "queryRef": "_Key Measures.Vietnamese Supported Games", "nativeQueryRef": "Vietnamese Supported Games"
            }]}
        },
        title_text="Game Có Tiếng Việt"
    )
    visuals.append(v_kpi5)

    # BIỂU ĐỒ 1: Clustered Bar Chart - Top 10 Thể loại theo Doanh thu
    v_bar_genres = create_visual_json(
        name="chart_top_genres", x=15, y=130, width=610, height=280, z=6,
        visual_type="clusteredBarChart",
        query_state={
            "Category": {"projections": [{
                "field": {"Column": {"Expression": {"SourceRef": {"Entity": "dim_genres"}}, "Property": "genre_name"}},
                "queryRef": "dim_genres.genre_name", "nativeQueryRef": "genre_name", "active": True
            }]},
            "Y": {"projections": [{
                "field": {"Measure": {"Expression": {"SourceRef": {"Entity": "_Key Measures"}}, "Property": "Total Estimated Revenue"}},
                "queryRef": "_Key Measures.Total Estimated Revenue", "nativeQueryRef": "Total Estimated Revenue"
            }]}
        },
        title_text="Top Thể Loại Đạt Doanh Thu Cao Nhất (USD)",
        sort_def={
            "sort": [{
                "field": {"Measure": {"Expression": {"SourceRef": {"Entity": "_Key Measures"}}, "Property": "Total Estimated Revenue"}},
                "direction": "Descending"
            }],
            "isDefaultSort": True
        }
    )
    visuals.append(v_bar_genres)

    # BIỂU ĐỒ 2: Clustered Column Chart - Tăng trưởng game phát hành theo Năm
    v_col_year = create_visual_json(
        name="chart_release_by_year", x=640, y=130, width=625, height=280, z=7,
        visual_type="clusteredColumnChart",
        query_state={
            "Category": {"projections": [{
                "field": {"Column": {"Expression": {"SourceRef": {"Entity": "dim_date"}}, "Property": "year"}},
                "queryRef": "dim_date.year", "nativeQueryRef": "year", "active": True
            }]},
            "Y": {"projections": [{
                "field": {"Measure": {"Expression": {"SourceRef": {"Entity": "_Key Measures"}}, "Property": "Total Games"}},
                "queryRef": "_Key Measures.Total Games", "nativeQueryRef": "Total Games"
            }]}
        },
        title_text="Xu Hướng Số Lượng Game Phát Hành Theo Năm",
        sort_def={
            "sort": [{
                "field": {"Column": {"Expression": {"SourceRef": {"Entity": "dim_date"}}, "Property": "year"}},
                "direction": "Ascending"
            }],
            "isDefaultSort": True
        }
    )
    visuals.append(v_col_year)

    # BIỂU ĐỒ 3: Donut Chart - Cơ cấu phân khúc giá
    v_donut_price = create_visual_json(
        name="chart_price_tier", x=15, y=425, width=440, height=280, z=8,
        visual_type="donutChart",
        query_state={
            "Category": {"projections": [{
                "field": {"Column": {"Expression": {"SourceRef": {"Entity": "dim_games"}}, "Property": "price_tier"}},
                "queryRef": "dim_games.price_tier", "nativeQueryRef": "price_tier", "active": True
            }]},
            "Y": {"projections": [{
                "field": {"Measure": {"Expression": {"SourceRef": {"Entity": "_Key Measures"}}, "Property": "Total Games"}},
                "queryRef": "_Key Measures.Total Games", "nativeQueryRef": "Total Games"
            }]}
        },
        title_text="Cơ Cấu Game Theo Phân Khúc Giá (Price Tiers)"
    )
    visuals.append(v_donut_price)

    # BIỂU ĐỒ 4: Clustered Bar Chart - Đánh giá người chơi (Review Score Tiers)
    v_bar_reviews = create_visual_json(
        name="chart_review_tiers", x=470, y=425, width=450, height=280, z=9,
        visual_type="clusteredBarChart",
        query_state={
            "Category": {"projections": [{
                "field": {"Column": {"Expression": {"SourceRef": {"Entity": "fact_game_metrics"}}, "Property": "review_score_tier"}},
                "queryRef": "fact_game_metrics.review_score_tier", "nativeQueryRef": "review_score_tier", "active": True
            }]},
            "Y": {"projections": [{
                "field": {"Measure": {"Expression": {"SourceRef": {"Entity": "_Key Measures"}}, "Property": "Total Games"}},
                "queryRef": "_Key Measures.Total Games", "nativeQueryRef": "Total Games"
            }]}
        },
        title_text="Phân Bổ Tầng Đánh Giá Người Chơi (Valve Tiers)",
        sort_def={
            "sort": [{
                "field": {"Measure": {"Expression": {"SourceRef": {"Entity": "_Key Measures"}}, "Property": "Total Games"}},
                "direction": "Descending"
            }],
            "isDefaultSort": True
        }
    )
    visuals.append(v_bar_reviews)

    # SLICER: Bộ lọc theo Hệ điều hành & Năm
    v_slicer_os = create_visual_json(
        name="slicer_platform", x=935, y=425, width=330, height=280, z=10,
        visual_type="slicer",
        query_state={
            "Values": {"projections": [{
                "field": {"Column": {"Expression": {"SourceRef": {"Entity": "dim_games"}}, "Property": "platform_support"}},
                "queryRef": "dim_games.platform_support", "nativeQueryRef": "platform_support"
            }]}
        },
        title_text="Bộ Lọc Hệ Điều Hành (OS Filter)"
    )
    visuals.append(v_slicer_os)

    # Lưu tất cả các visual files
    for v in visuals:
        v_path = os.path.join(visuals_dir, f"{v['name']}.json")
        with open(v_path, "w", encoding="utf-8") as f:
            json.dump(v, f, indent=2)
        print(f"   [OK] Visual tạo thành công: {v['name']:25s} ({v['visual']['visualType']})")

    print("=" * 80)
    print(f"HOÀN THÀNH: Đã tạo xong toàn bộ Dashboard trong: {pbip_file}")
    print("=" * 80)


if __name__ == "__main__":
    build_steam_pbip()
