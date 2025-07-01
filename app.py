from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from auth import register_user, login_user, change_password
from models import db, User, LoginLog
from dotenv import load_dotenv
from urllib.parse import quote_plus
import os

# Load .env configs
load_dotenv()

app = Flask(__name__)
db = SQLAlchemy() # Khởi tạo đối tượng SQLAlchemy

if os.getenv("USE_WINDOWS_AUTH") == "True":
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"mssql+pyodbc://@{os.getenv('DB_SERVER')}/{os.getenv('DB_NAME')}?"
        f"driver={quote_plus(os.getenv('DB_DRIVER'))}&trusted_connection=yes"
    )
else:
    username = os.getenv("DB_USER")
    password = quote_plus(os.getenv("DB_PASSWORD"))  # tránh lỗi ký tự đặc biệt trong password
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"mssql+pyodbc://{username}:{password}@{os.getenv('DB_SERVER')}/"
        f"{os.getenv('DB_NAME')}?driver={quote_plus(os.getenv('DB_DRIVER'))}"
    )

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        message = register_user(username, password)
        return render_template('register.html', message=message)
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        ip = request.remote_addr
        message, success = login_user(username, password, ip)
        if success:
            session['username'] = username
            return redirect(url_for('index'))
        return render_template('login.html', message=message)
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/change-password', methods=['GET', 'POST'])
def change_password_route():
    if request.method == 'POST':
        if 'username' not in session:
            return redirect(url_for('login'))
        username = session['username']
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        message = change_password(username, old_password, new_password)
        return render_template('change_password.html', message=message)
    return render_template('change_password.html')

@app.route('/admin')
def admin():
    access_key = request.args.get('key')
    expected_key = os.getenv('ADMIN_ACCESS_KEY')

    if access_key != expected_key:
        return "Bạn không có quyền truy cập trang quản trị.", 403

    users = User.query.order_by(User.created_at.desc()).all()
    logs = LoginLog.query.order_by(LoginLog.timestamp.desc()).limit(100).all()
    return render_template('admin.html', users=users, logs=logs)

@app.route('/admin/unlock/<int:user_id>')
def unlock_user(user_id):
    access_key = request.args.get('key')
    expected_key = os.getenv('ADMIN_ACCESS_KEY')

    if access_key != expected_key:
        return "Bạn không có quyền truy cập.", 403

    user = User.query.get(user_id)
    if user:
        user.is_locked = False
        user.fail_count = 0
        db.session.commit()
    return redirect(url_for('admin', key=access_key))

@app.route('/admin/delete/<int:user_id>')
def delete_user(user_id):
    access_key = request.args.get('key')
    expected_key = os.getenv('ADMIN_ACCESS_KEY')

    if access_key != expected_key:
        return "Bạn không có quyền truy cập.", 403

    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
    return redirect(url_for('admin', key=access_key))

if __name__ == '__main__':
    app.run(debug=True)
