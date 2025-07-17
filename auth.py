from flask import request
from flask_restx import Namespace, Resource, fields
from extensions import db
from models import User
from flask_jwt_extended import create_access_token

auth_ns = Namespace('auth', description='Autentikasi')

# Skema model input untuk login dan register
user_model = auth_ns.model('User', {
    'username': fields.String(required=True, description='Username pengguna'),
    'password': fields.String(required=True, description='Password pengguna'),
})

@auth_ns.route('/register')
class Register(Resource):
    @auth_ns.expect(user_model)
    def post(self):
        data = request.json
        if User.query.filter_by(username=data['username']).first():
            return {'message': 'Username sudah terdaftar'}, 409

        user = User(username=data['username'])
        user.set_password(data['password'])

        db.session.add(user)
        db.session.commit()
        return {'message': 'User berhasil didaftarkan'}, 201

@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(user_model)
    def post(self):
        data = request.json
        user = User.query.filter_by(username=data['username']).first()
        if user and user.check_password(data['password']):
            # PERBAIKAN: Konversi user.id menjadi string untuk JWT identity
            token = create_access_token(identity=str(user.id))
            return {'access_token': token}, 200
        return {'message': 'Username atau password salah'}, 401
