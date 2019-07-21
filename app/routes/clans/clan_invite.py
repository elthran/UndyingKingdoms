from importlib import import_module

from flask import url_for
from flask_login import login_required, current_user
from werkzeug.utils import redirect

from app import app
get_models = lambda: import_module('app.models.exports')


@app.route('/clans/clan_invite/<int:user_id>/<int:clan_id>', methods=['GET', 'POST'])
@login_required
def clan_invite(user_id, clan_id):
    models = get_models()
    county = current_user.county
    invited_user = models.User.query.get(user_id)
    clan = models.Clan.query.get(clan_id)

    member_history = models.Clan.query.filter_by(id=clan_id, user_id=user_id).first()
    if member_history:
        print("history", user_id, clan_id)
        member_history.status = "Invited"
    else:
        print("nully")
        invite = models.Clan(clan.kingdom_id, user_id, status="Invited")
        invite.save()
    message = models.Notification(
        invited_user.county,
        "Clan Invite",
        "You were invited to join a clan",
        "Clan"
    )
    message.save()
    return redirect(url_for('generic_clan'))
