from datetime import date, datetime
from email.policy import default
from enum import unique
from werkzeug.security import generate_password_hash, check_password_hash
from typing import Union, NoReturn
from flask_login import UserMixin, AnonymousUserMixin
from flask import current_app
from datetime import datetime

from . import login_manager, db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120))
    nama_lengkap = db.Column(db.String(50))
    jabatan = db.Column(db.String(35))
    foto_profile = db.Column(db.String(
        250), default="http://www.gravatar.com/avatar/3b3be63a4c2a439b013787725dfce802?d=identicon")

    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    surat_masuk = db.relationship('SuratMasuk', backref="user", lazy=True)

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        if self.role == None:
            if self.email == current_app.config['IS_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    def can(self, permissions):
        return self.role is not None and (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    def __repr__(self) -> str:
        return f'<User {self.username}>'

    @property
    def password(self) -> NoReturn:
        raise AttributeError('password is not a readable attributes')

    @password.setter
    def password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions) -> bool:
        return False

    def is_administrator(self) -> bool:
        return False


login_manager.anonymous_user = AnonymousUser


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

    @staticmethod
    def insert_roles():
        """
        role:
            1. Super Admin
            2. Pimpinan
            3. Pegawai Tu
            4. Pegawai
        """

        roles = {
            'Pegawai': (Permission.LAPORAN_HARIAN | Permission.PERMOHONAN_SURAT, True),
            'Tu': (Permission.LAPORAN_HARIAN | Permission.ARSIP | Permission.REKAP_BULANAN, Permission.PERMOHONAN_SURAT, False),
            'Kasubid': (Permission.LAPORAN_HARIAN | Permission.TANDA_TANGAN,  False),
            'Administrator': (0xff, False)
        }

        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()


class Permission:
    LAPORAN_HARIAN = 0x01
    PERMOHONAN_SURAT = 0x02
    ARSIP = 0x04
    REKAP_BULANAN = 0x08
    TANDA_TANGAN = 0x16
    ADMINISTER = 0x80


class SuratMasuk(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    no_surat = db.Column(db.String(64), unique=True)
    asal = db.Column(db.String(125), nullable=False)
    perihal = db.Column(db.String(255), nullable=False)
    tanggal_terima = db.Column(db.DateTime, default=datetime.utcnow)
    nama_file = db.Column(db.String(255), nullable=False)
    lampiran = db.Column(db.LargeBinary, nullable=False)
    tujuan = db.Column(db.String(125), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self) -> str:
        return "<No Surat {}>".format(self.no_surat)
