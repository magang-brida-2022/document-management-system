import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    SECRET_KEY = os.urandom(24)

    SQLALCHEMY_DATABASE_URI = 'postgresql://superiorkid:root@localhost/surat'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # toastr
    TOASTR_POSITION_CLASS = 'toast-bottom-right'

    # admin-example
    IS_ADMIN = "susan@example.com"


# class ProductionConfig(Config):
#     SQLALCHEMY_DATABASE_URI = 'postgresql://superiorkid:root@localhost/surat'
#     DEBUG = True


# class DevelopmentConfig(Config):
#     SQLALCHEMY_DATABASE_URI = 'postgresql://superiorkid:root@localhost/surat-dev'
#     SQLALCHEMY_TRACK_MODIFICATIONS = False


# class TestingConfig(Config):
#     pass
