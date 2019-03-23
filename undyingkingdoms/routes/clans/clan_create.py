from flask import render_template
from flask_login import login_required

from undyingkingdoms import app


@app.route('/clans/clan_create/', methods=['GET', 'POST'])
@login_required
def clan_create(template):
    return render_template(template)
