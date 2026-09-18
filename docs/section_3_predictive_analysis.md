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

## 2. Tiền xử lý & Trích xuất Đặc trưng Nâng cao (Feature Pipeline & Engineering)

### 2.1 Khám phá Mẫu Vi mô & Trích xuất Đặc trưng Phái sinh
Dựa trên phân tích tương quan và trực quan hóa phân phối, nhóm nghiên cứu đã triển khai **3 bước phân tích sâu** trước khi đưa dữ liệu vào mô hình:

1. **Phân tích Xu hướng Rủi ro theo Khung giờ (Hourly Risk Trend)**:
   - Tỷ lệ tai nạn nghiêm trọng tăng cao đột biến vào 2 mốc chính: **Giờ cao điểm giao thông** (7h-9h & 16h-18h) do mật độ xe cao, và **Ban đêm muộn** (22h-5h) do chạy quá tốc độ và mệt mỏi/sương mù.
   - *Đặc trưng phái sinh*: `Is_Rush_Hour` (Giờ cao điểm), `Is_Night` (Ban đêm).
2. **Phân tích Mức độ Rủi ro theo Hạ tầng POI (POI Risk Level)**:
   - Khảo sát các điểm xung đột luồng giao thông (`Junction`, `Railway`, `Crossing`, `Traffic_Signal`). 
   - *Đặc trưng phái sinh*: `POI_Count` (Tổng số mốc giao cắt hạ tầng tại điểm xảy ra tai nạn).

### 2.2 Pipeline Tiền xử lý tự động hóa (Scikit-Learn ColumnTransformer)

1. **Nhóm đặc trưng định lượng (Numerical Features)**: 
   - `Hour`, `Month`, `Temperature(F)`, `Humidity(%)`, `Pressure(in)`, `Visibility(mi)`, `Wind_Speed(mph)`, `Precipitation(in)`, `Start_Lat`, `Start_Lng`, và `POI_Count`.
   - *Xử lý*: Điền giá trị thiếu bằng trung vị (`SimpleImputer(strategy='median')`) và chuẩn hóa z-score (`StandardScaler`).
2. **Nhóm đặc trưng định tính (Categorical Features)**:
   - `Weather_Group` (7 nhóm lớn), `Visibility_Level`, `Temp_Level`, `Season`, `DayOfWeek`, `State`.
   - *Xử lý*: Điền yếu tố xuất hiện nhiều nhất (`SimpleImputer(strategy='most_frequent')`) và mã hóa biến giả (`OneHotEncoder(handle_unknown='ignore')`).
3. **Nhóm đặc trưng hạ tầng đường bộ POI & Thời tiết xấu (Boolean Features)**:
   - `Amenity`, `Crossing`, `Junction`, `Railway`, `Stop`, `Traffic_Signal`, `Is_Daytime`, `Is_Precipitation`, `Is_Adverse_Weather`, `Is_Low_Visibility`, `Is_Rush_Hour`, `Is_Night`.
   - *Xử lý*: Ép kiểu về `int` (0/1) để đảm bảo tính toán ổn định.

---

## 3. Huấn luyện & So sánh Hiệu năng Mô hình

Để đáp ứng yêu cầu của đề tài, 2 thuật toán đã được triển khai và so sánh:
1. **Baseline Model — Logistic Regression**: Mô hình học tuyến tính cơ bản, có tích hợp `class_weight='balanced'` để bù đắp mất cân bằng lớp.
2. **Advanced Model — XGBoost Classifier**: Mô hình Gradient Boosting dựa trên cây quyết định nâng cao, sử dụng `scale_pos_weight` tối ưu cho dữ liệu imbalanced.

### 3.1 Bảng Kết quả So sánh Hiệu năng trên Tập Test (594,578 mẫu)

| Mô hình | Accuracy | Precision (High Sev) | Recall (High Sev) | F1-Score (High Sev) | F1-Macro | ROC-AUC Score |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Baseline (Logistic Regression)** | **60.86%** | 4.70% | **70.54%** | 0.0881 | **0.4195** | 0.6767 |
| **Advanced (XGBoost Classifier)** | 58.30% | **4.76%** | **76.50%** | **0.0896** | 0.4096 | **0.7068** |

### 3.2 Nhận xét Hiệu năng
- **Mô hình XGBoost (Advanced)** đạt chỉ số **ROC-AUC (0.7068)** cao hơn rõ rệt so với Baseline (0.6767), chứng tỏ khả năng học mối quan hệ phi tuyến phức tạp giữa thời tiết và hạ tầng đường bộ tốt hơn.
- **Khả năng bắt tai nạn nghiêm trọng (Recall)**: XGBoost đạt mức **Recall cao vượt trội tới 76.50%** (so với 70.54% của Logistic Regression). Trong bài toán cảnh báo giao thông đô thị, chỉ số Recall giữ vai trò quan trọng nhất vì giúp Sở GTVT **bắt trúng hơn 3/4 số vụ tai nạn nghiêm trọng** để triển khai lực lượng ứng cứu khẩn cấp kịp thời.

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
