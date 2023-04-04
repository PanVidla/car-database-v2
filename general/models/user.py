from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from general import database, login


class User(UserMixin, database.Model):

    __tablename__ = "users"

    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.Unicode, nullable=False, unique=True)
    password_hash = database.Column(database.Unicode)
    current_instance = database.Column(database.Integer, default=0, nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
