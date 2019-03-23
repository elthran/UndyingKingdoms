from flask import render_template
from flask_login import login_required, current_user

from undyingkingdoms import app, db
from undyingkingdoms.models import Clan


@app.route('/clans/clan_leave/', methods=['GET', 'POST'])
@login_required
def clan_leave(template):
    relation = Clan.query.filter_by(user_id=current_user.id).first()
    db.session.delete(relation)
    return render_template(template)
