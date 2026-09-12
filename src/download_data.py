"""
Script hỗ trợ tải hoặc kiểm tra dữ liệu US Accidents (2016-2023) từ Kaggle.
Sử dụng cho toàn bộ thành viên trong nhóm.
"""

import os
import sys
from pathlib import Path

# Đảm bảo in tiếng Việt mượt mà trên Windows console (tránh lỗi charmap cp1252)
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Xác định project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"

def check_local_dataset():
    """Kiểm tra xem dataset đã có sẵn tại máy cục bộ hay chưa."""
    search_dirs = [RAW_DIR, DATA_DIR]
    for d in search_dirs:
        if d.exists():
            csv_files = [f for f in d.glob("*.csv") if "accident" in f.name.lower() or "us" in f.name.lower()]
            if csv_files:
                largest_csv = max(csv_files, key=lambda p: p.stat().st_size)
                print(f"[OK] Da tim thay du lieu tho tai: {largest_csv}")
                print(f"     Dung luong: {largest_csv.stat().st_size / (1024 * 1024):.2f} MB")
                return largest_csv
    return None

def download_via_kagglehub():
    """Tự động tải dataset từ Kaggle bằng thư viện kagglehub."""
    try:
        import kagglehub
    except ImportError:
        print("[LOI] Chua cai dat thu vien 'kagglehub'. Hay chay: pip install kagglehub")
        sys.exit(1)

    print("[BAT DAU] Dang tai dataset tu Kaggle ('sobhanmoosavi/us-accidents')...")
    print("          Qua trinh nay co the mat tu 5 - 15 phut tuy toc do mang.")
    try:
        path = kagglehub.dataset_download("sobhanmoosavi/us-accidents")
        print(f"[HOAN TAT] Dataset da duoc tai ve cache tai: {path}")
        return path
    except Exception as e:
        print(f"\n[LOI] Tai du lieu that bai: {e}")
        print("\n" + "="*70)
        print("HUONG DAN DU PHONG TAI THU CONG CHO THANH VIEN:")
        print("1. Dang nhap Kaggle va truy cap: https://www.kaggle.com/datasets/sobhanmoosavi/us-accidents")
        print("2. Nhan 'Download' de tai file zip ve may.")
        print("3. Giai nen file 'US_Accidents_March23.csv'.")
        print(f"4. Dat file CSV vua giai nen vao thu muc: {RAW_DIR}")
        print("="*70)
        return None

def main():
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    existing = check_local_dataset()
    if existing:
        print("\n-> Ban da co san du lieu, co the chay thang notebook 01_data_cleaning.ipynb!")
        return

    print("[THONG BAO] Chua co du lieu tai local. Bat dau tai qua KaggleHub...")
    download_via_kagglehub()

if __name__ == "__main__":
    main()
