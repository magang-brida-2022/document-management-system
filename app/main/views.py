from flask import render_template
from flask_login import login_required
from app.decorators import admin_required, permission_required
from app.models import Permission

from .forms import SuratMasukForm

from . import main


@main.get('/')
def index():
    return render_template('index.html')


@main.get('/surat_masuk')
@login_required
@permission_required(Permission.ARSIP)
def surat_masuk():
    form = SuratMasukForm()

    if form.validate_on_submit():
        pass

    return render_template('arsip/surat_masuk.html', form=form)


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
