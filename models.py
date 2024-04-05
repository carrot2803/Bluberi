from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.query import Query
from sqlalchemy import Column, String, Integer, ForeignKey
from flask_login import UserMixin
from werkzeug.security import generate_password_hash


db = SQLAlchemy()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(60), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, username, email, password) -> None:
        self.username = username
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        self.password = generate_password_hash(password, method="scrypt")

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
        ) #  move this into rooms? actually idk  ifto
        if rooms_updated is None:
            return False
        db.session.commit()
        return True

    def delete_room(self, room_name) -> bool:
        room = Rooms.query.filter_by(room_name=room_name).first()
        if room is None:
            return False
        db.session.delete(room)
        RoomMembers.query.filter_by(room_name=room_name).delete()  # prob move this into rooms
        StoringMessages.query.filter_by(room_name=room_name).delete() # move this into rooms
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


class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)


class Rooms(db.Model):
    room_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    room_name = db.Column(db.String(50), nullable=False, unique=False)
    created_by = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.String(40), nullable=False)

    def __init__(self, room_name, created_by, created_at):
        self.room_name = room_name
        self.created_by = created_by
        self.created_at = created_at

    def get_room_members(self) -> Query:
        return RoomMembers.query.filter_by(room_name=self.room_name)

    def get_room(room_name):
        return Rooms.query.filter_by(room_name=room_name).first()

    def get_messages(room_name):
        return StoringMessages.query.filter_by(room_name=room_name)


class RoomMembers(db.Model):
    member_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    member_name = db.Column(db.String(50), nullable=False, unique=False)
    room_name = db.Column(db.String(50), nullable=False, unique=False)
    added_by = db.Column(db.String(50), nullable=False)
    is_room_admin = db.Column(db.String(10), nullable=False)
    added_at = db.Column(db.String(40), nullable=False)

    def __init__(self, member_name, room_name, added_by, is_room_admin, added_at):
        self.member_name = member_name
        self.room_name = room_name
        self.added_by = added_by
        self.is_room_admin = is_room_admin
        self.added_at = added_at


class StoringMessages(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sender_name = db.Column(db.String(50), nullable=False)
    room_name = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.String(20), nullable=False)

    def __init__(self, sender_name, room_name, message, created_at):
        self.sender_name = sender_name
        self.room_name = room_name
        self.message = message
        self.created_at = created_at


# temp class remove ltr
class User_login:
    def __init__(self, id, username, email, password):
        self.id = id
        self.username = username
        self.email = email
        self.password = password

    def is_authenticated(self):
        return True

    def is_anonimous(self):
        return False

    def is_active(self):
        return True

    def get_id(self):
        return self.username

    def check_password(self, password_input):
        return True
