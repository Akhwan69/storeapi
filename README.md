# 🛒 StoreAPI — REST API Manajemen Toko

REST API untuk manajemen toko sederhana, dibangun dengan **Python Flask** dan **PostgreSQL**.  
Dibuat sebagai project portofolio PKL - RPL.

---

## 🔧 Teknologi yang Digunakan

| Teknologi        | Kegunaan                        |
|------------------|---------------------------------|
| Python 3.10+     | Bahasa pemrograman utama        |
| Flask 3.0        | Web framework                   |
| Flask-SQLAlchemy | ORM untuk database              |
| Flask-JWT-Extended | Autentikasi dengan JWT token  |
| PostgreSQL       | Database relasional             |
| bcrypt           | Enkripsi password               |

---

## 📁 Struktur Project

```
storeapi/
├── app.py              ← Entry point aplikasi
├── config.py           ← Konfigurasi (database, JWT, dll)
├── database.py         ← Inisialisasi SQLAlchemy
├── requirements.txt    ← Daftar library yang dibutuhkan
├── .env.example        ← Template environment variables
├── models/
│   ├── user.py         ← Model User (autentikasi)
│   └── produk.py       ← Model Produk & Kategori
└── routes/
    ├── auth.py         ← Endpoint register, login, profil
    ├── produk.py       ← Endpoint CRUD produk + stok
    └── kategori.py     ← Endpoint CRUD kategori
```

---

## ⚙️ Cara Menjalankan

### 1. Clone / download project ini

### 2. Buat virtual environment
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### 3. Install library
```bash
pip install -r requirements.txt
```

### 4. Setup database PostgreSQL
Buat database baru di PostgreSQL:
```sql
CREATE DATABASE storeapi_db;
```

### 5. Buat file `.env`
Salin `.env.example` menjadi `.env` dan isi:
```
DATABASE_URL=postgresql://postgres:PASSWORD_KAMU@localhost:5432/storeapi_db
JWT_SECRET_KEY=isi-dengan-string-acak
SECRET_KEY=flask-secret
```

### 6. Jalankan aplikasi
```bash
python app.py
```
Server berjalan di: **http://localhost:5000**

---

## 📡 Dokumentasi API

### 🔐 Autentikasi

| Method | Endpoint           | Deskripsi              | Auth? |
|--------|--------------------|------------------------|-------|
| POST   | /api/auth/register | Daftar akun baru       | ❌    |
| POST   | /api/auth/login    | Login & dapat token    | ❌    |
| GET    | /api/auth/profil   | Lihat profil sendiri   | ✅    |
| POST   | /api/auth/refresh  | Perpanjang access token| ✅    |

#### Contoh Register
```json
POST /api/auth/register
{
  "nama": "Budi Santoso",
  "email": "budi@gmail.com",
  "password": "rahasia123"
}
```

#### Contoh Login
```json
POST /api/auth/login
{
  "email": "budi@gmail.com",
  "password": "rahasia123"
}
```
Response:
```json
{
  "message": "Login berhasil",
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "user": { "id": 1, "nama": "Budi Santoso", "role": "staff" }
}
```

> Untuk endpoint yang butuh Auth ✅, tambahkan header:  
> `Authorization: Bearer <access_token>`

---

### 📦 Kategori

| Method | Endpoint          | Deskripsi           |
|--------|-------------------|---------------------|
| GET    | /api/kategori/    | Semua kategori      |
| GET    | /api/kategori/:id | Detail kategori     |
| POST   | /api/kategori/    | Tambah kategori     |
| PUT    | /api/kategori/:id | Update kategori     |
| DELETE | /api/kategori/:id | Hapus kategori      |

---

### 🏷️ Produk

| Method | Endpoint                         | Deskripsi                        |
|--------|----------------------------------|----------------------------------|
| GET    | /api/produk/                     | Semua produk (bisa filter/search)|
| GET    | /api/produk/:id                  | Detail produk                    |
| POST   | /api/produk/                     | Tambah produk baru               |
| PUT    | /api/produk/:id                  | Update produk                    |
| DELETE | /api/produk/:id                  | Hapus produk                     |
| PATCH  | /api/produk/:id/tambah-stok      | Tambah stok                      |
| PATCH  | /api/produk/:id/kurangi-stok     | Kurangi stok                     |

#### Filter produk
```
GET /api/produk/?search=baju
GET /api/produk/?kategori_id=1
GET /api/produk/?stok_habis=true
```

#### Contoh Tambah Produk
```json
POST /api/produk/
{
  "nama": "Kaos Polos Putih",
  "harga": 45000,
  "stok": 100,
  "satuan": "pcs",
  "kategori_id": 1,
  "deskripsi": "Kaos bahan cotton combed 30s"
}
```

#### Contoh Tambah Stok
```json
PATCH /api/produk/1/tambah-stok
{
  "jumlah": 50
}
```

---

## 👤 Author

**Akhwan** — RPL  
