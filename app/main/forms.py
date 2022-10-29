from wsgiref.validate import validator
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, DateField,  SubmitField, TextAreaField, SelectField, BooleanField
from wtforms.validators import DataRequired

from ..models import Disposisi


class SuratMasukForm(FlaskForm):
    no_surat = StringField('No Surat', validators=[DataRequired()])
    asal = StringField('Dari Instansi', validators=[DataRequired()])
    perihal = TextAreaField('Perihal', validators=[DataRequired()])
    jenis = SelectField(
        "Jenis", choices=[("", "---"), ('biasa', "Biasa"), ('luar_biasa', 'Luar Biasa')])
    tanggal_surat = DateField('Tanggal Surat', validators=[DataRequired()])
    tanggal_diterima = DateField(
        "Tanggal Diterima", validators=[DataRequired()])
    lampiran = FileField("Lampiran", validators=[DataRequired()])
    rak = StringField('Rak', validators=[DataRequired()])

    submit = SubmitField('Simpan')


class DisposisiKeForm(FlaskForm):
    disposisi = SelectField('Disposisi Ke', coerce=str,
                            validators=[DataRequired()])
    pesan = TextAreaField('Pesan')
    submit = SubmitField('Simpan')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.disposisi.choices = [('0', "---")]+[(disposisi.nama, disposisi.nama)
                                                 for disposisi in Disposisi.query.order_by(Disposisi.alias).all()]


class SuratKeluarForm(FlaskForm):
    no_surat = StringField('No Surat', validators=[DataRequired()])
    jenis = SelectField("Jenis", choices=[
                        ("", "---"), ('biasa', "Biasa"), ('luar_biasa', 'Luar Biasa')])
    perihal = StringField('Perihal', validators=[DataRequired()])
    tanggal_dikeluarkan = DateField(
        'Taggal Dikeluarkan', validators=[DataRequired()])
    tujuan = StringField('Tujuan', validators=[DataRequired()])
    lampiran = FileField("Lampiran", validators=[DataRequired()])
    submit = SubmitField("Simpan")


# class SuratBalasanForm(FlaskForm):
#     kepala = TextAreaField("Kepala Surat", validators=[DataRequired()])
#     isi = TextAreaField("Isi Surat", validators=[DataRequired()])
#     penutup = TextAreaField("Penutup", validators=[DataRequired()])
#     submit = SubmitField("Simpan")


class BidangForm(FlaskForm):
    kode = StringField("Kode Bidang", validators=[DataRequired()])
    nama = StringField("Nama Bidang", validators=[DataRequired()])
    submit = SubmitField("Tambah")


class DisposisiForm(FlaskForm):
    alias = StringField('Alias', validators=[DataRequired()])
    nama = StringField('Nama Disposisi', validators=[DataRequired()])
    submit = SubmitField("Tambah")


class SudahDitindakLanjutForm(FlaskForm):
    ditindak_lanjut = BooleanField('Sudah Ditindak Lanjut?')
    submit = SubmitField('Simpan')


'''
    =========================
    Edit Surat
    ========================
'''


class EditSuratMasukForm(SuratMasukForm, DisposisiKeForm):
    lampiran = FileField('Lampiran')


class EditSuratKeluarForm(SuratKeluarForm):
    lampiran = FileField('Lampiran')


class EditBidangForm(BidangForm):
    pass


class EditDisposisiForm(DisposisiForm):
    pass


class JenisSuratBalasanForm(FlaskForm):
    jenis = SelectField(u'Jenis Surat', choices=[
                        ('0', '---'), ('magang', 'Magang'), ('other', 'Other')])
    submit = SubmitField('Pilih')


class SuratMagangForm(FlaskForm):
    tanggal_mulai = StringField('Tanggal Mulai', validators=[DataRequired()])
    lama_kegiatan = StringField('Lama Kegiatan', validators=[DataRequired()])
    tanggal_surat = StringField('Tanggal Surat', validators=[DataRequired()])
    peserta = TextAreaField('Peserta', validators=[DataRequired()])
    sifat_surat = SelectField('Sifat Surat', choices=[("0", "---"), (
        'biasa', "Biasa"), ('luar_biasa', 'Luar Biasa')])
    jumlah_lampiran = StringField(
        'Jumlah Lampiran', validators=[DataRequired()])
    submit = SubmitField('Generate')


class AgendaForm(FlaskForm):
    waktu_mulai = StringField('Waktu Mulai', validators=[DataRequired()])
    waktu_selesai = StringField('Waktu Selesai')
    kegiatan = TextAreaField('Kegiatan')
    tempat = StringField('Tempat')
    submit = SubmitField("Tambah")
