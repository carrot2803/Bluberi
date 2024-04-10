from App.database import db
from App.models import User
from App.app import create_app

app = create_app()


@app.cli.command("init", help="Creates and initializes the database")
def initialize():
    initialize_db()
    print("database initialized")


def initialize_db():
    db.drop_all()
    db.create_all()
    bob = User(username="bob", email="bob@mail.com", password="bobpass")
    db.session.add(bob)
    db.session.commit()


# if __name__ == "__main__":
# socket.run(app, debug=True)
