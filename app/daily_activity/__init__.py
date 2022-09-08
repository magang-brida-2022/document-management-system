from flask import Blueprint

daily_activity = Blueprint('daily_activity', __name__)

from . import views