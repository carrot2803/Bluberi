from App.database import db
from App.models.ChatMessage import ChatMessage


class RoomMember(db.Model):
    member_id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    room_name: str = db.Column(db.ForeignKey("room.name"))
    member_name: str = db.Column(db.ForeignKey("user.username"))
    added_by: str = db.Column(db.String(50), nullable=False)
    is_room_admin = db.Column(db.String(10), nullable=False)
    added_at: str = db.Column(db.String(40), nullable=False)

    def __init__(self, member_name, room_name, added_by, is_room_admin, added_at):
        self.member_name: str = member_name
        self.room_name: str = room_name
        self.added_by: str = added_by
        self.is_room_admin = is_room_admin
        self.added_at: str = added_at

    def get_last_message(self):
        last_message = (
            ChatMessage.query.filter_by(room_name=self.room_name)
            .order_by(ChatMessage.created_at.desc())  # type: ignore
            .first()
        )
        return last_message

    def get_num_messages(self) -> int:
        return ChatMessage.query.filter_by(room_name=self.room_name).count()
