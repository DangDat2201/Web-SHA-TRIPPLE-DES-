# Sơ đồ thư mục dự án
```
📁 BTL-ATBM/
│
├── app.py                   # Điểm khởi động Flask app
├── .env                     # Biến môi trường (DB, SECRET_KEY, ...)
├── requirements.txt         # Các thư viện cần cài
│
├── models.py                # Định nghĩa bảng User & LoginLog
├── utils.py                 # Xử lý SHA, salt, Triple DES
├── auth.py                  # Xử lý logic: đăng ký, đăng nhập, đổi mật khẩu
│
├── templates/               # Giao diện HTML
│   ├── layout.html
│   ├── index.html
│   ├── register.html
│   ├── login.html
│   ├── change_password.html
│   └── admin.html
│
└── static/                  # CSS, JS, ảnh (nếu có)
```
# Nội dung CSDL
```
-- Tạo CSDL
CREATE DATABASE FlaskAuth;
GO
USE FlaskAuth;

-- Bảng người dùng
CREATE TABLE NguoiDung (
    id INT IDENTITY(1,1) PRIMARY KEY,
    username_hash VARCHAR(64) NOT NULL UNIQUE,
    password_encrypted VARCHAR(256) NOT NULL,
    salt VARCHAR(32) NOT NULL,
    fail_count INT DEFAULT 0,
    is_locked BIT DEFAULT 0,
    is_admin BIT DEFAULT 0
);

-- Bảng lịch sử đăng nhập
CREATE TABLE LichSuDangNhap (
    id INT IDENTITY(1,1) PRIMARY KEY,
    username_hash VARCHAR(64),
    ip_address VARCHAR(45),
    success BIT,
    timestamp DATETIME DEFAULT GETDATE()
);
```
# Lệnh truy vấn
## Hiển thị tất cả người dùng
```
SELECT * FROM User;
```
## Hiển thị các tài khoản bị khóa
```
SELECT username, is_locked, fail_count 
FROM User 
WHERE is_locked = 1;
```
## Xem lịch sử đăng nhập gần nhất
```
SELECT TOP 50 * 
FROM LoginLog 
ORDER BY timestamp DESC;
```
# Nội dung file .env
```
DB_SERVER=localhost\SQLEXPRESS
DB_NAME=FlaskAuth
DB_DRIVER=ODBC Driver 17 for SQL Server
USE_WINDOWS_AUTH=True
SECRET_KEY=Hello World
ADMIN_ACCESS_KEY=admin1
```
# Cách chạy
## Lệnh cấp phép tạm thời
```
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
```
## Tạo/Kích hoạt môi trường ảo
```
python -m venv venv
.\venv\Scripts\activate
```
## Tải thư viện
```
pip install -r requirements.txt
```
## Chạy dự án
```
python app.py
```
