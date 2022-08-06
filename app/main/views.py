from flask import render_template
from flask_login import login_required

from . import main


@main.get('/')
def index():
    return render_template('index.html')


@main.get('/protected')
@login_required
def protected_routes():
    return 'only authenticate users are allowed!'
