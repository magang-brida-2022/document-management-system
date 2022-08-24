from flask import render_template, flash, redirect, request, send_file
from flask_login import login_required, current_user
from io import BytesIO

from app.decorators import admin_required, permission_required
from app.models import Permission
from .forms import SuratMasukForm
from ..models import SuratMasuk
from . import main
from .. import db


@main.get('/')
def index():
    return render_template('index.html')


@main.get('/surat_masuk')
@main.post('/surat_masuk')
@login_required
@permission_required(Permission.ARSIP)
def surat_masuk():
    form = SuratMasukForm()
    surat_masuk = SuratMasuk.query.all()

    if form.validate_on_submit():
        no_surat = form.no_surat.data
        asal = form.asal.data
        perihal = form.perihal.data
        tanggal_diterima = form.tanggal_diterima.data
        lampiran = form.lampiran.data
        tujuan = form.tujuan.data

        surat_masuk = SuratMasuk(no_surat=no_surat, asal=asal, perihal=perihal,
                                 tanggal_terima=tanggal_diterima, nama_file=lampiran.filename, lampiran=lampiran.read(), tujuan=tujuan, user=current_user)
        db.session.add(surat_masuk)
        db.session.commit()

        flash("Surat masuk baru berhasil di tambahkan", "success")
        return redirect(request.base_url)

    return render_template('arsip/surat_masuk.html', form=form, surat_masuk=surat_masuk)


@main.get('/surat_keluar')
@login_required
@permission_required(Permission.ARSIP)
def surat_keluar():
    return render_template('arsip/surat_keluar.html')


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
