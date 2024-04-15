from typing import Any
from sqlalchemy.orm.relationships import RelationshipProperty
from App.database import db


class Room(db.Model):
    room_id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    room_name: str = db.Column(db.String(50), nullable=False, unique=True)
    created_by: str = db.Column(db.String(50), nullable=False)
    created_at: str = db.Column(db.String(40), nullable=False)
    members = db.relationship(
        "RoomMember", backref="room", lazy="dynamic", cascade="all, delete-orphan"
    )
    messages = db.relationship(
        "ChatMessage", backref="room", lazy="dynamic", cascade="all, delete-orphan"
    )

    def __init__(self, room_name: str, created_by: str, created_at: str) -> None:
        self.room_name: str = room_name
        self.created_by: str = created_by
        self.created_at: str = created_at

    def get_room_members(self) -> RelationshipProperty[Any]:
        return self.members

    def get_messages(self) -> RelationshipProperty[Any]:
        return self.messages


class RoomMember(db.Model):
    member_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    room_name = db.Column(db.ForeignKey("room.room_name"))
    member_name = db.Column(db.ForeignKey("user.username"))
    added_by = db.Column(db.String(50), nullable=False)
    is_room_admin = db.Column(db.String(10), nullable=False)
    added_at = db.Column(db.String(40), nullable=False)

    def __init__(self, member_name, room_name, added_by, is_room_admin, added_at):
        self.member_name = member_name
        self.room_name = room_name
        self.added_by = added_by
        self.is_room_admin = is_room_admin
        self.added_at = added_at
