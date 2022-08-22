from flask import render_template, abort, flash, url_for, redirect
from . import users

from app.models import User, Role
from flask_login import login_required, current_user
from app.decorators import admin_required, permission_required
from .forms import EditProfileForm, EditProfileAdminForm
from .. import db


@users.get('/<username>')
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)

    return render_template('user/profile.html', user=user)


@users.get('/edit-profile')
@users.post('/edit-profile')
@login_required
def edit_profile():
    form = EditProfileForm()

    if form.validate_on_submit():
        current_user.nama_lengkap = form.nama_lengkap.data
        current_user.jabatan = form.jabatan.data
        db.session.commit()

        flash("User Profile Updated Successfully.", "success")
        return redirect(url_for('users.profile', username=current_user.username))

    form.nama_lengkap.data = current_user.nama_lengkap
    form.jabatan.data = current_user.jabatan

    return render_template('user/edit_user.html', form=form)


@users.get('/edit-profile/<int:id>')
@users.post('/edit-profile/<int:id>')
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user)
    
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.role = Role.query.get(form.role.data)
        user.nama_lengkap = form.nama_lengkap.data
        user.jabatan = form.jabatan.data

        db.session.commit()
        flash("User Profile Updated Successfully.", 'success')
        return redirect(url_for('users.profile', username=current_user.username))

    form.email.data = user.email
    form.username.data = user.username
    form.role.data = user.role_id
    form.nama_lengkap.data = user.nama_lengkap
    form.jabatan.data = user.jabatan
    return render_template('user/edit_user_admin.html', form=form, user=user)
