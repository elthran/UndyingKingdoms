from flask import render_template, url_for
from flask_login import login_required, current_user
from werkzeug.utils import redirect

from undyingkingdoms import app, User
from undyingkingdoms.models import Clan, Notification


@app.route('/clans/clan_invite/<int:user_id>/<int:clan_id>', methods=['GET', 'POST'])
@login_required
def clan_invite(user_id, clan_id):
    county = current_user.county
    kingdom = county.kingdom
    user = User.query.get(user_id)
    clan = Clan.query.get(clan_id)
    invite = Clan(clan.kingdom_id, user.id, status="Pending")
    invite.save()
    message = Notification(user.county.id,
                           "Clan Invite",
                           "You were invited to join a clan",
                           kingdom.world.day,
                           "Clan")
    message.save()
    return redirect(url_for('generic_clan'))
