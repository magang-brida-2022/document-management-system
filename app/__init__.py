from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .models import db

# import config
from config import Config

db = SQLAlchemy()
migrate = Migrate()

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

  from .auth import auth as auth_blueprint
  from .main import main as main_blueprint

  app.register_blueprint(auth_blueprint, url_prefix='/auth')
  app.register_blueprint(main_blueprint)

  # error handler
  app.register_error_handler(404, page_not_found)
  app.register_error_handler(403, forbidden)
  app.register_error_handler(500, internat_server_error)

  return app