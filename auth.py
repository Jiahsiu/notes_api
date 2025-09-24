from flask import request
from flask_restx import Namespace, Resource, fields
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from models import User
from extensions import db

ns = Namespace("auth", description="Authentication")

user_model = ns.model("UserRegister", {
    "email": fields.String(required=True, example="test@test.com"),
    "password": fields.String(required=True, example="secret")
})

login_model = ns.clone("UserLogin", user_model)

token_model = ns.model("Token", {"access_token": fields.String})

@ns.route("/register")
class Register(Resource):
    @ns.expect(user_model)
    @ns.marshal_with(token_model, code=201)
    def post(self):
        data = request.get_json() or {}
        if User.query.filter_by(email=data["email"]).first():
            ns.abort(409, "Email already registered")
        user = User(email=data["email"], password_hash=generate_password_hash(data["password"]))
        db.session.add(user)
        db.session.commit()
        token = create_access_token(identity=user.id)
        return {"access_token": token}, 201

@ns.route("/login")
class Login(Resource):
    @ns.expect(login_model)
    @ns.marshal_with(token_model)
    def post(self):
        data = request.get_json() or {}
        user = User.query.filter_by(email=data.get("email")).first()
        if not user or not check_password_hash(user.password_hash, data.get("password", "")):
            ns.abort(401, "Invalid credentials")
        token = create_access_token(identity=user.id)
        return {"access_token": token}