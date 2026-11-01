"""
=============================================================================
Module: 01_download_data.py
Mục đích: Tự động tải bộ dữ liệu Steam Games Dataset từ KaggleHub
Tác giả: Data Analyst Team
Ngày tạo: 2026-11-01
=============================================================================
Quy trình:
1. Sử dụng thư viện `kagglehub` để tải phiên bản mới nhất từ:
   https://www.kaggle.com/datasets/artermiloff/steam-games-dataset
2. Xác định thư mục cache lưu trữ của KaggleHub.
3. Sao chép (copy) file dữ liệu chuẩn hóa thô `games_march2025_cleaned.csv`
   vào thư mục dự án cục bộ: `data/raw/`.
4. Ghi log kiểm tra kích thước và tính toàn vẹn của tệp đã tải.
=============================================================================
"""

import os
import shutil
import kagglehub


def download_steam_dataset(target_dir: str = "data/raw") -> str:
    """
    Tải bộ dữ liệu Steam Games Dataset và lưu vào thư mục `data/raw`.

    Parameters:
    -----------
    target_dir : str
        Đường dẫn thư mục đích lưu trữ dữ liệu thô (mặc định: 'data/raw').

    Returns:
    --------
    str : Đường dẫn tuyệt đối đến tệp dữ liệu thô đã tải và sao chép.
    """
    print("=" * 70)
    print("BẮT ĐẦU: Tải bộ dữ liệu Steam Games từ KaggleHub...")
    print("=" * 70)

    # 1. Gọi KaggleHub API để tải bộ dữ liệu
    dataset_name = "artermiloff/steam-games-dataset"
    download_path = kagglehub.dataset_download(dataset_name)
    print(f"-> Dữ liệu tải về tại cache: {download_path}")

    # 2. Đảm bảo thư mục data/raw tồn tại
    os.makedirs(target_dir, exist_ok=True)

    # 3. Tệp dữ liệu chính cần sử dụng (phiên bản mới nhất Tháng 3/2025 đã lọc app rác)
    target_filename = "games_march2025_cleaned.csv"
    src_file_path = os.path.join(download_path, target_filename)

    # Nếu không tìm thấy file cleaned, thử lấy file full hoặc file bất kỳ
    if not os.path.exists(src_file_path):
        print(f"[Cảnh báo] Không tìm thấy '{target_filename}'. Đang quét thư mục cache...")
        csv_files = [f for f in os.listdir(download_path) if f.endswith(".csv")]
        if not csv_files:
            raise FileNotFoundError("Không tìm thấy tệp CSV nào trong thư mục tải về!")
        # Ưu tiên march2025_cleaned -> march2025_full -> tệp đầu tiên
        selected_file = "games_march2025_cleaned.csv" if "games_march2025_cleaned.csv" in csv_files else csv_files[0]
        src_file_path = os.path.join(download_path, selected_file)

    dst_file_path = os.path.join(target_dir, os.path.basename(src_file_path))

    # 4. Sao chép tệp vào thư mục data/raw của dự án
    print(f"-> Đang sao chép '{src_file_path}' vào '{dst_file_path}'...")
    shutil.copy2(src_file_path, dst_file_path)

    # 5. Kiểm tra kích thước tệp sau khi sao chép
    file_size_mb = os.path.getsize(dst_file_path) / (1024 * 1024)
    print(f"-> Sao chép hoàn tất! Kích thước tệp: {file_size_mb:.2f} MB")
    print("=" * 70)
    print("HOÀN THÀNH: Tải và thiết lập dữ liệu thô thành công.")
    print("=" * 70)

    return dst_file_path


if __name__ == "__main__":
    download_steam_dataset()
