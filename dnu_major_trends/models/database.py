from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# SQLAlchemy instance (initialized in app factory)
db = SQLAlchemy()

class TimestampMixin:
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class User(UserMixin, TimestampMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='user')  # 'admin' or 'user'

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

class MajorData(TimestampMixin, db.Model):
    __tablename__ = 'majors_data'
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False, index=True)
    major = db.Column(db.String(120), nullable=False, index=True)
    students = db.Column(db.Integer, nullable=False)
    male = db.Column(db.Integer, nullable=True)
    female = db.Column(db.Integer, nullable=True)
    region = db.Column(db.String(30), nullable=True)  # Bac/Trung/Nam
    avg_score = db.Column(db.Float, nullable=True)

    __table_args__ = (
        db.UniqueConstraint('year', 'major', 'region', name='uq_year_major_region'),
    )

    @property
    def total_gender(self):
        return (self.male or 0) + (self.female or 0)


def init_db(app):
    """Bind db to app and create tables."""
    db.init_app(app)
    with app.app_context():
        db.create_all()


class ForecastCache(TimestampMixin, db.Model):
    __tablename__ = 'forecasts_cache'
    id = db.Column(db.Integer, primary_key=True)
    major = db.Column(db.String(120), index=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    yhat = db.Column(db.Float, nullable=False)
    __table_args__ = (
        db.UniqueConstraint('major', 'year', name='uq_major_year'),
    )


class ChatMessage(TimestampMixin, db.Model):
    __tablename__ = 'chat_messages'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    text = db.Column(db.Text, nullable=False)
    score = db.Column(db.Float, nullable=True)
    suggestions = db.Column(db.Text, nullable=True)  # JSON string of suggestions
