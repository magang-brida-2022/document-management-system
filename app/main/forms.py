from sqlite3 import DatabaseError
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, MultipleFileField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class SuratMasukForm(FlaskForm):
    kode_klasifikasi = StringField(
        'Kode Klasifikasi', validators=[DataRequired()])
    no_surat = StringField('No Surat', validators=[DataRequired()])
    tanggal = DateField("Tanggal", validators=[DataRequired()])
    prihal = StringField('Prihal', validators=[DataRequired()])
    ditujukan = StringField('Ditujukan', validators=[DataRequired()])
    lampiran = MultipleFileField("Lampiran", validators=[DataRequired()])
    status = BooleanField('Status', validators=[DataRequired()])
    disposisi = StringField("Disposisi ke", validators=[DataRequired()])
    submit = SubmitField('Simpan')
