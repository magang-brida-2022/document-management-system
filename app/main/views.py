from flask import render_template, flash, redirect, request, send_file, url_for
from flask_login import login_required, current_user
from io import BytesIO

from app.decorators import admin_required, permission_required
from app.models import Permission
from .forms import SuratMasukForm, SuratKeluarForm, DisposisiForm, BidangForm, DisposisiKeForm, EditSuratMasukForm, EditSuratKeluarForm
from ..models import SuratMasuk, SuratKeluar, Bidang, Disposisi
from . import main
from .. import db


@main.get('/')
# @login_required
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))

    return render_template('index.html')


@main.get('/surat_masuk')
@main.post('/surat_masuk')
@login_required
# @permission_required(Permission.ARSIP)
def surat_masuk():
    form = SuratMasukForm()
    surat_masuk = SuratMasuk.query.all()

    if form.validate_on_submit():
        no_surat = form.no_surat.data
        asal = form.asal.data
        perihal = form.perihal.data
        tanggal_surat = form.tanggal_surat.data
        tanggal_diterima = form.tanggal_diterima.data
        lampiran = form.lampiran.data

        surat_masuk = SuratMasuk(nomor=no_surat, asal=asal, perihal=perihal, tanggal_surat=tanggal_surat,
                                 tanggal_diterima=tanggal_diterima, nama_file=lampiran.filename, lampiran=lampiran.read())
        db.session.add(surat_masuk)
        db.session.commit()

        flash("Surat masuk baru berhasil di tambahkan", "success")
        return redirect(url_for('main.surat_masuk'))

    return render_template('arsip/surat_masuk.html', form=form, surat_masuk=surat_masuk)


@main.get('/surat_keluar')
@main.post('/surat_keluar')
@login_required
# @permission_required(Permission.ARSIP)
def surat_keluar():
    form = SuratKeluarForm()
    surat_keluar = SuratKeluar.query.all()

    if form.validate_on_submit():
        nomor_surat = form.no_surat.data
        jenis_surat = form.jenis_surat.data
        ringkasan = form.ringkasan.data
        tanggal_dikeluarkan = form.tanggal_dikeluarkan.data
        tujuan = form.tujuan.data
        lampiran = form.lampiran.data

        surat_keluar = SuratKeluar(nomor=nomor_surat, jenis=jenis_surat, ringkasan=ringkasan, tanggal_dikeluarkan=tanggal_dikeluarkan,
                                   tujuan=tujuan, nama_file=lampiran.filename, lampiran=lampiran.read())
        db.session.add(surat_keluar)
        db.session.commit()

        flash("Surat keluar baru berhasil ditambahkan", "success")
        return redirect(request.base_url)

    return render_template('arsip/surat_keluar.html', form=form, surat_keluar=surat_keluar)


@main.get('/arsip')
@login_required
@permission_required(Permission.ARSIP)
def arsip():
    return render_template('arsip/arsip.html')


@main.get('/surat_masuk_download/<upload_id>')
@login_required
def download_surat_masuk(upload_id):
    surat_masuk = SuratMasuk.query.filter_by(id=upload_id).first()
    return send_file(BytesIO(surat_masuk.lampiran), download_name=surat_masuk.nama_file, as_attachment=True)


@main.get('/daily_activity')
@main.post('/daily_activity')
@login_required
def daily_activity():
    return render_template('daily_activity/daily_activity.html')


@main.get('/disposisi_ke')
def disposisi_ke():
    surat_masuk = SuratMasuk.query.filter_by(dilihat=False)
    return render_template('arsip/disposisi.html', surat_masuk=surat_masuk)


@main.get('/edit/disposisi/<id>')
@main.post('/edit/disposisi/<id>')
def edit_disposisi(id):
    form = DisposisiKeForm()
    disposisi = SuratMasuk.query.filter_by(id=id).first()
    if form.validate_on_submit():
        disposisi.disposisi_ke = form.disposisi.data
        disposisi.dilihat = form.dilihat.data
        db.session.commit()

        flash('Disposisi Successfully', 'success')
        return redirect(url_for('main.disposisi_ke'))

    form.disposisi.data = disposisi.disposisi_ke
    form.dilihat.data = disposisi.dilihat
    return render_template('arsip/edit_disposisi.html', form=form, disposisi=disposisi)


@main.get('/disposisi')
@main.post('/disposisi')
@admin_required
def disposisi():
    form = DisposisiForm()
    disposisi = Disposisi.query.all()
    if form.validate_on_submit():
        disposisi_baru = Disposisi(alias=form.alias.data, nama=form.nama.data)
        db.session.add(disposisi_baru)
        db.session.commit()
        flash('Data Berhasil di Tambahkan', 'success')
        return redirect(url_for('main.disposisi'))

    return render_template('arsip/tambah_disposisi.html', form=form, disposisi=disposisi)


@main.get('/bidang')
@main.post('/bidang')
@admin_required
def bidang():
    form = BidangForm()
    bidang = Bidang.query.all()
    if form.validate_on_submit():
        bidang_baru = Bidang(alias=form.alias.data, nama=form.nama.data)
        db.session.add(bidang_baru)
        db.session.commit()
        flash('Data berhasil di Tambahkan', 'success')
        return redirect(url_for('main.bidang'))

    return render_template('arsip/tambah_bidang.html', form=form, bidang=bidang)


'''
    =========================
    Edit Surat
    ========================
'''


@main.get('/surat_masuk/edit/<id>')
@main.post('/surat_masuk/edit/<id>')
def edit_surat_masuk(id):
    form = EditSuratMasukForm()
    if form.validate_on_submit():
        pass

    return render_template('arsip/edit_surat_masuk.html', form=form)


@main.get('/surat_keluar/<id>/edit')
@main.post('/surat_keluar/<id>/edit')
def edit_surat_keluar(id):
    form = EditSuratKeluarForm()
    if form.validate_on_submit():
        pass

    return render_template('arsip/edit_surat_keluar.html', form=form)


'''
    =========================
    Delete Surat
    ========================
'''


@main.get('/surat_masuk/<id>/delete')
@main.post('/surat_masuk/<id>/delete')
def delete_surat_masuk(id):
    delete_surat = SuratMasuk.query.filter_by(id=id).first()
    db.session.delete(delete_surat)
    db.session.commit()
    flash('Delete Surat Successfully', "success")
    return redirect(url_for('main.surat_masuk'))


@main.get('/surat_keluar/<id>/delete')
@main.post('/surat_keluar/<id>/delete')
def delete_surat_keluar(id):
    delete_surat = SuratKeluar.query.filter_by(id=id).first()
    db.session.delete(delete_surat)
    db.session.commit()
    flash('Delete Surat Successfully', "success")
    return redirect(url_for('main.surat_keluar'))


'''
    =========================
    Lihat dokumen
    ========================
'''


@main.get('/surat_masuk/lampiran/<id>/open')
def open_surat_masuk_dokumen(id):
    surat_masuk = SuratMasuk.query.filter_by(id=id).first()
    return send_file(BytesIO(surat_masuk.lampiran), mimetype='application/pdf')


@main.get('/surat_keluar/lampiran/<id>/open')
def open_surat_keluar_dokumen(id):
    surat_keluar = SuratKeluar.query.filter_by(id=id).first()
    return send_file(BytesIO(surat_keluar.lampiran), mimetype='application/pdf')


'''
    =========================
    Eksperiment route 
    ========================
'''


@main.get('/protected')
@login_required
def protected_routes():
    return 'only authenticate users are allowed!'


@main.get('/admin')
@login_required
@admin_required
def for_admin_only():
    return "For administrators!"


@main.get('/pegawaitu')
@login_required
@permission_required(Permission.ARSIP)
def for_admin_tu():
    return "for admin tu"


@main.get('/pegawai')
@login_required
@permission_required(Permission.PERMOHONAN_SURAT)
def for_pagawai():
    return "for staff"
