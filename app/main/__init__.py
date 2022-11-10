from flask import Blueprint, abort
from sqlalchemy import and_, or_
from flask_login import current_user, login_required

from ..models import Permission, SuratMasuk

main = Blueprint('main', __name__)

from . import views

@main.app_context_processor
def app_context():
    if current_user.is_anonymous:
        return dict(Permission=Permission, TotalDisposisi=SuratMasuk.query.filter(SuratMasuk.disposisi_ke == None).count())

    return dict(Permission=Permission, TotalDisposisi=SuratMasuk.query.filter(SuratMasuk.disposisi_ke == None).count(), TotalFeedback=SuratMasuk.query.filter(and_(SuratMasuk.tindak_lanjut == False, current_user.bidang.nama == SuratMasuk.disposisi_ke)).count())
