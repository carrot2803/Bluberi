from datetime import datetime
from flask_login import (
    LoginManager,
    login_required,
    login_user,
    logout_user,
    current_user,
)
from flask import Flask, render_template, redirect, request, url_for, flash, session
from flask_socketio import SocketIO, send, join_room, emit
from models import User, db
from hooks import (
    User_login,
    get_user,
    save_rooms,
    add_room_member,
    get_room,
    get_rooms_for_users,
    is_room_member,
    get_room_members,
    is_room_admin_1,
    updated_room,
    update_members_room,
    remove_rooms,
    save_messages,
    get_messages,
)

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
loginmanager.login_view = "Login"
loginmanager.login_message = "Login to Access that page"
loginmanager.login_message_category = "danger"

users = {}


@loginmanager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("base.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["user_name"]
        password_input = request.form["pass_word"]
        if user and password_input is not None:

            if get_user(user):
                test_user_data = User.query.filter_by(username=user).first()
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


@app.route("/sign_up", methods=["POST", "GET"])
def sign_up():
    if request.method == "POST":
        sessionid = request.form["sessionid"]
        username = request.form["user_username"]
        password = request.form["user_password"]
        email = request.form["Email"]

        user = get_user(username)
        if user is None:
            new_user = User(username, email, password, sessionid)
            db.session.add(new_user)
            db.session.commit()
            flash("user successfully added", "success")

        else:
            flash("user already exist", "danger")

    return render_template("user_login.html")


@app.route("/chat", methods=["GET", "POST"])
def chat():
    return render_template("_chat_app.html", username=session.get("username"))


@app.route("/create_room", methods=["GET", "POST"])
@login_required
def create_room():
    if request.method == "POST":
        room_name = request.form["room_name"]
        if get_room(room_name):
            flash("Room already exist", "danger")
        else:
            roomid = save_rooms(room_name, current_user.username)
            add_room_member(
                room_name,
                current_user.username,
                current_user.username,
                is_room_admin=True,
            )
            if roomid:
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
        if get_room(room_name) and is_room_admin_1(room_name, current_user.username):
            if User.query.filter_by(username=usernames1).first():
                if is_room_member(usernames1, room_name) is None:
                    if usernames1 == current_user.username:
                        add_room_member(
                            room_name,
                            usernames1,
                            current_user.username,
                            is_room_admin=True,
                        )
                        return redirect(url_for("get_rooms"))
                    else:
                        add_room_member(
                            room_name,
                            usernames1,
                            current_user.username,
                            is_room_admin=False,
                        )
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
        rooms = get_rooms_for_users(current_user.username)
        return render_template("_get_rooms.html", rooms=rooms)
    else:
        flash("you are not a member of any room", "warning")
    return render_template("_get_rooms.html")


@app.route("/view_room/<room_name>/", methods=["GET"])
@login_required
def view_room(room_name):
    room = get_room(room_name)
    if room and is_room_member(current_user.username, room_name):
        messages = get_messages(room_name)
        room_members = get_room_members(room_name)
        return render_template(
            "_view_room.html", room=room, room_members=room_members, messages=messages
        )

    else:
        flash(
            f"You are not a member of this group {room_name} please go back ", "warning"
        )
        return render_template("error.html")


@app.route("/update_room_names/<room_name>/", methods=["GET", "POST"])
@login_required
def update_room_names(room_name):
    rooms = get_room(room_name)
    member = get_room_members(room_name)
    if request.method == "POST":
        new_room_name = request.form["new_room_name"]
        if is_room_admin_1(room_name, session.get("username")):
            if updated_room(room_name, new_room_name) and update_members_room(
                room_name, new_room_name
            ):
                flash(
                    "successfully updated room name and members room names", "success"
                )
                return redirect(url_for("get_rooms"))
            else:
                flash("failed to update members room name and room names", "danger")
        else:
            flash("your are not a admin of this group", "warning")
    return render_template("_edit_room.html", rooms=rooms, member=member)


@app.route("/delete_room", methods=["POST", "GET"])  # make delete
@login_required
def delete():
    if request.method == "POST":
        room_name = request.form["room_name"]
        if room_name and is_room_admin_1(room_name, current_user.username):
            remove_rooms(room_name)
            flash("rooms successfully deleted", "Danger")
            return redirect(url_for("get_rooms"))
        else:
            flash("failed to delete room", "secondary")
    return render_template("delete.html")


# group chat
@socketio.on("incoming-msg")
def on_message(data):
    rooms = get_room(data["room"])
    if rooms:
        users_rooms = get_room_members(rooms.room_name)
        if users_rooms:
            for members in users_rooms:
                msg = data["msg"]
                if members.member_name == current_user.username:
                    room = rooms.room_name
                    now = datetime.now()
                    time_stamp = now.strftime("%H:%M:%S")
                    message = save_messages(
                        current_user.username, room, msg, time_stamp
                    )
                    if message:
                        print("message saved")
                        print(time_stamp)
                        send(
                            {
                                "username": current_user.username,
                                "msg": msg,
                                "time": time_stamp,
                            },
                            room=room,
                        )
                    else:
                        print("Something went wrong")
    else:
        return "message not sent"


@socketio.on("join")
def on_join(data):
    rooms = get_room(data["room"])
    if rooms:
        username = get_user(data["username"])
        room = rooms.room_name
        join_room(room)
        now = datetime.now()
        time_stamp = now.strftime("%H:%M:%S")
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
