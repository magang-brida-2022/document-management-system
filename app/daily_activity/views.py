from flask import render_template, flash, redirect, url_for, request, make_response
from flask_login import login_required, current_user
from datetime import datetime

from app.decorators import permission_required

from . import daily_activity
from .forms import DailyActivityForm, EditDailyActivityForm, RekapBulananForm
from ..models import DailyActivity, Permission
from .. import db


@daily_activity.get('/')
@daily_activity.post('/')
@login_required
def daily():
    form = DailyActivityForm()
    daily_activity = current_user.posts

    if form.validate_on_submit():
        date_parse = datetime.strptime(form.tanggal.data, "%m/%d/%Y")
        new_activity = DailyActivity(tanggal=date_parse, kegiatan=form.kegiatan.data,
                                     deskripsi=form.deskripsi.data, output=form.output.data, author=current_user)
        db.session.add(new_activity)
        db.session.commit()
        flash("Aktivitas berhasil ditambahkan.", "success")
        return redirect(request.url)

    return render_template('daily_activity/daily_activity.html', form=form, title="Daily Activity", daily_activity=daily_activity, page='activity')


@daily_activity.get('<id>/edit')
@daily_activity.post('<id>/edit')
@login_required
def edit_activity(id):
    form = EditDailyActivityForm()
    activity = DailyActivity.query.filter_by(id=id).first()

    if form.validate_on_submit():
        activity.kegiatan = form.kegiatan.data
        activity.deskripsi = form.deskripsi.data
        activity.output = form.output.data

        db.session.commit()
        flash("Edit aktivitas harian sukses", "success")
        return redirect(url_for('daily_activity.daily'))

    form.kegiatan.data = activity.kegiatan
    form.tanggal.data = activity.tanggal
    form.deskripsi.data = activity.deskripsi
    form.output.data = activity.output
    return render_template('daily_activity/edit_daily_activity.html', form=form, title="Edit Laporan Harian")


@daily_activity.get('/<id>/delete')
@daily_activity.post('/<id>/delete')
@login_required
def delete_aktivity(id):
    del_aktivity = DailyActivity.query.get_or_404(id)
    db.session.delete(del_aktivity)
    db.session.commit()
    flash("Aktivitas berhasil dihapus", "success")
    return redirect(url_for('daily_activity.daily'))


@daily_activity.get('/rekap')
@daily_activity.post('/rekap')
@login_required
def rekap_bulanan():
    form = RekapBulananForm()
    if form.validate_on_submit():
        cetak = DailyActivity.query.filter(
            DailyActivity.filter_by_month == form.bulan.data, DailyActivity.filter_by_year == form.tahun.data).filter_by(author=current_user).all()

        return render_template('daily_activity/cetak_daily_activity.html', data=cetak)

    return render_template('daily_activity/rekap_bulanan.html', form=form, page='rekap')
