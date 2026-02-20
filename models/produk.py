"""
Model Kategori dan Produk
"""

from database import db
from datetime import datetime


class Kategori(db.Model):
    __tablename__ = "kategori"

    id         = db.Column(db.Integer, primary_key=True)
    nama       = db.Column(db.String(100), nullable=False, unique=True)
    deskripsi  = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relasi: satu kategori bisa punya banyak produk
    produk = db.relationship("Produk", backref="kategori", lazy=True)

    def to_dict(self):
        return {
            "id":        self.id,
            "nama":      self.nama,
            "deskripsi": self.deskripsi,
            "jumlah_produk": len(self.produk)
        }


class Produk(db.Model):
    __tablename__ = "produk"

    id           = db.Column(db.Integer, primary_key=True)
    nama         = db.Column(db.String(150), nullable=False)
    deskripsi    = db.Column(db.Text, nullable=True)
    harga        = db.Column(db.Numeric(12, 2), nullable=False)
    stok         = db.Column(db.Integer, default=0)
    satuan       = db.Column(db.String(20), default="pcs")  # pcs, kg, liter, dll
    kategori_id  = db.Column(db.Integer, db.ForeignKey("kategori.id"), nullable=True)
    created_at   = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at   = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id":          self.id,
            "nama":        self.nama,
            "deskripsi":   self.deskripsi,
            "harga":       float(self.harga),
            "stok":        self.stok,
            "satuan":      self.satuan,
            "kategori":    self.kategori.nama if self.kategori else None,
            "kategori_id": self.kategori_id,
            "created_at":  self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at":  self.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
        }
