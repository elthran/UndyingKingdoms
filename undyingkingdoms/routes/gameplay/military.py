from flask import redirect, url_for, request
from flask_login import login_required

from undyingkingdoms import app


@app.route('/gameplay/military/', methods=['GET', 'POST'])
@login_required
def military():
    return redirect(url_for('mobile', path=request.path[1:]))
