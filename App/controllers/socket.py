import datetime
from flask_jwt_extended import current_user, jwt_required
from flask_socketio import SocketIO, send, join_room
from App.models import Room

socket = SocketIO(cors_allowed_origins="*")


@socket.on("incoming-msg")
@jwt_required()
def on_message(data):
    room_name = data.get("room")
    rooms = Room.query.filter_by(name=room_name).first()
    if rooms:
        users_rooms = rooms.get_room_members()
        if users_rooms:
            for members in users_rooms:
                msg = data["msg"]
                if members.member_name == current_user.username:
                    room = rooms.name
                    message = current_user.send_message(room, msg)
                    if message:
                        print("message saved")
                        print(message.created_at)
                        send(
                            {
                                "username": current_user.username,
                                "msg": msg,
                                "time": message.created_at,
                            },
                            room=room,
                        )
                    else:
                        print("Something went wrong")
    else:
        return "message not sent"


@socket.on("join")
@jwt_required()
def on_join(data) -> None:
    room_name = data.get("room")
    room: Room | None = Room.query.filter_by(name=room_name).first()
    if room is None:
        return
    room_name: str = room.name
    join_room(room_name)
    time: str = datetime.now().strftime("%H:%M:%S")
    send(
        {
            "username": current_user.username,
            "msg": "has came to online",
            "time": time,
        },
        room=room_name,
    )
    print("message got sent")