from flask import render_template
from flask_login import login_required

from undyingkingdoms import app


@app.route('/clans/clan_home/', methods=['GET', 'POST'])
@login_required
def clan_home(template):
    return render_template(template)
