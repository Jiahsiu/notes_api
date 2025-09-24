import os
from flask import Flask, jsonify
from dotenv import load_dotenv

from extensions import db, jwt, api
from auth import ns as auth_ns
from notes import ns as notes_ns

load_dotenv()

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///notes.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "supersecret")
    app.config["PROPAGATE_EXCEPTIONS"] = True

    db.init_app(app)
    jwt.init_app(app)
    api.init_app(app)

    # Register namespaces
    api.add_namespace(auth_ns, path="/api/auth")
    api.add_namespace(notes_ns, path="/api/notes")

    @app.get("/openapi.json")
    def openapi_json():
        return jsonify(api.__schema__)

    with app.app_context():
        db.create_all()

    return app

app = create_app()