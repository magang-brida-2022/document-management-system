from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from typing import Union, NoReturn
from flask_login import UserMixin, AnonymousUserMixin
from flask import current_app
from datetime import datetime
from base64 import b64encode
from sqlalchemy import extract
from sqlalchemy.ext.hybrid import hybrid_property


from . import login_manager, db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120))
    nama = db.Column(db.String(50))
    jabatan = db.Column(db.String(35))
    no_telpon = db.Column(db.String(100))
    foto = db.Column(db.LargeBinary())

    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    bidang_id = db.Column(db.Integer, db.ForeignKey('bidang.id'))

    posts = db.relationship(
        'DailyActivity', backref="author", lazy=True)

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

    def get_photo(self):
        if self.foto:
            return b64encode(self.foto).decode('utf-8')


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
        roles = {
            'Pegawai': (Permission.LAPORAN_HARIAN | Permission.PERMOHONAN_SURAT, True),
            'Tu': (Permission.LAPORAN_HARIAN | Permission.PERMOHONAN_SURAT | Permission.REKAP_BULANAN | Permission.ARSIP, False),
            'Kasubid': (Permission.LAPORAN_HARIAN | Permission.PERMOHONAN_SURAT | Permission.REKAP_BULANAN | Permission.FEEDBACK, False),
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
    ARSIP = 0x08
    FEEDBACK = 0x16
    DISPOSISI = 0x32
    ADMINISTER = 0x80


class Bidang(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kode = db.Column(db.String(50))
    nama = db.Column(db.String(100))

    users = db.relationship('User', backref="bidang", lazy='dynamic')

    def __repr__(self) -> str:
        return '<Bidang {}>'.format(self.nama)


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
    jenis = db.Column(db.String(50))
    tanggal_surat = db.Column(db.DateTime, default=datetime.utcnow)
    tanggal_diterima = db.Column(db.DateTime, default=datetime.utcnow)
    rak = db.Column(db.String, nullable=False)
    lampiran = db.Column(db.LargeBinary, nullable=False)
    disposisi_ke = db.Column(db.String(50))
    pesan = db.Column(db.Text)
    dilihat = db.Column(db.Boolean, default=False)
    tindak_lanjut = db.Column(db.Boolean, default=False)

    # balasan = db.relationship('SuratBalasan', backref="surat_masuk", lazy=True)

    def __repr__(self) -> str:
        return "<No Surat Masuk: {}>".format(self.nomor)


class SuratBalasan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kepala = db.Column(db.Text, nullable=False)
    isi = db.Column(db.Text, nullable=False)
    penutup = db.Column(db.Text, nullable=False)

    # surat_masuk_id = db.Column(db.Integer, db.ForeignKey(
    #     'surat_masuk.id'), nullable=False)

    def __repr__(self) -> str:
        return '<Balasan ID: {}>'.format(self.id)


class SuratKeluar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nomor = db.Column(db.String(64), nullable=True)
    jenis = db.Column(db.String(125), nullable=False)
    perihal = db.Column(db.String(255), nullable=False)
    tanggal_dikeluarkan = db.Column(db.DateTime, default=datetime.now)
    tujuan = db.Column(db.String(64), nullable=False)
    status = db.Column(db.Boolean, default=False)
    lampiran = db.Column(db.LargeBinary, nullable=False)

    def __repr__(self) -> str:
        return '<No Surat Keluar: {}>'.format(self.nomor)


class DailyActivity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kegiatan = db.Column(db.String(64))
    tanggal = db.Column(db.DateTime)
    deskripsi = db.Column(db.Text)
    output = db.Column(db.String(120))

    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id'))

    def __repr__(self) -> str:
        return "<Kegiatan {}>".format(self.kegiatan)

    @hybrid_property
    def filter_by_year(self):
        return self.tanggal.year

    @filter_by_year.expression
    def filter_by_year(cls):
        return extract('year', cls.tanggal)

    @hybrid_property
    def filter_by_month(self):
        return self.tanggal.month

    @filter_by_month.expression
    def filter_by_month(cls):
        return extract('month', cls.tanggal)
