import datetime
from flask_jwt_extended import current_user, jwt_required
from flask_socketio import SocketIO, send, join_room
from App.models import Room

socket = SocketIO(cors_allowed_origins="*")


@socket.on("incoming-msg")
@jwt_required()
def on_message(data) -> None:
    room_name = data.get("room")
    room: Room | None = Room.query.filter_by(name=room_name).first()
    if not room:
        return
    users_rooms = room.get_room_members()
    if not users_rooms:
        return
    for members in users_rooms:
        msg = data["msg"]
        if members.member_name == current_user.username:
            message = current_user.send_message(room.name, msg)
            if message:
                send({"username": current_user.username, "msg": msg, "time": message.created_at, "sender_id": current_user.id}, room=room.name)  # type: ignore


@socket.on("join")
@jwt_required()
def on_join(data) -> None:
    room_name = data.get("room")
    room: Room | None = Room.query.filter_by(name=room_name).first()
    if room is None:
        return
    room_name: str = room.name
    join_room(room_name)
    time: str = datetime.now().strftime("%H:%M")  # type: ignore
    send(
        {
            "username": current_user.username,
            "msg": "has came to online",
            "time": time,
        },  # type: ignore
        room=room_name,
    )
    print("message got sent")
