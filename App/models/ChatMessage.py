from App.database import db


class ChatMessage(db.Model):
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sender_id: int = db.Column(db.ForeignKey("user.id"), nullable=False)
    sender_name: str = db.Column(db.ForeignKey("user.username"), nullable=False)
    room_name: str = db.Column(db.ForeignKey("room.name"), nullable=False)
    message: str = db.Column(db.String(255), nullable=False)
    created_at: str = db.Column(db.String(20), nullable=False)

    def __init__(self, sender_id, sender_name, room_name, message, created_at) -> None:
        self.sender_id: int = sender_id
        self.sender_name: str = sender_name
        self.room_name: str = room_name
        self.message: str = message
        self.created_at: str = created_at
