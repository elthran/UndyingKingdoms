from flask import render_template
from flask_login import login_required
from flask_mobility.decorators import mobile_template

from undyingkingdoms import app
from undyingkingdoms.routes.helpers import in_active_session


@app.route('/user/versions/', methods=['GET', 'POST'])
@mobile_template('{mobile/}user/versions.html')
@login_required
@in_active_session
def versions(template):
    return render_template(template)
