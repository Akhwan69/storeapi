"""
Routes Produk - CRUD + Manajemen Stok
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from database import db
from models.produk import Produk, Kategori

produk_bp = Blueprint("produk", __name__)


# ── GET SEMUA PRODUK (dengan filter & search) ─────────
@produk_bp.route("/", methods=["GET"])
@jwt_required()
def get_all():
    # Query params opsional: ?search=nama&kategori_id=1&stok_habis=true
    search      = request.args.get("search", "")
    kategori_id = request.args.get("kategori_id", type=int)
    stok_habis  = request.args.get("stok_habis", "false").lower() == "true"

    query = Produk.query

    if search:
        query = query.filter(Produk.nama.ilike(f"%{search}%"))
    if kategori_id:
        query = query.filter_by(kategori_id=kategori_id)
    if stok_habis:
        query = query.filter(Produk.stok == 0)

    produk = query.order_by(Produk.nama).all()
    return jsonify({
        "total":  len(produk),
        "produk": [p.to_dict() for p in produk]
    }), 200


# ── GET PRODUK BY ID ──────────────────────────────────
@produk_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_by_id(id):
    p = Produk.query.get_or_404(id, description="Produk tidak ditemukan")
    return jsonify(p.to_dict()), 200


# ── TAMBAH PRODUK ─────────────────────────────────────
@produk_bp.route("/", methods=["POST"])
@jwt_required()
def create():
    data = request.get_json()

    required = ["nama", "harga"]
    for field in required:
        if not data or not data.get(field):
            return jsonify({"error": f"Field '{field}' wajib diisi"}), 400

    # Validasi kategori jika dikirim
    if data.get("kategori_id"):
        if not Kategori.query.get(data["kategori_id"]):
            return jsonify({"error": "Kategori tidak ditemukan"}), 404

    p = Produk(
        nama        = data["nama"],
        deskripsi   = data.get("deskripsi"),
        harga       = data["harga"],
        stok        = data.get("stok", 0),
        satuan      = data.get("satuan", "pcs"),
        kategori_id = data.get("kategori_id")
    )
    db.session.add(p)
    db.session.commit()
    return jsonify({"message": "Produk berhasil ditambahkan", "data": p.to_dict()}), 201


# ── UPDATE PRODUK ─────────────────────────────────────
@produk_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update(id):
    p    = Produk.query.get_or_404(id, description="Produk tidak ditemukan")
    data = request.get_json()

    fields = ["nama", "deskripsi", "harga", "stok", "satuan", "kategori_id"]
    for field in fields:
        if field in data:
            setattr(p, field, data[field])

    db.session.commit()
    return jsonify({"message": "Produk berhasil diupdate", "data": p.to_dict()}), 200


# ── HAPUS PRODUK ──────────────────────────────────────
@produk_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete(id):
    p = Produk.query.get_or_404(id, description="Produk tidak ditemukan")
    db.session.delete(p)
    db.session.commit()
    return jsonify({"message": f"Produk '{p.nama}' berhasil dihapus"}), 200


# ── TAMBAH STOK ───────────────────────────────────────
@produk_bp.route("/<int:id>/tambah-stok", methods=["PATCH"])
@jwt_required()
def tambah_stok(id):
    """
    PATCH /api/produk/<id>/tambah-stok
    Body: { "jumlah": 10 }
    """
    p    = Produk.query.get_or_404(id, description="Produk tidak ditemukan")
    data = request.get_json()

    jumlah = data.get("jumlah", 0)
    if jumlah <= 0:
        return jsonify({"error": "Jumlah harus lebih dari 0"}), 400

    p.stok += jumlah
    db.session.commit()
    return jsonify({
        "message":    f"Stok berhasil ditambah {jumlah} {p.satuan}",
        "stok_baru":  p.stok,
        "produk":     p.nama
    }), 200


# ── KURANGI STOK ──────────────────────────────────────
@produk_bp.route("/<int:id>/kurangi-stok", methods=["PATCH"])
@jwt_required()
def kurangi_stok(id):
    """
    PATCH /api/produk/<id>/kurangi-stok
    Body: { "jumlah": 5 }
    """
    p    = Produk.query.get_or_404(id, description="Produk tidak ditemukan")
    data = request.get_json()

    jumlah = data.get("jumlah", 0)
    if jumlah <= 0:
        return jsonify({"error": "Jumlah harus lebih dari 0"}), 400
    if jumlah > p.stok:
        return jsonify({"error": f"Stok tidak cukup. Stok tersedia: {p.stok} {p.satuan}"}), 400

    p.stok -= jumlah
    db.session.commit()
    return jsonify({
        "message":    f"Stok berhasil dikurangi {jumlah} {p.satuan}",
        "stok_baru":  p.stok,
        "produk":     p.nama
    }), 200
