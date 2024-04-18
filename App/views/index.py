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
    return render_template("start.html")


@index.route("/delete_room", methods=["GET"])
@jwt_required()
def delete():
    return render_template("delete.html")


@index.route("/update_room_names/<room_name>/", methods=["GET"])  # add type
def update_room_view(room_name):
    room: Room | None = Room.query.filter_by(name=room_name).first()
    member: RoomMember = room.get_room_members()
    return render_template("_edit_room.html", room=room, member=member)


@index.route("/create_room", methods=["GET", "POST"])
@jwt_required()
def create_room():
    if request.method == "POST":
        room_name = request.form["room_name"]
        room = Room.query.filter_by(name=room_name).first()
        if room:
            flash("Room already exist", "danger")
        else:
            room_created = current_user.create_room(room_name)
            current_user.add_room_member(current_user.username, room_name, True)
            if room_created:
                return redirect(url_for("index.add_members"))

    return render_template("_create_room.html")


@index.route("/add_members", methods=["POST", "GET"])
@jwt_required()
def add_members():
    if request.method == "POST":
        room_name = request.form["room_name"]
        usernames1 = request.form["username"]
        room_admin = RoomMember.query.filter_by(
            member_name=current_user.username, room_name=room_name, is_room_admin=True
        ).first()
        room = Room.query.filter_by(name=room_name).first()
        if room and room_admin:
            if User.query.filter_by(username=usernames1).first():
                room_member = RoomMember.query.filter_by(
                    member_name=usernames1, room_name=room_name
                ).first()
                if room_member is None:
                    if usernames1 == current_user.username:
                        current_user.add_room_member(usernames1, room_name, True)
                        return redirect(url_for("index.chat"))
                    else:
                        current_user.add_room_member(usernames1, room_name, False)
                        return redirect(url_for("index.chat"))
                else:
                    flash(f"{usernames1} already in a room", "warning")
            else:
                flash(
                    f"{usernames1} is not a registered member..Register first", "danger"
                )
        else:
            flash("failed to add members", "danger")
    return render_template("add_room_member.html")


@index.route("/chat", methods=["GET"])
@jwt_required()
def chat():
    rooms = RoomMember.query.filter_by(member_name=current_user.username).all()
    return render_template("chat.html", rooms=rooms, current_user=current_user)


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


@index.route("/update_room_names/<room_name>/", methods=["PUT"])
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


@index.route("/delete_room/<room_name>", methods=["DELETE"])
@jwt_required()
def delete_room(room_name):
    room_admin = RoomMember.query.filter_by(
        member_name=current_user.username, room_name=room_name, is_room_admin=True
    ).first()
    if room_admin:
        current_user.delete_room(room_name)
        flash("Room successfully deleted", "danger")
    else:
        flash("Failed to delete room", "secondary")
    return jsonify("Deleted"), 200
