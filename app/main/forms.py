from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, DateField,  SubmitField, BooleanField
from wtforms.validators import DataRequired


class SuratMasukForm(FlaskForm):
    no_surat = StringField('No Surat', validators=[DataRequired()])
    asal = StringField('Ditujukan', validators=[DataRequired()])
    perihal = StringField('Prihal', validators=[DataRequired()])
    tanggal_diterima = DateField(
        "Tanggal Diterima", validators=[DataRequired()])
    lampiran = FileField("Lampiran", validators=[DataRequired()])
    tujuan = StringField('Tujuan', validators=[DataRequired()])
    submit = SubmitField('Simpan')


class SuratKeluarForm(FlaskForm):
    no_surat = StringField('No Surat', validators=[DataRequired()])
    jenis_surat = StringField('Jenis Surat', validators=[DataRequired()])
    ringkasan = StringField('Ringkasan', validators=[DataRequired()])
    tanggal_dikeluarkan = DateField(
        'Taggal Dikeluarkan', validators=[DataRequired()])
    tujuan = StringField('Tujuan', validators=[DataRequired()])
    lampiran = FileField("Lampiran", validators=[DataRequired()])
    submit = SubmitField("Simpan")
