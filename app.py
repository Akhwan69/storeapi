"""
StoreAPI - REST API Manajemen Toko
Dibuat dengan Flask + PostgreSQL
Author: Portfolio Project - XI RPL
"""

from flask import Flask
from flask_jwt_extended import JWTManager
from config import Config
from database import db
from routes.auth import auth_bp
from routes.produk import produk_bp
from routes.kategori import kategori_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inisialisasi database dan JWT
    db.init_app(app)
    JWTManager(app)

    # Daftarkan Blueprint (route)
    app.register_blueprint(auth_bp,     url_prefix="/api/auth")
    app.register_blueprint(produk_bp,   url_prefix="/api/produk")
    app.register_blueprint(kategori_bp, url_prefix="/api/kategori")

    # Buat tabel otomatis jika belum ada
    with app.app_context():
        db.create_all()

    @app.route("/")
    def index():
        return {
            "message": "Selamat datang di StoreAPI 🛒",
            "versi": "1.0.0",
            "endpoints": {
                "auth":     "/api/auth",
                "produk":   "/api/produk",
                "kategori": "/api/kategori",
            }
        }

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
