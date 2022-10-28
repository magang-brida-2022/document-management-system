import os

from flask import render_template, flash, redirect, request, send_file, url_for, make_response, abort
from flask_login import login_required, current_user
from io import BytesIO
from docxtpl import DocxTemplate
from sqlalchemy import and_

from app.decorators import admin_required, permission_required
from app.models import Permission, Bidang, Disposisi
from .forms import SuratMagangForm, SuratMasukForm, SuratKeluarForm, DisposisiForm, BidangForm, DisposisiKeForm, EditSuratMasukForm, EditSuratKeluarForm, EditBidangForm, EditDisposisiForm, JenisSuratBalasanForm, AgendaForm
from ..models import SuratMasuk, SuratKeluar, Bidang, Disposisi, User, Agenda
from . import main
from .. import db, documents_allowed_extension
from .. import create_app
from .utils.local_datetime_formatting import to_localtime


@main.get('/')
@main.post('/')
# @login_required
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))

    agenda_form = AgendaForm()
    agenda = Agenda.query.all()

    if agenda_form.validate_on_submit():
        if agenda_form.waktu_selesai:
            waktu = f"{agenda_form.waktu_mulai.data} - {agenda_form.waktu_selesai.data}"
        else:
            waktu = {agenda_form.waktu_mulai}
        agenda = agenda_form.kegiatan.data
        tempat = agenda_form.tempat

        agenda_baru = Agenda(waktu=waktu, agenda=agenda, tempat=tempat)
        db.session.add(agenda_baru)
        db.session.commit()
        flash("Agenda Berhasil Ditambahkan", "success")

        return redirect(url_for('main.index'))

    total_user = User.query.count()
    total_surat_masuk = SuratMasuk.query.count()
    total_surat_keluar = SuratKeluar.query.count()

    return render_template('index.html', title="Dashboard", total_user=total_user, total_surat_masuk=total_surat_masuk, total_surat_keluar=total_surat_keluar, page='dashboard', agenda_form=agenda_form, agenda=agenda)


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
        rak = form.rak.data
        lampiran = form.lampiran.data

        if lampiran and documents_allowed_extension(lampiran.filename):
            surat_masuk = SuratMasuk(nomor=no_surat, asal=asal, perihal=perihal, jenis=jenis, tanggal_surat=tanggal_surat,
                                     tanggal_diterima=tanggal_diterima, rak=rak, lampiran=lampiran.read())
            db.session.add(surat_masuk)
            db.session.commit()

            flash("Surat masuk baru berhasil di tambahkan", "success")
            return redirect(request.base_url)
        else:
            flash('allowed file types are .pdf only', 'error')
            return redirect(request.base_url)

    return render_template('arsip/surat_masuk.html', form=form, surat_masuk=surat_masuk, title="Surat Masuk", page='surat_masuk')


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
            surat_keluar = SuratKeluar(nomor=nomor_surat, jenis=jenis, perihal=perihal,
                                       tanggal_dikeluarkan=tanggal_dikeluarkan, tujuan=tujuan, lampiran=lampiran.read())
            db.session.add(surat_keluar)
            db.session.commit()
            flash("Surat keluar baru berhasil ditambahkan", "success")
            return redirect(request.base_url)
        else:
            flash('allowed file types are .pdf only', 'error')
            return redirect(request.base_url)

    return render_template('arsip/surat_keluar.html', form=form, surat_keluar=surat_keluar, title="Surat Keluar", page='surat_keluar')


@main.get('/ditindak/')
@main.post('/ditindak/')
@login_required
def feedback():
    # surat masuk yang belum ditindaklanjuti
    surat_masuk = SuratMasuk.query.filter(and_(
        SuratMasuk.disposisi_ke == current_user.bidang.nama, SuratMasuk.tindak_lanjut == False)).all()

    # surat masuk yang sudah ditindaklanjuti
    surat_masuk_confirm = SuratMasuk.query.filter(and_(
        SuratMasuk.disposisi_ke == current_user.bidang.nama, SuratMasuk.tindak_lanjut == True)).all()

    return render_template('arsip/feedback.html', surat_masuk=surat_masuk, page='feedback', surat_masuk_confirm=surat_masuk_confirm)


@main.get('/arsip')
@login_required
@permission_required(Permission.ARSIP)
def arsip():
    return render_template('arsip/arsip.html')


@main.get('/disposisi_ke')
def disposisi_ke():
    surat_masuk = SuratMasuk.query.filter(
        SuratMasuk.disposisi_ke == None).all()

    history = SuratMasuk.query.filter(SuratMasuk.disposisi_ke != None).all()
    return render_template('arsip/disposisi.html', surat_masuk=surat_masuk, history=history, title="Atur Disposisi", page='disposisi')


@main.get('/diteruskan/<id>')
@main.post('/diteruskan/<id>')
def diteruskan(id):
    form = DisposisiKeForm()
    disposisi = SuratMasuk.query.filter_by(id=id).first()
    if form.validate_on_submit():
        disposisi.disposisi_ke = form.disposisi.data
        disposisi.pesan = form.pesan.data
        disposisi.dilihat = True
        db.session.commit()

        flash('Disposisi Successfully', 'success')
        return redirect(url_for('main.disposisi_ke'))

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

    return render_template('arsip/tambah_disposisi.html', form=form, disposisi=disposisi, title="Disposisi Management", page='disposisi_management')


@main.get('/bidang')
@main.post('/bidang')
@admin_required
def bidang():
    form = BidangForm()
    bidang = Bidang.query.all()
    if form.validate_on_submit():
        bidang_baru = Bidang(kode=form.kode.data, nama=form.nama.data)
        db.session.add(bidang_baru)
        db.session.commit()
        flash('Data berhasil di Tambahkan', 'success')
        return redirect(url_for('main.bidang'))

    return render_template('arsip/tambah_bidang.html', form=form, bidang=bidang, title="Bidang Management", page="bidang")


'''
    =========================
    Edit Surat
    ========================
'''


@ main.get('/surat_masuk/edit/<id>')
@ main.post('/surat_masuk/edit/<id>')
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
        surat_masuk.rak = form.rak.data
        surat_masuk.tanggal_surat = form.tanggal_surat.data
        surat_masuk.tanggal_diterima = form.tanggal_diterima.data
        surat_masuk.disposisi_ke = Disposisi.query.get(form.disposisi.data)

        db.session.commit()
        flash("surat masuk update successfully", 'success')
        return redirect(url_for('main.surat_masuk'))

    form.no_surat.data = surat_masuk.nomor
    form.asal.data = surat_masuk.asal
    form.perihal.data = surat_masuk.perihal
    form.tanggal_surat.data = surat_masuk.tanggal_surat
    form.tanggal_diterima.data = surat_masuk.tanggal_diterima
    form.lampiran.data = surat_masuk.lampiran
    form.rak.data = surat_masuk.rak
    form.disposisi.data = surat_masuk.disposisi_ke

    return render_template('arsip/edit_surat_masuk.html', form=form, title="Edit Surat Masuk")


@ main.get('/surat_keluar/<id>/edit')
@ main.post('/surat_keluar/<id>/edit')
def edit_surat_keluar(id):
    form = EditSuratKeluarForm()
    surat_keluar = SuratKeluar.query.filter_by(id=id).first()
    if form.validate_on_submit():
        if form.lampiran.data is not None:
            surat_keluar.lampiran = form.lampiran.data.read()
            surat_keluar.nama_file = form.lampiran.data.filename

        surat_keluar.nomor = form.no_surat.data
        surat_keluar.jenis = form.jenis.data
        surat_keluar.perihal = form.perihal.data
        surat_keluar.tanggal_dikeluarkan = form.tanggal_dikeluarkan.data
        surat_keluar.tujuan = form.tujuan.data

        db.session.commit()
        flash('Surat Keluar Update Successfully', "Success")
        return redirect(url_for('main.surat_keluar'))

    form.no_surat.data = surat_keluar.nomor
    form.jenis.data = surat_keluar.jenis
    form.perihal.data = surat_keluar.perihal
    form.tanggal_dikeluarkan.data = surat_keluar.tanggal_dikeluarkan
    form.tujuan.data = surat_keluar.tujuan
    form.lampiran.data = surat_keluar.lampiran
    return render_template('arsip/edit_surat_keluar.html', form=form, title="Edit Surat Keluar")


@ main.get('/bidang/<id>/edit')
@ main.post('/bidang/<id>/edit')
def edit_bidang(id):
    form = EditBidangForm()
    bidang = Bidang.query.filter_by(id=id).first()
    if form.validate_on_submit():
        bidang.kode = form.kode.data
        bidang.nama = form.nama.data

        db.session.commit()
        flash('Update Bidang Successfully', 'success')
        return redirect(url_for('main.bidang'))

    form.kode.data = bidang.kode
    form.nama.data = bidang.nama
    return render_template('arsip/edit_bidang.html', form=form, bidang=bidang, title="Edit Bidang")


@ main.get('/disposisi/<id>/edit')
@ main.post('/disposisi/<id>/edit')
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


@ main.get('/ditindak/<id>')
@ main.post('/ditindak/<id>')
def edit_feedback(id):
    # form = SudahDitindakLanjutForm()
    surat_masuk = SuratMasuk.query.get_or_404(id)
    surat_masuk.tindak_lanjut = True
    db.session.commit()
    flash("Task Complete", "success")
    return redirect(url_for('main.feedback'))


'''
    =========================
    Delete
    ========================
'''


@ main.get('/surat_masuk/<id>/delete')
@ main.post('/surat_masuk/<id>/delete')
def delete_surat_masuk(id):
    delete_surat = SuratMasuk.query.filter_by(id=id).first()
    db.session.delete(delete_surat)
    db.session.commit()
    flash('Delete Surat Successfully', "success")
    return redirect(url_for('main.surat_masuk'))


@ main.get('/surat_keluar/<id>/delete')
@ main.post('/surat_keluar/<id>/delete')
def delete_surat_keluar(id):
    delete_surat = SuratKeluar.query.filter_by(id=id).first()
    db.session.delete(delete_surat)
    db.session.commit()
    flash('Delete Surat Successfully', "success")
    return redirect(url_for('main.surat_keluar'))


@ main.get('/bidang/<id>/delete')
@ main.post('/bidang/<id>/delete')
@ admin_required
def delete_bidang(id):
    delete_bidang = Bidang.query.filter_by(id=id).first()
    db.session.delete(delete_bidang)
    db.session.commit()
    flash("Delete Bidang Successfully", 'success')
    return redirect(url_for('main.bidang'))


@ main.get('/disposisi/<id>/delete')
@ main.post('/disposisi/<id>/delete')
@ admin_required
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


@ main.get('/surat_masuk/lampiran/<id>/open')
def open_surat_masuk_dokumen(id):
    surat_masuk = SuratMasuk.query.filter_by(id=id).first()
    return send_file(BytesIO(surat_masuk.lampiran), mimetype='application/pdf')


@ main.get('/surat_keluar/lampiran/<id>/open')
def open_surat_keluar_dokumen(id):
    surat_keluar = SuratKeluar.query.filter_by(id=id).first()
    return send_file(BytesIO(surat_keluar.lampiran), mimetype='application/pdf')


'''
    =========================
    download dokumen
    ========================
'''


@ main.get('/surat_masuk_download/<upload_id>')
@ login_required
def download_surat_masuk(upload_id):
    surat_masuk = SuratMasuk.query.filter_by(id=upload_id).first()
    return send_file(BytesIO(surat_masuk.lampiran), download_name=surat_masuk.nama_file, as_attachment=True)


@ main.get('/surat_keluar_download/<upload_id>')
@ login_required
def download_surat_keluar(upload_id):
    surat_keluar = SuratKeluar.query.filter_by(id=upload_id).first()
    return send_file(BytesIO(surat_keluar.lampiran), download_name=surat_keluar.nama_file, as_attachment=True)


@main.get('/surat_balasan/jenis_surat')
@main.post('/surat_balasan/jenis_surat')
def pilih_jenis_surat():
    form = JenisSuratBalasanForm()
    _id = request.args.get('id')

    if form.validate_on_submit():
        jenis = form.jenis.data
        if jenis == "magang":
            return redirect(url_for('main.generate_surat', id=_id))

    return render_template('arsip/jenis_surat.html', form=form)


@main.get('/surat_balasan/magang/<int:id>')
@main.post('/surat_balasan/magang/<int:id>')
def generate_surat(id):
    surat = SuratMasuk.query.filter_by(id=id).first()
    form = SuratMagangForm()

    docx_in_memory = BytesIO()
    SRCDIR = os.path.dirname(os.path.abspath(__file__))
    DATADIR = os.path.join(SRCDIR, 'docx_template')

    if form.validate_on_submit():
        context = {
            "penerima": surat.asal,
            "nomor_surat_masuk": surat.nomor,
            "tanggal_diterima": to_localtime(surat.tanggal_diterima),
            "perihal": surat.perihal,
            "tanggal_mulai": form.tanggal_mulai.data,
            "lama_kegiatan": form.lama_kegiatan.data,
            "tanggal_surat": form.tanggal_surat.data,
            "sifat_surat": form.sifat_surat.data,
            "jumlah_lampiran": form.jumlah_lampiran.data
        }

        document = DocxTemplate(os.path.join(
            DATADIR, 'balasan_magang.docx'))
        document.render(context)
        document.save(docx_in_memory)
        docx_in_memory.seek(0)
        return send_file(docx_in_memory, as_attachment=True, download_name='untitled.docx')

    return render_template('arsip/surat_balasan_form/balasan_magang.html', form=form, surat=surat)


@main.get('/settings')
def settings():
    return render_template('settings.html')
