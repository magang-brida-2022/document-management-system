from flask import Flask, render_template

# import config
from config import Config

def page_not_found(e):
  return "Page not found", 404

def forbidden(e):
  return 'Forbidden', 403  

def create_app():
  app = Flask(__name__)
  app.config.from_object(Config)

  from .auth import auth as auth_blueprint

  app.register_blueprint(auth_blueprint, url_prefix='/auth')

  # error handler
  app.register_error_handler(404, page_not_found)
  app.register_error_handler(403, forbidden)

  return app