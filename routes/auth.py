"""
Routes Autentikasi - Register, Login, Profil
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity
)
from database import db
from models.user import User

auth_bp = Blueprint("auth", __name__)


# ── REGISTER ──────────────────────────────────────────
@auth_bp.route("/register", methods=["POST"])
def register():
    """
    POST /api/auth/register
    Body: { "nama": "...", "email": "...", "password": "..." }
    """
    data = request.get_json()

    # Validasi input
    required = ["nama", "email", "password"]
    for field in required:
        if not data or not data.get(field):
            return jsonify({"error": f"Field '{field}' wajib diisi"}), 400

    # Cek email sudah terdaftar
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email sudah terdaftar"}), 409

    # Simpan user baru
    user = User(nama=data["nama"], email=data["email"])
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "Registrasi berhasil",
        "user": user.to_dict()
    }), 201


# ── LOGIN ─────────────────────────────────────────────
@auth_bp.route("/login", methods=["POST"])
def login():
    """
    POST /api/auth/login
    Body: { "email": "...", "password": "..." }
    """
    data = request.get_json()

    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"error": "Email dan password wajib diisi"}), 400

    user = User.query.filter_by(email=data["email"]).first()

    if not user or not user.check_password(data["password"]):
        return jsonify({"error": "Email atau password salah"}), 401

    # Buat token JWT
    access_token  = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))

    return jsonify({
        "message":       "Login berhasil",
        "access_token":  access_token,
        "refresh_token": refresh_token,
        "user":          user.to_dict()
    }), 200


# ── PROFIL (butuh login) ───────────────────────────────
@auth_bp.route("/profil", methods=["GET"])
@jwt_required()
def profil():
    """
    GET /api/auth/profil
    Header: Authorization: Bearer <token>
    """
    user_id = get_jwt_identity()
    user    = User.query.get_or_404(user_id)
    return jsonify({"user": user.to_dict()}), 200


# ── REFRESH TOKEN ─────────────────────────────────────
@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    user_id      = get_jwt_identity()
    access_token = create_access_token(identity=user_id)
    return jsonify({"access_token": access_token}), 200
