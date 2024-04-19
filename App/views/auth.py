from sqlite3 import IntegrityError
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    set_access_cookies,
    unset_jwt_cookies,
)

from flask import Blueprint, render_template, redirect, request, url_for, flash
from werkzeug import Response
from App.database import db
from App.models import User
from App.controllers import login_user

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET"])
def login_page() -> str:
    return render_template("login.html")


@auth.route("/signup", methods=["GET"])
def sign_up_page() -> str:
    return render_template("signup.html")


@auth.route("/login", methods=["POST"])
def login() -> Response:
    username: str = request.form["username"]
    password: str = request.form["password"]
    token: str | None = login_user(username, password)
    if token is None:
        flash("Invalid Credintials", "danger")
        response: Response = redirect(url_for("auth.login"))
    else:
        flash("Login was successful", "success")
        response: Response = redirect(url_for("chat.chat_page"))
    set_access_cookies(response, token)
    return response


@auth.route("/signup", methods=["POST"])
def sign_up() -> Response:
    try:
        username: str = request.form["username"]
        password: str = request.form["password"]
        email: str = request.form["email"]
        user = User(username, email, password)
        db.session.add(user)
        db.session.commit()
        response: Response = redirect(url_for("auth.login"))
        token: str = create_access_token(identity=user)
        set_access_cookies(response, token)
    except IntegrityError:
        flash("Username already exist", "danger")
        response = redirect(url_for("auth.sign_up"))
    return response


@auth.route("/logout")
@jwt_required()
def logout() -> Response:
    response: Response = redirect(url_for("auth.login"))
    unset_jwt_cookies(response)
    return response
