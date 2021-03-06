from flask import request, url_for, redirect
from flask_login import login_required, current_user

from app import app


@app.route('/gameplay/research/', methods=['GET'])
@login_required
def research():
    return redirect(url_for('mobile', path=request.path[1:]))
