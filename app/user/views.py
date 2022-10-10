from flask import render_template, abort, flash, url_for, redirect, request, abort
from . import users

from app.models import User, Role, Bidang
from flask_login import login_required, current_user
from app.decorators import admin_required, permission_required
from .forms import EditProfileForm, EditProfileAdminForm
from .. import db, images_allowed_extension


@users.get('/profile')
@users.post('/profile')
@login_required
def profile():
    user = User.query.filter_by(id=current_user.id).first()
    return render_template('user/profile.html', user=user, title="Profile")


@users.get('/edit-profile')
@users.post('/edit-profile')
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.nama = form.nama_lengkap.data
        current_user.jabatan = form.jabatan.data
        current_user.no_telpon = form.no_telpon.data

        if form.foto.data and images_allowed_extension(form.foto.data.filename):
            current_user.foto = form.foto.data.read()

        db.session.commit()
        flash("User Profile update successfully", "success")
        return redirect(url_for("users.profile"))

    form.nama_lengkap.data = current_user.nama
    form.jabatan.data = current_user.jabatan
    form.no_telpon.data = current_user.no_telpon
    return render_template('user/edit_user.html', form=form, title="Edit Profile")


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
        user.nama = form.nama_lengkap.data
        user.bidang = Bidang.query.get(form.bidang.data)
        user.jabatan = form.jabatan.data
        user.no_telpon = form.no_telpon.data

        if form.foto.data and images_allowed_extension(form.foto.data.filename):
            user.foto = form.foto.data.read()

        db.session.commit()
        flash("User Profile Updated Successfully.", 'success')
        return redirect(url_for('auth.register'))

    form.email.data = user.email
    form.username.data = user.username
    form.role.data = user.role_id
    form.nama_lengkap.data = user.nama
    form.jabatan.data = user.jabatan
    form.bidang.data = user.bidang_id
    form.no_telpon.data = user.no_telpon
    return render_template('user/edit_user_admin.html', form=form, user=user, title="Edit Profile [ADMIN]")


@users.get('/delete/<id>')
@users.post('/delete/<id>')
@login_required
@admin_required
def delete_user(id):
    user = User.query.filter_by(id=id).first()

    if not user:
        abort(404)

    db.session.delete(user)
    db.session.commit()
    flash("User deleted Successfully", "success")
    return redirect(url_for('auth.register'))
