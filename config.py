import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    SECRET_KEY = os.urandom(24)
    CKEDITOR_PKG_TYPE = "basic"

    # toastr
    TOASTR_POSITION_CLASS = 'toast-bottom-right'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    IS_ADMIN = os.getenv('IS_ADMIN')


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    pass
