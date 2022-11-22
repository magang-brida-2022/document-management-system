from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from datetime import datetime
from bs4 import BeautifulSoup

from . import daily_activity
from .forms import DailyActivityForm, EditDailyActivityForm, RekapBulananForm, CariPegawaiForm
from ..models import DailyActivity, Bidang, User
from .. import db
from ..main.utils.local_datetime_formatting import to_localtime


@daily_activity.get('/')
@daily_activity.post('/')
@login_required
def daily():
    form = DailyActivityForm()
    cari_pegawai_form = CariPegawaiForm()

    daily_activity = current_user.posts

    if form.validate_on_submit():
        soup = BeautifulSoup(form.kegiatan.data, "html.parser")
        output = soup.find_all("li")

        output_value = f'{len(output)} Kegiatan' if output else "1 Kegiatan"
        new_activity = DailyActivity(tanggal=form.tanggal.data, kegiatan=form.kegiatan.data,
                                     deskripsi=form.deskripsi.data, output=output_value, author=current_user)

        db.session.add(new_activity)
        db.session.commit()
        flash("Aktivitas berhasil ditambahkan.", "success")
        return redirect(request.url)

    if cari_pegawai_form.validate_on_submit():
        id = cari_pegawai_form.pilih_pegawai.data
        pegawai_selected = User.query.filter_by(id=id).first()

        return render_template('daily_activity/daily_activity.html', form=form, title="Daily Activity", daily_activity=daily_activity, page='activity', cari_pegawai_form=cari_pegawai_form, pegawai_selected=pegawai_selected.posts)

    return render_template('daily_activity/daily_activity.html', form=form, title="Daily Activity", daily_activity=daily_activity, page='activity', cari_pegawai_form=cari_pegawai_form)


@daily_activity.get('<id>/edit')
@daily_activity.post('<id>/edit')
@login_required
def edit_activity(id):
    form = EditDailyActivityForm()
    activity = DailyActivity.query.filter_by(id=id).first()

    if form.validate_on_submit():
        soup = BeautifulSoup(form.kegiatan.data, "html.parser")
        li = soup.find_all('li')

        activity.kegiatan = form.kegiatan.data
        activity.deskripsi = form.deskripsi.data
        if li:
            activity.output = f"{len(li)} kegiatan"
        else:
            activity.output = "1 Kegiatan"

        db.session.commit()
        flash("Edit aktivitas harian sukses", "success")
        return redirect(url_for('daily_activity.daily'))

    form.tanggal.data = activity.tanggal
    form.kegiatan.data = activity.kegiatan
    form.deskripsi.data = activity.deskripsi
    form.tanggal.data = activity.tanggal

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
        data = DailyActivity.query.filter(
            DailyActivity.filter_by_month == form.bulan.data, DailyActivity.filter_by_year == form.tahun.data).filter_by(author=current_user).all()

        return render_template('daily_activity/rekap_bulanan.html', form=form, page="rekap", data=data, bulan=form.bulan.data, tahun=form.tahun.data, title="Cetak aktifitas harian")

    return render_template('daily_activity/rekap_bulanan.html', form=form, page='rekap', title="Cetak aktifitas harian")


@daily_activity.get('/cetak')
@login_required
def cetak_rekap_bulanan():
    str_month = {
        "1": "Januari",
        "2": "Februari",
        "3": "Maret",
        "4": "April",
        "5": "Mei",
        "6": "Juni",
        "7": "Juli",
        "8": "Agustus",
        "9": "September",
        "10": "Oktober",
        "11": "November",
        "12": "Desember"
    }

    tahun = request.args.get("tahun")
    bulan = request.args.get("bulan")

    bulan_str = str_month[bulan]

    current_datetime = to_localtime(datetime.now())

    # user = User.query.filter_by(
    #     id=int(current_user.subbidang_id.kepala_sub_bidang)).first()
    # print(user)

    kasubid = User.query.filter_by(
        nama=current_user.subbidang.kepala_sub_bidang).first()

    activity = DailyActivity.query.filter(
        DailyActivity.filter_by_month == bulan, DailyActivity.filter_by_year == tahun).filter_by(author=current_user).all()

    data = {
        "kasubid": kasubid,
        "activity": activity,
        "periode": {
            "bulan": bulan_str,
            "tahun": tahun
        },
        "tanggal_cetak": current_datetime
    }

    return render_template('daily_activity/cetak_daily_activity.html', data=data)
