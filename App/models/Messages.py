from App.database import db


class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)


class StoringMessages(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sender_name = db.Column(db.String(50), nullable=False)
    room_name = db.Column(db.ForeignKey("room.room_name"), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.String(20), nullable=False)

    def __init__(self, sender_name, room_name, message, created_at):
        self.sender_name = sender_name
        self.room_name = room_name
        self.message = message
        self.created_at = created_at
