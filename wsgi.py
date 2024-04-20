from flask import Flask
from App.database import db
from App.models import User
from App.app import create_app

app: Flask = create_app()


@app.cli.command("init", help="Creates and initializes the database")
def initialize() -> None:
    initialize_db()
    print("database initialized")


def initialize_db() -> None:
    db.drop_all()
    db.create_all()
    bob = User(username="bob", email="bob@mail.com", password="bobpass")
    rob = User(username="rob", email="rob@mail.com", password="robpass")
    db.session.add(bob)
    db.session.add(rob)
    db.session.commit()
