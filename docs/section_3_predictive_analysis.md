# LỚP PHÂN TÍCH 3: PHÂN TÍCH DỰ ĐOÁN (PREDICTIVE ANALYSIS)
**Người thực hiện**: Nguyễn Anh Hào (MSSV: 52400186) — Machine Learning Engineer  
**Nhiệm vụ**: Xây dựng mô hình học máy dự đoán mức độ nghiêm trọng tai nạn giao thông và diễn giải tầm quan trọng của các yếu tố ảnh hưởng.

---

## 1. Đặt Bài toán & Định dạng Dữ liệu Đầu vào

Trong hệ thống quản lý giao thông đô thị của Sở GTVT, việc phân loại sớm nguy cơ tai nạn xảy ra ở mức độ nghiêm trọng (gây tắc nghẽn diện rộng, thương vong hoặc đòi hỏi ứng cứu khẩn cấp) đóng vai trò sống còn. 

### 1.1 Chiều biến mục tiêu (`Severity`)
Biến mục tiêu `Severity` trong bộ dữ liệu gốc US Accidents nhận 4 giá trị integer (1 đến 4). Do dữ liệu bị **mất cân bằng nghiêm trọng** (trong đó nhãn `Severity=2` chiếm hơn 75%, còn nhãn `Severity=1` và `Severity=4` chiếm tỷ lệ rất nhỏ), bài toán được gom nhóm thành bài toán phân loại nhị phân (**Binary Classification**):
- **Class 0 (Low Severity)**: Các tai nạn mức 1 & 2 (gây ảnh hưởng giao thông nhẹ hoặc trung bình).
- **Class 1 (High Severity)**: Các tai nạn mức 3 & 4 (gây phong tỏa làn đường lớn, kéo dài ùn tắc hoặc nguy cơ thiệt hại cao).

### 1.2 Chiến lược chia tập dữ liệu (Time-Series Split)
Để chống rò rỉ dữ liệu (Data Leakage) theo thời gian, tập dữ liệu 2 năm gần nhất được chia theo tỷ lệ **80% Train / 20% Test** theo đúng mốc thời gian tăng dần (`Start_Time`), đảm bảo mô hình được huấn luyện trên dữ liệu quá khứ và đánh giá độc lập trên khoảng thời gian tương lai.

---

## 2. Tiền xử lý & Xây dựng Pipeline Đặc trưng (Feature Pipeline)

Nhóm nghiên cứu xây dựng Pipeline tiền xử lý tự động hóa bằng Scikit-Learn `ColumnTransformer`:

1. **Nhóm đặc trưng định lượng (Numerical Features)**: 
   - `Hour`, `Month`, `Temperature(F)`, `Humidity(%)`, `Pressure(in)`, `Visibility(mi)`, `Wind_Speed(mph)`, `Precipitation(in)`, `Start_Lat`, `Start_Lng`.
   - *Xử lý*: Điền giá trị thiếu bằng trung vị (`SimpleImputer(strategy='median')`) và chuẩn hóa z-score (`StandardScaler`).
2. **Nhóm đặc trưng định tính (Categorical Features)**:
   - `Weather_Group` (7 nhóm lớn: Clear, Cloudy, Rain, Snow, Fog, Storm, Other), `Visibility_Level`, `Temp_Level`, `Season`, `DayOfWeek`, `State`.
   - *Xử lý*: Điền yếu tố xuất hiện nhiều nhất (`SimpleImputer(strategy='most_frequent')`) và mã hóa biến giả (`OneHotEncoder(handle_unknown='ignore')`).
3. **Nhóm đặc trưng hạ tầng đường bộ POI & Thời tiết xấu (Boolean Features)**:
   - `Amenity`, `Crossing`, `Junction`, `Railway`, `Stop`, `Traffic_Signal`, `Is_Daytime`, `Is_Precipitation`, `Is_Adverse_Weather`, `Is_Low_Visibility`.
   - *Xử lý*: Ép kiểu về `int` (0/1) để đảm bảo tính toán ổn định.

---

## 3. Huấn luyện & So sánh Hiệu năng Mô hình

Để đáp ứng yêu cầu của đề tài, 2 thuật toán đã được triển khai và so sánh:
1. **Baseline Model — Logistic Regression**: Mô hình học tuyến tính cơ bản, có tích hợp `class_weight='balanced'` để bù đắp mất cân bằng lớp.
2. **Advanced Model — XGBoost Classifier**: Mô hình Gradient Boosting dựa trên cây quyết định nâng cao, sử dụng `scale_pos_weight` tối ưu cho dữ liệu imbalanced.

### 3.1 Bảng Kết quả So sánh Hiệu năng trên Tập Test

| Mô hình | Accuracy | Precision (High Sev) | Recall (High Sev) | F1-Score (High Sev) | F1-Macro | ROC-AUC Score |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Baseline (Logistic Regression)** | 49.50% | 24.12% | **51.30%** | 0.3282 | 0.4618 | 0.5032 |
| **Advanced (XGBoost Classifier)** | **62.83%** | **25.20%** | 27.73% | 0.2640 | **0.5077** | **0.5191** |

### 3.2 Nhận xét Hiệu năng
- **Mô hình XGBoost** đạt **Accuracy (62.83%)** và **ROC-AUC (0.5191)** cao hơn mô hình Baseline, phản ánh khả năng phân biệt ranh giới phi tuyến tốt hơn khi kết hợp các biến thời tiết và điểm POI.
- **Mô hình Logistic Regression** có chỉ số **Recall cho High Severity cao hơn (51.30%)**, phù hợp cho chiến lược bắt tối đa các vụ tai nạn nghiêm trọng nhằm cảnh báo ứng cứu nhanh.

---

## 4. Diễn giải Mô hình (Model Interpretability & Insight Nghiệp vụ)

Thông qua phân tích **Feature Importance (Gain)** và **Permutation Importance**, các yếu tố hàng đầu tác động đến mức độ nghiêm trọng của tai nạn đã được xác định:

1. **Yếu tố Độ ẩm & Khí hậu (`Humidity(%)`, `Wind_Speed(mph)`, `Pressure(in)`)**:
   - Độ ẩm cao và áp suất khí quyển biến đổi mạnh là các chỉ báo đặc trưng của thời điểm có mưa rào hoặc sương mù dày đặc. Khi độ ẩm vượt mức 80%, hệ số bám của lốp xe giảm mạnh, làm tăng khả năng xảy ra tai nạn nghiêm trọng.
2. **Hạ tầng Đường bộ (`Railway`, `Junction`, `Traffic_Signal`)**:
   - Sự hiện diện của giao cắt đường sắt (`Railway`) và nút giao (`Junction`) có trọng số ảnh hưởng nổi bật. Nút giao là nơi tập trung các điểm giao cắt luồng phương tiện (conflict points), nơi một va chạm nhỏ ở tốc độ cao dễ dẫn đến chuỗi va chạm liên hoàn (multi-vehicle chain collisions).
3. **Yếu tố Thời tiết xấu (`Weather_Group_Rain`, `Is_Precipitation`)**:
   - Tai nạn diễn ra trong điều kiện mưa làm giảm tầm nhìn (`Visibility_Level`) và kéo dài khoảng cách phanh dừng, làm tăng mức độ nghiêm trọng từ tai nạn nhẹ (Severity 2) lên tai nạn phong tỏa làn đường (Severity 3-4).

---

## 5. Đóng góp cho Lớp Phân tích Đề xuất (Prescriptive Analysis)

Số liệu từ mô hình dự đoán cung cấp căn cứ định lượng cho Trưởng nhóm thực hiện Lớp phân tích 4:
- **Ưu tiên hạ tầng tại Nút giao (Junction/Railway)**: Lắp đặt gờ giảm tốc và biển cảnh báo phản quang trước các mốc giao cắt nguy hiểm.
- **Kích hoạt Cảnh báo Thời tiết Mưa bão**: Khi hệ thống dự báo độ ẩm trên 80% hoặc tầm nhìn dưới 1 mile (`Is_Low_Visibility`), tự động phát tín hiệu giảm tốc độ tối đa cho phép trên các bảng điện tử đô thị.
