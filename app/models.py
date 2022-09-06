from datetime import datetime
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
    nama = db.Column(db.String(50))
    jabatan = db.Column(db.String(35))
    no_telpon = db.Column(db.String(100))
    foto_profile = db.Column(db.String(
        250), default="http://www.gravatar.com/avatar/3b3be63a4c2a439b013787725dfce802?d=identicon")

    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    bidang_id = db.Column(db.Integer, db.ForeignKey('bidang.id'))

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
            'Tu': (Permission.LAPORAN_HARIAN | Permission.ARSIP | Permission.REKAP_BULANAN | Permission.PERMOHONAN_SURAT, False),
            'Kasubid': (Permission.LAPORAN_HARIAN | Permission.REKAP_BULANAN | Permission.PERMOHONAN_SURAT, False),
            "Sekban": (Permission.LAPORAN_HARIAN | Permission.PERMOHONAN_SURAT | Permission.DISPOSISI, False),
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
    REKAP_BULANAN = 0x04
    ARSIP = 0x16
    DISPOSISI = 0x64
    ADMINISTER = 0x80


class Bidang(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    alias = db.Column(db.String(50))
    nama = db.Column(db.String(100))

    users = db.relationship('User', backref="bidang", lazy='dynamic')

    def __repr__(self) -> str:
        return '<Bidang {}>'.format(self.nama_bidang)


class Disposisi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    alias = db.Column(db.String(50))
    nama = db.Column(db.String(100))

    def __repr__(self) -> str:
        return '<Disposisi ke {}>'.format(self.nama)


class SuratMasuk(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nomor = db.Column(db.String(64), nullable=True)
    asal = db.Column(db.String(125), nullable=False)
    perihal = db.Column(db.Text, nullable=False)
    tanggal_surat = db.Column(db.DateTime, default=datetime.utcnow)
    tanggal_diterima = db.Column(db.DateTime, default=datetime.utcnow)
    nama_file = db.Column(db.String(255), nullable=False)
    lampiran = db.Column(db.LargeBinary, nullable=False)
    disposisi_ke = db.Column(db.String(50))
    dilihat = db.Column(db.Boolean, default=False)

    def __repr__(self) -> str:
        return "<No Surat: {}>".format(self.nomor)


class SuratKeluar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nomor = db.Column(db.String(64), nullable=True)
    jenis = db.Column(db.String(125), nullable=False)
    ringkasan = db.Column(db.String(255), nullable=False)
    tanggal_dikeluarkan = db.Column(db.DateTime, default=datetime.now)
    tujuan = db.Column(db.String(64), nullable=False)
    status = db.Column(db.Boolean, default=False)
    nama_file = db.Column(db.String(255), nullable=False)
    lampiran = db.Column(db.LargeBinary, nullable=False)

    def __repr__(self) -> str:
        return '<Surat keluar dengan nomor: {}, tujuan {}, status {}>'.format(self.nomor, self.tujuan, self.status)


class DailyActivity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kegiatan = db.Column(db.String(64), nullable=False)
    tanggal = db.Column(db.DateTime, nullable=False)
    deskripsi = db.Column(db.Text, nullable=False)
    output = db.Column(db.String(120), nullable=False)

    def __repr__(self) -> str:
        return "<Kegiatan {}>".format(self.kegiatan)
