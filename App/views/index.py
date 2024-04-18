from flask_jwt_extended import current_user, jwt_required
from flask import (
    jsonify,
    render_template,
    redirect,
    request,
    url_for,
    flash,
)
from werkzeug import Response
from App.models import RoomMember, Room, User
from flask import Blueprint

from App.models.Messages import ChatMessage


index = Blueprint("index", __name__)


@index.route("/", methods=["GET", "POST"])
def home() -> str:
    return render_template("index.html")


@index.route("/chat/<string:room_name>", methods=["POST"])
@jwt_required()
def create_chat(room_name):
    room_exist = Room.query.filter_by(name=room_name).first()
    if room_exist:
        return jsonify("Room already exist"), 400
    room_created = current_user.create_room(room_name)
    if room_created is False:
        return jsonify("Failed to create room"), 400
    return jsonify("Room created"), 200


@index.route("/chat/<string:room_name>/add_member", methods=["POST"])
@jwt_required()
def add_member(room_name):
    data = request.get_json()
    username = data.get("username")
    is_room_admin = RoomMember.query.filter_by(
        member_name=current_user.username, room_name=room_name, is_room_admin=True
    ).first()
    room = Room.query.filter_by(name=room_name).first()
    if not room:
        return jsonify("Room not found"), 400
    if not is_room_admin:
        return jsonify("You are not an admin of this group"), 400
    is_member = RoomMember.query.filter_by(
        member_name=username, room_name=room_name
    ).first()
    if is_member:
        return jsonify("User already in room"), 400
    current_user.add_room_member(username, room_name, False)
    return jsonify("User added to room"), 200


@index.route("/chat", methods=["GET"])
@jwt_required()
def chat():
    rooms = RoomMember.query.filter_by(member_name=current_user.username).all()
    return render_template("chat.html", rooms=rooms, current_user=current_user)


@index.route("/get_usernames", methods=["GET"])
def get_usernames():
    return jsonify(message=[user.username for user in User.query.all()]), 200


@index.route("/chat/<string:room_name>", methods=["GET"])
@jwt_required()
def chat_room(room_name):
    room = Room.query.filter_by(name=room_name).first()
    room_member = RoomMember.query.filter_by(
        member_name=current_user.username, room_name=room_name
    ).first()
    rooms = RoomMember.query.filter_by(member_name=current_user.username).all()

    if room and room_member:
        messages = ChatMessage.query.filter_by(room_name=room.name).all()
        print(room_name)
        print(messages)
        room_members = room.get_room_members()
        return render_template(
            "chat.html",
            rooms=rooms,
            room=room,
            room_members=room_members,
            messages=messages,
            current_user=current_user,
        )
    else:
        flash(
            f"You are not a member of this group {room_name} please go back ", "warning"
        )
        return render_template("error.html")


@index.route("/chat/<room_name>", methods=["PUT"])
@jwt_required()
def update_room_names(room_name):
    rooms = Room.query.filter_by(name=room_name).first()
    member = rooms.get_room_members()
    data = request.get_json()
    new_room_name = data["new_room_name"]
    room_admin = RoomMember.query.filter_by(
        member_name=current_user.username, room_name=room_name, is_room_admin=True
    ).first()
    if room_admin:
        room_updated = current_user.update_room(room_name, new_room_name)
        if room_updated:
            flash("Successfully updated room name and members room names", "success")
            return jsonify("Updated"), 200
        else:
            flash("Failed to update members room name and room names", "danger")
    else:
        flash("You are not an admin of this group", "warning")


@index.route("/chat/<string:room_name>", methods=["DELETE"])
@jwt_required()
def delete_room(room_name):
    room_admin = RoomMember.query.filter_by(
        member_name=current_user.username, room_name=room_name, is_room_admin=True
    ).first()
    if room_admin is None:
        return jsonify("Failed to delete room"), 400
    current_user.delete_room(room_name)
    return jsonify("Deleted"), 200
