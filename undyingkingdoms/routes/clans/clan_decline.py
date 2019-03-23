from flask import render_template, url_for
from flask_login import login_required, current_user
from flask_mobility.decorators import mobile_template
from werkzeug.utils import redirect

from undyingkingdoms import app, db
from undyingkingdoms.models import Clan


@app.route('/clans/clan_decline/', methods=['GET', 'POST'])
@login_required
def clan_decline():
    invite = Clan.query.filter_by(user_id=current_user.id, status="Pending").first()
    invite.status = "Declined"
    return redirect(url_for('generic_clan'))
