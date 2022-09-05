from tokenize import String
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, DateField,  SubmitField, TextAreaField, SelectField, BooleanField
from wtforms.validators import DataRequired

from ..models import Disposisi


class SuratMasukForm(FlaskForm):
    no_surat = StringField('No Surat', validators=[DataRequired()])
    asal = StringField('Dari Instansi', validators=[DataRequired()])
    perihal = TextAreaField('Perihal', validators=[DataRequired()])
    tanggal_surat = DateField('Tanggal Surat', validators=[DataRequired()])
    tanggal_diterima = DateField(
        "Tanggal Diterima", validators=[DataRequired()])
    lampiran = FileField("Lampiran", validators=[DataRequired()])

    submit = SubmitField('Simpan')


class DisposisiKeForm(FlaskForm):
    disposisi = SelectField('Disposisi Ke', coerce=int)
    dilihat = BooleanField('Sudah Dilihat')
    submit = SubmitField('Simpan')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.disposisi.choices = [(disposisi.id, disposisi.nama)
                                  for disposisi in Disposisi.query.order_by(Disposisi.alias).all()]


class SuratKeluarForm(FlaskForm):
    no_surat = StringField('No Surat', validators=[DataRequired()])
    jenis_surat = StringField('Jenis Surat', validators=[DataRequired()])
    ringkasan = StringField('Ringkasan', validators=[DataRequired()])
    tanggal_dikeluarkan = DateField(
        'Taggal Dikeluarkan', validators=[DataRequired()])
    tujuan = StringField('Tujuan', validators=[DataRequired()])
    lampiran = FileField("Lampiran", validators=[DataRequired()])
    submit = SubmitField("Simpan")


class BidangForm(FlaskForm):
    alias = StringField("Alias", validators=[DataRequired()])
    nama = StringField("Nama Bidang", validators=[DataRequired()])
    submit = SubmitField("Tambah")


class DisposisiForm(FlaskForm):
    alias = StringField('Alias', validators=[DataRequired()])
    nama = StringField('Nama Disposisi', validators=[DataRequired()])
    submit = SubmitField("Tambah")


'''
    =========================
    Edit Surat
    ========================
'''


class EditSuratMasukForm(SuratMasukForm, DisposisiKeForm):
    pass


class EditSuratKeluarForm(SuratKeluarForm):
    pass
