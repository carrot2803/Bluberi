from datetime import datetime
from typing import Any
from werkzeug.security import generate_password_hash, check_password_hash
from App.database import db
from App.models.Room import Room, RoomMember
from App.models.Messages import StoringMessages


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(60), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, username, email, password) -> None:
        self.username = username
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def create_room(self, room_name):
        new_room = Room(room_name, self.username, datetime.now())
        if new_room is None:
            return False
        db.session.add(new_room)
        db.session.commit()
        return True

    def update_room(self, old_room_name, new_room_name):
        room = Room.query.filter_by(room_name=old_room_name).first()
        if room is None:
            return False
        room.room_name = new_room_name
        RoomMember.query.filter_by(room_name=old_room_name).update(
            {RoomMember.room_name: new_room_name}
        )
        db.session.commit()
        return True

    def delete_room(self, room_name) -> bool:
        room: Room | None = Room.query.filter_by(room_name=room_name).first()
        if room is None:
            return False
        db.session.delete(room)
        db.session.commit()
        return True

    def send_message(self, room_name, message) -> StoringMessages | None:
        new_message = StoringMessages(
            self.username, room_name, message, datetime.now().strftime("%H:%M:%S")
        )
        if new_message is None:
            return None
        db.session.add(new_message)
        db.session.commit()
        return new_message

    def add_room_member(self, member_name, room_name, is_room_admin) -> None:
        room_member = RoomMember(
            member_name,
            room_name,
            self.username,
            is_room_admin,
            datetime.now().strftime("%H:%M:%S"),
        )
        db.session.add(room_member)
        db.session.commit()
