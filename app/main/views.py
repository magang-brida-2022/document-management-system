import os
from flask import render_template, flash, redirect, request, send_file, url_for, make_response
from flask_login import login_required, current_user
from io import BytesIO


from app.decorators import admin_required, permission_required
from app.models import Permission, Bidang, Disposisi
from .forms import SuratMasukForm, SuratKeluarForm, DisposisiForm, BidangForm, DisposisiKeForm, EditSuratMasukForm, EditSuratKeluarForm, EditBidangForm, EditDisposisiForm, SudahDitindakLanjutForm, SuratBalasanForm
from ..models import SuratMasuk, SuratKeluar, Bidang, Disposisi, SuratBalasan
from . import main
from .. import db, documents_allowed_extension
from .helpers.surat_balasan_helper import PDF
from .. import create_app


@main.get('/')
# @login_required
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))

    return render_template('index.html', title="Dashboard")


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
        jenis = form.jenis.data
        tanggal_surat = form.tanggal_surat.data
        tanggal_diterima = form.tanggal_diterima.data
        lampiran = form.lampiran.data

        if lampiran and documents_allowed_extension(lampiran.filename):
            surat_masuk = SuratMasuk(nomor=no_surat, asal=asal, perihal=perihal, jenis=jenis, tanggal_surat=tanggal_surat,
                                     tanggal_diterima=tanggal_diterima, nama_file=lampiran.filename, lampiran=lampiran.read())
            db.session.add(surat_masuk)
            db.session.commit()

            flash("Surat masuk baru berhasil di tambahkan", "success")
            return redirect(request.base_url)
        else:
            flash('allowed file types are .pdf only', 'error')
            return redirect(request.base_url)

    return render_template('arsip/surat_masuk.html', form=form, surat_masuk=surat_masuk, title="Surat Masuk")


@main.get('/surat_keluar')
@main.post('/surat_keluar')
@login_required
# @permission_required(Permission.ARSIP)
def surat_keluar():
    form = SuratKeluarForm()
    surat_keluar = SuratKeluar.query.all()

    if form.validate_on_submit():
        nomor_surat = form.no_surat.data
        jenis = form.jenis.data
        perihal = form.perihal.data
        tanggal_dikeluarkan = form.tanggal_dikeluarkan.data
        tujuan = form.tujuan.data
        lampiran = form.lampiran.data

        if lampiran and documents_allowed_extension(lampiran.filename):
            surat_keluar = SuratKeluar(nomor=nomor_surat, jenis=jenis, perihal=perihal, tanggal_dikeluarkan=tanggal_dikeluarkan,
                                       tujuan=tujuan, nama_file=lampiran.filename, lampiran=lampiran.read())
            db.session.add(surat_keluar)
            db.session.commit()
            flash("Surat keluar baru berhasil ditambahkan", "success")
            return redirect(request.base_url)
        else:
            flash('allowed file types are .pdf only', 'error')
            return redirect(request.base_url)

    return render_template('arsip/surat_keluar.html', form=form, surat_keluar=surat_keluar, title="Surat Keluar")


@main.get('/ditindak/')
@main.post('/ditindak/')
def feedback():
    surat_masuk = SuratMasuk.query.filter_by(tindak_lanjut=False).all()
    return render_template('arsip/feedback.html', surat_masuk=surat_masuk)


@main.get('/arsip')
@login_required
@permission_required(Permission.ARSIP)
def arsip():
    return render_template('arsip/arsip.html')


@main.get('/disposisi_ke')
def disposisi_ke():
    surat_masuk = SuratMasuk.query.filter_by(dilihat=False)
    return render_template('arsip/disposisi.html', surat_masuk=surat_masuk, title="Atur Disposisi")


@main.get('/diteruskan/<id>')
@main.post('/diteruskan/<id>')
def diteruskan(id):
    form = DisposisiKeForm()
    disposisi = SuratMasuk.query.filter_by(id=id).first()
    if form.validate_on_submit():
        disposisi.disposisi_ke = form.disposisi.data
        disposisi.pesan = form.pesan.data
        disposisi.dilihat = form.dilihat.data
        db.session.commit()

        flash('Disposisi Successfully', 'success')
        return redirect(url_for('main.disposisi_ke'))

    form.disposisi.data = disposisi.disposisi_ke
    form.pesan.data = disposisi.pesan
    form.dilihat.data = disposisi.dilihat
    return render_template('arsip/disposisi_ke.html', form=form, disposisi=disposisi, title="Pilih Disposisi")


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

    return render_template('arsip/tambah_disposisi.html', form=form, disposisi=disposisi, title="Disposisi Management")


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

    return render_template('arsip/tambah_bidang.html', form=form, bidang=bidang, title="Bidang Management")


@main.get('/surat_balasan')
@main.post('/surat_balasan')
def surat_balasan():
    pdf = PDF()
    form = SuratBalasanForm()

    pdf.add_page(orientation='P', format='Legal')

    pdf.gambar(os.path.join(create_app().static_folder, 'img/ntblogo.png'))
    pdf.judul('PEMERINTAH PROVINSI NUSA TENGGARA BARAT', 'BADAN RISET DAN INOVASI DAERAH',
              'Jalan Bypass ZAMIA 2 - Desa Lelede - Kecamatan Kediri - kode pos 83362', 'Kabupaten Lombok Barat - Provinsi NTB, Email: brida@ntbprov.go.id Website: brida.ntbprov.go.id')
    pdf.garis()

    _id = request.args.get('id')
    surat_masuk = SuratMasuk.query.filter_by(
        id=_id).first()

    if form.validate_on_submit():
        response = make_response(pdf.output())
        response.headers.set('Content-Disposition',
                             'attachment', filename='test.pdf')
        response.headers.set('Content-Type', 'application/pdf')
        return response

        # return send_file(BytesIO(surat_keluar.lampiran), mimetype='application/pdf')

        # return send_file(BytesIO(pdf.output(name="test.pdf")), mimetype="application/pdf")

        # balas = SuratBalasan(kepala=form.kepala.data, isi=form.isi.data,
        #                      penutup=form.penutup.data, surat_masuk=surat_masuk)
        # db.session.add(balas)
        # db.session.commit()
        # flash("Surat Balasan Berhasil di Tambahkan", "success")
        # return redirect(request.base_url)

    form.kepala.data = 'test kepala data'
    form.isi.data = 'test isi data'
    form.penutup.data = 'test penututp data'
    return render_template("arsip/surat_balasan.html", form=form)


'''
    =========================
    Edit Surat
    ========================
'''


@main.get('/surat_masuk/edit/<id>')
@main.post('/surat_masuk/edit/<id>')
def edit_surat_masuk(id):
    form = EditSuratMasukForm()
    surat_masuk = SuratMasuk.query.filter_by(id=id).first()
    if form.validate_on_submit():
        if form.lampiran.data is not None:
            surat_masuk.lampiran = form.lampiran.data.read()
            surat_masuk.nama_file = form.lampiran.data.filename

        surat_masuk.nomor = form.no_surat.data
        surat_masuk.asal = form.asal.data
        surat_masuk.perihal = form.perihal.data
        surat_masuk.tanggal_surat = form.tanggal_surat.data
        surat_masuk.tanggal_diterima = form.tanggal_diterima.data
        surat_masuk.disposisi_ke = form.disposisi.data

        db.session.commit()
        flash("surat masuk update successfully", 'success')
        return redirect(url_for('main.surat_masuk'))

    form.no_surat.data = surat_masuk.nomor
    form.asal.data = surat_masuk.asal
    form.perihal.data = surat_masuk.perihal
    form.tanggal_surat.data = surat_masuk.tanggal_surat
    form.tanggal_diterima.data = surat_masuk.tanggal_diterima
    form.lampiran.data = surat_masuk.lampiran
    form.disposisi.data = surat_masuk.disposisi_ke

    return render_template('arsip/edit_surat_masuk.html', form=form, title="Edit Surat Masuk")


@main.get('/surat_keluar/<id>/edit')
@main.post('/surat_keluar/<id>/edit')
def edit_surat_keluar(id):
    form = EditSuratKeluarForm()
    surat_keluar = SuratKeluar.query.filter_by(id=id).first()
    if form.validate_on_submit():
        if form.lampiran.data is not None:
            surat_keluar.lampiran = form.lampiran.data.read()
            surat_keluar.nama_file = form.lampura.data.filename

        surat_keluar.nomor = form.no_surat.data
        surat_keluar.jenis = form.jenis_surat.data
        surat_keluar.ringkasan = form.ringkasan.data
        surat_keluar.tanggal_dikeluarkan = form.tanggal_dikeluarkan.data
        surat_keluar.tujuan = form.tujuan.data

        db.session.commit()
        flash('Surat Keluar Update Successfully', "Success")
        return redirect(url_for('main.surat_keluar'))

    form.no_surat.data = surat_keluar.nomor
    form.jenis_surat.data = surat_keluar.jenis
    form.ringkasan.data = surat_keluar.ringkasan
    form.tanggal_dikeluarkan.data = surat_keluar.tanggal_dikeluarkan
    form.tujuan.data = surat_keluar.tujuan
    form.lampiran.data = surat_keluar.lampiran
    return render_template('arsip/edit_surat_keluar.html', form=form, title="Edit Surat Keluar")


@main.get('/bidang/<id>/edit')
@main.post('/bidang/<id>/edit')
def edit_bidang(id):
    form = EditBidangForm()
    bidang = Bidang.query.filter_by(id=id).first()
    if form.validate_on_submit():
        bidang.alias = form.alias.data
        bidang.nama = form.nama.data

        db.session.commit()
        flash('Update Bidang Successfully', 'success')
        return redirect(url_for('main.bidang'))

    form.alias.data = bidang.alias
    form.nama.data = bidang.nama
    return render_template('arsip/edit_bidang.html', form=form, bidang=bidang, title="Edit Bidang")


@main.get('/disposisi/<id>/edit')
@main.post('/disposisi/<id>/edit')
def edit_disposisi(id):
    form = EditDisposisiForm()
    disposisi = Disposisi.query.filter_by(id=id).first()
    if form.validate_on_submit():
        disposisi.alias = form.alias.data
        disposisi.nama = form.nama.data

        db.session.commit()
        flash("Update Disposisi Successfully", 'success')
        return redirect(url_for('main.disposisi'))

    form.alias.data = disposisi.alias
    form.nama.data = disposisi.nama
    return render_template('arsip/edit_disposisi.html', form=form, disposisi=disposisi, title="Edit Disposisi")


@main.get('/ditindak/<id>')
@main.post('/ditindak/<id>')
def edit_feedback(id):
    form = SudahDitindakLanjutForm()
    surat_masuk = SuratMasuk.query.filter_by(
        disposisi_ke=current_user.bidang.nama).all()
    if form.validate_on_submit():
        surat_masuk.tindak_lanjut = form.ditindak_lanjut.data

        db.session.commit()
        flash("Task Complete", "success")
        return redirect(url_for('main.feedback'))

    return render_template('arsip/edit_feedback.html', form=form, surat_masuk=surat_masuk)


'''
    =========================
    Delete
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
@admin_required
def delete_surat_keluar(id):
    delete_surat = SuratKeluar.query.filter_by(id=id).first()
    db.session.delete(delete_surat)
    db.session.commit()
    flash('Delete Surat Successfully', "success")
    return redirect(url_for('main.surat_keluar'))


@main.get('/bidang/<id>/delete')
@main.post('/bidang/<id>/delete')
@admin_required
def delete_bidang(id):
    delete_bidang = Bidang.query.filter_by(id=id).first()
    db.session.delete(delete_bidang)
    db.session.commit()
    flash("Delete Bidang Successfully", 'success')
    return redirect(url_for('main.bidang'))


@main.get('/disposisi/<id>/delete')
@main.post('/disposisi/<id>/delete')
@admin_required
def delete_disposisi(id):
    delete_disposisi = Disposisi.query.filter_by(id=id).first()
    db.session.delete(delete_disposisi)
    db.session.commit()
    flash('Delete Bidang Successfully', 'success')
    return redirect(url_for('main.disposisi'))


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
    download dokumen 
    ========================
'''


@main.get('/surat_masuk_download/<upload_id>')
@login_required
def download_surat_masuk(upload_id):
    surat_masuk = SuratMasuk.query.filter_by(id=upload_id).first()
    return send_file(BytesIO(surat_masuk.lampiran), download_name=surat_masuk.nama_file, as_attachment=True)


@main.get('/surat_keluar_download/<upload_id>')
@login_required
def download_surat_keluar(upload_id):
    surat_keluar = SuratKeluar.query.filter_by(id=upload_id).first()
    return send_file(BytesIO(surat_keluar.lampiran), download_name=surat_keluar.nama_file, as_attachment=True)


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
