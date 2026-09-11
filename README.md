# US Accidents Analysis & Prediction Project

## 📋 Mục lục

1. [Giới thiệu dự án](#1-giới-thiệu-dự-án)
2. [Cấu trúc thư mục dự án](#2-cấu-trúc-thư-mục-dự-án)
3. [Yêu cầu hệ thống & Cài đặt](#3-yêu-cầu-hệ-thống--cài-đặt)
4. [Cách chạy dự án](#4-cách-chạy-dự-án)
5. [Chi tiết quy trình Tiền xử lý dữ liệu](#5-chi-tiết-quy-trình-tiền-xử-lý-dữ-liệu)
6. [Giải thích định dạng dữ liệu đầu ra](#6-giải-thích-định-dạng-dữ-liệu-đầu-ra)
7. [Kiểm tra sau khi chạy](#7-kiểm-tra-sau-khi-chạy)
8. [Luồng dữ liệu (Data Pipeline Flow)](#8-luồng-dữ-liệu-data-pipeline-flow)
9. [Lưu ý khi làm việc nhóm (Git & Version Control)](#9-lưu-ý-khi-làm-việc-nhóm-git--version-control)
10. [Phân công thành viên](#10-phân-công-thành-viên)
11. [Liên hệ & Đóng góp](#11-liên-hệ--đóng-góp)

---

## 1. Giới thiệu dự án

Dự án này thực hiện **quy trình khoa học dữ liệu hoàn chỉnh** trên bộ dữ liệu
**US Accidents** (cung cấp bởi Sobhan Moosavi trên Kaggle — [link dataset](https://www.kaggle.com/datasets/sobhanmoosavi/us-accidents)).

### 🎯 Mục tiêu chính

- **Tiền xử lý dữ liệu:** Lọc, làm sạch, xử lý missing values trên ~7.7 triệu bản ghi.
- **Trích xuất đặc trưng:** Tạo đặc trưng thời gian và thời tiết phục vụ phân tích.
- **Phân tích khám phá (EDA):** Tìm hiểu quy luật, xu hướng, yếu tố ảnh hưởng tai nạn.
- **Dashboard BI:** Xây dựng dashboard trực quan hóa dữ liệu tai nạn đô thị.
- **Mô hình hóa ML:** Huấn luyện mô hình dự đoán mức độ nghiêm trọng tai nạn.

### 📌 Bối cảnh nghiệp vụ

Bộ dữ liệu US Accidents ghi lại các vụ tai nạn giao thông trên toàn nước Mỹ
(49 bang) từ **tháng 2/2016 đến tháng 3/2023**. Dự án tập trung vào bài toán
**"Phân tích điểm đen tai nạn giao thông đô thị"** — nhằm hỗ trợ Sở GTVT xác định
các vị trí nguy hiểm và đề xuất giải pháp cải thiện an toàn giao thông.

---

## 2. Cấu trúc thư mục dự án

```
repo/
└── data-analysis-us-accidents/         # Thư mục gốc dự án
    ├── dashboard/                      # Mã nguồn / cấu hình Dashboard BI
    │
    ├── data/                           # Dữ liệu (tự động tạo khi chạy notebook)
    │   ├── .gitkeep                    # Giữ cấu trúc thư mục trên Git
    │   ├── accidents_clean_2y.csv      # Dữ liệu sạch toàn bộ (cho EDA / BI)
    │   ├── train.csv                   # 80% dữ liệu quá khứ (train model)
    │   └── test.csv                    # 20% dữ liệu tương lai (test model)
    │
    ├── docs/                           # Tài liệu báo cáo, tài nguyên dự án
    │
    ├── notebooks/                      # Chứa các notebook Jupyter
    │   └── 01_data_cleaning.ipynb      # Notebook chính xử lý và làm sạch dữ liệu
    │
    ├── .gitignore                      # Bỏ qua file dữ liệu thô và file nặng
    ├── README.md                       # Tài liệu hướng dẫn dự án (file này)
    └── requirements.txt                # Danh sách thư viện Python cần thiết
```

> **Lưu ý:** Nếu notebook nằm ở thư mục khác, cần điều chỉnh đường dẫn tương ứng
> thành `../data` để ghi file CSV đúng vị trí.

---

## 3. Yêu cầu hệ thống & Cài đặt

### 📌 Yêu cầu hệ thống

| Thành phần | Phiên bản tối thiểu | Ghi chú |
|---|---|---|
| Python | 3.10+ | Bắt buộc (dùng cú pháp mới) |
| RAM | 8 GB | 16 GB khuyến nghị để xử lý ~7.7 triệu dòng |
| Ổ cứng trống | ~10 GB | Chứa dataset raw + 3 file CSV đầu ra |
| Môi trường | Jupyter Notebook / VS Code | Có hỗ trợ kernel Python |

### 📦 Cài đặt thư viện

Chạy lệnh sau trong Terminal tại thư mục gốc dự án:

```bash
pip install pandas numpy kagglehub jupyter
```

Hoặc cài từ file `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 🔑 Cấu hình Kaggle API (nếu cần)

`kagglehub` thường tải dataset không cần API key. Nếu gặp lỗi xác thực:

1. Truy cập [kaggle.com/settings](https://www.kaggle.com/settings) → **Create New Token**.
2. Tải file `kaggle.json` về máy.
3. Đặt file vào:
   - **Windows:** `C:\Users\<username>\.kaggle\kaggle.json`
   - **Linux/macOS:** `~/.kaggle/kaggle.json`

---

## 4. Cách chạy dự án

### 🅰️ Cách 1: Sử dụng Jupyter Notebook

1. Mở Terminal tại thư mục gốc dự án.
2. Khởi động Jupyter:
   ```bash
   jupyter notebook
   ```
3. Mở thư mục `notebooks/` → chọn file `01_data_cleaning.ipynb`.
4. Chọn Python Kernel phù hợp (góc trên bên phải).
5. Bấm **Kernel → Restart Kernel and Run All Cells** để chạy tuần tự từ đầu.
6. Kiểm tra kết quả sinh ra trong thư mục `data/`.

### 🅱️ Cách 2: Sử dụng VS Code

1. Mở thư mục dự án bằng VS Code.
2. Mở file `notebooks/01_data_cleaning.ipynb`.
3. Chọn Python Kernel phù hợp (góc trên bên phải).
4. Bấm **Run All** để thực thi toàn bộ các cell.
5. Kiểm tra kết quả trong thư mục `data/`.

> ⚠️ **Quan trọng:** Luôn chạy **tuần tự từ cell đầu tiên** — vì các cell sau phụ
> thuộc vào biến và dữ liệu được tạo ở cell trước. Không chạy từng cell rời rạc
> sẽ gây lỗi `NameError`.

---

## 5. Chi tiết quy trình Tiền xử lý dữ liệu

Notebook `01_data_cleaning.ipynb` thực hiện **7 bước tuần tự** sau:

### 5.1. Tải dữ liệu tự động từ Kaggle

Dữ liệu thô được tải trực tiếp qua thư viện `kagglehub`:

```python
import kagglehub
dataset_path = kagglehub.dataset_download("sobhanmoosavi/us-accidents")
```

- Không cần tải file CSV thủ công.
- Không cần commit file CSV lớn vào Git.
- Tự động cache tại `~/.cache/kagglehub/` cho lần chạy sau.

**Kết quả:** `df_raw` có shape `(7,728,394, 24)`.

### 5.2. Lọc dữ liệu 2 năm gần nhất (Dynamic Date Logic)

Thay vì hard-code năm, notebook **neo vào mốc thời gian mới nhất trong dataset**:

```python
latest_date = df_raw["Start_Time"].max()
cutoff_date = latest_date - pd.DateOffset(years=2)
df_recent   = df_raw[df_raw["Start_Time"] >= cutoff_date]
```

**Ưu điểm:**
- Luôn lấy đúng 2 năm gần nhất, không phụ thuộc thời điểm chạy.
- **Tái lập được (reproducible)** — chạy lúc nào cũng cho cùng output.
- Tự động thích nghi nếu Kaggle cập nhật dataset mới.

**Kết quả:** `df_recent` có shape `(3,174,360, 24)` — chiếm 41.1% dữ liệu gốc.

### 5.3. Xử lý giá trị bị thiếu (Tiered Strategy)

Dựa trên tỷ lệ missing của từng cột, áp dụng **3 tầng chiến lược**:

| Tỷ lệ thiếu | Chiến lược | Lý do |
|---|---|---|
| **> 40%** | Xóa toàn bộ cột | Quá nhiều thông tin mất, impute sẽ gây nhiễu |
| **5% – 40%** | Impute (median cho số, mode cho phân loại) | Đủ dữ liệu để ước lượng hợp lý |
| **< 5%** | Xóa dòng chứa missing | Tỉ lệ nhỏ, không ảnh hưởng kích thước mẫu |

**Kết quả:** `df_clean` không còn giá trị missing nào.

### 5.4. Feature Engineering — Đặc trưng thời gian (Mục 5.1)

Trích xuất từ cột `Start_Time` **5 đặc trưng thời gian**:

| Đặc trưng | Mô tả | Giá trị |
|---|---|---|
| `Hour` | Giờ xảy ra tai nạn | 0 → 23 |
| `DayOfWeek` | Thứ trong tuần | Monday → Sunday |
| `Month` | Tháng trong năm | 1 → 12 |
| `Year` | Năm | 2021, 2022, 2023 |
| `Season` | Mùa (chuẩn khí tượng) | Winter / Spring / Summer / Fall |

**Quy tắc chia mùa:** 12-1-2 = Winter, 3-4-5 = Spring, 6-7-8 = Summer, 9-10-11 = Fall.

### 5.5. Feature Engineering — Đặc trưng thời tiết (Mục 5.2)

Tạo **7 đặc trưng phái sinh** từ dữ liệu thời tiết:

| Đặc trưng | Mô tả | Giá trị |
|---|---|---|
| `Is_Precipitation` | Có mưa/tuyết | True / False |
| `Weather_Group` | Nhóm thời tiết (gom 101 → 7 nhóm) | Clear / Cloudy / Rain / Snow / Fog / Storm / Other |
| `Visibility_Level` | Mức tầm nhìn | Very_Low / Low / Medium / High |
| `Temp_Level` | Mức nhiệt độ | Freezing / Cold / Mild / Hot |
| `Is_Adverse_Weather` | Thời tiết xấu | True / False |
| `Is_Low_Visibility` | Tầm nhìn < 1 dặm | True / False |
| `Is_Daytime` | Ban ngày | True / False |

**Ngoài ra:** Giữ nguyên và ép kiểu `bool` cho **13 cột POI** (Junction,
Traffic_Signal, Crossing, Railway...).

### 5.6. Chia tách tập dữ liệu (Time-Series Split)

Dữ liệu được **sắp xếp theo thời gian** rồi chia theo tỷ lệ **80/20**:

| Tập | Tỉ lệ | Thời gian | Kích thước |
|---|---|---|---|
| **Train** | 80% | 2021-03-31 → 2022-10-04 | ~2,378,000 dòng |
| **Test** | 20% | 2022-10-04 → 2023-03-31 | ~594,000 dòng |

**⚠️ Lý do KHÔNG dùng Random Split:**

Đây là **dữ liệu chuỗi thời gian**. Nếu chia ngẫu nhiên, các bản ghi tương lai có
thể lọt vào tập train → gây **rò rỉ dữ liệu (data leakage)** → mô hình đánh giá
quá lạc quan, không phản ánh đúng khả năng dự báo thực tế.

**✅ Cách làm đúng:** Cắt tại một mốc thời gian — train là quá khứ, test là tương lai.

### 5.7. Xuất dữ liệu đã làm sạch

Notebook ghi ra **3 file CSV** trong thư mục `../data/`:

| File | Kích thước | Mục đích |
|---|---|---|
| `accidents_clean_2y.csv` | ~590 MB | Cho Member 3 (EDA / BI / Dashboard) |
| `train.csv` | ~474 MB | Cho Member 4 (huấn luyện model) |
| `test.csv` | ~118 MB | Cho Member 4 (đánh giá model) |

---

## 6. Giải thích định dạng dữ liệu đầu ra

**Vì sao dùng CSV thay vì TXT?**

| Tiêu chí | CSV | TXT |
|---|---|---|
| Đọc trực tiếp bằng pandas | ✅ `pd.read_csv()` | ❌ Phải tự parse |
| Tương thích Excel / Power BI / Tableau | ✅ Có | ❌ Không |
| Giữ cấu trúc hàng / cột | ✅ Có | ❌ Văn bản thuần |
| Đưa trực tiếp vào mô hình ML | ✅ Có | ❌ Phải tiền xử lý |
| Chia sẻ và cộng tác nhóm | ✅ Dễ | ⚠️ Khó |

**→ Kết luận:** CSV là lựa chọn tối ưu cho dự án dữ liệu dạng bảng.

---

## 7. Kiểm tra sau khi chạy

Cuối notebook sẽ kiểm tra sự tồn tại của 3 file đầu ra và in ra shape:

```text
===== KIỂM TRA FILE ĐẦU RA =====
[OK] accidents_clean_2y.csv
     Kích thước: 591.69 MB
     Shape: (2972890, 37)
[OK] train.csv
     Kích thước: 473.92 MB
     Shape: (2378312, 37)
[OK] test.csv
     Kích thước: 117.78 MB
     Shape: (594578, 37)

Tổng số ô còn thiếu trong CLEANING: 0
[OK] Dữ liệu cleaning không còn giá trị thiếu.
```

Nếu thấy cả 3 dòng `[OK]` → pipeline hoàn tất thành công.

---

## 8. Luồng dữ liệu (Data Pipeline Flow)

```
┌──────────────────────────────────────────────┐
│   Kaggle US Accidents Dataset (~7.7M dòng)   │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
        ┌─────────────────────────────────┐
        │  01_data_cleaning.ipynb         │
        │  (Tiền xử lý + Trích xuất)      │
        └──────────────┬──────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
 ┌────────────┐ ┌────────────┐ ┌────────────┐
 │  clean_2y  │ │   train    │ │    test    │
 │    .csv    │ │    .csv    │ │    .csv    │
 └─────┬──────┘ └─────┬──────┘ └─────┬──────┘
       │              │              │
       ▼              ▼              ▼
 ┌────────────┐ ┌────────────┐ ┌────────────┐
 │ Member 3   │ │ Member 4   │ │ Member 4   │
 │ EDA / BI   │ │ Train ML   │ │ Evaluate   │
 └────────────┘ └────────────┘ └────────────┘
```

---

## 9. Lưu ý khi làm việc nhóm (Git & Version Control)

### 🚫 KHÔNG commit dữ liệu thô / dữ liệu lớn

Các file CSV có dung lượng rất lớn (~1.2 GB tổng), nếu đưa lên Git sẽ làm
**phình to repository** và gây **chậm cho các thành viên khác khi clone**.

### ✅ Cấu hình `.gitignore`

Thêm các dòng sau vào file `.gitignore` ở gốc repository:

```text
# Dữ liệu thô và dữ liệu đã xử lý dung lượng lớn
data/raw/*
data/*.csv
!data/.gitkeep

# Jupyter checkpoints
.ipynb_checkpoints/

# Python cache
__pycache__/
*.pyc
```

### 🔄 Khi thành viên khác clone project về

Không cần copy file CSV nặng thủ công. Chỉ cần:

1. Cài đặt môi trường (mục 3).
2. Mở notebook `01_data_cleaning.ipynb`.
3. Bấm **Run All** — notebook sẽ tự tải dataset qua `kagglehub` và tạo lại 3 file CSV.

### ⚠️ Nguyên tắc vàng

- **Không chỉnh sửa file CSV bằng Excel thủ công.** Mọi thay đổi dữ liệu phải
  xuất phát từ việc chạy lại notebook → đảm bảo **tính tái lập (reproducibility)**.
- **Luôn chạy `Restart Kernel and Run All`** trước khi commit notebook — tránh
  lưu lại output lỗi hoặc không đồng bộ.
- **Commit thường xuyên** với message rõ ràng (theo chuẩn Conventional Commits).

---

## 10. Phân công thành viên

| # | Thành viên | Vai trò | Notebook / Sản phẩm |
|---|---|---|---|
| 1 | (Tên + MSSV) | Project Lead / Business Analyst | Điều phối, viết báo cáo tổng hợp |
| 2 | **Nguyễn Trọng Quý (52400230)** | **Data Engineer** | `01_data_cleaning.ipynb`, phần (1) & (2) báo cáo |
| 3 | (Tên + MSSV) | Data Analyst / Visualization | `02_descriptive_diagnostic.ipynb`, biểu đồ EDA |
| 4 | (Tên + MSSV) | Data Scientist / ML Engineer | `03_predictive_modeling.ipynb`, mô hình ML |
| 5 | (Tên + MSSV) | BI Developer / Prescriptive | `04_prescriptive_analysis.ipynb`, dashboard |

### 📌 Chi tiết nhiệm vụ Member 2 (Data Engineer)

- Lọc bộ dữ liệu US Accidents lấy **2 năm gần nhất** theo yêu cầu Sở GTVT.
- Xử lý missing values, chuẩn hóa định dạng datetime.
- Trích xuất đặc trưng thời gian (Hour, DayOfWeek, Month, Season) và thời tiết.
- Chia tập train/test theo phương pháp **time-series split** (không random).
- Xuất 3 file CSV sạch cho các thành viên khác sử dụng.
- Viết phần **(1) Giới thiệu** và **(2) Dữ liệu** trong báo cáo Word.

---

## 11. Liên hệ & Đóng góp

- **Repository:** `data-analysis-us-accidents`
- **Branch chính:** `main`
- **Branch cá nhân:** `member/<tên>-<MSSV>` (ví dụ: `member/quy-52400230`)
- **Quy trình làm việc:**
  1. Tạo branch cá nhân từ `main`.
  2. Commit thường xuyên với message rõ ràng.
  3. Tạo Pull Request khi hoàn thành.
  4. Review code trước khi merge.

---

**📅 Cập nhật lần cuối:** *(ngày/tháng/năm)*  
**📚 Môn học:** Phân tích và Trực quan hóa Dữ liệu  
**🏫 Trường:** *(tên trường)*