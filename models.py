from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Pasien(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama_pasien = db.Column(db.String(100), nullable=False)
    no_ktp = db.Column(db.String(20), unique=True, nullable=False)
    tanggal_lahir = db.Column(db.String(20), nullable=False)
    alamat = db.Column(db.String(200), nullable=False)
    jenis_kelamin = db.Column(db.String(10), nullable=False)
    no_hp = db.Column(db.String(20), nullable=False)
    gambar_ktp = db.Column(db.String(100))  # nama file upload
