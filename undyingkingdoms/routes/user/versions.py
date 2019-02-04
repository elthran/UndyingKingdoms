from flask import render_template
from flask_login import login_required

from undyingkingdoms import app
from undyingkingdoms.routes.helpers import in_active_session


@app.route('/user/versions/', methods=['GET', 'POST'])
@login_required
@in_active_session
def versions():
    return render_template('user/versions.html')
