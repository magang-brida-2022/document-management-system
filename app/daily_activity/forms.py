from flask_wtf import FlaskForm
from flask import flash
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, ValidationError
from flask_login import current_user
from sqlalchemy import and_

from ..models import DailyActivity, User


class DailyActivityForm(FlaskForm):
    kegiatan = StringField('Kegiatan', validators=[DataRequired()])
    tanggal = StringField('Tanggal', validators=[DataRequired()])
    deskripsi = TextAreaField('Deskripsi')
    output = StringField('Output')
    submit = SubmitField('Simpan')

    def validate_tanggal(self, tanggal):
        activity = DailyActivity.query.filter_by(tanggal=tanggal.data).first()
        if activity:
            list_activity = current_user.posts
            for a in list_activity:
                if activity.tanggal == a.tanggal:
                    flash(
                        f'Tanggal {tanggal.data} sudah diisi, silahkan di edit jika ingin diubah', 'error')
                    raise ValidationError("")


class EditDailyActivityForm(FlaskForm):
    kegiatan = StringField('Kegiatan')
    tanggal = StringField('Tanggal')
    deskripsi = TextAreaField('Deskripsi')
    output = StringField('Output')


class RekapBulananForm(FlaskForm):
    bulan = SelectField('Bulan', coerce=int)
    tahun = SelectField('Tahun', coerce=int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tahun.choices = [(0, "-- Pilih --")] + list(set([(activity.tanggal.year, activity.tanggal.year)
                                                              for activity in DailyActivity.query.filter_by(author=current_user).all()]))
        self.bulan.choices = [(0, "-- Pilih --")] + list(set([(activity.tanggal.month, activity.tanggal.month)
                                                              for activity in DailyActivity.query.filter_by(author=current_user).all()]))


class CariPegawaiForm(FlaskForm):
    pilih_pegawai = SelectField(
        'Pilih', coerce=int, validators=[DataRequired()])
    submit = SubmitField("Cari")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pilih_pegawai.choices = [(0, "-- Pilih --")]+[(user.id, user.nama)
                                                           for user in User.query.filter(and_(User.bidang == current_user.bidang, User.nama != current_user.nama)).all()]
