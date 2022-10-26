from flask import Blueprint

from ..models import Permission, SuratMasuk

main = Blueprint('main', __name__)

from . import views

@main.app_context_processor
def app_context():
    return dict(Permission=Permission, TotalDisposisi=SuratMasuk.query.filter(SuratMasuk.disposisi_ke == None).count(), TotalFeedback=SuratMasuk.query.filter_by(tindak_lanjut=False).count())
