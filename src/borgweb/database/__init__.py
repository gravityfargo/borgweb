from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.security import check_password_hash, generate_password_hash
import click


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class Database:

    @staticmethod
    @click.command("create-user")
    @click.argument("username")
    @click.argument("password")
    def create_user(username, password):
        from borgweb.database.models import User

        user = User(username=username, password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        print(f"User {username} created successfully")

    def login_user(self, username, password):
        from borgweb.database.models import User

        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            return False
        return True

    def get_user(self, username):
        from borgweb.database.models import User

        return User.query.filter_by(username=username).first()

    def get_users(self):
        from borgweb.database.models import User

        return User.query.all()
