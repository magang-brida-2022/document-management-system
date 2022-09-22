from flask_wtf import FlaskForm
from flask import flash
from wtforms import StringField, SubmitField, DateField, TextAreaField, SelectField
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


class EditDailyActivityForm(DailyActivityForm):
    pass


class RekapBulananForm(FlaskForm):
    bulan = SelectField()
