from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user, current_user
from sqlalchemy.exc import IntegrityError

from app.decorators import admin_required

from . import auth
from .forms import LoginForm, RegistrationForm
from app.models import User, Bidang, SubBidang, Role
from .. import db, images_allowed_extension


@auth.get('/signin')
@auth.post('/signin')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))

        flash(
            'Username atau Password yang anda masukkan salah. Silahkan coba lagi.', 'error')

    return render_template('auth/login.html', form=form, title="Login")


@auth.get('/daftar_pengguna')
@auth.post('/daftar_pengguna')
@login_required
@admin_required
def register():
    all_user = User.query.all()
    form = RegistrationForm()

    if form.validate_on_submit():
        try:
            if form.foto_profile.data and images_allowed_extension(form.foto_profile.data.filename):
                user = User(email=form.email.data, username=form.username.data, password=form.password.data, role=Role.query.get(form.role.data), nama=form.nama_lengkap.data, nip=form.nip.data,
                            bidang=Bidang.query.get(form.bidang.data), jabatan=form.jabatan.data, no_telpon=form.no_telpon.data, foto=form.foto_profile.data.read())
                db.session.add(user)
                db.session.commit()
                flash('Penguna baru berhasil dibuat.', 'success')
                return redirect(request.base_url)
            else:
                flash('Support hanya file dengan format .img/.png', 'error')
                return redirect(request.base_url)
        except IntegrityError:
            db.session.rollback()

    return render_template('auth/register.html', form=form, all_user=all_user, title="User Management", page='user_management')


@auth.get('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout berhasil', "warning")
    return redirect(url_for('auth.login'))
