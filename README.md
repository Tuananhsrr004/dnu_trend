# 🎓 DNU Major Trends - Hệ thống Phân tích và Dự báo Xu hướng Chọn ngành

## Giới thiệu

DNU Major Trends là hệ thống phân tích và dự báo xu hướng chọn ngành nghề tại **Đại học Đại Nam**. Hệ thống sử dụng công nghệ AI và Machine Learning để giúp sinh viên và nhà quản lý đưa ra quyết định đúng đắn về ngành học.

## ✨ Tính năng chính

### Cho Sinh viên:
- 📊 **Dashboard Thống kê**: Xem xu hướng chọn ngành qua các năm với biểu đồ trực quan
- 📈 **Dự báo Xu hướng**: Dự đoán số lượng sinh viên chọn ngành trong 5 năm tới bằng AI
- 💬 **Chatbot Tư vấn**: AI chatbot giúp tư vấn ngành học phù hợp dựa trên sở thích và năng lực
- 🔍 **So sánh Ngành**: So sánh nhiều ngành với nhau để đưa ra lựa chọn tốt nhất

### Cho Quản trị viên:
- 📤 **Upload Dữ liệu**: Import dữ liệu từ file CSV/Excel
- 📑 **Báo cáo Chi tiết**: Tạo báo cáo tổng quan và xuất dưới dạng Excel/PDF
- 📊 **Phân tích Sâu**: Xem thống kê chi tiết theo giới tính, khu vực, điểm chuẩn
- 🎯 **Insights**: Xác định ngành HOT và ngành có xu hướng tăng trưởng

## 🚀 Cài đặt và Chạy

### Yêu cầu:
- Python 3.10+

### Các bước:

1. **Cài đặt dependencies:**
```bash
pip install -r requirements.txt
```

2. **Chạy ứng dụng:**
```bash
python app.py
```

3. **Truy cập:**
- URL: `http://localhost:5000`
- Username: `admin`
- Password: `admin`

---

**Developed with ❤️ for Đại học Đại Nam**

Phân tích và dự báo xu hướng chọn ngành tại Đại học Đại Nam.

## Tính năng chính
- Upload dữ liệu CSV/Excel → lưu SQLite
- Dashboard phân tích xu hướng, phân bố giới tính/khu vực, heatmap độ hot ngành
- Dự báo 3–5 năm bằng Prophet (nếu cài đặt), fallback Linear Regression/ARIMA
- Xuất báo cáo Excel/PDF
- Đăng nhập quản trị (mặc định: admin/admin)

## Cài đặt (Windows PowerShell)
```powershell
# tạo môi trường ảo (khuyến nghị)
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r dnu_major_trends\requirements.txt
```

## Chạy ứng dụng
```powershell
$env:FLASK_APP = "dnu_major_trends/app.py"; python dnu_major_trends/app.py
```
Mở http://localhost:5000 và đăng nhập bằng admin/admin.

## Tạo dữ liệu mẫu (tùy chọn)
```powershell
python dnu_major_trends/seed_data.py
```

## Định dạng dữ liệu
CSV/Excel yêu cầu các cột: `year, major, students, male, female, region, avg_score`.

Ví dụ CSV:
```
year,major,students,male,female,region,avg_score
2023,Công nghệ thông tin,200,120,80,Bắc,23.5
2023,Công nghệ thông tin,150,90,60,Trung,23.2
```

## API chính
- GET /api/overview
- GET /api/majors
- GET /api/trend?major=...
- GET /api/gender?major=...
- GET /api/region?major=...
- GET /api/heatmap
- GET /api/forecast?major=...&years=5
- GET /api/forecast/summary
- GET /export/excel, GET /export/pdf

## Celery + Beat (tự động cập nhật dự báo)
Yêu cầu Redis đang chạy ở `redis://localhost:6379/0` (có thể sửa trong `config.py` hoặc biến môi trường `CELERY_BROKER_URL`).

Chạy worker và beat trên Windows PowerShell (2 cửa sổ riêng):
```powershell
# Cửa sổ 1: worker
Set-Location 'd:\CDS NTA\dnu_major_trends'
celery -A celery_app.celery worker --loglevel=info

# Cửa sổ 2: beat (lên lịch mỗi ngày 02:00)
celery -A celery_app.celery beat --loglevel=info
```
Bạn cũng có thể chạy thủ công nhiệm vụ trong Python REPL:
```powershell
python - <<'PY'
from celery_app import update_all_forecasts
update_all_forecasts.delay()
PY
```

## Lưu ý Prophet
Prophet có thời gian cài đặt lâu và yêu cầu build. Nếu không cài được, hệ thống sẽ tự động dùng Linear Regression hoặc ARIMA làm dự phòng.

## Bảo mật
- Thay đổi SECRET_KEY trong biến môi trường khi triển khai thật.
- Đổi mật khẩu tài khoản admin mặc định sau khi chạy lần đầu.
