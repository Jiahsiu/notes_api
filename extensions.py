from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_restx import Api

# 可集中管理擴充套件，避免循環引用

db = SQLAlchemy()
jwt = JWTManager()
api = Api(title="Notes API", version="1.0", doc="/docs")  # Swagger UI 在 /docs