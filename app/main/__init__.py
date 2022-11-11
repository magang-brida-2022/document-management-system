from flask import Blueprint
from sqlalchemy import and_
from flask_login import current_user

from ..models import Permission, SuratMasuk

main = Blueprint('main', __name__)

from . import views

@main.app_context_processor
def app_context():
    if current_user.is_anonymous:
        return dict(Permission=Permission, TotalDisposisi=SuratMasuk.query.filter(SuratMasuk.disposisi_ke == None).count())

    def decrypt_password(hash_passowrd):
        return hash_passowrd


    return dict(Permission=Permission, TotalDisposisi=SuratMasuk.query.filter(SuratMasuk.disposisi_ke == None).count(), TotalFeedback=SuratMasuk.query.filter(and_(SuratMasuk.tindak_lanjut == False, current_user.bidang.nama == SuratMasuk.disposisi_ke)).count(), decrypt_password=decrypt_password)
