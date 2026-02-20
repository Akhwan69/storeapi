"""
Konfigurasi aplikasi StoreAPI
"""

import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Koneksi ke PostgreSQL
    # Format: postgresql://user:password@host:port/nama_database
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg://postgres:password@localhost:5432/storeapi_db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Secret key untuk JWT (ganti dengan string acak yang panjang di production!)
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "storeapi-secret-key-2024")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=2)   # Token berlaku 2 jam
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)  # Refresh token 30 hari

    SECRET_KEY = os.getenv("SECRET_KEY", "flask-secret-key")
