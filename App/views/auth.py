from sqlite3 import IntegrityError
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    set_access_cookies,
    unset_jwt_cookies,
)
from flask import Blueprint, render_template, redirect, request, url_for, flash
from App.database import db
from App.models import User

auth = Blueprint("auth", __name__)


def login_user(username: str, password: str):
    user: User | None = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        token: str = create_access_token(identity=user)
        return token
    return None


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["user_name"]
        password = request.form["pass_word"]
        token = login_user(username, password)
        if token is None:
            flash("Invalid Credintials", "danger")
            response = redirect(url_for("auth.login"))
        else:
            flash("Login was successful", "success")
            response = redirect(url_for("index.get_rooms"))
        set_access_cookies(response, token)
        return response

    return render_template("login.html")


@auth.route("/signup", methods=["POST", "GET"])
def sign_up():
    if request.method == "POST":
        try:
            username = request.form["user_username"]
            password = request.form["user_password"]
            email = request.form["Email"]
            user = User(username, email, password)
            db.session.add(user)
            db.session.commit()
            response = redirect(url_for("auth.login"))
            token = create_access_token(identity=user)
            set_access_cookies(response, token)
        except IntegrityError:
            flash("Username already exist", "danger")
            response = redirect(url_for("auth.sign_up"))
        return response

    return render_template("signup.html")


@auth.route("/logout")
@jwt_required()
def logout():
    response = redirect(url_for("auth.login"))
    unset_jwt_cookies(response)
    flash("Logged out")
    return response
