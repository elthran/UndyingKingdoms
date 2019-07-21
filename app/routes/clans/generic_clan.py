from importlib import import_module

from flask import render_template, redirect, url_for
from flask_login import login_required, current_user
from flask_mobility.decorators import mobile_template

from app import app
get_models = lambda: import_module('app.models.exports')
get_forms = lambda: import_module('app.models.forms.create_kingdom')


@app.route('/clans/generic_clan/', methods=['GET', 'POST'])
@mobile_template('{mobile/}clans/generic_clan.html')
@login_required
def generic_clan(template):
    models = get_models()
    forms = get_forms()
    user = current_user
    form = forms.CreateKingdomForm()
    clan = user.clan

    invite = models.Clan.query.filter_by(user_id=user.id, status="Invited").first()
    if invite:
        invited_clan = models.Clan.query.get(invite.id)
        return render_template(template, form=form, invited_clan=invited_clan)

    if clan:

        kingdom = models.Kingdom.query.get(clan.kingdom_id)
        all_users = models.User.query.filter(
            models.User.id != user.id, ~models.User.is_bot
        ).all()
        eligible_users = [
            user
            for user in all_users
            if user not in clan.members and
               user not in clan.invited and
               user.county
        ]
        return render_template(template, form=form, kingdom=kingdom, users=eligible_users)

    if form.validate_on_submit():
        # user.gems -= 500
        kingdom = models.Kingdom(form.name.data)
        kingdom.clan = True
        kingdom.save()
        clan = models.Clan(kingdom.id, user.id, is_owner=True)
        clan.save()
        return redirect(url_for('generic_clan'))

    return render_template(template, form=form)


