from app import create_app, db
from app.models import User, Role, Permission, SuratMasuk, SuratKeluar, DailyActivity, Bidang, Disposisi, SuratBalasan, InformasiBadan, SubBidang

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Role': Role, 'Permission': Permission, "SuratMasuk": SuratMasuk, "SuratKeluar": SuratKeluar, "DailyActivity": DailyActivity, 'Bidang': Bidang, 'Disposisi': Disposisi, 'SuratBalasan': SuratBalasan, "InformasiBadan": InformasiBadan, "SubBidang": SubBidang}
