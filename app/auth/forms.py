from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from flask_wtf.file import FileField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from flask import flash

from ..models import User, Bidang, SubBidang, Role


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
                           DataRequired()], render_kw={'autofocus': True})
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Ingat Saya')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    username = StringField('Username', validators=[
                           DataRequired(), Length(1, 64)])
    password = PasswordField('Password', validators=[
                             DataRequired(), EqualTo('confirm_password', 'Password must match')])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired()])
    role = SelectField('Role', coerce=int)
    nama_lengkap = StringField('Nama Lengkap', validators=[Length(0, 64)])
    nip = StringField('NIP', validators=[DataRequired()])
    bidang = SelectField('Bidang', coerce=int)
    # sub_bidang = SelectField("Sub Bidang", coerce=int)
    jabatan = SelectField('Jabatan', choices=[
                          ("0", "-- Pilih --"), ("sekban", "Sekretaris Badan"), ("kabid", "Kepala Bidang"), ("kasubid", "Kepala Sub-Bidang"), ("pegawai", "Pegawai")])
    no_telpon = StringField('No Telpon')
    foto_profile = FileField("Select Photo Profile")
    submit = SubmitField('Register')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bidang.choices = [(0, "-- Pilih --")]+[(bidang.id, bidang.nama)
                                                    for bidang in Bidang.query.order_by(Bidang.kode).all()]
        self.role.choices = [(0, "-- Pilih --")] + [(role.id, role.name)
                                                    for role in Role.query.order_by(Role.name).all()]

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            flash("Email sudah terdaftar", "error")
            return False

    def validate_username(self, username):
        if User.query.filter_by(username=username.data).first():
            flash("Username sudah terdaftar", "error")
            return False
