import os
from models import db, User, LoginLog
from utils import sha256_hash, triple_des_encrypt, generate_salt
from sqlalchemy.exc import IntegrityError

def register_user(username, password):
    if User.query.filter_by(username=username).first():
        return "Tên đăng nhập đã tồn tại."

    salt = generate_salt()
    password_hash = sha256_hash(password + salt)
    username_hash = sha256_hash(username)
    combined_hash = sha256_hash(username_hash + password_hash)
    encrypted_password = triple_des_encrypt(combined_hash)

    user = User(
        username=username,
        username_hash=username_hash,
        password_encrypted=encrypted_password,
        salt=salt,
        fail_count=0,
        is_locked=False,
    )
    try:
        db.session.add(user)
        db.session.commit()
        return "Đăng ký thành công."
    except IntegrityError:
        db.session.rollback()
        return "Lỗi: không thể lưu tài khoản."

def login_user(username, password, ip_address):
    user = User.query.filter_by(username=username).first()
    if not user:
        return "Tài khoản không tồn tại.", False

    if user.is_locked:
        return "Tài khoản bị khóa. Vui lòng liên hệ quản trị viên.", False

    password_hash = sha256_hash(password + user.salt)
    username_hash = sha256_hash(username)
    combined_hash = sha256_hash(username_hash + password_hash)
    encrypted_input = triple_des_encrypt(combined_hash)

    if encrypted_input == user.password_encrypted:
        user.fail_count = 0
        db.session.commit()
        log = LoginLog(username_hash=user.username_hash, ip_address=ip_address, success=True)
        db.session.add(log)
        db.session.commit()
        return "Đăng nhập thành công.", True
    else:
        user.fail_count += 1
        log = LoginLog(username_hash=user.username_hash, ip_address=ip_address, success=False)
        db.session.add(log)

        if user.fail_count >= 5:
            user.is_locked = True

        db.session.commit()
        attempts_left = max(0, 5 - user.fail_count)
        return f"Sai mật khẩu. Bạn còn {attempts_left} lần thử.", False

def change_password(username, old_password, new_password):
    user = User.query.filter_by(username=username).first()
    if not user:
        return "Tài khoản không tồn tại."

    old_hash = sha256_hash(old_password + user.salt)
    username_hash = sha256_hash(username)
    combined_hash = sha256_hash(username_hash + old_hash)
    encrypted_old = triple_des_encrypt(combined_hash)

    if encrypted_old != user.password_encrypted:
        return "Mật khẩu cũ không đúng."

    new_salt = generate_salt()
    new_hash = sha256_hash(new_password + new_salt)
    new_combined = sha256_hash(username_hash + new_hash)
    encrypted_new = triple_des_encrypt(new_combined)

    user.password_encrypted = encrypted_new
    user.salt = new_salt
    user.fail_count = 0
    user.is_locked = False

    db.session.commit()
    return "Đổi mật khẩu thành công."
