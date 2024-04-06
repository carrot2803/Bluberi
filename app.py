from datetime import datetime
from operator import is_
from flask_login import (
    LoginManager,
    login_required,
    login_user,
    logout_user,
    current_user,
)
from flask import (
    Flask,
    jsonify,
    render_template,
    redirect,
    request,
    url_for,
    flash,
    session,
)
from flask_socketio import SocketIO, send, join_room, emit
from models import RoomMembers, Rooms, User, User_login, db


app = Flask(__name__)

# database config
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
app.config["SECRET_KEY"] = "felicia is an egg"
socketio = SocketIO(app, cors_allowed_origins="*")

# login config
loginmanager = LoginManager(app)
loginmanager.init_app(app)
loginmanager.login_view = "login"
loginmanager.login_message = "Login to Access that page"
loginmanager.login_message_category = "danger"

users = {}


@loginmanager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("start.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["user_name"]
        password_input = request.form["pass_word"]
        if username and password_input is not None:
            user = User.query.filter_by(username=username).first()
            if user is not None:
                test_user_data = User.query.filter_by(username=username).first()
                user_models = User_login(
                    test_user_data.id,
                    test_user_data.username,
                    test_user_data.email,
                    test_user_data.password,
                )
                password = user_models.check_password(password_input)
                if password:
                    login_user(test_user_data)
                    flash("login successfull", "success")
                    return redirect(url_for("get_rooms"))
                else:
                    flash("password is incorrect", "danger")
            else:
                flash("Invalid Credintials", "danger")
        else:
            flash("username and password not met", "danger")

    return render_template("login.html")


@app.route("/signup", methods=["POST", "GET"])
def sign_up():
    if request.method == "POST":
        username = request.form["user_username"]
        password = request.form["user_password"]
        email = request.form["Email"]
        print(email)
        print(username)
        print("Password here", password)

        user = User.query.filter_by(username=username).first()
        if user is None:
            new_user = User(username, email, password)
            db.session.add(new_user)
            db.session.commit()
            flash("user successfully added", "success")

        else:
            flash("user already exist", "danger")

    return render_template("signup.html")


@app.route("/chat", methods=["GET", "POST"])
def chat():
    return render_template("_chat_app.html", username=session.get("username"))


@app.route("/create_room", methods=["GET", "POST"])
@login_required
def create_room():
    if request.method == "POST":
        room_name = request.form["room_name"]
        if Rooms.get_room(room_name):
            flash("Room already exist", "danger")
        else:
            room_created = current_user.create_room(room_name)
            current_user.add_room_member(current_user.username, room_name, True)
            if room_created:
                return redirect(
                    url_for(
                        "add_members",
                    )
                )

    return render_template("_create_room.html")


@app.route("/add_members", methods=["POST", "GET"])
@login_required
def add_members():
    if request.method == "POST":
        room_name = request.form["room_name"]
        usernames1 = request.form["usernames"]
        room_admin = RoomMembers.query.filter_by(
            member_name=current_user.username, room_name=room_name, is_room_admin=True
        ).first()
        if Rooms.get_room(room_name) and room_admin:
            if User.query.filter_by(username=usernames1).first():
                room_member = RoomMembers.query.filter_by(
                    member_name=usernames1, room_name=room_name
                ).first()
                if room_member is None:
                    if usernames1 == current_user.username:
                        current_user.add_room_member(usernames1, room_name, True)
                        return redirect(url_for("get_rooms"))
                    else:
                        current_user.add_room_member(usernames1, room_name, False)
                        return redirect(url_for("get_rooms"))
                else:
                    flash(f"{usernames1} already in a room", "warning")
            else:
                flash(
                    f"{usernames1} is not a registered member..Register first", "danger"
                )
        else:
            flash("failed to add members", "danger")
    return render_template("add_room_member.html")


@app.route("/get_rooms", methods=["GET", "POST"])
@login_required
def get_rooms():
    if request.method == "GET":
        room = RoomMembers.query.filter_by(member_name=current_user.username)
        return render_template("_get_rooms.html", rooms=room)
    else:
        flash("you are not a member of any room", "warning")
    return render_template("_get_rooms.html")


@app.route("/view_room/<room_name>/", methods=["GET"])
@login_required
def view_room(room_name):
    room = Rooms.get_room(room_name)
    room_member = RoomMembers.query.filter_by(
        member_name=current_user.username, room_name=room_name
    ).first()
    if room and room_member:
        messages = Rooms.get_messages(room_name)
        room_members = room.get_room_members()
        return render_template(
            "_view_room.html", room=room, room_members=room_members, messages=messages
        )
    else:
        flash(
            f"You are not a member of this group {room_name} please go back ", "warning"
        )
        return render_template("error.html")


@app.route("/update_room_names/<room_name>/", methods=["GET"])  # add type
def update_room_view(room_name):
    rooms = Rooms.get_room(room_name)
    member = rooms.get_room_members()
    return render_template("_edit_room.html", rooms=rooms, member=member)


@app.route("/update_room_names/<room_name>/", methods=["PUT"])
@login_required
def update_room_names(room_name):
    rooms = Rooms.get_room(room_name)
    member = rooms.get_room_members()
    data = request.get_json()
    new_room_name = data["new_room_name"]
    room_admin = RoomMembers.query.filter_by(
        member_name=current_user.username, room_name=room_name, is_room_admin=True
    ).first()
    if room_admin:
        room_updated = current_user.update_room(room_name, new_room_name)
        if room_updated:
            flash("Successfully updated room name and members room names", "success")
            return jsonify("Updated"), 200
        else:
            flash("Failed to update members room name and room names", "danger")
    else:
        flash("You are not an admin of this group", "warning")


@app.route("/delete_room", methods=["GET"])
@login_required
def delete():
    return render_template("delete.html")


@app.route("/delete_room/<room_name>", methods=["DELETE"])
@login_required
def delete_room(room_name):
    room_admin = RoomMembers.query.filter_by(
        member_name=current_user.username, room_name=room_name, is_room_admin=True
    ).first()
    if room_admin:
        current_user.delete_room(room_name)
        flash("Room successfully deleted", "danger")
    else:
        flash("Failed to delete room", "secondary")
    return jsonify("Deleted"), 200


# group chat
@socketio.on("incoming-msg")
def on_message(data):
    rooms = Rooms.get_room(data["room"])
    if rooms:
        users_rooms = rooms.get_room_members()
        if users_rooms:
            for members in users_rooms:
                msg = data["msg"]
                if members.member_name == current_user.username:
                    room = rooms.room_name
                    message = current_user.send_message(room, msg)
                    if message:
                        print("message saved")
                        print(message.created_at)
                        send(
                            {
                                "username": current_user.username,
                                "msg": msg,
                                "time": message.created_at,
                            },
                            room=room,
                        )
                    else:
                        print("Something went wrong")
    else:
        return "message not sent"


@socketio.on("join")
def on_join(data):
    rooms = Rooms.get_room(data["room"])
    if rooms:
        room = rooms.room_name
        join_room(room)
        now = datetime.now().strftime("%H:%M:%S")
        time_stamp = now
        send(
            {
                "username": current_user.username,
                "msg": "has came to online",
                "time": time_stamp,
            },
            room=room,
        )
        print("message got sent")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("successfully logged out", "success")
    return redirect(url_for("login"))


if __name__ == "__main__":
    socketio.run(app, debug=True)
