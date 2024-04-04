from datetime import datetime

from flask_sqlalchemy.query import Query

from models import Rooms, RoomMembers, StoringMessages, User, db


def save_messages(username, room_name, message, created_at):  # big hook
    message = StoringMessages(
        sender_name=username,
        room_name=room_name,
        message=message,
        created_at=created_at,
    )
    if message:
        db.session.add(message)
        db.session.commit()
        return message
    else:
        return None


def add_room_member(room_name, usernames, added_by, is_room_admin):  # big hook
    roommembers = RoomMembers(
        member_name=usernames,
        room_name=room_name,
        added_by=added_by,
        added_at=datetime.now(),
        is_room_admin=is_room_admin,
    )
    db.session.add(roommembers)
    db.session.commit()


def add_room_members(room_name, username, added_by):  # big hook
    bulk = RoomMembers(
        member_name=username,
        room_name=room_name,
        added_by=added_by,
        added_at=datetime.now(),
        is_room_admin=False,
    )
    db.session.add(bulk)
    db.session.commit()


def is_room_member(member_name, room_name):  # big hook
    isroommember = RoomMembers.query.filter_by(
        member_name=member_name, room_name=room_name
    ).first()
    if isroommember:
        return isroommember
    else:
        return None


def get_room(room_name):
    room_names = Rooms.query.filter_by(room_name=room_name).first()
    if room_names:
        return room_names
    else:
        return None


def get_rooms_for_users(username) -> Query:
    rooms: Query = RoomMembers.query.filter_by(member_name=username)
    return rooms


def get_room_members(room_name) -> Query:
    rooms: Query = RoomMembers.query.filter_by(room_name=room_name)
    return rooms


def is_room_admin_1(room_name, member_name):
    return RoomMembers.query.filter_by(
        room_name=room_name, member_name=member_name, is_room_admin=True
    ).first()


def updated_room(old_room_name, new_room_name):
    rooms = Rooms.query.filter_by(room_name=old_room_name).update(
        {Rooms.room_name: new_room_name}
    )
    if rooms:
        db.session.commit()
        return rooms
    else:
        return None


def update_members_room(old_members_room, new_members_room):
    old_member_room = RoomMembers.query.filter_by(room_name=old_members_room).update(
        {RoomMembers.room_name: new_members_room}
    )
    if old_member_room:
        db.session.commit()
        return old_member_room
    else:
        return None


def updated_room_members(old_member_name, new_member_names):
    for new_names in new_member_names:
        return RoomMembers.query.filter_by(member_name=old_member_name).update(
            {RoomMembers.member_name: new_names}
        )


def remove_rooms(room_name):
    deleted_room = Rooms.query.filter_by(room_name=room_name).delete()
    if deleted_room:
        db.session.commit()
        RoomMembers.query.filter_by(room_name=room_name).delete()
        db.session.commit()
        StoringMessages.query.filter_by(room_name=room_name).delete()
        db.session.commit()
        return deleted_room
    else:
        return None


def get_messages(room_name):
    return StoringMessages.query.filter_by(room_name=room_name)


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
