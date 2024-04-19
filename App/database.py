from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()


def get_migrate(app) -> Migrate:
    return Migrate(app, db)


def create_db() -> None:
    db.create_all()


def init_db(app) -> None:
    db.init_app(app)
