"""
Model User - untuk autentikasi
"""

from database import db
from datetime import datetime
import bcrypt


class User(db.Model):
    __tablename__ = "users"

    id         = db.Column(db.Integer, primary_key=True)
    nama       = db.Column(db.String(100), nullable=False)
    email      = db.Column(db.String(150), unique=True, nullable=False)
    password   = db.Column(db.String(255), nullable=False)
    role       = db.Column(db.String(20), default="staff")  # admin / staff
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, plain_password):
        """Hash password sebelum disimpan ke database"""
        salt = bcrypt.gensalt()
        self.password = bcrypt.hashpw(plain_password.encode("utf-8"), salt).decode("utf-8")

    def check_password(self, plain_password):
        """Verifikasi password saat login"""
        return bcrypt.checkpw(
            plain_password.encode("utf-8"),
            self.password.encode("utf-8")
        )

    def to_dict(self):
        return {
            "id":         self.id,
            "nama":       self.nama,
            "email":      self.email,
            "role":       self.role,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
