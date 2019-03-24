from flask import render_template, redirect, url_for
from flask_login import login_required, current_user
from flask_mobility.decorators import mobile_template

from undyingkingdoms import app, User
from undyingkingdoms.models import Kingdom
from undyingkingdoms.models.clans import Clan
from undyingkingdoms.models.forms.create_kingdom import CreateKingdomForm


@app.route('/clans/generic_clan/', methods=['GET', 'POST'])
@mobile_template('{mobile/}clans/generic_clan.html')
@login_required
def generic_clan(template):
    user = current_user
    clan = user.clan
    if clan and user not in clan.users:
        clan = None

    print("Clan is:", clan)
    form = CreateKingdomForm()

    invite = Clan.query.filter_by(user_id=user.id, status="Pending").first()
    if invite:
        invited_clan = Clan.query.get(invite.id)
        return render_template(template, clan=clan, form=form, invited_clan=invited_clan)

    if clan:

        kingdom = Kingdom.query.get(clan.kingdom_id)
        all_users = User.query.filter(User.id != user.id).all()
        already_invited_users = Clan.query.filter_by(kingdom_id=clan.kingdom_id, status="Pending").all()
        already_invited_user_ids = [user.user_id for user in already_invited_users]
        the_users = [user for user in all_users if user.id not in already_invited_user_ids]

        return render_template(template, clan=clan, form=form, kingdom=kingdom, users=the_users)

    if form.validate_on_submit():
        # user.gems -= 500
        kingdom = Kingdom(form.name.data)
        kingdom.save()
        clan = Clan(kingdom.id, user.id, True)
        clan.save()
        return redirect(url_for('generic_clan'))

    return render_template(template, clan=clan, form=form)


