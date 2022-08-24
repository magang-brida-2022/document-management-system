from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap5

# import config
from config import Config

db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap5()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def page_not_found(e):
    return "Page not found", 404


def internat_server_error(e):
    db.session.rollback()
    return 'Internal server error', 500


def forbidden(e):
    return 'Forbidden', 403


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bootstrap.init_app(app)

    from .auth import auth as auth_blueprint
    from .main import main as main_blueprint
    from .user import users as user_blueprint

    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(user_blueprint, url_prefix='/user')
    app.register_blueprint(main_blueprint)

    # error handler
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(403, forbidden)
    app.register_error_handler(500, internat_server_error)

    return app
