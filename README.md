# 🎓 DNU Major Trends - Hệ thống Phân tích và Dự báo Xu hướng Chọn ngành

## 📚 Chuyển đổi số trong Giáo dục là gì?

### Khái niệm Chuyển đổi số (Digital Transformation)

Chuyển đổi số là quá trình ứng dụng công nghệ số vào mọi hoạt động của tổ chức nhằm tạo ra giá trị mới, cải thiện hiệu quả và nâng cao trải nghiệm người dùng. Trong lĩnh vực giáo dục đại học, chuyển đổi số không chỉ là việc số hóa tài liệu hay sử dụng phần mềm quản lý, mà còn là việc **tái cấu trúc toàn bộ quy trình** từ tuyển sinh, đào tạo, đến tư vấn nghề nghiệp.

### Tại sao Giáo dục cần Chuyển đổi số?

#### 1. **Dữ liệu lớn và Phân tích thông minh**
- Mỗi năm, hàng nghìn sinh viên đăng ký vào các ngành học khác nhau
- Dữ liệu về xu hướng chọn ngành, giới tính, khu vực, điểm số tạo thành "Big Data"
- Phân tích thủ công không còn hiệu quả → Cần AI và Machine Learning

#### 2. **Ra quyết định dựa trên bằng chứng (Evidence-based Decision Making)**
- Thay vì dựa vào cảm tính, nhà quản lý cần số liệu cụ thể
- Dự báo xu hướng giúp lập kế hoạch tuyển sinh, phân bổ nguồn lực
- Sinh viên được tư vấn ngành học phù hợp dựa trên dữ liệu thực tế

#### 3. **Cá nhân hóa trải nghiệm**
- Mỗi sinh viên có sở thích, năng lực khác nhau
- Chatbot AI có thể tư vấn 24/7 dựa trên profile cá nhân
- Hệ thống gợi ý ngành học thông minh thay cho tư vấn truyền thống

#### 4. **Minh bạch và Dễ tiếp cận**
- Thông tin về xu hướng ngành, tỷ lệ nam/nữ, khu vực được hiển thị rõ ràng
- Dashboard trực quan giúp mọi người dễ hiểu
- Export báo cáo Excel/PDF để chia sẻ với phụ huynh, giáo viên

### Chuyển đổi số tại Đại học Đại Nam

Đại học Đại Nam nhận thấy nhu cầu cấp thiết trong việc **hiểu rõ xu hướng chọn ngành** của sinh viên qua các năm. Những câu hỏi cần giải đáp:

- Ngành nào đang được sinh viên ưa chuộng nhất?
- Xu hướng chọn ngành thay đổi như thế nào theo thời gian?
- Có sự khác biệt giữa nam và nữ sinh viên không?
- Khu vực nào có nhiều sinh viên chọn ngành công nghệ?
- Làm thế nào để dự báo số lượng sinh viên trong 3-5 năm tới?

Từ những câu hỏi này, **DNU Major Trends** ra đời như một giải pháp chuyển đổi số toàn diện.

---

## 🎯 Giới thiệu Hệ thống

**DNU Major Trends** là hệ thống phân tích và dự báo xu hướng chọn ngành nghề tại **Đại học Đại Nam**, được xây dựng dựa trên nền tảng công nghệ hiện đại:

- **Backend**: Flask (Python) - Framework web nhẹ, linh hoạt
- **Database**: SQLite - Lưu trữ dữ liệu lịch sử và dự báo
- **AI/ML**: Prophet, scikit-learn - Dự báo xu hướng và phân tích
- **Frontend**: Bootstrap 5, Chart.js - Giao diện thân thiện, biểu đồ tương tác
- **Task Queue**: Celery + Redis - Tự động cập nhật dự báo định kỳ

Hệ thống giúp **sinh viên, phụ huynh và nhà quản lý** đưa ra quyết định thông minh về việc chọn ngành học, dựa trên dữ liệu thực tế và dự báo khoa học.

---

## ✨ Tính năng chính

### Cho Sinh viên và Phụ huynh:

#### 📊 **Dashboard Thống kê Trực quan**
- Xem xu hướng chọn ngành qua 5 năm (2020-2024) với biểu đồ đường/cột
- Phân tích phân bố theo **giới tính** (Nam/Nữ) cho từng ngành
- Xem biểu đồ **Heatmap** để nhanh chóng nhận biết ngành "HOT"
- Thống kê theo **khu vực** (Miền Bắc, Trung, Nam)
- Dữ liệu được cập nhật tự động từ database

**Ví dụ**: Sinh viên có thể thấy rằng ngành **Công nghệ thông tin** tăng trưởng 89% từ 2020-2024, trong khi **Quản trị kinh doanh** tăng ổn định 47%.

#### 📈 **Dự báo Xu hướng bằng AI**
- Dự đoán số lượng sinh viên chọn ngành trong **1-10 năm tới**
- Sử dụng thuật toán Prophet (Facebook) hoặc Linear Regression/ARIMA
- Hiển thị biểu đồ dự báo với khoảng tin cậy (confidence interval)
- Tự động cập nhật dự báo mỗi ngày lúc 02:00 sáng (Celery Beat)

**Ví dụ**: Hệ thống dự báo ngành **Khoa học dữ liệu** sẽ có 1,200 sinh viên vào năm 2026, tăng 30% so với 2024.

#### 💬 **Chatbot Tư vấn Thông minh**
- AI chatbot sử dụng **TF-IDF + Cosine Similarity** để hiểu câu hỏi
- Tư vấn ngành học phù hợp dựa trên:
  - Sở thích (lập trình, kinh doanh, y tế...)
  - Năng lực (toán, văn, ngoại ngữ...)
  - Giới tính và khu vực
- Trả lời các câu hỏi như:
  - "Ngành nào phù hợp với nam sinh viên thích công nghệ?"
  - "Ngành nào đang HOT nhất?"
  - "So sánh Công nghệ thông tin và Khoa học dữ liệu"

Xem mã nguồn chatbot tại [services/chatbot.py](services/chatbot.py).

#### 🔍 **So sánh Ngành**
- Chọn nhiều ngành để so sánh cùng lúc
- Biểu đồ radar hiển thị điểm mạnh/yếu của từng ngành
- So sánh số lượng sinh viên, tỷ lệ nam/nữ, điểm chuẩn trung bình

---

### Cho Quản trị viên (Admin):

#### 📤 **Upload Dữ liệu CSV/Excel**
- Import dữ liệu từ file CSV hoặc Excel
- Hỗ trợ **UTF-8 có dấu tiếng Việt**
- Tự động validate định dạng: `year, major, students, male, female, region, avg_score`
- Cập nhật hoặc thêm mới dữ liệu tự động
- Xử lý file tối đa 10MB

Xem hướng dẫn upload tại [templates/upload.html](templates/upload.html).

**Dữ liệu mẫu**:
- [sample_data/du_lieu_chon_nganh_2020_2024.csv](sample_data/du_lieu_chon_nganh_2020_2024.csv) - Dữ liệu 5 năm, 210 bản ghi
- [sample_data/du_lieu_2023_chi_tiet.csv](sample_data/du_lieu_2023_chi_tiet.csv) - Dữ liệu chi tiết 2023, 60 bản ghi

#### 📑 **Báo cáo Chi tiết**
- Xuất báo cáo tổng quan dưới dạng **Excel (.xlsx)**
- Xuất báo cáo dưới dạng **PDF** (kèm biểu đồ)
- Báo cáo bao gồm:
  - Thống kê tổng quan (tổng sinh viên, số ngành, xu hướng)
  - Bảng chi tiết theo năm, ngành, khu vực
  - Top 5 ngành hot nhất
  - Dự báo 5 năm tới

Xem trang báo cáo tại [templates/report.html](templates/report.html).

#### 📊 **Phân tích Sâu**
- Dashboard admin với nhiều biểu đồ tương tác
- Phân tích theo **giới tính**: Ngành nào nữ sinh viên ưa chuộng?
- Phân tích theo **khu vực**: Khu vực nào chọn ngành công nghệ nhiều nhất?
- Phân tích **điểm chuẩn**: Ngành nào có điểm chuẩn cao nhất?
- Heatmap độ "HOT" của ngành theo năm

#### 🎯 **Insights và Khuyến nghị**
- Tự động xác định ngành **HOT** (tăng trưởng > 50% trong 3 năm)
- Ngành có xu hướng **tăng trưởng** hoặc **suy giảm**
- Khuyến nghị về việc mở ngành mới hoặc điều chỉnh chỉ tiêu tuyển sinh

---

## 🚀 Cài đặt và Chạy

### Yêu cầu Hệ thống:
- **Python 3.10+** (khuyến nghị 3.11)
- **Redis** (tùy chọn, cho Celery)
- Hệ điều hành: Windows, macOS, Linux

### Bước 1: Clone hoặc tải project
```bash
git clone <repository-url>
cd dnu_major_trends
