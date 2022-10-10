from email.mime import image
from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user, current_user

from app.decorators import admin_required

from . import auth
from .forms import LoginForm, RegistrationForm
from app.models import User, Bidang
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

        flash('Invalid Username or password', 'error')

    return render_template('auth/login.html', form=form, title="Login")


@auth.get('/signup')
@auth.post('/signup')
@admin_required
def register():
    all_user = User.query.all()
    print(all_user)
    form = RegistrationForm()

    if form.validate_on_submit():

        if form.foto_profile.data and images_allowed_extension(form.foto_profile.data.filename):
            user = User(email=form.email.data, username=form.username.data, password=form.password.data,
                        nama=form.nama_lengkap.data, bidang=Bidang.query.get(form.bidang.data), jabatan=form.jabatan.data, no_telpon=form.no_telpon.data, foto=form.foto_profile.data.read())
            db.session.add(user)
            db.session.commit()
            flash('User created successfully', 'success')
            return redirect(request.base_url)
        else:
            flash('allowed file types are .img/.png only', 'error')
            return redirect(request.base_url)

    return render_template('auth/register.html', form=form, all_user=all_user, title="User Management")


@auth.get('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', "warning")
    return redirect(url_for('auth.login'))
