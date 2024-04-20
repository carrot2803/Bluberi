from datetime import timedelta
from typing import Literal
from dotenv import load_dotenv
from flask import Flask, render_template
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from App.controllers import socket, setup_jwt, add_auth_context
from App.database import init_db
from os import getenv


def add_views(app) -> None:
    from App.views import auth, index, chat

    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(index, url_prefix="/")
    app.register_blueprint(chat, url_prefix="/")


def create_app(overrides={}) -> Flask:
    app = Flask(__name__)

    load_config(app, overrides)
    CORS(app)
    add_auth_context(app)
    add_views(app)
    init_db(app)
    socket.init_app(app)

    jwt: JWTManager = setup_jwt(app)

    @jwt.invalid_token_loader
    @jwt.unauthorized_loader
    def custom_unauthorized_response(error) -> tuple[str, Literal[401]]:
        return render_template("login.html", error=error), 401

    @app.errorhandler(404)
    def page_not_found(error) -> tuple[str, Literal[404]]:
        return render_template("error.html", error=error), 404

    app.app_context().push()

    return app


def load_config(app, overrides=None):
    load_dotenv()
    app.config["ENV"] = "development"
    app.config["JWT_SECRET_KEY"] = getenv("JWT_SECRET_KEY")
    app.config["SECRET_KEY"] = getenv("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = getenv("SQLALCHEMY_DATABASE_URI")
    app.config["PYTHON_VERSION"] = getenv("PYTHON_VERSION")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(
        hours=int(getenv("JWT_ACCESS_TOKEN_EXPIRES", default=15))
    )

    # General config
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_ACCESS_COOKIE_NAME"] = "access_token"
    app.config["JWT_REFRESH_COOKIE_NAME"] = "refresh_token"
    app.config["JWT_TOKEN_LOCATION"] = ["cookies", "headers"]
    app.config["JWT_HEADER_NAME"] = "Cookie"
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False
    app.config["JWT_COOKIE_SECURE"] = True
