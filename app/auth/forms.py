from xml.dom import ValidationErr
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo

from ..models import User, Bidang


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()], render_kw={
                           "placeholder": "Username"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={
                             "placeholder": "Password"})
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    username = StringField('Username', validators=[
                           DataRequired(), Length(1, 64)])
    password = PasswordField('Password', validators=[
                             DataRequired(), EqualTo('confirm_password', 'Password must match')])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired()])
    nama_lengkap = StringField('Nama Lengkap', validators=[Length(0, 64)])
    bidang = SelectField('Bidang', coerce=int)
    jabatan = StringField('Jabatan', validators=[Length(0, 64)])
    no_telpon = StringField('No Telpon')
    submit = SubmitField('Register')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bidang.choices = [(bidang.id, bidang.nama_bidang)
                               for bidang in Bidang.query.order_by(Bidang.alias).all()]

    def validate_username(self, username):
        if User.query.filter_by(username=username.data).first():
            raise ValidationErr("Username already registered")
