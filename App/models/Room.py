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

    def get_room_members(self):
        return self.members

    def get_messages(self):
        return self.messages
