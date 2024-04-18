from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from App.database import db
from App.models.Room import Room
from App.models.RoomMember import RoomMember
from App.models.Messages import ChatMessage


class User(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    username: str = db.Column(db.String(50), nullable=False)
    email: str = db.Column(db.String(60), nullable=False, unique=True)
    password: str = db.Column(db.String(100), nullable=False)

    def __init__(self, username: str, email: str, password: str) -> None:
        self.username = username
        self.email = email
        self.set_password(password)

    def create_room(self, room_name: str) -> bool:
        new_room = Room(room_name, self.username, datetime.now())
        if new_room is None:
            return False
        db.session.add(new_room)
        db.session.commit()
        return True

    def update_room(self, old_room_name: str, new_room_name: str) -> bool:
        room: Room | None = Room.query.filter_by(name=old_room_name).first()
        if room is None:
            return False
        room.name = new_room_name
        RoomMember.query.filter_by(room_name=old_room_name).update(
            {RoomMember.room_name: new_room_name}
        )
        ChatMessage.query.filter_by(room_name=old_room_name).update(
            {ChatMessage.room_name: new_room_name}
        )
        db.session.commit()
        return True

    def delete_room(self, room_name: str) -> bool:
        room: Room | None = Room.query.filter_by(name=room_name).first()
        if room is None:
            return False
        db.session.delete(room)
        db.session.commit()
        return True

    def send_message(self, room_name: str, message: str) -> ChatMessage | None:
        new_message = ChatMessage(
            self.id,
            self.username,
            room_name,
            message,
            datetime.now().strftime("%H:%M:%S"),
        )
        if new_message is None:
            return None
        db.session.add(new_message)
        db.session.commit()
        return new_message

    def add_room_member(self, member_name: str, room_name: str, is_room_admin) -> None:
        room_member = RoomMember(
            member_name,
            room_name,
            self.username,
            is_room_admin,
            datetime.now().strftime("%H:%M:%S"),
        )
        db.session.add(room_member)
        db.session.commit()

    def set_password(self, password: str) -> None:
        self.password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)
