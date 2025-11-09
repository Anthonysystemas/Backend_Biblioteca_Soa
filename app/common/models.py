from datetime import datetime, timedelta
from enum import Enum
from sqlalchemy import func
from ..extensions import db

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(160), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    full_name = db.Column(db.String(200), nullable=True)
    is_active = db.Column(db.Boolean, default=True)

class PasswordResetToken(db.Model):
    __tablename__ = "password_reset_tokens"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    token = db.Column(db.String(100), unique=True, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    used = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(20), unique=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(120))
    available_copies = db.Column(db.Integer, default=0)

class ReservationStatus(str, Enum):
    PENDING = "PENDING"
    HELD = "HELD"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"

class Reservation(db.Model):
    __tablename__ = "reservations"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    book_id = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Enum(ReservationStatus), default=ReservationStatus.PENDING, nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.now())

class Outbox(db.Model):
    __tablename__ = "outbox"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    topic = db.Column(db.String(100), nullable=False)
    payload = db.Column(db.JSON, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    processed = db.Column(db.Boolean, default=False)

def create_all_tables():
    db.create_all()
