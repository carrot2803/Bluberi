from App.database import db


class Messages(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    username: str = db.Column(db.String(50), nullable=False)


class ChatMessage(db.Model):
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sender_name: str = db.Column(db.ForeignKey("user.username"), nullable=False)
    room_name: str = db.Column(db.ForeignKey("room.name"), nullable=False)
    message: str = db.Column(db.String(255), nullable=False)
    created_at: str = db.Column(db.String(20), nullable=False)

    def __init__(self, sender_name, room_name, message, created_at) -> None:
        self.sender_name: str = sender_name
        self.room_name: str = room_name
        self.message: str = message
        self.created_at: str = created_at
