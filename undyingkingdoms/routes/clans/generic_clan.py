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
    form = CreateKingdomForm()

    if clan:
        kingdom = Kingdom.query.get(clan.kingdom_id)
        users = User.query.filter(User.id != user.id).all()
        return render_template(template, form=form, kingdom=kingdom, users=users)

    invites = Clan.query.filter_by(user_id=user.id, status="Pending").all()

    if form.validate_on_submit():
        # user.gems -= 500
        kingdom = Kingdom(form.name.data)
        kingdom.save()
        clan = Clan(kingdom.id, user.id, True)
        clan.save()
        return redirect(url_for('generic_clan'))

    return render_template(template, form=form, invites=invites)


