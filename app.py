from flask import Flask
from flask_restx import Api
from extensions import db, jwt
import os

def create_app():
    app = Flask(__name__)
    
    # Konfigurasi dasar
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pasien.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'super-secret'
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # max 2MB

    # Buat folder upload jika belum ada
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Inisialisasi ekstensi
    db.init_app(app)
    jwt.init_app(app)

    # Konfigurasi Swagger API + Security JWT
    authorizations = {
        "Bearer Auth": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "Masukkan token dengan format: **Bearer <token>**"
        }
    }

    api = Api(
        app,
        version="1.0",
        title="API Pendaftaran Pasien",
        description="UAS Framework Programming || Fanny Faqih Subekti",
        security="Bearer Auth",
        authorizations=authorizations
    )

    # Import & registrasi namespace
    from auth import auth_ns
    from pasien import pasien_ns
    api.add_namespace(auth_ns)
    api.add_namespace(pasien_ns)

    # Buat tabel database
    with app.app_context():
        db.create_all()

    return app

# Run
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
