from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user

from app.decorators import admin_required

from . import auth
from .forms import LoginForm, RegistrationForm
from app.models import User
from .. import db


@auth.get('/signin')
@auth.post('/signin')
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))

        flash('Invalid Username or password', 'danger')

    return render_template('auth/login.html', form=form)


@auth.get('/signup')
@auth.post('/signup')
@admin_required
def register():
    all_user = User.query.all()
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('User created successfully', 'success')
        return redirect(request.url)

    return render_template('auth/register.html', form=form, all_user=all_user)


@auth.get('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', "warning")
    return redirect(url_for('auth.login'))
