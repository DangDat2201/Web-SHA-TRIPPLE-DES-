from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    username_hash = db.Column(db.String(64), unique=True, nullable=False)
    password_encrypted = db.Column(db.String(256), nullable=False)
    salt = db.Column(db.String(32), nullable=False)
    fail_count = db.Column(db.Integer, default=0)
    is_locked = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class LoginLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username_hash = db.Column(db.String(64), nullable=False)
    ip_address = db.Column(db.String(64))
    success = db.Column(db.Boolean)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
