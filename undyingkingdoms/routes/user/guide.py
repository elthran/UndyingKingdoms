from flask import render_template
from flask_login import login_required, current_user
from flask_mobility.decorators import mobile_template

from undyingkingdoms import app
from undyingkingdoms.routes.helpers import in_active_session


@app.route('/user/guide/', methods=['GET', 'POST'])
@mobile_template('{mobile/}user/guide.html')
@login_required
@in_active_session
def guide(template):
    return render_template(template)
