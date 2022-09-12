import os
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY') or os.urandom(12)
    SQLALCHEMY_DATABASE_URI = 'postgresql://superiorkid:root@localhost/surat'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # toastr
    TOASTR_POSITION_CLASS = 'toast-bottom-right'

    IS_ADMIN = "susan@example.com"
