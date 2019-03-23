from flask import render_template, url_for
from flask_login import login_required, current_user
from flask_mobility.decorators import mobile_template
from werkzeug.utils import redirect

from undyingkingdoms import app, db
from undyingkingdoms.models import Clan


@app.route('/clans/clan_leave/', methods=['GET', 'POST'])
@login_required
def clan_leave():
    relation = Clan.query.filter_by(user_id=current_user.id).first()
    db.session.delete(relation)
    return redirect(url_for('generic_clan'))
