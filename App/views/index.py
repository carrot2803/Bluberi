from flask_jwt_extended import jwt_required
from flask import Response, jsonify, render_template
from App.models import User
from flask import Blueprint


index = Blueprint("index", __name__)


@index.route("/", methods=["GET"])
def home() -> str:
    return render_template("index.html")


@index.route("/get_usernames", methods=["GET"])
@jwt_required()
def get_usernames() -> tuple[Response, int]:
    return jsonify(message=[user.username for user in User.query.all()]), 200
