# 🏥 API Pendaftaran Pasien — UAS Framework Programming

Proyek ini merupakan aplikasi REST API untuk pendaftaran pasien, dilengkapi dengan autentikasi JWT, CRUD data pasien, upload file KTP, dan dokumentasi Swagger UI.

---

## 🚀 Fitur

- ✅ Register & Login User (dengan JWT Token)
- ✅ CRUD Data Pasien
- ✅ Upload Gambar KTP
- ✅ Filter pasien berdasarkan jenis kelamin
- ✅ Autentikasi JWT pada endpoint yang dilindungi
- ✅ Swagger UI untuk dokumentasi dan uji API langsung

---

## 🧰 Tech Stack

- Python 3
- Flask
- Flask-RESTX
- Flask-JWT-Extended
- SQLite (via SQLAlchemy)
- Swagger UI (bawaan dari Flask-RESTX)

---

## 📁 Struktur Proyek

```
flask_pasien_api/
├── app.py               # Main entry point
├── models.py            # Model SQLAlchemy (User, Pasien)
├── auth.py              # Register & Login
├── pasien.py            # CRUD pasien & upload KTP
├── extensions.py        # Init DB & JWT
├── uploads/             # Folder upload file KTP
├── requirements.txt     # Semua dependensi
└── README.md            # Dokumentasi proyek ini
```

---

## ⚙️ Instalasi & Menjalankan

1. Clone atau salin proyek:

```bash
git clone <URL-REPO>  # atau salin folder ke lokal
cd flask_pasien_api
```

2. Buat virtual environment & aktifkan:

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate    # Windows
```

3. Install dependensi:

```bash
pip install -r requirements.txt
```

4. Jalankan aplikasi:

```bash
python3 app.py
```

5. Buka di browser:

```
http://127.0.0.1:5000
```

---

## 🔐 Cara Menggunakan Autentikasi

1. Jalankan `POST /auth/register` untuk membuat user.
2. Login via `POST /auth/login` untuk mendapatkan token JWT.
3. Klik tombol **Authorize** di Swagger → Masukkan token:
   ```
   Bearer <token>
   ```

---

## 📤 Upload File KTP

- Endpoint: `POST /pasien/upload/{id}`
- Klik **Try it out** → Masukkan `id pasien` → Pilih file → **Execute**
- File disimpan ke folder `/uploads` dan tersimpan di database.

---

## 🧪 Contoh CURL

```bash
curl -X POST http://127.0.0.1:5000/pasien/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "nama_pasien": "Siti",
    "no_ktp": "1234567890123456",
    "tanggal_lahir": "2000-01-01",
    "alamat": "Jl. Contoh No.1",
    "jenis_kelamin": "Perempuan",
    "no_hp": "08123456789"
}'
```

---

## 📸 Dokumentasi Swagger UI

- Dokumentasi otomatis tersedia di root:
  ```
  http://127.0.0.1:5000/
  ```

---

## 👨‍💻 Author

- Nama: **Fanny Faqih Subekti**
- Kelas: **RPL 5R3**
- Matkul: **Framework Programming**

---

## ✅ Status: Selesai ✅
