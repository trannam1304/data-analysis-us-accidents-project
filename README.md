# Phân tích Điểm đen Tai nạn Giao thông Đô thị với Python

Dự án phân tích tai nạn giao thông đô thị dựa trên bộ dữ liệu **US Accidents (2016–2023)** với vai trò là chuyên viên phân tích dữ liệu của Sở Giao thông vận tải. Bộ dữ liệu gốc chứa hơn 7.7 triệu bản ghi tai nạn, bao gồm thông tin chi tiết về thời gian, địa điểm, mức độ nghiêm trọng (Severity), điều kiện thời tiết và đặc điểm hạ tầng giao thông (đèn tín hiệu, nút giao, lối qua đường...).

- **Nguồn dữ liệu gốc:** [Kaggle - US Accidents (2016 - 2023)](https://www.kaggle.com/datasets/sobhanmoosavi/us-accidents)

---

## 🎯 Mục tiêu phân tích của dự án

Dự án tập trung giải quyết các bài toán trọng tâm:
1. **Phân tích không gian:** Khu vực, thành phố, tuyến đường nào có mật độ tai nạn cao nhất (Top điểm đen cần ưu tiên can thiệp)?
2. **Phân tích thời gian:** Khung giờ cao điểm, ngày trong tuần, tháng hoặc mùa nào ghi nhận tỷ lệ tai nạn cao nhất?
3. **Phân tích điều kiện môi trường:** Mức độ nghiêm trọng của tai nạn thay đổi như thế nào theo thời tiết (mưa bão, sương mù, tầm nhìn thấp)?
4. **Phân tích hạ tầng:** Các yếu tố đường bộ (giao lộ, đèn tín hiệu, vạch qua đường, đường sắt...) liên quan thế nào đến tai nạn nghiêm trọng?
5. **Mô hình hóa dự báo (Machine Learning):** Dự đoán mức độ nghiêm trọng của tai nạn và đề xuất giải pháp cảnh báo sớm.

---

## ⚠️ QUY ĐỊNH BẮT BUỘC VỀ DỮ LIỆU & GIT (DATA POLICY)

> [!CAUTION]
> **TUYỆT ĐỐI KHÔNG COMMIT HOẶC PUSH CÁC FILE DỮ LIỆU CÓ DUNG LƯỢNG LỚN LÊN GITHUB!**
> - File dữ liệu thô (`US_Accidents_March23.csv`) có dung lượng lên đến **~3GB - 8GB**, vượt xa giới hạn 100MB của GitHub.
> - Nếu vô tình commit file nặng, lệnh `git push` sẽ bị **GitHub chặn (pre-receive hook declined)** và làm hỏng lịch sử commit của cả nhóm.
> - Toàn bộ các file trong thư mục `data/raw/` và các file `data/*.csv` đã được cấu hình loại trừ trong file [`.gitignore`](file:///.gitignore).

Vì vậy, **mỗi thành viên sau khi clone repo về máy CẦN TỰ CHẠY notebook `01_data_cleaning.ipynb`** theo hướng dẫn bên dưới để tự sinh ra bộ dữ liệu sạch trong thư mục `data/` trên máy cá nhân trước khi thực hiện nhiệm vụ của mình.

---

## 📁 Cấu trúc thư mục dự án

```text
data-analysis-us-accidents-project/
├── data/
│   ├── raw/                       # Chứa file CSV thô tải từ Kaggle (được .gitignore bảo vệ)
│   │   └── .gitkeep
│   ├── accidents_clean_2y.csv    # Dữ liệu 2 năm gần nhất sau khi làm sạch (tự sinh ra)
│   ├── train.csv                  # Tập huấn luyện 80% (tự sinh ra)
│   ├── test.csv                   # Tập kiểm thử 20% (tự sinh ra)
│   └── .gitkeep
├── docs/                          # Tài liệu báo cáo, thuyết minh đề tài
├── notebooks/
│   ├── 01_data_cleaning.ipynb     # Tiền xử lý, làm sạch, feature engineering, train/test split
│   ├── 02_descriptive_diagnostic.ipynb  # Phân tích mô tả & chẩn đoán (EDA)
│   ├── 03_predictive_modeling.ipynb     # Xây dựng mô hình học máy dự báo
│   └── 04_prescriptive_analysis.ipynb   # Đề xuất giải pháp & khuyến nghị chính sách
├── src/
│   └── download_data.py           # Script hỗ trợ tải và kiểm tra dữ liệu
├── .gitignore                     # Cấu hình bỏ qua file dữ liệu nặng, môi trường ảo
├── README.md                      # Hướng dẫn dự án & Onboarding cho thành viên
└── requirements.txt               # Danh sách thư viện Python bắt buộc
```

---

## 🚀 HƯỚNG DẪN CHI TIẾT TỪNG BƯỚC CHO THÀNH VIÊN NHÓM (ONBOARDING GUIDE)

Khi được phân công làm việc trên dự án, mỗi thành viên thực hiện tuần tự các bước sau:

### Bước 1: Clone Repository & Tạo nhánh làm việc cá nhân

Mở terminal (PowerShell / Command Prompt / Git Bash) và chạy các lệnh:

```bash
# 1. Clone dự án về máy
git clone https://github.com/trannam1304/data-analysis-us-accidents-project.git

# 2. Di chuyển vào thư mục dự án
cd data-analysis-us-accidents-project

# 3. Tạo và chuyển sang nhánh riêng của bạn (Quy ước: member/<ten-mssv>)
# Ví dụ:
git checkout -b member/hoang-52400191
```

---

### Bước 2: Thiết lập môi trường Python ảo & Cài đặt thư viện

Sử dụng **Python 3.10 trở lên** để đảm bảo tương thích:

```bash
# 1. Tạo môi trường ảo .venv
python -m venv .venv

# 2. Kích hoạt môi trường ảo:
# Trên Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# (Nếu gặp lỗi Execution Policy trên PowerShell, chạy: Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass)

# Hoặc trên Windows Command Prompt (cmd):
.\.venv\Scripts\activate.bat

# Hoặc trên macOS / Linux / Git Bash:
source .venv/bin/activate

# 3. Cập nhật pip và cài đặt thư viện từ requirements.txt
pip install --upgrade pip
pip install -r requirements.txt
```

---

### Bước 3: Chuẩn bị dữ liệu thô (2 Phương án linh hoạt)

Bạn có thể lựa chọn 1 trong 2 cách sau tùy vào điều kiện mạng:

#### 👉 Cách A (Tự động tải qua KaggleHub - Khuyến nghị nếu mạng ổn định):
- Bạn không cần làm gì thêm ở bước này. Khi chạy notebook `01_data_cleaning.ipynb`, thư viện `kagglehub` sẽ tự động tải dữ liệu về máy.
- Hoặc bạn có thể chạy script terminal kiểm tra trước:
  ```bash
  python src/download_data.py
  ```

#### 👉 Cách B (Tải thủ công từ Web - Dùng khi mạng lag, timeout hoặc không có Kaggle API token):
1. Truy cập trực tiếp link Kaggle: [https://www.kaggle.com/datasets/sobhanmoosavi/us-accidents](https://www.kaggle.com/datasets/sobhanmoosavi/us-accidents)
2. Nhấn nút **Download** (khoảng 650 MB file zip).
3. Giải nén file vừa tải, bạn sẽ được file `US_Accidents_March23.csv`.
4. Copy file `US_Accidents_March23.csv` vào thư mục:
   ```text
   data-analysis-us-accidents-project/data/raw/
   ```
5. Notebook `01_data_cleaning.ipynb` đã được lập trình để **ưu tiên nhận diện file CSV trong `data/raw/` trước**, giúp bạn bỏ qua bước tải trên mạng và chạy ngay lập tức!

---

### Bước 4: Chạy toàn bộ file tiền xử lý (`01_data_cleaning.ipynb`)

1. Mở dự án trong **VS Code** hoặc **JupyterLab**.
2. Mở file [notebooks/01_data_cleaning.ipynb](file:///d:/PTTQH-DL/data-analysis-us-accidents-project/notebooks/01_data_cleaning.ipynb).
3. **Quan trọng:** Chọn **Kernel** là môi trường ảo `.venv` vừa tạo (hoặc môi trường Python đã cài `requirements.txt`).
4. Nhấn **Run All** (Chạy toàn bộ các cell).
5. Quá trình xử lý sẽ thực hiện tuần tự:
   - **Nạp dữ liệu:** Tự động đọc file từ `data/raw/` hoặc tải qua `kagglehub`.
   - **Lọc dữ liệu:** Sử dụng logic động lấy đúng **2 năm gần nhất** (`Start_Time.max() - 2 năm`).
   - **Giải phóng RAM:** Tự động xóa `df_raw` khỏi bộ nhớ để máy 8GB RAM không bị quá tải.
   - **Xử lý Missing Data:** Áp dụng chiến lược phân tầng (Tiered Strategy: Loại cột thiếu >40%, Impute median/mode cho cột 5-40%, Drop dòng thiếu <5%).
   - **Feature Engineering:** Tạo các cột thời gian (`Hour`, `DayOfWeek`, `Month`, `Season`), thời tiết (`Weather_Group`, `Visibility_Level`, `Temp_Level`, `Is_Adverse_Weather`), đặc trưng boolean POI.
   - **Time-Series Split:** Chia tập train (80%) và test (20%) theo trình tự thời gian nghiêm ngặt, đảm bảo không rò rỉ dữ liệu (data leakage).
   - **Xuất file:** Lưu kết quả trực tiếp vào thư mục `data/` của dự án.

---

### Bước 5: Kiểm tra kết quả trong thư mục `data/`

Sau khi chạy xong notebook, kiểm tra thư mục `data/` trên máy bạn. Thư mục phải có đủ 3 file:

| File | Số dòng (ước tính) | Mô tả & Mục đích |
|---|---|---|
| `data/accidents_clean_2y.csv` | ~2.97 triệu | Toàn bộ dữ liệu sạch 2 năm gần nhất (dùng cho EDA, Thống kê mô tả, Dashboard) |
| `data/train.csv` | ~2.37 triệu (80%) | Dữ liệu huấn luyện theo chuỗi thời gian (dùng cho Modeling) |
| `data/test.csv` | ~594 nghìn (20%) | Dữ liệu kiểm thử theo chuỗi thời gian (dùng để đánh giá Model) |

---

### Bước 6: Bắt đầu thực hiện nhiệm vụ theo phân công

Khi thư mục `data/` đã có dữ liệu, các thành viên bắt đầu làm nhiệm vụ trên nhánh của mình:

- **Thành viên 2 (Descriptive & Diagnostic EDA - `02_descriptive_diagnostic.ipynb`):**
  ```python
  import pandas as pd
  from pathlib import Path
  # Đọc dữ liệu sạch
  df = pd.read_csv("../data/accidents_clean_2y.csv")
  ```
- **Thành viên 3 (Prescriptive Analysis & Dashboard - `04_prescriptive_analysis.ipynb` / `dashboard/`):**
  ```python
  import pandas as pd
  df = pd.read_csv("../data/accidents_clean_2y.csv")
  ```
- **Thành viên 4 (Predictive Modeling - `03_predictive_modeling.ipynb`):**
  ```python
  import pandas as pd
  # Đọc train và test riêng biệt
  train_df = pd.read_csv("../data/train.csv")
  test_df  = pd.read_csv("../data/test.csv")
  ```

---

## 🛠️ QUY TẮC LÀM VIỆC VỚI GIT CỦA NHÓM

1. **Trước khi commit code:**
   - Luôn chạy lệnh kiểm tra trạng thái:
     ```bash
     git status
     ```
   - **Kiểm tra kỹ:** Danh sách file chuẩn bị commit TUYỆT ĐỐI KHÔNG chứa file đuôi `.csv`, `.zip`, `.parquet` trong thư mục `data/`.
2. **Clear Output các Notebook nếu file quá nặng:**
   - Trong VS Code / Jupyter, chọn **Clear All Outputs** trước khi commit notebook để tránh file `.ipynb` phình to dung lượng.
3. **Commit & Push lên nhánh riêng:**
   ```bash
   git add notebooks/02_descriptive_diagnostic.ipynb
   git commit -m "feat(eda): hoan thanh phan tich diem den theo khung gio va thoi tiet"
   git push origin member/<ten-mssv>
   ```
4. **Tạo Pull Request:**
   - Lên GitHub tạo Pull Request từ nhánh `member/...` vào nhánh `main`.
   - Báo Leader review và merge code.

---

## ❓ XỬ LÝ SỰ CỐ THƯỜNG GẶP (TROUBLESHOOTING)

### 1. Lỗi `ModuleNotFoundError: No module named 'kagglehub'` (hoặc `pandas`)
- **Nguyên nhân:** Chưa kích hoạt môi trường ảo `.venv` hoặc chưa cài `requirements.txt`.
- **Khắc phục:**
  ```bash
  .\.venv\Scripts\Activate.ps1
  pip install -r requirements.txt
  ```
  Trong notebook, hãy nhấn vào góc trên bên phải để chọn đúng Kernel của `.venv`.

### 2. Lỗi mạng khi KaggleHub đang tải dữ liệu (Timeout / ConnectionReset / HTTP Error)
- **Nguyên nhân:** File nén Kaggle nặng ~650MB, đường truyền quốc tế chập chờn có thể gây ngắt kết nối giữa chừng.
- **Khắc phục:** Áp dụng ngay **Cách B ở Bước 3**: Tải file trực tiếp từ trình duyệt web tại [Kaggle US Accidents](https://www.kaggle.com/datasets/sobhanmoosavi/us-accidents), giải nén rồi đưa file `US_Accidents_March23.csv` vào thư mục `data/raw/`. Sau đó chạy lại cell 4.

### 3. Lỗi `MemoryError` hoặc Kernel bị tắt đột ngột (Kernel Died / OOM)
- **Nguyên nhân:** Đọc 7.7 triệu dòng chiếm nhiều RAM.
- **Khắc phục:**
  - Notebook đã được cập nhật lệnh tự động dọn rác RAM (`del df_raw; gc.collect()`).
  - Đóng bớt các ứng dụng nặng (trình duyệt, game, phần mềm đồ họa) trước khi nhấn Run All.
  - Nếu máy chỉ có 4GB - 8GB RAM, hãy tăng dung lượng Virtual Memory (Paging File) trên Windows lên 8GB - 16GB.

### 4. Chạy xong nhưng không thấy file trong thư mục `data/` của dự án
- **Nguyên nhân:** Trước đây code dùng `Path("../data")` nên khi chạy từ thư mục gốc, file bị lưu nhầm ra ngoài project.
- **Khắc phục:** Code Cell 18 đã được chuẩn hóa tự động phát hiện đường dẫn gốc dự án. File sẽ luôn xuất hiện chính xác tại `<project_root>/data/`.
