from flask_login import login_required

from . import main


@main.get('/')
def index():
    return 'ini index'


@main.get('/protected')
@login_required
def protected_routes():
    return 'only authenticate users are allowed!'
