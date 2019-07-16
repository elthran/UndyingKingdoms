from flask import url_for, redirect
from flask_login import login_required, current_user

from app import app
from app.models.exports import Clan


@app.route('/clans/clan_leave/', methods=['GET', 'POST'])
@login_required
def clan_leave():
    relation = Clan.query.filter_by(user_id=current_user.id).first()
    relation.status = "Quit"
    return redirect(url_for('generic_clan'))
