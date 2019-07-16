from flask import redirect, url_for, request
from flask_login import login_required

from app import app


@app.route('/user/forum/<int:thread_id>/<int:post_id>', methods=['GET'])
@login_required
def forum(thread_id, post_id):
    return redirect(url_for('mobile', path=request.path[1:]))
