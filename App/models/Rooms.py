from App.database import db
from App.models.Messages import StoringMessages


class Rooms(db.Model):
    room_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    room_name = db.Column(db.String(50), nullable=False, unique=False)
    created_by = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.String(40), nullable=False)

    def __init__(self, room_name, created_by, created_at):
        self.room_name = room_name
        self.created_by = created_by
        self.created_at = created_at

    def get_room_members(self):
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
