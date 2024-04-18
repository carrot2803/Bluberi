from datetime import timedelta
from flask import Flask, render_template
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from App.controllers import socket, setup_jwt, add_auth_context
from App.database import init_db


def add_views(app):
    from App.views import auth, index

    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(index, url_prefix="/")


def create_app(overrides={}):
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
    def custom_unauthorized_response(error):
        return render_template("error.html", error=error), 401

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("error.html", error=error), 404

    app.app_context().push()

    return app


def load_config(app, overrides):
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "felicia is an egg"
    app.config["JWT_SECRET_KEY"] = "jwt-secret-string"
    app.config["JWT_ACCESS_COOKIE_NAME"] = "access_token"
    app.config["JWT_REFRESH_COOKIE_NAME"] = "refresh_token"
    app.config["JWT_TOKEN_LOCATION"] = ["cookies", "headers"]
    app.config["JWT_HEADER_NAME"] = "Cookie"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=15)
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False
    app.config["JWT_COOKIE_SECURE"] = True
