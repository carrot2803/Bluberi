from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    set_access_cookies,
    unset_jwt_cookies,
)

from flask import Blueprint, render_template, redirect, request, url_for
from App.database import db
from App.models import User
from App.controllers import login_user
from werkzeug.wrappers import Response

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET"])
def login_page() -> str:
    return render_template("login.html")


@auth.route("/signup", methods=["GET"])
def sign_up_page() -> str:
    return render_template("signup.html")


@auth.route("/login", methods=["POST"])
def login() -> Response | str:
    data: dict[str, str] = request.form
    username: str | None = data.get("username")
    password: str | None = data.get("password")
    if not username or not password:
        return render_template("login.html", error="No data provided")
    token: str | None = login_user(username, password)
    if token is None:
        return render_template("login.html", error="Invalid Credentials")
    response: Response = redirect(url_for("chat.chat_page"))
    set_access_cookies(response, token)  # type: ignore
    return response


@auth.route("/signup", methods=["POST"])
def sign_up() -> Response | str:
    data: dict[str, str] = request.form
    email: str | None = data.get("email")
    username: str | None = data.get("username")
    password: str | None = data.get("password")
    if not username or not password or not email:
        return render_template("signup.html", error="No data provided")

    username_exist: User | None = User.query.filter_by(username=username).first()
    email_exist: User | None = User.query.filter_by(email=email).first()
    if username_exist or email_exist:
        return render_template("signup.html", error="Username/Email Already Exist")

    user = User(username, email, password)
    db.session.add(user)
    db.session.commit()
    token: str = create_access_token(identity=user)
    response: Response = redirect(url_for("chat.chat_page"))
    set_access_cookies(response, token)  # type: ignore
    return response


@auth.route("/logout", methods=["GET"])
@jwt_required()
def logout() -> Response:
    response: Response = redirect(url_for("auth.login"))
    unset_jwt_cookies(response)  # type: ignore
    return response
