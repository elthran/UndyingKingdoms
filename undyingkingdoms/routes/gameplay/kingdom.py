from flask import render_template
from flask_login import login_required

from undyingkingdoms import app


@login_required
@app.route('/gameplay/kingdom/', methods=['GET', 'POST'])
def kingdom():
    return render_template('gameplay/kingdom.html')
