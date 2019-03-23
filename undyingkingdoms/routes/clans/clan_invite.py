from flask import render_template
from flask_login import login_required, current_user

from undyingkingdoms import app, User
from undyingkingdoms.models import Clan, Notification


@app.route('/clans/clan_invite/<int:user_id>/<int:clan_id>', methods=['GET', 'POST'])
@login_required
def clan_invite(template, user_id, clan_id):
    user = User.query.get(user_id)
    clan = Clan.query.get(clan_id)
    invite = Clan(clan.kingdom_id, user.id, status="Pending")
    invite.save()
    message = Notification(user.county.id,
                           "Clan Invite",
                           "You were invited to join a clan",
                           current_user.county.world.day,
                           "Clan")
    message.save()
    return render_template(template)
