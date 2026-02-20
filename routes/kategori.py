"""
Routes Kategori - CRUD
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from database import db
from models.produk import Kategori

kategori_bp = Blueprint("kategori", __name__)


# ── GET SEMUA KATEGORI ────────────────────────────────
@kategori_bp.route("/", methods=["GET"])
@jwt_required()
def get_all():
    data = Kategori.query.all()
    return jsonify({
        "total": len(data),
        "kategori": [k.to_dict() for k in data]
    }), 200


# ── GET KATEGORI BY ID ────────────────────────────────
@kategori_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_by_id(id):
    k = Kategori.query.get_or_404(id, description="Kategori tidak ditemukan")
    return jsonify(k.to_dict()), 200


# ── TAMBAH KATEGORI ───────────────────────────────────
@kategori_bp.route("/", methods=["POST"])
@jwt_required()
def create():
    data = request.get_json()
    if not data or not data.get("nama"):
        return jsonify({"error": "Nama kategori wajib diisi"}), 400

    if Kategori.query.filter_by(nama=data["nama"]).first():
        return jsonify({"error": "Nama kategori sudah ada"}), 409

    k = Kategori(nama=data["nama"], deskripsi=data.get("deskripsi"))
    db.session.add(k)
    db.session.commit()
    return jsonify({"message": "Kategori berhasil ditambahkan", "data": k.to_dict()}), 201


# ── UPDATE KATEGORI ───────────────────────────────────
@kategori_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update(id):
    k    = Kategori.query.get_or_404(id, description="Kategori tidak ditemukan")
    data = request.get_json()

    if data.get("nama"):
        k.nama = data["nama"]
    if "deskripsi" in data:
        k.deskripsi = data["deskripsi"]

    db.session.commit()
    return jsonify({"message": "Kategori berhasil diupdate", "data": k.to_dict()}), 200


# ── HAPUS KATEGORI ────────────────────────────────────
@kategori_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete(id):
    k = Kategori.query.get_or_404(id, description="Kategori tidak ditemukan")
    db.session.delete(k)
    db.session.commit()
    return jsonify({"message": f"Kategori '{k.nama}' berhasil dihapus"}), 200
