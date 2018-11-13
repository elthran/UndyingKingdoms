from flask import render_template
from flask_login import login_required

from undyingkingdoms import app


@login_required
@app.route('/gameplay/attack_results/', methods=['GET', 'POST'])
def attack_results():
    return render_template('gameplay/attack_results.html', results=results)
