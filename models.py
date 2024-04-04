from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, ForeignKey
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

db = SQLAlchemy()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(60), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    friends = db.relationship("Friends", backref="user")

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = self.generate_password_hash(password)

    def generate_password_hash(self, password):
        return generate_password_hash(password)

    def create_room(self, room_name):
        new_room = Rooms(room_name, self.username, datetime.now())
        if new_room is None:
            return False
        db.session.add(new_room)
        db.session.commit()
        return True

    def send_message(self, room_name, message):
        new_message = StoringMessages(
            self.username, room_name, message, created_at=datetime.now()
        )
        if new_message:
            return None
        db.session.add(new_message)
        db.session.commit()
        return new_message


class Friends(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    friend_name = db.Column(db.String(50), nullable=True)
    added_by = db.Column(db.String(50), nullable=False)
    # change to id ltr
    user_email = db.Column(db.String(50), db.ForeignKey("user.email"))


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


class RoomMembers(db.Model):
    member_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    member_name = db.Column(db.String(50), nullable=False, unique=False)
    room_name = db.Column(db.String(50), nullable=False, unique=False)
    added_by = db.Column(db.String(50), nullable=False)
    is_room_admin = db.Column(db.String(10), nullable=False)
    added_at = db.Column(db.String(40), nullable=False)


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
