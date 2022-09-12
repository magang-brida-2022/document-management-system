from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, TextAreaField
from wtforms.validators import DataRequired, ValidationError
from datetime import datetime

from ..models import DailyActivity


class DailyActivityForm(FlaskForm):
    kegiatan = StringField('Kegiatan', validators=[DataRequired()])
    tanggal = StringField('Tanggal', validators=[DataRequired()])
    deskripsi = TextAreaField('Deskripsi')
    output = StringField('Output')
    submit = SubmitField('Simpan')
