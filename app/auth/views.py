from flask import flash, redirect, render_template, request, url_for
from flask_login import login_user

from . import auth
from .forms import LoginForm
from app.models import User


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
def register():
    return "registration form"
