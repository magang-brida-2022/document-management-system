from flask_wtf import FlaskForm
from flask import flash
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, ValidationError

from ..models import DailyActivity


class DailyActivityForm(FlaskForm):
    kegiatan = StringField('Kegiatan', validators=[DataRequired()])
    tanggal = StringField('Tanggal', validators=[DataRequired()])
    deskripsi = TextAreaField('Deskripsi')
    output = StringField('Output')
    submit = SubmitField('Simpan')

    def validate_tanggal(self, tanggal):
        if DailyActivity.query.filter_by(tanggal=tanggal.data).first():
            flash(
                f'Tanggal {tanggal.data} sudah diisi, silahkan di edit jika ingin diubah', 'error')
            raise ValidationError()


class EditDailyActivityForm(FlaskForm):
    kegiatan = StringField('Kegiatan')
    tanggal = StringField('Tanggal')
    deskripsi = TextAreaField('Deskripsi')
    output = StringField('Output')
    submit = SubmitField('Simpan')


class RekapBulananForm(FlaskForm):
    bulan = SelectField('Bulan', coerce=int)
    tahun = SelectField('Tahun', coerce=int)
    submit = SubmitField('Cetak')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.bulan.choices = [(0, "---")] + [(activity.tanggal, activity.tanggal.month)
        # for activity in DailyActivity.query.all()]
