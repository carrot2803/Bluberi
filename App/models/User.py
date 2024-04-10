from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from App.database import db
from App.models.Rooms import Rooms, RoomMembers, StoringMessages


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
        # self.password = generate_password_hash(password, method="scrypt")

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def create_room(self, room_name):
        new_room = Rooms(room_name, self.username, datetime.now())
        if new_room is None:
            return False
        db.session.add(new_room)
        db.session.commit()
        return True

    def update_room(self, old_room_name, new_room_name):
        room = Rooms.query.filter_by(room_name=old_room_name).first()
        if room is None:
            return False
        room.room_name = new_room_name
        rooms_updated = RoomMembers.query.filter_by(room_name=old_room_name).update(
            {RoomMembers.room_name: new_room_name}
        )  #  move this into rooms? actually idk  ifto
        if rooms_updated is None:
            return False
        db.session.commit()
        return True

    def delete_room(self, room_name) -> bool:
        room = Rooms.query.filter_by(room_name=room_name).first()
        if room is None:
            return False
        db.session.delete(room)
        RoomMembers.query.filter_by(
            room_name=room_name
        ).delete()  # prob move this into rooms
        StoringMessages.query.filter_by(
            room_name=room_name
        ).delete()  # move this into rooms
        db.session.commit()
        return True

    def send_message(self, room_name, message):
        new_message = StoringMessages(
            self.username, room_name, message, datetime.now().strftime("%H:%M:%S")
        )
        if new_message is None:
            return None
        db.session.add(new_message)
        db.session.commit()
        return new_message

    def add_room_member(self, member_name, room_name, is_room_admin):
        room_member = RoomMembers(
            member_name,
            room_name,
            self.username,
            is_room_admin,
            datetime.now().strftime("%H:%M:%S"),
        )
        db.session.add(room_member)
        db.session.commit()
