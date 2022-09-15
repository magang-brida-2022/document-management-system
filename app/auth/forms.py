from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from flask_wtf.file import FileField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError

from ..models import User, Bidang


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()], render_kw={
                           "placeholder": "Username", 'autofocus': True})
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
    foto_profile = FileField("Select Photo Profile")
    submit = SubmitField('Register')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bidang.choices = [(0, "---")]+[(bidang.id, bidang.nama)
                                            for bidang in Bidang.query.order_by(Bidang.alias).all()]

    def validate_username(self, username):
        if User.query.filter_by(username=username.data).first():
            raise ValidationError("Username already registered")
