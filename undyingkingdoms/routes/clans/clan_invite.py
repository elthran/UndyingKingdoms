from flask import url_for
from flask_login import login_required, current_user
from werkzeug.utils import redirect

from undyingkingdoms import app, User
from undyingkingdoms.models import Clan, Notification


@app.route('/clans/clan_invite/<int:user_id>/<int:clan_id>', methods=['GET', 'POST'])
@login_required
def clan_invite(user_id, clan_id):
    county = current_user.county
    kingdom = county.kingdom
    invited_user = User.query.get(user_id)
    clan = Clan.query.get(clan_id)

    member_history = Clan.query.filter_by(id=clan_id, user_id=user_id).first()
    if member_history:
        print("history", user_id, clan_id)
        member_history.status = "Invited"
    else:
        print("nully")
        invite = Clan(clan.kingdom_id, user_id, status="Invited")
        invite.save()
    message = Notification(invited_user.county.id,
                           "Clan Invite",
                           "You were invited to join a clan",
                           kingdom.world.day,
                           "Clan")
    message.save()
    return redirect(url_for('generic_clan'))
