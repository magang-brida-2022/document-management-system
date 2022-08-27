from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import Length, ValidationError

from ..models import Role, User


class EditProfileForm(FlaskForm):
    nama_lengkap = StringField('Nama Lengkap', validators=[Length(0, 64)])
    jabatan = StringField('Jabatan', validators=[Length(0, 64)])
    no_telpon = StringField('No Telpon')
    submit = SubmitField('Simpan')


class EditProfileAdminForm(FlaskForm):
    email = StringField('Email')
    username = StringField('Username', validators=[Length(1, 64)])
    role = SelectField('Role', coerce=int)
    nama_lengkap = StringField('Nama Lengkap', validators=[Length(0, 64)])
    jabatan = StringField('Jabatan', validators=[Length(0, 64)])
    no_telpon = StringField('No Telpon')
    submit = SubmitField('Simpan')

    def __init__(self, user, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.user = user
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]

    def validate_email(self, email):
        if email.data != self.user.email and User.query.filter_by(email=email.data).first():
            raise ValidationError('Email Already Registered')

    def validate_username(self, username):
        if username.data != self.user.username and User.query.filter_by(username=username.data).first():
            raise ValidationError("Username already used.")
