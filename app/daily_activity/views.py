from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required
from datetime import datetime

from . import daily_activity
from .forms import DailyActivityForm
from ..models import DailyActivity
from .. import db


@daily_activity.get('/')
@daily_activity.post('/')
@login_required
def daily():
    form = DailyActivityForm()
    daily_activity = DailyActivity.query.all()

    if form.validate_on_submit():
        date_parse = datetime.strptime(form.tanggal.data, "%m/%d/%Y")

        print(type(date_parse))

        new_activity = DailyActivity(tanggal=date_parse, kegiatan=form.kegiatan.data,
                                     deskripsi=form.deskripsi.data, output=form.output.data)
        db.session.add(new_activity)
        db.session.commit()
        flash("Aktivitas Berhasil Ditambahkan", "Success")
        return redirect(request.url)

    return render_template('daily_activity/daily_activity.html', form=form, title="Daily Activity", daily_activity=daily_activity)


@daily_activity.get('/<id>/delete')
@daily_activity.post('/<id>/delete')
@login_required
def delete_aktivity(id):
    del_aktivity = DailyActivity.query.get_or_404(id)
    db.session.delete(del_aktivity)
    db.session.commit()
    flash("Aktivitas berhasil di Hapus", "Success")
    return redirect(url_for('daily_activity.daily'))
