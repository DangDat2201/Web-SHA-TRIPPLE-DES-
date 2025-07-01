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
# Hình ảnh minh hoạ 
## Trang chủ 
![image](https://github.com/user-attachments/assets/ef27d84e-ad59-4e14-bf9a-7b1f13a9dd8d)

## Đăng ký
![image](https://github.com/user-attachments/assets/9b3b7b15-1078-4114-a614-255a2127e649)

## Đăng ký thành công 
![image](https://github.com/user-attachments/assets/7e9c1de7-af8d-450f-8dd7-70133931a30b)

## Đăng ký thất bại 
![image](https://github.com/user-attachments/assets/a91ef4a8-6661-4fcc-972b-dc44bdb8aa92)

## Đăng nhập
![image](https://github.com/user-attachments/assets/28ff0892-707c-444f-bb65-171a511fccbb)

## Đăng nhập thành công 
![image](https://github.com/user-attachments/assets/f30e8816-11e5-4fd1-8aee-b6a19eb64abc)

## Đăng nhập thất bại
![image](https://github.com/user-attachments/assets/8bf70224-706d-4210-a7ed-786f10032d76)

## Đăng nhập bị khoá tài khoản 
![image](https://github.com/user-attachments/assets/3ed4ffbe-3969-440d-bc28-f9dce1b7f2bb)

## Đổi mật khẩu 
![image](https://github.com/user-attachments/assets/989197c0-69a6-4233-b497-f5afa13f03f7)

## Đổi mật khẩu thành công 
![image](https://github.com/user-attachments/assets/6a138501-21ba-40c8-a81b-7ca714cad102)

## Đổi mật khẩu thất bại 
![image](https://github.com/user-attachments/assets/70ec0466-f4a1-4166-8c35-e2442eec5e36)

# Quản trị 
## Bình thường 
![image](https://github.com/user-attachments/assets/dc169fcc-85b2-4305-8192-216f05f507bd)

## Có tài khoản bị khoá 
![image](https://github.com/user-attachments/assets/3f4a825e-2400-401b-bcb2-64cebcb43a1b)












