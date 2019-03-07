from flask import render_template
from flask_login import login_required
from flask_mobility.decorators import mobile_template

from undyingkingdoms import app


@app.route('/user/versions/', methods=['GET', 'POST'])
@mobile_template('{mobile/}user/versions.html')
@login_required
def versions(template):
    return render_template(template)
