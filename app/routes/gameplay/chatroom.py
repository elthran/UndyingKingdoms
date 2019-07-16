from flask import url_for, request
from flask_login import login_required
from werkzeug.utils import redirect

from app import app


@app.route('/gameplay/chatroom', methods=["GET"])
@login_required
def chatroom():
    # slice of leading /
    return redirect(url_for('mobile', path=request.path[1:]))
