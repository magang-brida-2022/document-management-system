from email.policy import default
from werkzeug.security import generate_password_hash, check_password_hash
from typing import Union
from flask_login import UserMixin

from . import login_manager, db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    nama_lengkap = db.Column(db.String(50))
    jabatan = db.Column(db.String(35))
    foto_profile = db.Column(db.String(
        250), default="http://www.gravatar.com/avatar/3b3be63a4c2a439b013787725dfce802?d=identicon")

    def __repr__(self) -> str:
        return f'<User {self.username}>'

    @property
    def password(self):
        raise AttributeError('password is not a readable attributes')

    @password.setter
    def password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id: Union[str, int]) -> int:
    return User.query.get(int(user_id))


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref="role", lazy='dynamic')

    def __repr__(self) -> str:
        return f'<Role {self.name}>'
