from flask import request, current_app
from flask_restx import Namespace, Resource, fields, reqparse
from flask_jwt_extended import jwt_required
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
import os
import re

from models import Pasien
from extensions import db

pasien_ns = Namespace('pasien', description='Manajemen Data Pasien')

# Schema input data pasien
pasien_model = pasien_ns.model('Pasien', {
    'nama_pasien': fields.String(required=True),
    'no_ktp': fields.String(required=True),
    'tanggal_lahir': fields.String(required=True),
    'alamat': fields.String(required=True),
    'jenis_kelamin': fields.String(required=True, enum=["Laki-laki", "Perempuan"]),
    'no_hp': fields.String(required=True),
})

# Parser untuk upload file
upload_parser = reqparse.RequestParser()
upload_parser.add_argument(
    'file',
    type=FileStorage,
    location='files',
    required=True,
    help='Upload file KTP (jpg, png, pdf)'
)

@pasien_ns.route('/')
class PasienList(Resource):
    @pasien_ns.doc(params={
        'jenis_kelamin': 'Filter berdasarkan jenis kelamin',
        'nama': 'Cari berdasarkan nama pasien (partial match)'
    })
    def get(self):
        jenis_kelamin = request.args.get('jenis_kelamin')
        nama = request.args.get('nama')

        query = Pasien.query
        if jenis_kelamin:
            query = query.filter_by(jenis_kelamin=jenis_kelamin)
        if nama:
            query = query.filter(Pasien.nama_pasien.ilike(f"%{nama}%"))

        data = query.all()
        return [{
            'id': p.id,
            'nama_pasien': p.nama_pasien,
            'no_ktp': p.no_ktp,
            'tanggal_lahir': p.tanggal_lahir,
            'alamat': p.alamat,
            'jenis_kelamin': p.jenis_kelamin,
            'no_hp': p.no_hp,
            'gambar_ktp': p.gambar_ktp
        } for p in data]

    @jwt_required()
    @pasien_ns.expect(pasien_model)
    def post(self):
        data = request.json

        # ✅ Validasi NIK
        if not re.fullmatch(r"\d{16}", data['no_ktp']):
            return {'message': 'Format NIK harus 16 digit angka'}, 400

        if Pasien.query.filter_by(no_ktp=data['no_ktp']).first():
            return {'message': 'Pasien dengan KTP ini sudah terdaftar'}, 409

        pasien = Pasien(**data)
        db.session.add(pasien)
        db.session.commit()
        return {'message': 'Pasien berhasil ditambahkan'}, 201

@pasien_ns.route('/<int:id>')
class PasienDetail(Resource):
    def get(self, id):
        pasien = Pasien.query.get_or_404(id)
        return {
            'id': pasien.id,
            'nama_pasien': pasien.nama_pasien,
            'no_ktp': pasien.no_ktp,
            'tanggal_lahir': pasien.tanggal_lahir,
            'alamat': pasien.alamat,
            'jenis_kelamin': pasien.jenis_kelamin,
            'no_hp': pasien.no_hp,
            'gambar_ktp': pasien.gambar_ktp
        }

    @jwt_required()
    @pasien_ns.expect(pasien_model)
    def put(self, id):
        pasien = Pasien.query.get_or_404(id)
        data = request.json

        # ✅ Validasi NIK
        if not re.fullmatch(r"\d{16}", data['no_ktp']):
            return {'message': 'Format NIK harus 16 digit angka'}, 400

        for key in data:
            setattr(pasien, key, data[key])
        db.session.commit()
        return {'message': 'Data pasien diperbarui'}, 200

    @jwt_required()
    def delete(self, id):
        pasien = Pasien.query.get_or_404(id)
        db.session.delete(pasien)
        db.session.commit()
        return {'message': 'Data pasien dihapus'}, 200

@pasien_ns.route('/upload/<int:id>')
class UploadKTP(Resource):
    @jwt_required()
    @pasien_ns.expect(upload_parser)
    def post(self, id):
        pasien = Pasien.query.get_or_404(id)
        args = upload_parser.parse_args()
        file = args['file']

        if file.filename == '':
            return {'message': 'Nama file kosong'}, 400

        if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.pdf')):
            return {'message': 'Format file tidak diizinkan'}, 400

        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        pasien.gambar_ktp = filename
        db.session.commit()

        return {'message': 'File berhasil diunggah'}, 200
