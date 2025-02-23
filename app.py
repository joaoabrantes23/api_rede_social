import secrets
import os

from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager

from utils.init_admin import create_admin
from settings.db import db
from settings.config import Config
import models

from routes.user_routes import blp as UserBlueprint
from routes.post_routes import blp as PostBlueprint


def create_app(db_url=None):
    app = Flask(__name__)

    # Carregar a configuração da classe Config
    app.config.from_object(Config)

    # Se db_url for passado, sobreponha o valor do banco de dados
    if db_url:
        app.config["SQLALCHEMY_DATABASE_URI"] = db_url


    db.init_app(app)

    api = Api(app)

    jwt = JWTManager(app)

    @jwt.needs_fresh_token_loader
    def token_not_fresh(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    "description": "Token de acesso não é fresh",
                    "error": "fresh_token_required",
                }
            )
        )
        

    with app.app_context():
        db.create_all()
        create_admin()



    api.register_blueprint(UserBlueprint)
    api.register_blueprint(PostBlueprint)

    return app
