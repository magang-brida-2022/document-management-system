import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'postgresql://superiorkid:root@localhost/surat'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)

    # toastr
    TOASTR_POSITION_CLASS = 'toast-bottom-right'

    # admin-example
    IS_ADMIN = "susan@example.com"


# class ProductionConfig(Config):
#     SQLALCHEMY_DATABASE_URI = 'postgresql://superiorkid:root@localhost/eletter'
#     SQLALCHEMY_TRACK_MODIFICATIONS = False


# class DevelopmentConfig(Config):
#     SQLALCHEMY_DATABASE_URI = 'postgresql://superiorkid:root@localhost/eletter-dev'
#     SQLALCHEMY_TRACK_MODIFICATIONS = False


# class TestingConfig(Config):
#     pass
