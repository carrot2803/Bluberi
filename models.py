from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

db = SQLAlchemy()


class User(UserMixin, db.Model):
    id = Column("id", Integer, primary_key=True)
    username = Column("username", String(50), nullable=False)
    email = Column("email", String(60), nullable=False, unique=True)
    password = Column("password", String(100), nullable=False)
    SessionId = Column(
        "SessionId", String(50), unique=True, default="asdsadadasd1232eqwdsadsa"
    )
    friends = db.relationship("Friends", backref="friends")

    def __init__(self, username, email, password, SessionId):
        self.username = username
        self.email = email
        self.password = password
        self.SessionId = SessionId
        self.generate_password_hash(password)

    def generate_password_hash(self, password):
        return  # fix with testing


class Friends(UserMixin, db.Model):
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    friend_name = Column("friend_name", String(50), nullable=True)
    added_by = Column("added_by", String(50), nullable=False)
    User_email = Column("user_email", String(50), db.ForeignKey("user.email"))


class messages(db.Model):  # fake messagesm maybe
    id = Column("id", Integer, primary_key=True)
    username = Column("username", String(50), nullable=False)
    SessionId = Column("SessionId", String(50), unique=True, default="123")


class Rooms(UserMixin, db.Model):
    room_id = Column("room_id", Integer, primary_key=True, autoincrement=True)
    room_name = Column("room_name", String(50), nullable=False, unique=False)
    created_by = Column("created_by", String(50), nullable=False)
    created_at = Column("created_at", String(40), nullable=False)


class Room_members(UserMixin, db.Model):
    member_id = Column("member_id", Integer, primary_key=True, autoincrement=True)
    member_name = Column("member_name", String(50), nullable=False, unique=False)
    room_name = Column("room_name", String(50), nullable=False, unique=False)
    added_by = Column("added_by", String(50), nullable=False)
    is_room_admin = Column("is_room_admin", String(10), nullable=False)
    added_at = Column("added_at", String(40), nullable=False)


class Storing_messages(UserMixin, db.Model):
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    sender_name = Column("sender_name", String(50), nullable=False)
    room_name = Column("room_name", String(50), nullable=False)
    message = Column("message", String(255), nullable=False)
    created_at = Column("created_at", String(20), nullable=False)


def main():
    User()
    Friends()
    messages()
    Rooms()
    Room_members()
    Storing_messages()


if __name__ == "__main__":
    main()
