from flask_jwt_extended import (
    create_access_token,
    JWTManager,
    get_jwt_identity,
    verify_jwt_in_request,
)
from App.models import User


def login_user(username: str, password: str):
    user: User | None = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        token: str = create_access_token(identity=user)
        return token
    return None


def setup_jwt(app) -> JWTManager:
    jwt = JWTManager(app)

    @jwt.user_identity_loader
    def user_identity_lookup(user) -> int:
        return user.id

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data) -> User | None:
        identity = jwt_data["sub"]
        return User.query.get(identity)

    return jwt


def add_auth_context(app) -> None:
    @app.context_processor
    def inject_user():
        try:
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            current_user = User.query.get(user_id)
            is_authenticated = True
        except Exception as e:
            print(e)
            is_authenticated = False
            current_user = None
        return dict(is_authenticated=is_authenticated, current_user=current_user)
