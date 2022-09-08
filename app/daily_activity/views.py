from flask import render_template
from flask_login import login_required
from . import daily_activity


@daily_activity.get('/')
@login_required
def daily():
    return render_template('daily_activity/daily_activity.html')
