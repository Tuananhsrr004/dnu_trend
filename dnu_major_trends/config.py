import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

class Config:
    APP_NAME = "DNU Major Trends"
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-me-in-production")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        f"sqlite:///{BASE_DIR / 'dnu_trends.sqlite3'}",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = str(BASE_DIR / "uploads")
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{BASE_DIR / 'test.sqlite3'}"

class DevConfig(Config):
    DEBUG = True

class ProdConfig(Config):
    DEBUG = False
