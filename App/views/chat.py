from flask import Response, jsonify, render_template, request
from flask_jwt_extended import current_user, jwt_required
from App.models import RoomMember, Room, ChatMessage
from flask import Blueprint

chat = Blueprint("chat", __name__)


@chat.route("/chat", methods=["GET"])
@jwt_required()
def chat_page() -> str:
    rooms: list = RoomMember.query.filter_by(member_name=current_user.username).all()
    return render_template("chat.html", rooms=rooms, current_user=current_user)


@chat.route("/chat/<string:room_name>", methods=["GET"])
@jwt_required()
def chat_room(room_name) -> str:
    room: Room | None = Room.query.filter_by(name=room_name).first()
    room_member: RoomMember | None = RoomMember.query.filter_by(
        member_name=current_user.username, room_name=room_name
    ).first()
    if room is None or room_member is None:
        return render_template("error.html")
    messages: list = ChatMessage.query.filter_by(room_name=room.name).all()
    rooms: list = RoomMember.query.filter_by(member_name=current_user.username).all()
    return render_template(
        "chat.html",
        rooms=rooms,
        room=room,
        room_members=room.get_room_members(),
        messages=messages,
        current_user=current_user,
    )


@chat.route("/chat/<string:room_name>/add_member", methods=["POST"])
@jwt_required()
def add_member(room_name) -> tuple[Response, 200 | 400]:
    data: dict = request.get_json()
    if not data:
        return jsonify("No data provided"), 400
    username: str | None = data.get("username")
    is_room_admin: RoomMember | None = RoomMember.query.filter_by(
        member_name=current_user.username, room_name=room_name, is_room_admin=True
    ).first()
    room: Room | None = Room.query.filter_by(name=room_name).first()
    if not room:
        return jsonify("Room not found"), 400
    if not is_room_admin:
        return jsonify("You are not an admin of this group"), 400
    is_member: RoomMember | None = RoomMember.query.filter_by(
        member_name=username, room_name=room_name
    ).first()
    if is_member:
        return jsonify("User already in room"), 400
    current_user.add_room_member(username, room_name, False)
    return jsonify("User added to room"), 200


@chat.route("/chat/<string:room_name>", methods=["POST"])
@jwt_required()
def create_chat(room_name) -> tuple[Response, 200 | 400]:
    room_exist: Room | None = Room.query.filter_by(name=room_name).first()
    if room_exist:
        return jsonify("Room already exist"), 400
    room_created: bool = current_user.create_room(room_name)
    if room_created is False:
        return jsonify("Failed to create room"), 400
    return jsonify("Room created"), 200


@chat.route("/chat/<room_name>", methods=["PUT"])
@jwt_required()
def update_room_names(room_name) -> tuple[Response, 200 | 400]:
    data: dict = request.get_json()
    new_room_name: str = data.get("new_room_name")
    room_admin: RoomMember | None = RoomMember.query.filter_by(
        member_name=current_user.username, room_name=room_name, is_room_admin=True
    ).first()
    if room_admin is None:
        return jsonify("You are not an admin of this group"), 400
    room_updated: bool = current_user.update_room(room_name, new_room_name)
    if room_updated is False:
        return jsonify("Failed to update room name"), 400
    return jsonify("Room name updated"), 200


@chat.route("/chat/<string:room_name>", methods=["DELETE"])
@jwt_required()
def delete_room(room_name) -> tuple[Response, 200 | 400]:
    room_admin: RoomMember | None = RoomMember.query.filter_by(
        member_name=current_user.username, room_name=room_name, is_room_admin=True
    ).first()
    if room_admin is None:
        return jsonify("You are not an admin of this group"), 400
    current_user.delete_room(room_name)
    return jsonify("Deleted"), 200
