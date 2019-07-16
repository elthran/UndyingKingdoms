from flask import render_template
from flask_login import login_required
from flask_mobility.decorators import mobile_template

from app import app


@app.route('/clans/clan_home/', methods=['GET', 'POST'])
@mobile_template('{mobile/}clans/clan_home.html')
@login_required
def clan_home(template):
    return render_template(template)
